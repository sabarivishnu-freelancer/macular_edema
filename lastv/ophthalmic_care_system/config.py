"""
Configuration file for the Ophthalmic Care System
Edit these settings to customize the application
"""

# Flask Configuration
FLASK_ENV = 'development'  # Change to 'production' for deployment
FLASK_DEBUG = True
SECRET_KEY = 'your-secret-key-change-in-production'
SERVER_PORT = 5000
SERVER_HOST = '0.0.0.0'

# Database Configuration
DATABASE_PATH = 'ophthalmic_care.db'
DATABASE_TYPE = 'sqlite'  # sqlite or postgresql

# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

# Model Configuration
MODEL_PATH = 'models/macular_edema_model.h5'
IMG_HEIGHT = 224
IMG_WIDTH = 224
NUM_CLASSES = 4

# Training Configuration
TRAINING_EPOCHS = 30
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2
LEARNING_RATE = 0.001

# Class Labels
CLASS_LABELS = {
    0: 'Normal',
    1: 'Mild Macular Edema',
    2: 'Moderate Macular Edema',
    3: 'Severe Macular Edema'
}

# Risk Levels
RISK_LEVELS = {
    0: 'Low',
    1: 'Moderate',
    2: 'High',
    3: 'Critical'
}

# Class Descriptions
CLASS_DESCRIPTIONS = {
    0: 'No signs of macular edema detected. Retina appears normal.',
    1: 'Mild swelling detected in the macula. Early intervention recommended.',
    2: 'Moderate fluid accumulation in the macula. Treatment advised.',
    3: 'Severe swelling with significant fluid. Urgent medical attention required.'
}

# Medical Recommendations
RECOMMENDATIONS = {
    0: 'Continue regular eye examinations. No immediate intervention needed.',
    1: 'Monitor closely. Consider anti-VEGF therapy or corticosteroid treatment.',
    2: 'Urgent treatment recommended. Refer to retina specialist immediately.',
    3: 'CRITICAL: Immediate specialist consultation required. Consider emergency treatment.'
}

# Grad-CAM Configuration
GRADCAM_LAYER_NAME = 'conv2d_3'
GRADCAM_OUTPUT_DIR = 'models/explanations'

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'ophthalmic_care.log'

# Security
REQUIRE_HTTPS = False  # Set to True in production
SESSION_TIMEOUT = 3600  # 1 hour in seconds
PASSWORD_MIN_LENGTH = 8

# Email Configuration (Optional)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-app-password'
ENABLE_EMAIL_NOTIFICATIONS = False

# Feature Flags
ENABLE_GRADCAM = True
ENABLE_PATIENT_EXPORT = True
ENABLE_BATCH_UPLOAD = False
ENABLE_API_KEY_AUTH = False

# Performance
ENABLE_CACHING = True
CACHE_TIMEOUT = 300  # 5 minutes
MAX_WORKERS = 4

# Analytics
TRACK_USER_ACTIVITY = True
ENABLE_USAGE_STATISTICS = True

# Testing
TESTING = False
TEST_DATABASE = 'ophthalmic_care_test.db'
