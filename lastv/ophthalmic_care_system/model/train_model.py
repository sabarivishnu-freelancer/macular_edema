"""
Training Script for Macular Edema CNN Model
Handles data loading, augmentation, training, and model evaluation
Author: Ophthalmic AI Research Team
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
from cnn_model import MacularEdemaCNN
import warnings
warnings.filterwarnings('ignore')

class MacularEdemaTrainer:
    """
    Trainer class for Macular Edema CNN model
    """
    
    def __init__(self, dataset_path='../dataset', model_save_path='../models'):
        """
        Initialize trainer
        
        Args:
            dataset_path: Path to dataset folder
            model_save_path: Path to save trained model
        """
        self.dataset_path = dataset_path
        self.model_save_path = model_save_path
        self.model = None
        self.history = None
        
        # Create model save path if it doesn't exist
        os.makedirs(model_save_path, exist_ok=True)
        
        # Class labels
        self.class_labels = {
            0: 'Normal',
            1: 'Mild Macular Edema',
            2: 'Moderate Macular Edema',
            3: 'Severe Macular Edema'
        }
    
    def create_sample_dataset(self, num_samples_per_class=50):
        """
        Create sample synthetic dataset for demonstration
        In production, use real retinal OCT/fundus images from Kaggle
        
        Args:
            num_samples_per_class: Number of samples per severity class
        """
        print("\n" + "=" * 60)
        print("Creating Sample Dataset for Demonstration")
        print("=" * 60)
        
        classes = ['normal', 'mild', 'moderate', 'severe']
        img_height, img_width = 224, 224
        
        # Create directory structure
        for class_name in classes:
            class_dir = os.path.join(self.dataset_path, 'train', class_name)
            os.makedirs(class_dir, exist_ok=True)
        
        # Generate synthetic images (random noise with patterns)
        for class_idx, class_name in enumerate(classes):
            print(f"\n✓ Generating {num_samples_per_class} images for {class_name.upper()}...")
            class_dir = os.path.join(self.dataset_path, 'train', class_name)
            
            for i in range(num_samples_per_class):
                # Create synthetic retinal-like image
                # In real scenario: load actual OCT/fundus images
                img = np.random.rand(img_height, img_width, 3) * 255
                
                # Add some pattern based on class
                if class_idx > 0:  # Add edema patterns
                    y, x = np.ogrid[:img_height, :img_width]
                    center_y, center_x = img_height // 2, img_width // 2
                    
                    # Create circular region (macula)
                    radius = 50 + (class_idx * 20)
                    mask = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
                    img[mask] = img[mask] * (0.5 + class_idx * 0.2)
                
                # Save as PNG
                img = np.clip(img, 0, 255).astype(np.uint8)
                from PIL import Image
                Image.fromarray(img).save(
                    os.path.join(class_dir, f'{class_name}_{i:03d}.png')
                )
        
        print("\n✓ Sample dataset created successfully!")
        print(f"  Location: {self.dataset_path}")
        return True
    
    def load_and_preprocess_data(self, batch_size=32, validation_split=0.2, test_split=0.1):
        """
        Load and preprocess image data with augmentation
        
        Args:
            batch_size: Batch size for training
            validation_split: Portion of data for validation
            test_split: Portion of data for testing
        
        Returns:
            train_generator, validation_generator, test_generator
        """
        print("\n" + "=" * 60)
        print("Loading and Preprocessing Data")
        print("=" * 60)
        
        train_path = os.path.join(self.dataset_path, 'train')
        
        if not os.path.exists(train_path):
            print("⚠ Training data not found. Creating sample dataset...")
            self.create_sample_dataset()
        
        # Define image augmentation for training
        train_augmentation = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            fill_mode='nearest',
            validation_split=validation_split
        )
        
        # Load training data with augmentation
        train_generator = train_augmentation.flow_from_directory(
            train_path,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        # Load validation data
        validation_generator = train_augmentation.flow_from_directory(
            train_path,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        print(f"\n✓ Training samples: {train_generator.samples}")
        print(f"✓ Validation samples: {validation_generator.samples}")
        print(f"✓ Batch size: {batch_size}")
        print(f"✓ Classes: {train_generator.class_indices}")
        
        return train_generator, validation_generator
    
    def train(self, epochs=50, batch_size=32, model_type='custom'):
        """
        Train the model
        
        Args:
            epochs: Number of training epochs
            batch_size: Batch size
            model_type: 'custom' or 'resnet'
        
        Returns:
            Training history
        """
        print("\n" + "=" * 60)
        print("Training Macular Edema Detection Model")
        print("=" * 60)
        
        # Load data
        train_gen, val_gen = self.load_and_preprocess_data(batch_size=batch_size)
        
        # Build model
        cnn = MacularEdemaCNN(img_height=224, img_width=224, num_classes=4)
        
        if model_type == 'resnet':
            print("\n→ Building ResNet50 Transfer Learning Model...")
            self.model = cnn.build_resnet_transfer_learning()
        else:
            print("\n→ Building Custom CNN Architecture...")
            self.model = cnn.build_custom_cnn()
        
        print(f"✓ Model built with {self.model.count_params():,} parameters")
        
        # Callbacks
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )
        
        model_checkpoint = ModelCheckpoint(
            os.path.join(self.model_save_path, 'best_model.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=0
        )
        
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=0.00001,
            verbose=1
        )
        
        # Train model
        print("\n→ Starting training...")
        self.history = self.model.fit(
            train_gen,
            epochs=epochs,
            validation_data=val_gen,
            callbacks=[early_stop, model_checkpoint, reduce_lr],
            verbose=1
        )
        
        print("\n✓ Training completed!")
        return self.history
    
    def evaluate(self, test_generator=None):
        """
        Evaluate model performance
        
        Args:
            test_generator: Test data generator
        
        Returns:
            Evaluation metrics
        """
        print("\n" + "=" * 60)
        print("Model Evaluation")
        print("=" * 60)
        
        if self.model is None:
            print("⚠ Model not trained yet!")
            return None
        
        # Use validation data if test data not provided
        if test_generator is None:
            _, test_generator = self.load_and_preprocess_data()
        
        # Evaluate
        eval_results = self.model.evaluate(test_generator, verbose=0)
        
        print(f"\n✓ Test Loss: {eval_results[0]:.4f}")
        print(f"✓ Test Accuracy: {eval_results[1]:.4f}")
        print(f"✓ Precision: {eval_results[2]:.4f}")
        print(f"✓ Recall: {eval_results[3]:.4f}")
        
        return eval_results
    
    def plot_training_history(self, save_path=None):
        """
        Plot training history
        
        Args:
            save_path: Path to save plot
        """
        if self.history is None:
            print("⚠ No training history available!")
            return
        
        print("\n" + "=" * 60)
        print("Plotting Training History")
        print("=" * 60)
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Accuracy plot
        axes[0].plot(self.history.history['accuracy'], label='Train Accuracy', linewidth=2)
        axes[0].plot(self.history.history['val_accuracy'], label='Val Accuracy', linewidth=2)
        axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Loss plot
        axes[1].plot(self.history.history['loss'], label='Train Loss', linewidth=2)
        axes[1].plot(self.history.history['val_loss'], label='Val Loss', linewidth=2)
        axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved to: {save_path}")
        
        plt.show()
    
    def save_model(self, model_name='macular_edema_model.h5'):
        """
        Save trained model
        
        Args:
            model_name: Name of the model file
        """
        if self.model is None:
            print("⚠ No model to save!")
            return
        
        model_path = os.path.join(self.model_save_path, model_name)
        self.model.save(model_path)
        
        print(f"\n✓ Model saved successfully!")
        print(f"  Location: {model_path}")


def train_macular_edema_model():
    """
    Main training pipeline
    """
    print("\n" + "=" * 70)
    print("MACULAR EDEMA DETECTION CNN - TRAINING PIPELINE")
    print("=" * 70)
    
    # Initialize trainer
    trainer = MacularEdemaTrainer(
        dataset_path='../dataset',
        model_save_path='../models'
    )
    
    # Train model
    trainer.train(epochs=30, batch_size=32, model_type='custom')
    
    # Evaluate
    trainer.evaluate()
    
    # Plot training history
    trainer.plot_training_history(
        save_path='../models/training_history.png'
    )
    
    # Save model
    trainer.save_model('macular_edema_model.h5')
    
    print("\n" + "=" * 70)
    print("✓ TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    train_macular_edema_model()
