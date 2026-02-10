#!/usr/bin/env python3
"""
Week 04, Lab 01 - Intensity Transformation I
Student Block Implementation with anfield.jpg
"""

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def gamma_correction(I_in, c, gamma):
    """Apply power law (gamma) transformation to an input image."""
    I_norm = I_in.astype('float32') / 255
    I_gamma = c * (I_norm ** gamma)
    I_out = np.clip(I_gamma * 255, 0, 255).astype('uint8')
    return I_out

def contrast_stretching(i_in, s_min=0, s_max=255):
    """Apply linear contrast stretching to an input image."""
    r_min = np.min(i_in)
    r_max = np.max(i_in)

    if r_max == r_min:
        return np.zeros_like(i_in, dtype='uint8')

    i_out = ((s_max - s_min) / (r_max - r_min)) * (i_in - r_min) + s_min
    i_out = np.clip(i_out, s_min, s_max).astype('uint8')

    return i_out

# ============================================================================
# TASK 1: GAMMA CORRECTION ON ANFIELD.JPG
# ============================================================================
print("="*70)
print("TASK 1: GAMMA CORRECTION ON ANFIELD.JPG")
print("="*70)

# Load the image
image_path = "/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/anfield.jpg"
I_anfield = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

print(f"\nOriginal Image Statistics (anfield.jpg):")
print(f"  Shape: {I_anfield.shape}")
print(f"  Min: {I_anfield.min()}, Max: {I_anfield.max()}")
print(f"  Mean: {I_anfield.mean():.2f}, Std: {I_anfield.std():.2f}")

# Test different gamma values
gamma_values = [0.33, 0.5, 0.67, 1.0, 1.5, 2.0, 3.0]
c = 1.0

fig, axes = plt.subplots(2, 4, figsize=(18, 10))
axes = axes.flatten()

# Display original
axes[0].imshow(I_anfield, cmap='gray')
axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
axes[0].axis('off')

print(f"\nGamma Correction Results:")
print(f"{'γ':<6} {'Min':<6} {'Max':<6} {'Mean':<8} {'Std':<8}")
print("-" * 40)

# Apply gamma correction for different values
for idx, gamma in enumerate(gamma_values, 1):
    I_gamma = gamma_correction(I_anfield, c, gamma)
    
    axes[idx].imshow(I_gamma, cmap='gray')
    axes[idx].set_title(f'γ = {gamma}', fontsize=11, fontweight='bold')
    axes[idx].axis('off')
    
    print(f"{gamma:<6.2f} {I_gamma.min():<6} {I_gamma.max():<6} {I_gamma.mean():<8.2f} {I_gamma.std():<8.2f}")

plt.tight_layout()
plt.savefig('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/anfield_gamma_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n✓ Gamma comparison image saved")

# Choose optimal gamma value and apply
best_gamma = 0.67
I_anfield_corrected = gamma_correction(I_anfield, c, best_gamma)

print(f"\nOptimal Gamma: γ = {best_gamma}")
print(f"  Original: min={I_anfield.min()}, max={I_anfield.max()}, mean={I_anfield.mean():.2f}")
print(f"  Corrected: min={I_anfield_corrected.min()}, max={I_anfield_corrected.max()}, mean={I_anfield_corrected.mean():.2f}")
print(f"\nReasoning:")
print(f"  • γ = 0.67 provides good brightness enhancement")
print(f"  • Preserves image details without over-brightening")
print(f"  • Suitable for moderate visibility improvement")

# Display result
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].imshow(I_anfield, cmap='gray')
axes[0].set_title('Original anfield.jpg', fontsize=13, fontweight='bold')
axes[0].axis('off')

axes[1].imshow(I_anfield_corrected, cmap='gray')
axes[1].set_title(f'Gamma Corrected (γ = {best_gamma})', fontsize=13, fontweight='bold')
axes[1].axis('off')

plt.tight_layout()
plt.savefig('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/anfield_gamma_result.png', dpi=150, bbox_inches='tight')
plt.close()

# Save the corrected image
cv2.imwrite('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/anfield_gamma_corrected.jpg', I_anfield_corrected)
print("✓ Gamma corrected image saved")

# ============================================================================
# TASK 2: CONTRAST STRETCHING ON ANFIELD.JPG
# ============================================================================
print("\n" + "="*70)
print("TASK 2: CONTRAST STRETCHING ON ANFIELD.JPG")
print("="*70)

# Part 1: Non-normalized Contrast Stretching (smax=255, smin=0)
print(f"\nPART 1: Non-normalized Contrast Stretching (smax=255, smin=0)")

