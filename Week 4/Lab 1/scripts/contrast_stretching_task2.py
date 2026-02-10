#!/usr/bin/env python3
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def contrast_stretching(image, smax, smin):
    """
    Apply contrast stretching to an image.
    
    Parameters:
    - image: input image (can be normalized or not)
    - smax: maximum value for output range
    - smin: minimum value for output range
    
    Returns:
    - transformed image
    
    Formula: s = ((smax - smin) / (rmax - rmin)) * (r - rmin) + smin
    """
    # Find min and max intensity values in the input image
    rmin = image.min()
    rmax = image.max()
    
    # Avoid division by zero
    if rmax == rmin:
        return np.ones_like(image) * smin
    
    # Apply contrast stretching
    I_stretched = ((smax - smin) / (rmax - rmin)) * (image - rmin) + smin
    
    # Clip to valid range
    I_stretched = np.clip(I_stretched, smin, smax)
    
    return I_stretched

# Load the image
image_path = "/Users/muhammadjonparpiyev/Documents/DIP/Week 4/4.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

print("\n" + "=" * 70)
print("TASK 2: CONTRAST STRETCHING - Image 4.png")
print("=" * 70)

print(f"\nOriginal Image Statistics:")
print(f"  Shape: {image.shape}")
print(f"  Intensity range: {image.min()} - {image.max()}")
print(f"  Mean: {image.mean():.2f}")
print(f"  Std: {image.std():.2f}")

# ========================
# Part 2.1: Non-normalized with smax=255, smin=0
# ========================
print("\n" + "=" * 70)
print("PART 1: NON-NORMALIZED IMAGE - Contrast Stretching")
print("=" * 70)

stretched_255_0 = contrast_stretching(image.astype('float32'), 255, 0)
stretched_255_0_8bit = stretched_255_0.astype(np.uint8)

print(f"\nContrast Stretching (smax=255, smin=0):")
print(f"  Original range: {image.min()} - {image.max()}")
print(f"  Stretched range: {stretched_255_0_8bit.min()} - {stretched_255_0_8bit.max()}")
print(f"  Mean: {stretched_255_0_8bit.mean():.2f}")
print(f"  Std: {stretched_255_0_8bit.std():.2f}")

# ========================
# Part 2.2: Normalized image with smax=1, smin=0
# ========================
print("\n" + "=" * 70)
print("PART 2: NORMALIZED IMAGE - Contrast Stretching")
print("=" * 70)

# Normalize the image
normalized_image = image.astype('float32') / 255
print(f"\nNormalized Image Statistics:")
print(f"  Range: {normalized_image.min():.4f} - {normalized_image.max():.4f}")
print(f"  Mean: {normalized_image.mean():.4f}")

stretched_norm = contrast_stretching(normalized_image, 1.0, 0.0)
print(f"\nContrast Stretching (smax=1, smin=0) on normalized:")
print(f"  Range: {stretched_norm.min():.4f} - {stretched_norm.max():.4f}")
print(f"  Mean: {stretched_norm.mean():.4f}")

# Convert back to 8-bit for visualization
stretched_norm_8bit = (stretched_norm * 255).astype(np.uint8)
print(f"  As 8-bit range: {stretched_norm_8bit.min()} - {stretched_norm_8bit.max()}")
print(f"  As 8-bit mean: {stretched_norm_8bit.mean():.2f}")

# ========================
# Part 2.3: Different parameter combinations
# ========================
print("\n" + "=" * 70)
print("PART 3: DIFFERENT PARAMETER COMBINATIONS (Non-normalized)")
print("=" * 70)

param_combinations = [
    (255, 0),      # Standard full range
    (255, 50),     # Adjusted smin
    (255, 100),    # Higher smin
    (160, 100),    # Custom range 1
    (200, 50),     # Custom range 2
]

results_dict = {}

for smax, smin in param_combinations:
    stretched = contrast_stretching(image.astype('float32'), smax, smin)
    stretched_8bit = stretched.astype(np.uint8)
    results_dict[(smax, smin)] = stretched_8bit
    
    print(f"\nContrast Stretching (smax={smax}, smin={smin}):")
    print(f"  Output range: {stretched_8bit.min()} - {stretched_8bit.max()}")
    print(f"  Mean: {stretched_8bit.mean():.2f}")
    print(f"  Std: {stretched_8bit.std():.2f}")
    print(f"  Observation: Adjusts the output intensity range to [{smin}, {smax}]")

# ========================
# Visualization
# ========================
print("\n" + "=" * 70)
print("Generating visualizations...")
print("=" * 70)

