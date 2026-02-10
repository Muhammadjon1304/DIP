#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def gamma_correction(image, c, gamma):
    """
    Apply gamma correction (power law transformation) to an image.
    
    Parameters:
    - image: input image
    - c: intensity scaling factor
    - gamma: power value (γ)
    
    Returns:
    - transformed image (normalized to [0, 1])
    """
    # Normalize the input image
    I_norm = image.astype('float32') / 255
    
    # Apply power law transformation
    I_transformed = c * (I_norm ** gamma)
    
    # Clip values to [0, 1] range
    I_transformed = np.clip(I_transformed, 0, 1)
    
    return I_transformed

# Load the image
image_path = "/Users/muhammadjonparpiyev/Documents/DIP/Week 4/4.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

print("=" * 60)
print("TASK 1: GAMMA CORRECTION - Image 4.png")
print("=" * 60)
print(f"\nImage shape: {image.shape}")
print(f"Image intensity range: {image.min()} - {image.max()}")
print(f"Image mean intensity: {image.mean():.2f}")
print(f"Image std intensity: {image.std():.2f}")

# Test different gamma values
gamma_values = [0.33, 0.5, 0.67, 1.0, 1.5, 2.0, 3.0]
c = 1.0  # scaling factor

print("\n" + "=" * 60)
print("Testing different gamma values...")
print("=" * 60)

# Create figure with subplots
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

# Original image
axes[0].imshow(image, cmap='gray')
axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
axes[0].axis('off')

# Apply gamma correction with different values
for idx, gamma in enumerate(gamma_values, 1):
    corrected = gamma_correction(image, c, gamma)
    # Convert back to 0-255 range for display
    corrected_8bit = (corrected * 255).astype(np.uint8)
    
    axes[idx].imshow(corrected_8bit, cmap='gray')
    axes[idx].set_title(f'γ = {gamma}', fontsize=11)
    axes[idx].axis('off')
    
    # Print statistics for each gamma
    print(f"  γ = {gamma}: min={corrected_8bit.min()}, max={corrected_8bit.max()}, mean={corrected_8bit.mean():.2f}")

plt.tight_layout()
gamma_comp_path = '/Users/muhammadjonparpiyev/Documents/DIP/Week 4/gamma_comparison.png'
plt.savefig(gamma_comp_path, dpi=150, bbox_inches='tight')
print(f"\n✓ Gamma comparison image saved: {gamma_comp_path}")
plt.close()

# Apply the best gamma value (0.5 for brightening the dark image)
print("\n" + "=" * 60)
print("ANALYSIS AND CHOICE:")
print("=" * 60)

best_gamma = 0.5
corrected_image = gamma_correction(image, c, best_gamma)
corrected_8bit = (corrected_image * 255).astype(np.uint8)

print(f"\nChosen γ = {best_gamma} (Square root transformation)")
print(f"\nReasoning:")
print(f"  • Original image is dark with low visibility")
print(f"  • γ < 1 produces brightening effect (applying square root)")
print(f"  • γ = 0.5 provides significant enhancement without over-brightening")
print(f"  • This improves visibility of details in dark regions")
print(f"\nTransformation formula: T(r) = c × r^γ = 1.0 × r^{best_gamma}")
print(f"\nResult statistics:")
print(f"  • Original: min={image.min()}, max={image.max()}, mean={image.mean():.2f}")
print(f"  • Corrected: min={corrected_8bit.min()}, max={corrected_8bit.max()}, mean={corrected_8bit.mean():.2f}")

# Display the result
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))

axes2[0].imshow(image, cmap='gray')
axes2[0].set_title('Original Image (4.png)', fontsize=12, fontweight='bold')
axes2[0].axis('off')

axes2[1].imshow(corrected_8bit, cmap='gray')
axes2[1].set_title(f'Gamma Corrected (γ = {best_gamma})', fontsize=12, fontweight='bold')
axes2[1].axis('off')

plt.tight_layout()
result_path = '/Users/muhammadjonparpiyev/Documents/DIP/Week 4/4_gamma_result.png'
plt.savefig(result_path, dpi=150, bbox_inches='tight')
print(f"\n✓ Result comparison image saved: {result_path}")
plt.close()

# Save the corrected image
output_path = "/Users/muhammadjonparpiyev/Documents/DIP/Week 4/4_gamma_corrected.png"
cv2.imwrite(output_path, corrected_8bit)
print(f"✓ Corrected image saved: {output_path}")

print("\n" + "=" * 60)
print("TASK 1 COMPLETED")
print("=" * 60)
