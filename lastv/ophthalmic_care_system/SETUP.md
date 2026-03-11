"""
Installation and Setup Instructions
For Ophthalmic Care System
"""

SETUP_INSTRUCTIONS = """
╔═══════════════════════════════════════════════════════════════════════╗
║       OPHTHALMIC CARE SYSTEM - INSTALLATION & SETUP GUIDE            ║
╚═══════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. PREREQUISITES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Python 3.8 or higher
✓ pip (Python package manager)
✓ 4GB RAM minimum (8GB recommended)
✓ 1GB free disk space
✓ Modern web browser (Chrome, Firefox, Safari, Edge)

Check Python installation:
  $ python --version
  $ pip --version

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. STEP-BY-STEP INSTALLATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Navigate to Project Directory
  $ cd ophthalmic_care_system

STEP 2: Create Virtual Environment

  On Windows:
    $ python -m venv venv
    $ venv\\Scripts\\activate

  On macOS/Linux:
    $ python3 -m venv venv
    $ source venv/bin/activate

  (You should see (venv) in your prompt)

STEP 3: Upgrade pip
  $ pip install --upgrade pip

STEP 4: Install Dependencies
  $ pip install -r requirements.txt

  This will install:
  - TensorFlow 2.13.0 (Deep Learning)
  - Flask 2.3.3 (Web Framework)
  - OpenCV 4.8.0 (Image Processing)
  - NumPy, Scikit-learn, Matplotlib, and more

STEP 5: Verify Installation
  $ python -c "import tensorflow as tf; print(tf.__version__)"
  $ python -c "import flask; print(flask.__version__)"

  Expected output:
    TensorFlow version: 2.13.0
    Flask version: 2.3.3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. QUICK START METHODS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

METHOD A: Using Interactive Menu (Recommended for Beginners)
  $ python quickstart.py
  
  This provides:
  - Interactive menu system
  - Guided training and prediction
  - Database operations
  - Web app launcher

METHOD B: Direct Python Execution

  A) Train the Model:
    $ cd model
    $ python train_model.py
    $ cd ..

  B) Make Predictions:
    $ cd model
    $ python predict.py
    $ cd ..

  C) Generate Grad-CAM:
    $ cd explainability
    $ python gradcam.py
    $ cd ..

  D) Start Web Application:
    $ cd backend
    $ python app.py
    Then open: http://localhost:5000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. TRAINING THE MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The system includes synthetic dataset generation for demonstration.

To train with real dataset:

1. Download Kaggle Dataset:
   - Visit: https://www.kaggle.com/datasets/paultimothymooney/kermany2018
   - Download OCT dataset

2. Extract and organize:
   dataset/
   ├── train/
   │   ├── normal/        (put images here)
   │   ├── mild/          
   │   ├── moderate/      
   │   └── severe/        

3. Run training:
   $ cd model
   $ python train_model.py
   $ cd ..

4. Expected output:
   - Training progress logs
   - Accuracy plots
   - Model saved as: models/macular_edema_model.h5
   - Training time: 15-60 minutes (depends on dataset size)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. RUNNING THE WEB APPLICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Start the Flask server:
  $ cd backend
  $ python app.py

Expected output:
  * Running on http://127.0.0.1:5000
  * Press CTRL+C to quit

Open in browser:
  http://localhost:5000

Login with demo credentials:
  Username: demo
  Password: demo123

Or register a new account:
  - Click "Register" button
  - Fill in details
  - Create account

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. USING THE WEB APPLICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After login, you can:

1. UPLOAD IMAGE:
   - Click "Upload Image" in navigation
   - Fill patient information
   - Select retinal OCT/fundus image
   - Click "Analyze Image"

2. VIEW RESULTS:
   - Severity classification (Normal, Mild, Moderate, Severe)
   - Confidence score
   - Grad-CAM heatmap visualization
   - Clinical recommendations

3. VIEW DASHBOARD:
   - Total patients count
   - Examination statistics
   - Severity distribution
   - Model performance metrics

4. VIEW PATIENT HISTORY:
   - List of all examinations
   - Trend analysis
   - Comparison over time

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERROR: "No module named tensorflow"
  Solution:
    $ pip install --upgrade tensorflow
    $ pip install --upgrade keras

ERROR: "Model not found"
  Solution:
    Go to model folder and train:
    $ cd model
    $ python train_model.py
    $ cd ..

ERROR: "Port 5000 already in use"
  Solution:
    On Windows:
      $ netstat -ano | findstr :5000
      $ taskkill /PID <PID> /F
    
    On macOS/Linux:
      $ lsof -i :5000
      $ kill -9 <PID>

ERROR: "Virtual environment not activated"
  Solution:
    Windows:
      $ venv\\Scripts\\activate
    
    macOS/Linux:
      $ source venv/bin/activate

ERROR: "Database locked"
  Solution:
    $ rm ophthalmic_care.db
    (Database will be recreated automatically)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. SYSTEM REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Supported Operating Systems:
  ✓ Windows 10/11
  ✓ macOS 10.13+
  ✓ Linux (Ubuntu 18.04+)

Python Versions:
  ✓ Python 3.8
  ✓ Python 3.9
  ✓ Python 3.10
  ✓ Python 3.11

Hardware Recommendations:
  CPU:    Intel i5/i7 or equivalent (4+ cores)
  RAM:    8GB minimum, 16GB recommended
  Storage: 2GB free space
  GPU:    NVIDIA GPU with CUDA support (optional, for faster training)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. USING GPU (OPTIONAL - For Faster Training)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For NVIDIA GPU acceleration:

1. Install CUDA Toolkit:
   https://developer.nvidia.com/cuda-downloads

2. Install cuDNN:
   https://developer.nvidia.com/cudnn

3. Install TensorFlow GPU version:
   $ pip install tensorflow[and-cuda]

4. Verify GPU:
   $ python -c "import tensorflow as tf; print(tf.sysconfig.get_build_info()['cuda_version'])"

Training with GPU is 10-50x faster than CPU!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. FILE ORGANIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After installation, your directory should look like:

ophthalmic_care_system/
├── venv/                   (Virtual environment)
├── model/
│   ├── cnn_model.py
│   ├── train_model.py
│   └── predict.py
├── backend/
│   ├── app.py
│   └── database.py
├── explainability/
│   └── gradcam.py
├── frontend/
│   ├── templates/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── upload.html
│   │   ├── result.html
│   │   └── history.html
│   └── static/css/
│       └── style.css
├── models/
│   └── macular_edema_model.h5  (created after training)
├── dataset/
│   └── train/              (create subdirectories as needed)
├── uploads/                (auto-created when running app)
├── requirements.txt
├── README.md
└── quickstart.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After successful installation:

1. Train the model with real data
2. Evaluate model performance
3. Deploy to production (Heroku, Azure, AWS)
4. Integrate with hospital systems
5. Conduct clinical validation
6. Gather feedback from doctors
7. Improve model with more data
8. Add new features (scheduling, reporting, etc.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12. GETTING HELP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Read documentation:
  - README.md (detailed project info)
  - Code comments in each Python file
  - Flask documentation: https://flask.palletsprojects.com/
  - TensorFlow guide: https://www.tensorflow.org/guide

Resources:
  - Keras API: https://keras.io/
  - OpenCV docs: https://docs.opencv.org/
  - scikit-learn: https://scikit-learn.org/

Debugging:
  - Check console output for error messages
  - Enable debug mode in Flask app.py
  - Add logging statements to track execution
  - Use print() statements strategically

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Installation complete! You're ready to use the Ophthalmic Care System.

For detailed usage instructions, see README.md

Happy analyzing! 👁️
"""

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