# Figure 1: Different smax, smin combinations
fig1, axes1 = plt.subplots(2, 3, figsize=(15, 10))
axes1 = axes1.flatten()

# Original
axes1[0].imshow(image, cmap='gray')
axes1[0].set_title('Original Image', fontsize=12, fontweight='bold')
axes1[0].axis('off')

# Non-normalized with smax=255, smin=0
axes1[1].imshow(stretched_255_0_8bit, cmap='gray')
axes1[1].set_title('smax=255, smin=0\n(Non-normalized)', fontsize=11, fontweight='bold')
axes1[1].axis('off')

# Normalized with smax=1, smin=0
axes1[2].imshow(stretched_norm_8bit, cmap='gray')
axes1[2].set_title('smax=1, smin=0\n(Normalized)', fontsize=11, fontweight='bold')
axes1[2].axis('off')

# Custom combinations
custom_params = [(255, 50), (255, 100), (160, 100)]
for idx, (smax, smin) in enumerate(custom_params, 3):
    if idx < len(axes1):
        stretched = results_dict[(smax, smin)]
        axes1[idx].imshow(stretched, cmap='gray')
        axes1[idx].set_title(f'smax={smax}, smin={smin}', fontsize=11, fontweight='bold')
        axes1[idx].axis('off')

plt.tight_layout()
fig1_path = '/Users/muhammadjonparpiyev/Documents/DIP/Week 4/contrast_stretching_comparison.png'
plt.savefig(fig1_path, dpi=150, bbox_inches='tight')
print(f"✓ Saved: {fig1_path}")
plt.close()

# Figure 2: Normalized vs Non-normalized comparison
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))

axes2[0].imshow(image, cmap='gray')
axes2[0].set_title('Original Image', fontsize=12, fontweight='bold')
axes2[0].axis('off')

axes2[1].imshow(stretched_255_0_8bit, cmap='gray')
axes2[1].set_title('Non-normalized\n(smax=255, smin=0)', fontsize=12, fontweight='bold')
axes2[1].axis('off')

axes2[2].imshow(stretched_norm_8bit, cmap='gray')
axes2[2].set_title('Normalized\n(smax=1, smin=0)', fontsize=12, fontweight='bold')
axes2[2].axis('off')

plt.tight_layout()
fig2_path = '/Users/muhammadjonparpiyev/Documents/DIP/Week 4/normalized_vs_nonnormalized.png'
plt.savefig(fig2_path, dpi=150, bbox_inches='tight')
print(f"✓ Saved: {fig2_path}")
plt.close()

# Save results
output_path = '/Users/muhammadjonparpiyev/Documents/DIP/Week 4/4_contrast_stretched.png'
cv2.imwrite(output_path, stretched_255_0_8bit)
print(f"✓ Saved: {output_path}")

# ========================
# Analysis and Observations
# ========================
print("\n" + "=" * 70)
print("ANALYSIS AND OBSERVATIONS")
print("=" * 70)

print(f"""
PART 1 & 2: Normalized vs Non-normalized Impact
════════════════════════════════════════════════

NON-NORMALIZED:
  • Input: 8-bit grayscale (0-255)
  • Stretches to full range [0, 255]
  • Original mean: {image.mean():.2f} → Stretched mean: {stretched_255_0_8bit.mean():.2f}
  • Full dynamic range utilization

NORMALIZED:
  • Input: Float (0-1) after dividing by 255
  • Stretches to range [0, 1], then converts back to 8-bit
  • Mathematically equivalent result to non-normalized
  • Same visual output but normalized allows precision in computation

Impact: NO significant difference in final output. Both methods produce
similar results. Normalized approach is useful for mathematical precision
and handling various image formats uniformly.


PART 3: Different Parameter Combinations
══════════════════════════════════════════

Results Summary:
  • (smax=255, smin=0):    Full range utilization
  • (smax=255, smin=50):   Restricts blacks to value 50 (increases brightness)
  • (smax=255, smin=100):  Further restricts blacks (much brighter)
  • (smax=160, smin=100):  Compresses range to [100, 160] (lower contrast)
  • (smax=200, smin=50):   Custom range [50, 200]

Observations:
  1. Adjusting smin upward → Brightens image (blacks become gray)
  2. Adjusting smax downward → Reduces peak brightness
  3. Smaller range (smax - smin) → Lower contrast
  4. Full range [0, 255] → Maximum contrast enhancement
  5. Custom ranges useful for specific contrast requirements
""")

print("\n" + "=" * 70)
print("TASK 2 COMPLETED")
print("=" * 70 + "\n")
