import platform
import os
import sys
import subprocess

print("✅ Environment Check\n")

print(
    f"Python version: {platform.python_version()} ({platform.python_implementation()}, {platform.python_compiler()})"
)
print(f"Python executable: {sys.executable}\n")

print(f"Operating System: {platform.system()} {platform.release()}")
print(f"Machine: {platform.machine()}\n")

# Check virtual environment
if sys.prefix != sys.base_prefix:
    print("🟢 You are inside a virtual environment.\n")
else:
    print("🔴 You are NOT inside a virtual environment.\n")

# Check installed packages
try:
    import pkg_resources

    print("📦 Installed packages:")
    packages = sorted(
        [f"{d.project_name}=={d.version}" for d in pkg_resources.working_set]
    )
    for pkg in packages:
        print(f"  - {pkg}")
    print()
except ImportError:
    print("❌ Could not list packages: 'pkg_resources' not found\n")

# YOLOv8 check
try:
    from ultralytics import YOLO

    print("🧠 YOLOv8 (Ultralytics) check:")
    print("✅ YOLOv8 is installed\n")
except ImportError:
    print("🧠 YOLOv8 (Ultralytics) check:")
    print("❌ YOLOv8 is NOT installed\n")
