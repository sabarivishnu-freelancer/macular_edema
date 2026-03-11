"""
Flask Backend Application
Ophthalmic Care System API
Author: Ophthalmic AI Research Team
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sys
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import DatabaseManager

# Flask app configuration
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'your_secret_key_change_in_production'

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize database
db = DatabaseManager(os.path.join(os.path.dirname(__file__), '..', 'ophthalmic_care.db'))

# Lazy load ML components
predictor = None
gradcam = None

def get_predictor():
    """Lazy load predictor"""
    global predictor
    if predictor is None:
        try:
            from model.predict import MacularEdemaPredictor
            predictor = MacularEdemaPredictor(
                model_path=os.path.join(os.path.dirname(__file__), '..', 'models', 'macular_edema_model.h5')
            )
        except Exception as e:
            print(f"Warning: Could not load predictor: {e}")
            return None
    return predictor

def get_gradcam():
    """Lazy load GradCAM"""
    global gradcam
    if gradcam is None:
        try:
            from explainability.gradcam import GradCAM
            gradcam = GradCAM(
                model_path=os.path.join(os.path.dirname(__file__), '..', 'models', 'macular_edema_model.h5')
            )
        except Exception as e:
            print(f"Warning: Could not load GradCAM: {e}")
            return None
    return gradcam



def allowed_file(filename):
    """
    Check if file extension is allowed
    
    Args:
        filename: Filename to check
    
    Returns:
        Boolean indicating if file is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_recommendation(severity_class):
    """
    Get medical recommendation based on severity
    
    Args:
        severity_class: Predicted class (0-3)
    
    Returns:
        Recommendation string
    """
    recommendations = {
        0: 'Continue regular eye examinations. No immediate intervention needed.',
        1: 'Monitor closely. Consider anti-VEGF therapy or corticosteroid treatment.',
        2: 'Urgent treatment recommended. Refer to retina specialist immediately.',
        3: 'CRITICAL: Immediate specialist consultation required. Consider emergency treatment.'
    }
    return recommendations.get(severity_class, 'Consult eye care specialist')


# Routes

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.authenticate_user(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('login.html', error='Passwords do not match')
        
        success, user_id = db.create_user(username, password, email, 'doctor')
        
        if success:
            return render_template('login.html', success='Registration successful! Please login.')
        else:
            return render_template('login.html', error='Username or email already exists')
    
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    """Doctor dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get statistics
    stats = db.get_dashboard_stats()
    
    return render_template('dashboard.html',
                         username=session.get('username'),
                         stats=stats)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload retinal image for analysis"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Check if file is in request
        if 'image' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'status': 'error', 'message': 'Invalid file format'}), 400
        
        # Get patient information
        patient_name = request.form.get('patient_name')
        patient_age = request.form.get('patient_age')
        patient_gender = request.form.get('patient_gender')
        patient_contact = request.form.get('patient_contact')
        
        try:
            # Create patient record
            patient_id = db.create_patient(
                patient_name,
                int(patient_age),
                patient_gender,
                patient_contact
            )
            
            if not patient_id:
                return jsonify({'status': 'error', 'message': 'Failed to create patient record'}), 500
            
            # Save uploaded file
            filename = f"patient_{patient_id}_{secure_filename(file.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Make prediction
            pred = get_predictor()
            if pred is None:
                return jsonify({'status': 'error', 'message': 'ML model not available. Demo mode enabled.'}), 500
            
            prediction_result = pred.predict(filepath)
            
            if prediction_result['status'] != 'success':
                return jsonify(prediction_result), 500
            
            # Add recommendation
            prediction_result['recommendation'] = get_recommendation(
                prediction_result['predicted_class']
            )
            
            # Create examination record
            exam_id = db.create_examination(
                patient_id,
                session.get('user_id'),
                filepath,
                prediction_result
            )
            
            if not exam_id:
                return jsonify({'status': 'error', 'message': 'Failed to save examination'}), 500
            
            # Generate Grad-CAM explanation
            try:
                grad = get_gradcam()
                if grad is not None:
                    gradcam_path = os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        f'gradcam_{exam_id}.png'
                    )
                    grad.visualize_gradcam(
                        filepath,
                        save_path=gradcam_path,
                        show_plot=False
                    )
                    prediction_result['gradcam_path'] = gradcam_path
            except Exception as e:
                print(f"Warning: Grad-CAM generation failed: {e}")
            
            prediction_result['patient_id'] = patient_id
            prediction_result['exam_id'] = exam_id
            
            return jsonify(prediction_result)
        
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return render_template('upload.html', username=session.get('username'))


@app.route('/result/<int:exam_id>')
def result(exam_id):
    """Display prediction result"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    exam = db.get_examination(exam_id)
    
    if not exam:
        return "Examination not found", 404
    
    patient = db.get_patient(exam['patient_id'])
    
    return render_template('result.html',
                         username=session.get('username'),
                         exam=exam,
                         patient=patient)


@app.route('/history/<int:patient_id>')
def history(patient_id):
    """View patient examination history"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    patient = db.get_patient(patient_id)
    examinations = db.get_patient_examinations(patient_id)
    
    return render_template('history.html',
                         username=session.get('username'),
                         patient=patient,
                         examinations=examinations)


@app.route('/api/patients/search', methods=['GET'])
def search_patients():
    """API endpoint to search patients"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    search_term = request.args.get('q', '')
    
    if len(search_term) < 2:
        return jsonify({'results': []})
    
    results = db.search_patients(search_term)
    
    return jsonify({'results': results})


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """API endpoint to get dashboard statistics"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    stats = db.get_dashboard_stats()
    
    return jsonify(stats)


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("OPHTHALMIC CARE SYSTEM - FLASK BACKEND")
    print("=" * 70)
    print(f"\n✓ Upload folder: {UPLOAD_FOLDER}")
    print(f"✓ Database: ophthalmic_care.db")
    print(f"✓ Model: macular_edema_model.h5")
    print(f"\n→ Starting Flask application on http://localhost:5000")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
