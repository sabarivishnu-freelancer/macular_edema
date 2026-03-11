"""
CNN Model Architecture for Macular Edema Detection
Author: Ophthalmic AI Research Team
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
import numpy as np

class MacularEdemaCNN:
    """
    Convolutional Neural Network for Macular Edema Classification
    Severity Classes: 0 (Normal), 1 (Mild), 2 (Moderate), 3 (Severe)
    """
    
    def __init__(self, img_height=224, img_width=224, num_classes=4):
        """
        Initialize CNN model parameters
        
        Args:
            img_height: Input image height (default: 224)
            img_width: Input image width (default: 224)
            num_classes: Number of severity classes (default: 4)
        """
        self.img_height = img_height
        self.img_width = img_width
        self.num_classes = num_classes
        self.model = None
    
    def build_custom_cnn(self):
        """
        Build custom CNN architecture with Conv2D, BatchNorm, Dropout, and Dense layers
        
        Returns:
            Compiled Keras model
        """
        model = models.Sequential([
            # Block 1
            layers.Input(shape=(self.img_height, self.img_width, 3)),
            layers.Conv2D(32, (3, 3), padding='same'),
            layers.BatchNormalization(),
            layers.Activation('relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 2
            layers.Conv2D(64, (3, 3), padding='same'),
            layers.BatchNormalization(),
            layers.Activation('relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 3
            layers.Conv2D(128, (3, 3), padding='same'),
            layers.BatchNormalization(),
            layers.Activation('relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 4
            layers.Conv2D(256, (3, 3), padding='same'),
            layers.BatchNormalization(),
            layers.Activation('relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Flatten and Dense layers
            layers.Flatten(),
            layers.Dense(512),
            layers.BatchNormalization(),
            layers.Activation('relu'),
            layers.Dropout(0.5),
            
            layers.Dense(256),
            layers.BatchNormalization(),
            layers.Activation('relu'),
            layers.Dropout(0.5),
            
            # Output layer
            layers.Dense(self.num_classes),
            layers.Activation('softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        self.model = model
        return model
    
    def build_resnet_transfer_learning(self):
        """
        Build model using transfer learning with ResNet50 pre-trained on ImageNet
        
        Returns:
            Compiled Keras model
        """
        # Load pre-trained ResNet50
        base_model = ResNet50(
            input_shape=(self.img_height, self.img_width, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom layers on top
        model = models.Sequential([
            layers.Input(shape=(self.img_height, self.img_width, 3)),
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        self.model = model
        return model
    
    def get_model(self):
        """
        Get the compiled model
        
        Returns:
            Keras model
        """
        return self.model
    
    def get_model_summary(self):
        """
        Print model summary
        """
        if self.model is None:
            print("Model not built yet. Call build_custom_cnn() or build_resnet_transfer_learning()")
        else:
            self.model.summary()


if __name__ == "__main__":
    # Test model creation
    print("=" * 60)
    print("Macular Edema CNN Model - Test")
    print("=" * 60)
    
    # Create custom CNN
    cnn = MacularEdemaCNN(img_height=224, img_width=224, num_classes=4)
    model = cnn.build_custom_cnn()
    
    print("\n✓ Custom CNN Model Built Successfully!")
    print(f"✓ Total Parameters: {model.count_params():,}")
    
    # Create ResNet model
    print("\n" + "=" * 60)
    print("Building ResNet50 Transfer Learning Model...")
    print("=" * 60)
    cnn_resnet = MacularEdemaCNN(img_height=224, img_width=224, num_classes=4)
    model_resnet = cnn_resnet.build_resnet_transfer_learning()
    
    print("\n✓ ResNet50 Transfer Learning Model Built Successfully!")
    print(f"✓ Total Parameters: {model_resnet.count_params():,}")
