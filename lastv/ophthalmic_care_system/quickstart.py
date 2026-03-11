"""
Quick Start Guide - Ophthalmic Care System
This script provides an interactive menu to train, test, and run the system
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 70)
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "   OPHTHALMIC CARE SYSTEM - MACULAR EDEMA DETECTION".center(68) + "║")
    print("║" + "          Using Convolutional Neural Networks (CNN)".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print("=" * 70 + "\n")

def print_menu():
    """Print main menu"""
    print("╔" + "=" * 68 + "╗")
    print("║" + " MAIN MENU ".center(68) + "║")
    print("╠" + "=" * 68 + "╣")
    print("║  1. Train CNN Model                                               ║")
    print("║  2. Make Predictions on Images                                   ║")
    print("║  3. Generate Grad-CAM Explanations                               ║")
    print("║  4. Start Web Application (Flask)                                ║")
    print("║  5. Database Operations                                          ║")
    print("║  6. View Project Structure                                       ║")
    print("║  0. Exit                                                         ║")
    print("╚" + "=" * 68 + "╝")

def main_menu():
    """Main menu loop"""
    print_banner()
    
    while True:
        print_menu()
        choice = input("\n→ Select an option (0-6): ").strip()
        
        if choice == '1':
            train_model()
        elif choice == '2':
            make_prediction()
        elif choice == '3':
            generate_gradcam()
        elif choice == '4':
            start_web_app()
        elif choice == '5':
            database_operations()
        elif choice == '6':
            view_structure()
        elif choice == '0':
            print("\n✓ Exiting Ophthalmic Care System...")
            break
        else:
            print("\n✗ Invalid option. Please try again.")

def train_model():
    """Train CNN model"""
    print("\n" + "=" * 70)
    print("TRAIN CNN MODEL")
    print("=" * 70)
    
    print("""
This will:
1. Generate synthetic dataset (sample images)
2. Create data generators with augmentation
3. Build and train CNN model for 30 epochs
4. Display training history plots
5. Save model as 'macular_edema_model.h5'

Estimated time: 10-15 minutes (depends on CPU/GPU)
""")
    
    response = input("→ Continue with training? (yes/no): ").strip().lower()
    
    if response == 'yes':
        try:
            os.chdir('model')
            subprocess.run([sys.executable, 'train_model.py'], check=True)
            os.chdir('..')
            print("\n✓ Training completed! Model saved to models/macular_edema_model.h5")
        except subprocess.CalledProcessError:
            print("\n✗ Training failed. Check error messages above.")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    else:
        print("✓ Training cancelled.")

def make_prediction():
    """Make prediction on image"""
    print("\n" + "=" * 70)
    print("MAKE PREDICTION ON IMAGE")
    print("=" * 70)
    
    image_path = input("\n→ Enter path to image file: ").strip()
    
    if not os.path.exists(image_path):
        print(f"✗ Image not found: {image_path}")
        return
    
    try:
        os.chdir('model')
        
        # Import predictor
        from predict import MacularEdemaPredictor
        
        predictor = MacularEdemaPredictor(
            model_path='../models/macular_edema_model.h5'
        )
        
        print("\n→ Analyzing image...")
        result = predictor.predict(image_path)
        
        if result['status'] == 'success':
            print("\n" + "=" * 70)
            print("PREDICTION RESULTS")
            print("=" * 70)
            print(f"✓ Severity: {result['severity']}")
            print(f"✓ Confidence: {result['confidence_percentage']}")
            print(f"✓ Risk Level: {result['risk_level']}")
            print(f"\nDescription: {result['description']}")
            print(f"\nClass Probabilities:")
            for class_name, prob in result['all_probabilities'].items():
                print(f"  • {class_name}: {prob*100:.2f}%")
            
            recommendation = {
                0: 'Continue regular eye examinations.',
                1: 'Monitor closely. Consider anti-VEGF or corticosteroid therapy.',
                2: 'Refer to retina specialist immediately.',
                3: 'CRITICAL: Requires immediate specialist intervention.'
            }
            print(f"\n🏥 Recommendation: {recommendation.get(result['predicted_class'], 'Consult specialist')}")
        else:
            print(f"✗ Prediction failed: {result['message']}")
        
        os.chdir('..')
        
    except Exception as e:
        print(f"✗ Error: {e}")
        os.chdir('..')

def generate_gradcam():
    """Generate Grad-CAM explanation"""
    print("\n" + "=" * 70)
    print("GENERATE GRAD-CAM EXPLANATION")
    print("=" * 70)
    
    image_path = input("\n→ Enter path to image file: ").strip()
    
    if not os.path.exists(image_path):
        print(f"✗ Image not found: {image_path}")
        return
    
    try:
        os.chdir('explainability')
        
        from gradcam import GradCAM
        
        gradcam = GradCAM(
            model_path='../models/macular_edema_model.h5'
        )
        
        print("\n→ Generating Grad-CAM heatmap...")
        save_path = '../models/gradcam_output.png'
        
        fig, heatmap = gradcam.visualize_gradcam(
            image_path=image_path,
            save_path=save_path,
            show_plot=True
        )
        
        if heatmap is not None:
            print(f"\n✓ Grad-CAM visualization saved to: {save_path}")
        else:
            print("✗ Failed to generate Grad-CAM visualization")
        
        os.chdir('..')
        
    except Exception as e:
        print(f"✗ Error: {e}")
        os.chdir('..')

def start_web_app():
    """Start Flask web application"""
    print("\n" + "=" * 70)
    print("START WEB APPLICATION")
    print("=" * 70)
    
    print("""
