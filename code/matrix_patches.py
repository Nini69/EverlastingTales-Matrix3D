import sys
import types
import torch
import torch.distributed
import torch.utils._pytree
import numpy as np
import inspect
from types import ModuleType

print("⚡ [Matrix3D] CHARGEMENT DU MASTER PATCH (V26 - FINAL)...")

# --- FIX 1-5: Base Fixes ---
if not hasattr(torch, 'xpu'):
    torch.xpu = type('XPU', (), {'is_available': lambda: False, 'empty_cache': lambda: None, 'device_count': lambda: 0, 'manual_seed': lambda s: None})

if not hasattr(torch.distributed, 'device_mesh'):
    m_dm = types.ModuleType('torch.distributed.device_mesh')
    m_dm.__path__ = []
    m_dm.DeviceMesh = type('DeviceMesh', (), {})
    m_dm.init_device_mesh = lambda *args, **kwargs: None
    sys.modules['torch.distributed.device_mesh'] = m_dm
    torch.distributed.device_mesh = m_dm

if not hasattr(torch.utils._pytree, 'register_pytree_node'):
    torch.utils._pytree.register_pytree_node = lambda c, f, u, serialized_type_name=None: torch.utils._pytree._register_pytree_node(c, f, u)

m_tensor = types.ModuleType('torch.distributed.tensor')
sys.modules['torch.distributed.tensor'] = m_tensor
sys.modules['torch.distributed.tensor.experimental'] = m_tensor # Redirect both
torch.distributed.tensor = m_tensor
m_tensor.experimental = m_tensor
m_attn = types.ModuleType('torch.distributed.tensor.experimental.attention')
sys.modules['torch.distributed.tensor.experimental.attention'] = m_attn
sys.modules['torch.distributed.tensor.experimental._attention'] = m_attn
m_tensor.experimental.attention = m_attn
m_tensor.experimental._attention = m_attn # Double tap

# --- FIX 7: WRAPPER unproject_cv (Pour l'argument depth manquant) ---
try:
    import utils3d
    import utils3d.numpy
    
    # On capture la vraie fonction (qui vient d'être réparée par repair_utils3d.py)
    _real_unproject = utils3d.numpy.unproject_cv
    
    def unproject_cv_wrapper(*args, **kwargs):
        # Si on appelle sans 'depth' (donc juste 1 arg positionnel 'uv'), on injecte depth=1.0
        if len(args) < 2 and 'depth' not in kwargs:
            # On suppose que args[0] est 'uv'. On crée un depth=1
            # print("🔧 [Patch V26] Injection automatique de depth=1.0 dans unproject_cv")
            new_args = list(args)
            new_args.append(1.0) # Ajout du 2ème argument positionnel
            return _real_unproject(*new_args, **kwargs)
        
        return _real_unproject(*args, **kwargs)
    
    # Remplacement
    utils3d.numpy.unproject_cv = unproject_cv_wrapper
    print("✅ [Patch V26] Wrapper unproject_cv installé.")

except ImportError:
    pass
except Exception as e:
    print(f"⚠️ Warning Patch V26: {e}")

print("⚡ [Matrix3D] V26 PRÊT.")
