
try:
    with open('b64.txt', 'r') as f:
        s = f.read().strip()
    
    chunks = [s[i:i+1000] for i in range(0, len(s), 1000)]
    
    print("rm blob.b64") # Clean start
    for i, c in enumerate(chunks):
        print(f'echo -n "{c}" >> blob.b64')
    
    print("base64 -d blob.b64 > fix_final.py")
    print("python fix_final.py")

except Exception as e:
    print(e)