The Flask web application will start on: http://localhost:5000

Features:
• Doctor authentication and registration
• Patient information management
• Image upload and analysis
• Real-time AI predictions
• Grad-CAM visualization
• Patient history tracking
• Dashboard analytics

Demo credentials:
  Username: demo
  Password: demo123
""")
    
    response = input("\n→ Continue? (yes/no): ").strip().lower()
    
    if response == 'yes':
        print("\n→ Starting Flask application...")
        print("   Open http://localhost:5000 in your browser")
        print("   Press Ctrl+C to stop\n")
        
        try:
            os.chdir('backend')
            subprocess.run([sys.executable, 'app.py'], check=True)
            os.chdir('..')
        except KeyboardInterrupt:
            print("\n✓ Flask application stopped.")
            os.chdir('..')
        except Exception as e:
            print(f"\n✗ Error: {e}")
            os.chdir('..')
    else:
        print("✓ Application start cancelled.")

def database_operations():
    """Database operations menu"""
    print("\n" + "=" * 70)
    print("DATABASE OPERATIONS")
    print("=" * 70)
    
    print("""
Options:
1. Initialize/Reset Database
2. View Database Statistics
3. Create Sample Data
4. Backup Database
0. Return to Main Menu
""")
    
    choice = input("→ Select an option (0-4): ").strip()
    
    if choice == '1':
        print("\n→ Initializing database...")
        try:
            from backend.database import DatabaseManager
            db = DatabaseManager()
            print("✓ Database initialized successfully!")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    elif choice == '2':
        print("\n→ Retrieving statistics...")
        try:
            from backend.database import DatabaseManager
            db = DatabaseManager()
            stats = db.get_dashboard_stats()
            print(f"\n  Total Patients: {stats.get('total_patients', 0)}")
            print(f"  Total Examinations: {stats.get('total_examinations', 0)}")
            print(f"  Average Confidence: {stats.get('average_confidence', 0):.4f}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    elif choice == '3':
        print("\n→ Creating sample data...")
        try:
            from backend.database import DatabaseManager
            db = DatabaseManager()
            success, user_id = db.create_user('doctor1', 'password123', 'doctor1@hospital.com')
            if success:
                print(f"✓ Sample doctor created (ID: {user_id})")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    elif choice == '4':
        print("\n✓ Backup database...")
        try:
            import shutil
            shutil.copy('ophthalmic_care.db', 'ophthalmic_care_backup.db')
            print("✓ Database backed up to: ophthalmic_care_backup.db")
        except Exception as e:
            print(f"✗ Error: {e}")

def view_structure():
    """View project structure"""
    print("\n" + "=" * 70)
    print("PROJECT STRUCTURE")
    print("=" * 70)
    
    structure = """
ophthalmic_care_system/
│
├── model/                          # Machine Learning
│   ├── cnn_model.py               # CNN Architecture
│   ├── train_model.py             # Training Pipeline
│   └── predict.py                 # Predictions
│
├── backend/                        # Flask Backend
│   ├── app.py                     # Main Application
│   └── database.py                # Database Mgmt
│
├── explainability/                # Explainable AI
│   └── gradcam.py                # Grad-CAM
│
├── frontend/                       # Web Interface
│   ├── templates/                # HTML Pages
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── upload.html
│   │   ├── result.html
│   │   └── history.html
│   └── static/css/               # Styling
│       └── style.css
│
├── models/                         # Saved Models
│   └── macular_edema_model.h5    # Trained Model
│
├── dataset/                        # Training Data
│   └── train/
│       ├── normal/
│       ├── mild/
│       ├── moderate/
│       └── severe/
│
├── requirements.txt               # Dependencies
├── README.md                      # Documentation
└── quickstart.py                  # This File
"""
    
    print(structure)
    
    print("\n📁 File Descriptions:\n")
    print("  cnn_model.py      - Defines CNN architecture and layers")
    print("  train_model.py    - Training loop with data generators")
    print("  predict.py        - Prediction on new images")
    print("  gradcam.py        - Explainable AI visualization")
    print("  app.py            - Flask routes and endpoints")
    print("  database.py       - SQLite operations")
    print("  login.html        - Authentication page")
    print("  dashboard.html    - Statistics and analytics")
    print("  upload.html       - Image upload interface")
    print("  result.html       - Prediction results page")
    print("  history.html      - Patient examination history")
    print("  style.css         - Complete styling")

if __name__ == "__main__":
    try:
        # Change to project directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Check if in correct directory
        if not os.path.exists('model') or not os.path.exists('backend'):
            print("✗ Error: Please run this script from the ophthalmic_care_system directory")
            sys.exit(1)
        
        main_menu()
    except KeyboardInterrupt:
        print("\n\n✓ Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
