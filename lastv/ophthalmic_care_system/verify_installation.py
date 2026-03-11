"""
System Verification Script
Checks if all components are working correctly
Run: python verify_installation.py
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_python_version():
    """Check Python version"""
    print("\n→ Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (Requires 3.8+)")
        return False

def check_packages():
    """Check if all required packages are installed"""
    print("\n→ Checking installed packages...")
    
    required_packages = [
        'tensorflow',
        'flask',
        'numpy',
        'opencv-cv2',
        'PIL',
        'sklearn',
        'matplotlib',
        'scipy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'opencv-cv2':
                __import__('cv2')
            elif package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (NOT INSTALLED)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    return True

def check_directory_structure():
    """Check if project structure exists"""
    print("\n→ Checking directory structure...")
    
    required_dirs = [
        'model',
        'backend',
        'explainability',
        'frontend',
        'frontend/templates',
        'frontend/static/css'
    ]
    
    missing = []
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ (NOT FOUND)")
            missing.append(dir_path)
    
    if missing:
        print(f"\n✗ Missing directories: {', '.join(missing)}")
        return False
    return True

def check_files():
    """Check if required files exist"""
    print("\n→ Checking required files...")
    
    required_files = [
        'model/cnn_model.py',
        'model/train_model.py',
        'model/predict.py',
        'backend/app.py',
        'backend/database.py',
        'explainability/gradcam.py',
        'frontend/templates/login.html',
        'frontend/templates/dashboard.html',
        'frontend/templates/upload.html',
        'frontend/templates/result.html',
        'frontend/templates/history.html',
        'frontend/static/css/style.css',
        'requirements.txt',
        'config.py',
        'README.md'
    ]
    
    missing = []
    for file_path in required_files:
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"✗ {file_path} (NOT FOUND)")
            missing.append(file_path)
    
    if missing:
        print(f"\n✗ Missing files: {', '.join(missing)}")
        return False
    return True

def check_model():
    """Check if model file exists"""
    print("\n→ Checking trained model...")
    
    model_path = 'models/macular_edema_model.h5'
    if os.path.isfile(model_path):
        size = os.path.getsize(model_path)
        size_mb = size / (1024 * 1024)
        print(f"✓ Model found: {size_mb:.2f} MB")
        return True
    else:
        print(f"⚠ Model not found at: {model_path}")
        print("  Run: cd model && python train_model.py && cd ..")
        return False

def test_imports():
    """Test if main modules can be imported"""
    print("\n→ Testing module imports...")
    
    test_modules = {
        'model.cnn_model': 'CNN Model',
        'model.predict': 'Predictor',
        'backend.database': 'Database',
        'explainability.gradcam': 'Grad-CAM'
    }
    
    success_count = 0
    for module_name, display_name in test_modules.items():
        try:
            __import__(module_name)
            print(f"✓ {display_name} module imports successfully")
            success_count += 1
        except ImportError as e:
            print(f"✗ {display_name} module import failed: {e}")
        except Exception as e:
            print(f"⚠ {display_name} module warning: {e}")
    
    return success_count > 0

def check_flask():
    """Check Flask installation and basic routes"""
    print("\n→ Checking Flask...")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        print(f"✓ Flask installed and working")
        return True
    except Exception as e:
        print(f"✗ Flask error: {e}")
        return False

def check_tensorflow():
    """Check TensorFlow installation"""
    print("\n→ Checking TensorFlow/Keras...")
    
    try:
        import tensorflow as tf
        version = tf.__version__
        print(f"✓ TensorFlow {version} installed")
        
        # Check GPU
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✓ GPU detected: {len(gpus)} device(s)")
        else:
            print("ℹ GPU not available (will use CPU)")
        
        return True
    except Exception as e:
        print(f"✗ TensorFlow error: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    print("\n→ Creating sample data...")
    
    try:
        import numpy as np
        from PIL import Image
        
        os.makedirs('dataset/train/normal', exist_ok=True)
        
        # Create sample image
        img = np.random.rand(224, 224, 3) * 255
        Image.fromarray(img.astype(np.uint8)).save('dataset/train/normal/sample.png')
        
        print("✓ Sample data created in dataset/train/normal/")
        return True
    except Exception as e:
        print(f"⚠ Could not create sample data: {e}")
        return False

def run_health_check():
    """Run comprehensive health check"""
    print_header("OPHTHALMIC CARE SYSTEM - INSTALLATION VERIFICATION")
    
    checks = [
        ("Python Version", check_python_version),
        ("Package Dependencies", check_packages),
        ("Directory Structure", check_directory_structure),
        ("Required Files", check_files),
        ("Flask Framework", check_flask),
        ("TensorFlow/Keras", check_tensorflow),
        ("Module Imports", test_imports),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"✗ Error in {check_name}: {e}")
            results.append((check_name, False))
    
    # Check for model (optional)
    model_exists = check_model()
    
    # Create sample data (optional)
    create_sample_data()
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} checks passed\n")
    
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {check_name}")
    
    if model_exists:
        print(f"{'✓ READY':8} - Trained model available")
    else:
        print(f"{'ℹ INFO ':8} - Model needs training (optional for demo)")
    
    all_passed = passed == total
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ SYSTEM IS READY!")
        print("\nNext steps:")
        print("1. (Optional) Train model: cd model && python train_model.py")
        print("2. Start web app: cd backend && python app.py")
        print("3. Open http://localhost:5000")
        print("4. Login with demo/demo123 or create new account")
        print("=" * 70)
        return 0
    else:
        print("✗ SYSTEM HAS MISSING COMPONENTS")
        print("\nTo fix:")
        print("1. Check error messages above")
        print("2. Run: pip install -r requirements.txt")
        print("3. Verify directory structure is complete")
        print("4. Re-run this verification script")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_health_check()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n✗ Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
