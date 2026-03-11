"""
Grad-CAM Implementation for Explainable AI
Visualizes which regions of the image influence the prediction
Author: Ophthalmic AI Research Team
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
import cv2
import os

class GradCAM:
    """
    Gradient-weighted Class Activation Mapping (Grad-CAM)
    Explains predictions by visualizing important image regions
    """
    
    def __init__(self, model_path='../models/macular_edema_model.h5', layer_name='conv2d_3'):
        """
        Initialize Grad-CAM
        
        Args:
            model_path: Path to trained model
            layer_name: Convolutional layer to visualize
        """
        self.model_path = model_path
        self.layer_name = layer_name
        self.model = None
        self.grad_model = None
        
        # Class labels
        self.class_labels = {
            0: 'Normal',
            1: 'Mild Macular Edema',
            2: 'Moderate Macular Edema',
            3: 'Severe Macular Edema'
        }
        
        self.load_model()
    
    def load_model(self):
        """
        Load the trained model
        """
        if not os.path.exists(self.model_path):
            print(f"⚠ Model file not found at: {self.model_path}")
            return False
        
        try:
            self.model = keras.models.load_model(self.model_path)
            print(f"✓ Model loaded for Grad-CAM")
            return True
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            return False
    
    def make_gradcam_heatmap(self, img_array, pred_index=None):
        """
        Generate Grad-CAM heatmap
        
        Args:
            img_array: Input image array (preprocessed)
            pred_index: Class index to explain (None = use predicted class)
        
        Returns:
            Heatmap array
        """
        if self.model is None:
            print("⚠ Model not loaded!")
            return None
        
        # Create model to output last conv layer and predictions
        last_conv_layer = self.model.get_layer(self.get_last_conv_layer_name())
        last_conv_layer_model = keras.Model(
            self.model.inputs,
            [last_conv_layer.output, self.model.output]
        )
        
        with tf.GradientTape() as tape:
            conv_outputs, predictions = last_conv_layer_model(img_array)
            
            if pred_index is None:
                pred_index = tf.argmax(predictions[0])
            
            class_channel = predictions[:, pred_index]
        
        grads = tape.gradient(class_channel, conv_outputs)
        
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        
        return heatmap.numpy()
    
    def get_last_conv_layer_name(self):
        """
        Get the name of the last convolutional layer
        
        Returns:
            Layer name
        """
        for layer in reversed(self.model.layers):
            if 'conv' in layer.name.lower():
                return layer.name
        return 'conv2d_3'
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for model input
        
        Args:
            image_path: Path to image
        
        Returns:
            Preprocessed array and original image
        """
        img = Image.open(image_path).convert('RGB')
        img_original = np.array(img)
        
        img = img.resize((224, 224), Image.Resampling.LANCZOS)
        img_array = np.array(img, dtype=np.float32)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array, img_original
    
    def visualize_gradcam(self, image_path, save_path=None, show_plot=True):
        """
        Generate and visualize Grad-CAM heatmap
        
        Args:
            image_path: Path to input image
            save_path: Path to save visualization
            show_plot: Whether to display the plot
        
        Returns:
            Figure and heatmap
        """
        if self.model is None:
            print("⚠ Model not loaded!")
            return None, None
        
        print(f"\n→ Generating Grad-CAM for: {image_path}")
        
        # Preprocess
        img_array, img_original = self.preprocess_image(image_path)
        
        # Predict
        prediction = self.model.predict(img_array, verbose=0)
        predicted_class = np.argmax(prediction[0])
        confidence = np.max(prediction[0])
        
        # Generate heatmap
        heatmap = self.make_gradcam_heatmap(img_array, pred_index=predicted_class)
        
        if heatmap is None:
            print("✗ Error generating heatmap")
            return None, None
        
        # Resize heatmap to original image size
        heatmap = cv2.resize(heatmap, (224, 224))
        
        # Normalize to 0-255
        heatmap = np.uint8(255 * heatmap)
        
        # Create figure
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Original image
        axes[0, 0].imshow(img_original)
        axes[0, 0].set_title('Original Retinal Image', fontweight='bold')
        axes[0, 0].axis('off')
        
        # Heatmap
        im = axes[0, 1].imshow(heatmap, cmap='jet')
        axes[0, 1].set_title('Grad-CAM Heatmap', fontweight='bold')
        axes[0, 1].axis('off')
        plt.colorbar(im, ax=axes[0, 1], fraction=0.046, pad=0.04)
        
        # Overlay
        img_resized = cv2.resize(img_original, (224, 224))
        img_resized = img_resized.astype(np.float32) / 255.0
        
        heatmap_color = cm.jet(heatmap / 255.0)[:, :, :3]
        overlay = cv2.addWeighted(img_resized, 0.6, heatmap_color, 0.4, 0)
        
        axes[1, 0].imshow(overlay)
        axes[1, 0].set_title('Overlay (Original + Heatmap)', fontweight='bold')
        axes[1, 0].axis('off')
        
        # Prediction info
        axes[1, 1].axis('off')
        info_text = f"""
PREDICTION RESULTS
{'=' * 40}

Predicted Severity:
{self.class_labels[predicted_class]}

Confidence: {confidence*100:.2f}%

Probabilities:
"""
        for idx in range(4):
            prob = prediction[0][idx]
            info_text += f"\n{self.class_labels[idx]}: {prob*100:.2f}%"
        
        axes[1, 1].text(0.1, 0.5, info_text, fontsize=11, 
                       verticalalignment='center',
                       fontfamily='monospace',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Visualization saved to: {save_path}")
        
        if show_plot:
            plt.show()
        
        return fig, heatmap
    
    def generate_batch_explanations(self, image_paths, output_dir='../models/explanations'):
        """
        Generate explanations for multiple images
        
        Args:
            image_paths: List of image paths
            output_dir: Directory to save visualizations
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n→ Generating explanations for {len(image_paths)} images...")
        
        for i, image_path in enumerate(image_paths):
            save_path = os.path.join(
                output_dir,
                f'gradcam_{i:03d}.png'
            )
            self.visualize_gradcam(image_path, save_path=save_path, show_plot=False)
        
        print(f"✓ All explanations generated in: {output_dir}")


def demo_gradcam():
    """
    Demo Grad-CAM visualization
    """
    print("\n" + "=" * 70)
    print("GRAD-CAM VISUALIZATION DEMO")
    print("=" * 70)
    
    gradcam = GradCAM(
        model_path='../models/macular_edema_model.h5',
        layer_name='conv2d_3'
    )
    
    # Create sample image for testing
    test_image_path = '../models/sample_gradcam_image.png'
    
    if not os.path.exists(test_image_path):
        sample_img = np.random.rand(224, 224, 3) * 255
        Image.fromarray(sample_img.astype(np.uint8)).save(test_image_path)
        print(f"\n✓ Sample image created at: {test_image_path}")
    
    # Generate visualization
    fig, heatmap = gradcam.visualize_gradcam(
        image_path=test_image_path,
        save_path='../models/gradcam_visualization.png',
        show_plot=False
    )
    
    if heatmap is not None:
        print("✓ Grad-CAM visualization generated successfully!")
    else:
        print("✗ Failed to generate Grad-CAM visualization")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo_gradcam()