I_stretched_255_0 = contrast_stretching(I_anfield.astype('float32'), s_min=0, s_max=255)

print(f"  Original: range={I_anfield.min()}-{I_anfield.max()}, mean={I_anfield.mean():.2f}")
print(f"  Stretched: range={I_stretched_255_0.min()}-{I_stretched_255_0.max()}, mean={I_stretched_255_0.mean():.2f}")

# Part 2: Normalized Contrast Stretching (smax=1, smin=0)
print(f"\nPART 2: Normalized Contrast Stretching (smax=1, smin=0)")

I_normalized = I_anfield.astype('float32') / 255
I_stretched_norm = contrast_stretching(I_normalized, s_min=0, s_max=1)
I_stretched_norm_8bit = (I_stretched_norm * 255).astype('uint8')

print(f"  Normalized: range={I_normalized.min():.4f}-{I_normalized.max():.4f}")
print(f"  After stretch: range={I_stretched_norm.min():.4f}-{I_stretched_norm.max():.4f}")
print(f"  As 8-bit: range={I_stretched_norm_8bit.min()}-{I_stretched_norm_8bit.max()}, mean={I_stretched_norm_8bit.mean():.2f}")

# Compare results
max_diff = np.max(np.abs(I_stretched_255_0.astype(float) - I_stretched_norm_8bit.astype(float)))
print(f"\nPART 3: Comparison Results")
print(f"  Max pixel difference: {max_diff:.2f}")
print(f"  Conclusion: Both methods produce {'IDENTICAL' if max_diff < 1 else 'similar'} results")
print(f"  Normalized approach preferred for mathematical precision")

# Part 4: Different parameter combinations
print(f"\nPART 4: Different Parameter Combinations (Non-normalized)")

param_combinations = [
    (255, 0),
    (255, 50),
    (255, 100),
    (160, 100),
    (200, 50),
]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

# Original image
axes[0].imshow(I_anfield, cmap='gray')
axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
axes[0].axis('off')

print(f"\n{'smax':<6} {'smin':<6} {'Min':<6} {'Max':<6} {'Mean':<8} {'Std':<8}")
print("-" * 50)

results_dict = {}
for idx, (smax, smin) in enumerate(param_combinations, 1):
    I_stretched = contrast_stretching(I_anfield.astype('float32'), s_min=smin, s_max=smax)
    results_dict[(smax, smin)] = I_stretched
    
    axes[idx].imshow(I_stretched, cmap='gray')
    axes[idx].set_title(f'smax={smax}, smin={smin}', fontsize=11, fontweight='bold')
    axes[idx].axis('off')
    
    print(f"{smax:<6} {smin:<6} {I_stretched.min():<6} {I_stretched.max():<6} {I_stretched.mean():<8.2f} {I_stretched.std():<8.2f}")

plt.tight_layout()
plt.savefig('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/anfield_contrast_stretching_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nObservations:")
print("  1. Increasing smin → Brightens image (blacks lifted)")
print("  2. Decreasing smax → Reduces peak brightness")
print("  3. Narrower range → Lower contrast")
print("  4. Full range [0,255] → Maximum contrast")
print("  5. Custom ranges allow fine-tuned control")
print("\n✓ Contrast stretching comparison saved")

# Normalized vs Non-normalized visualization
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(I_anfield, cmap='gray')
axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
axes[0].axis('off')

axes[1].imshow(I_stretched_255_0, cmap='gray')
axes[1].set_title('Non-normalized\n(smax=255, smin=0)', fontsize=12, fontweight='bold')
axes[1].axis('off')

axes[2].imshow(I_stretched_norm_8bit, cmap='gray')
axes[2].set_title('Normalized\n(smax=1, smin=0)', fontsize=12, fontweight='bold')
axes[2].axis('off')

plt.tight_layout()
plt.savefig('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/anfield_normalized_vs_nonnormalized.png', dpi=150, bbox_inches='tight')
plt.close()

print("✓ Normalized vs non-normalized comparison saved")

# Save final contrast stretched image
cv2.imwrite('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/anfield_contrast_stretched.jpg', I_stretched_255_0)
print("✓ Contrast stretched image saved")

print("\n" + "="*70)
print("ALL TASKS COMPLETED SUCCESSFULLY")
print("="*70)
print("\nGenerated Files:")
print("  1. anfield_gamma_comparison.png")
print("  2. anfield_gamma_result.png")
print("  3. anfield_gamma_corrected.jpg")
print("  4. anfield_contrast_stretching_comparison.png")
print("  5. anfield_normalized_vs_nonnormalized.png")
print("  6. anfield_contrast_stretched.jpg")
