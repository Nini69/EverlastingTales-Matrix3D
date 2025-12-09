@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion
:: ================================
::  Fix 0xc0000017 (BadMemory list)
:: ================================

:: Require admin
net session >nul 2>&1
if %errorlevel% neq 0 (
  echo [!] Lancez ce script par clic-droit ^> "Executer en tant qu'administrateur".
  pause
  exit /b 1
)

set LOG=%USERPROFILE%\Desktop\Fix-0xc0000017.log
(echo [%date% %time%] Debut correctif 0xc0000017) > "%LOG%"

echo [1/6] Etat actuel du BCD {badmemory}
>>"%LOG%" %SystemRoot%\Sysnative\bcdedit.exe /enum {badmemory}
if %errorlevel% neq 0 echo   (Info: aucune entree ou acces limite)

:: Sauvegarde BCD (precaution)
echo [2/6] Sauvegarde du magasin BCD dans %USERPROFILE%\Desktop\BCD_Backup
set BCD_BK=%USERPROFILE%\Desktop\BCD_Backup
mkdir "%BCD_BK%" >nul 2>&1
%SystemRoot%\Sysnative\bcdedit.exe /export "%BCD_BK%\BCD_Backup.bak" >nul 2>&1

:: Nettoyage de la liste badmemory
set STEP=[3/6] Suppression de la liste badmemory
%SystemRoot%\Sysnative\bcdedit.exe /deletevalue {badmemory} badmemorylist >nul 2>&1 && (
  echo %STEP% ^: OK
  echo %STEP% : OK >> "%LOG%"
) || (
  echo %STEP% ^: (peut etre deja vide)
  echo %STEP% : deja vide ou non applicable >> "%LOG%"
)

:: Pagefile: forcer en gestion automatique
set STEP=[4/6] Activation du fichier d'echange (auto)
wmic computersystem where name="%computername%" set AutomaticManagedPagefile=True >nul 2>&1 && (
  echo %STEP% ^: OK
  echo %STEP% : OK >> "%LOG%"
) || (
  echo %STEP% ^: WMIC indisponible, on force via registre
  reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v PagingFiles /t REG_MULTI_SZ /d "?:\pagefile.sys" /f >nul 2>&1
  echo %STEP% : Registre ajuste >> "%LOG%"
)

:: Desactiver la compression memoire (optionnel, reversible)
echo [5/6] Desactivation temporaire de la compression memoire (reversible)
PowerShell -NoLogo -NoProfile -Command "Disable-MMAgent -MemoryCompression; Get-MMAgent | Format-List *" >> "%LOG%" 2>&1

:: Verification et reparation systeme (sures)
echo [6/6] SFC puis DISM (laissez finir)
sfc /scannow >> "%LOG%" 2>&1
DISM /Online /Cleanup-Image /RestoreHealth >> "%LOG%" 2>&1

echo.
echo Terminee. Un redemarrage est recommande. Journal : %LOG%
echo Vous pouvez re-activer la compression plus tard :
echo   PowerShell ^> Enable-MMAgent -MemoryCompression
pause
