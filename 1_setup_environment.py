#!/usr/bin/env python3
"""
Chatterbox TTS - Environment Setup and Verification Script
Step 1: Run this first to check your system is ready
"""

import sys
import subprocess
import platform
import os

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    print(f"✓ {text}")

def print_warning(text):
    print(f"⚠ {text}")

def print_error(text):
    print(f"✗ {text}")

def check_python_version():
    print_header("Checking Python Version")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Python version: {version_str}")
    print(f"Python executable: {sys.executable}")
    
    if version.major == 3 and version.minor >= 10:
        print_success(f"Python {version_str} is compatible!")
        return True
    else:
        print_error(f"Python {version_str} is not supported")
        print("   Please install Python 3.10 or 3.11")
        print("   Download from: https://www.python.org/downloads/")
        return False

def check_system_info():
    print_header("System Information")
    
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    
    return True

def check_pip():
    print_header("Checking pip (Package Manager)")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout.strip())
        print_success("pip is installed and working!")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is not installed or not working")
        print("   Install pip: python -m ensurepip --upgrade")
        return False

def check_venv():
    print_header("Checking Virtual Environment")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print_success("You are in a virtual environment!")
        print(f"   Environment: {sys.prefix}")
        return True
    else:
        print_warning("You are NOT in a virtual environment")
        print("\nRecommended: Create and activate a virtual environment first:")
        print("\n  Option A (Conda):")
        print("    conda create -n chatterbox python=3.11 -y")
        print("    conda activate chatterbox")
        print("\n  Option B (venv):")
        print("    python -m venv chatterbox_env")
        if platform.system() == "Windows":
            print("    chatterbox_env\\Scripts\\activate")
        else:
            print("    source chatterbox_env/bin/activate")
        print("\nThen run this script again.")
        return False

def check_disk_space():
    print_header("Checking Disk Space")
    
    try:
        if platform.system() == "Windows":
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(os.getcwd()),
                None, None,
                ctypes.pointer(free_bytes)
            )
            free_gb = free_bytes.value / (1024**3)
        else:
            stat = os.statvfs(os.getcwd())
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        
        print(f"Available disk space: {free_gb:.2f} GB")
        
        if free_gb >= 10:
            print_success("Sufficient disk space available")
            return True
        else:
            print_warning(f"Low disk space: {free_gb:.2f} GB")
            print("   Recommended: At least 10 GB free for models and dependencies")
            return True  # Warning, not error
    except Exception as e:
        print_warning(f"Could not check disk space: {e}")
        return True

def check_internet():
    print_header("Checking Internet Connection")
    
    try:
        import urllib.request
        urllib.request.urlopen('https://pypi.org', timeout=5)
        print_success("Internet connection OK")
        return True
    except Exception as e:
        print_error("No internet connection detected")
        print("   Internet is required to download models and dependencies")
        return False

def check_gpu():
    print_header("Checking GPU Availability (Optional)")
    
    print("Attempting to detect CUDA-capable GPU...")
    print("(This requires PyTorch, which will be installed in step 2)")
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            print_success(f"CUDA GPU detected: {gpu_count} device(s)")
            for i in range(gpu_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / (1024**3)
                print(f"   GPU {i}: {gpu_name}")
                print(f"   Memory: {gpu_memory:.2f} GB")
            return True
        else:
            print_warning("No CUDA GPU detected")
            print("   TTS will run on CPU (slower but functional)")
            return True
    except ImportError:
        print_warning("PyTorch not installed yet")
        print("   GPU detection will happen after running 2_install_dependencies.py")
        return True

def main():
    print("\n" + "="*60)
    print("  CHATTERBOX TTS - ENVIRONMENT SETUP CHECKER")
    print("  Step 1 of 5: Verify Your System")
    print("="*60)
    
    checks = []
    
    # Critical checks
    checks.append(("Python Version", check_python_version()))
    checks.append(("System Info", check_system_info()))
    checks.append(("pip", check_pip()))
    checks.append(("Virtual Environment", check_venv()))
    checks.append(("Disk Space", check_disk_space()))
    checks.append(("Internet", check_internet()))
    
    # Optional checks
    checks.append(("GPU (Optional)", check_gpu()))
    
    # Summary
    print_header("SETUP CHECK SUMMARY")
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for check_name, result in checks:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {check_name}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n" + "="*60)
        print_success("All checks passed! You're ready for the next step.")
        print("\nNext step: Run the dependency installer:")
        print("  python 2_install_dependencies.py")
        print("="*60 + "\n")
        return 0
    else:
        print("\n" + "="*60)
        print_warning("Some checks failed. Please fix the issues above.")
        print("\nTip: Make sure you're in a virtual environment!")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
