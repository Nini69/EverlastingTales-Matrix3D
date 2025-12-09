import utils3d
import utils3d.numpy
import inspect
import numpy as np

print("🔍 DIAGNOSTIC utils3d.numpy.unproject_cv")

func = utils3d.numpy.unproject_cv
print(f"Function object: {func}")
try:
    sig = inspect.signature(func)
    print(f"Signature: {sig}")
except Exception as e:
    print(f"Signature Error: {e}")

# Test 1: Calling with 3 positional args (Like library expects)
print("\n🧪 Test 1: Call with depth (Standard)")
try:
    uv = np.zeros((1, 1, 2), dtype=np.float32)
    depth = np.ones((1, 1, 1), dtype=np.float32)
    intrinsics = np.eye(3, dtype=np.float32).reshape(1, 3, 3)
    extrinsics = np.eye(4, dtype=np.float32).reshape(1, 4, 4)
    
    res = func(uv, depth, intrinsics, extrinsics)
    print("✅ OK")
except Exception as e:
    print(f"❌ FAIL: {e}")

# Test 2: Calling with 1 positional arg (Like code does)
print("\n🧪 Test 2: Call without depth (Legacy Code)")
try:
    # Simulating: unproject_cv(uv, extrinsics=..., intrinsics=...)
    res = func(uv, extrinsics=extrinsics, intrinsics=intrinsics)
    print("✅ OK (Wrapper worked!)")
except Exception as e:
    print(f"❌ FAIL: {e}")

# Check Matrix Patches
try:
    import matrix_patches
    print("\n✅ matrix_patches imported.")
except ImportError:
    print("\n⚠️ matrix_patches NOT imported.")
