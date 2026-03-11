"""
Prediction Module for Macular Edema Detection
Loads trained model and performs predictions on new images
Author: Ophthalmic AI Research Team
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import json
from datetime import datetime

class MacularEdemaPredictor:
    """
    Predictor class for Macular Edema severity classification
    """
    
    def __init__(self, model_path='../models/macular_edema_model.h5'):
        """
        Initialize predictor with trained model
        
        Args:
            model_path: Path to trained model file
        """
        self.model_path = model_path
        self.model = None
        self.img_height = 224
        self.img_width = 224
        
        # Severity classes
        self.class_labels = {
            0: 'Normal',
            1: 'Mild Macular Edema',
            2: 'Moderate Macular Edema',
            3: 'Severe Macular Edema'
        }
        
        self.class_descriptions = {
            0: 'No signs of macular edema detected. Retina appears normal.',
            1: 'Mild swelling detected in the macula. Early intervention recommended.',
            2: 'Moderate fluid accumulation in the macula. Treatment advised.',
            3: 'Severe swelling with significant fluid. Urgent medical attention required.'
        }
        
        # Risk values for each class
        self.risk_levels = {
            0: 'Low',
            1: 'Moderate',
            2: 'High',
            3: 'Critical'
        }
        
        self.load_model()
    
    def load_model(self):
        """
        Load pre-trained model from disk
        """
        if not os.path.exists(self.model_path):
            print(f"⚠ Model file not found at: {self.model_path}")
            print("  Please train the model first using train_model.py")
            return False
        
        try:
            self.model = keras.models.load_model(self.model_path)
            print(f"✓ Model loaded successfully from: {self.model_path}")
            return True
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            return False
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for prediction
        
        Args:
            image_path: Path to image file
        
        Returns:
            Preprocessed image array
        """
        try:
            # Load image
            img = Image.open(image_path).convert('RGB')
            
            # Resize to model input size
            img = img.resize((self.img_width, self.img_height), Image.Resampling.LANCZOS)
            
            # Convert to numpy array
            img_array = np.array(img, dtype=np.float32)
            
            # Normalize to range [0, 1]
            img_array = img_array / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            print(f"✗ Error preprocessing image: {str(e)}")
            return None
    
    def predict(self, image_path):
        """
        Predict macular edema severity from image
        
        Args:
            image_path: Path to retinal image
        
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            return {
                'status': 'error',
                'message': 'Model not loaded. Please train the model first.'
            }
        
        # Preprocess image
        img_array = self.preprocess_image(image_path)
        if img_array is None:
            return {
                'status': 'error',
                'message': 'Failed to preprocess image'
            }
        
        # Make prediction
        try:
            prediction = self.model.predict(img_array, verbose=0)
            
            # Get predicted class
            predicted_class = np.argmax(prediction[0])
            confidence = float(np.max(prediction[0]))
            
            # Get all class probabilities
            class_probabilities = {
                self.class_labels[i]: float(prediction[0][i])
                for i in range(len(self.class_labels))
            }
            
            result = {
                'status': 'success',
                'predicted_class': int(predicted_class),
                'severity': self.class_labels[predicted_class],
                'description': self.class_descriptions[predicted_class],
                'confidence': confidence,
                'confidence_percentage': f"{confidence * 100:.2f}%",
                'risk_level': self.risk_levels[predicted_class],
                'all_probabilities': class_probabilities,
                'timestamp': datetime.now().isoformat(),
                'image_path': image_path
            }
            
            return result
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Prediction error: {str(e)}'
            }
    
    def predict_batch(self, image_paths):
        """
        Predict on multiple images
        
        Args:
            image_paths: List of image paths
        
        Returns:
            List of prediction results
        """
        results = []
        for image_path in image_paths:
            result = self.predict(image_path)
            results.append(result)
        
        return results
    
    def get_recommendation(self, severity_class):
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


def demo_prediction():
    """
    Demo prediction on sample image
    """
    print("\n" + "=" * 70)
    print("MACULAR EDEMA DETECTION - PREDICTION DEMO")
    print("=" * 70)
    
    predictor = MacularEdemaPredictor(
        model_path='../models/macular_edema_model.h5'
    )
    
    # Example: Create a sample image for testing
    print("\n→ Creating sample test image...")
    
    test_image_path = '../models/sample_test_image.png'
    
    # Create a sample image if it doesn't exist
    if not os.path.exists(test_image_path):
        sample_img = np.random.rand(224, 224, 3) * 255
        Image.fromarray(sample_img.astype(np.uint8)).save(test_image_path)
        print(f"✓ Sample image created at: {test_image_path}")
    
    # Make prediction
    print("\n→ Making prediction...")
    result = predictor.predict(test_image_path)
    
    # Display results
    if result['status'] == 'success':
        print("\n" + "=" * 70)
        print("PREDICTION RESULTS")
        print("=" * 70)
        print(f"Severity Class: {result['severity']}")
        print(f"Confidence: {result['confidence_percentage']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"\nDescription: {result['description']}")
        print(f"\nMedical Recommendation: {predictor.get_recommendation(result['predicted_class'])}")
        print(f"\nAll Class Probabilities:")
        for class_name, prob in result['all_probabilities'].items():
            print(f"  {class_name}: {prob:.4f} ({prob*100:.2f}%)")
    else:
        print(f"✗ Prediction failed: {result['message']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo_prediction()
