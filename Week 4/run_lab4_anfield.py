#!/usr/bin/env python3
"""
Lab 4 - Intensity Transformation I: Complete Analysis
Working with anfield.jpg
"""

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ====================================================================
# FUNCTIONS
# ====================================================================

def gamma_correction(image, c, gamma):
    """Apply gamma correction (power law transformation)."""
    I_norm = image.astype('float32') / 255
    I_transformed = c * (I_norm ** gamma)
    I_transformed = np.clip(I_transformed, 0, 1)
    return I_transformed

def contrast_stretching(image, smax, smin):
    """Apply contrast stretching to an image."""
    rmin = image.min()
    rmax = image.max()
    
    if rmax == rmin:
        return np.ones_like(image) * smin
    
    I_stretched = ((smax - smin) / (rmax - rmin)) * (image - rmin) + smin
    I_stretched = np.clip(I_stretched, smin, smax)
    return I_stretched

# ====================================================================
# LOAD AND ANALYZE IMAGE
# ====================================================================

image_path = "/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/anfield.jpg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

print("\n" + "="*70)
print("LAB 4 - INTENSITY TRANSFORMATION I: ANFIELD.JPG")
print("="*70)

print(f"\nIMAGE ANALYSIS: anfield.jpg")
print(f"  Shape: {image.shape}")
print(f"  Min intensity: {image.min()}")
print(f"  Max intensity: {image.max()}")
print(f"  Mean intensity: {image.mean():.2f}")
print(f"  Std deviation: {image.std():.2f}")

# ====================================================================
# TASK 1: GAMMA CORRECTION
# ====================================================================

print("\n" + "="*70)
print("TASK 1: POWER LAW TRANSFORMATION (GAMMA CORRECTION)")
print("="*70)

gamma_values = [0.33, 0.5, 0.67, 1.0, 1.5, 2.0, 3.0]
c = 1.0

# Test all gamma values
fig, axes = plt.subplots(2, 4, figsize=(18, 10))
axes = axes.flatten()

axes[0].imshow(image, cmap='gray')
axes[0].set_title('Original Image', fontsize=13, fontweight='bold')
axes[0].axis('off')

print(f"\nGamma Correction Results:")
print(f"{'γ':<6} {'Min':<6} {'Max':<6} {'Mean':<8} {'Std':<8}")
print("-" * 40)

results_gamma = {}
for idx, gamma in enumerate(gamma_values, 1):
    corrected = gamma_correction(image, c, gamma)
    corrected_8bit = (corrected * 255).astype(np.uint8)
    results_gamma[gamma] = corrected_8bit
    
    axes[idx].imshow(corrected_8bit, cmap='gray')
    axes[idx].set_title(f'γ = {gamma}', fontsize=12, fontweight='bold')
    axes[idx].axis('off')
    
    print(f"{gamma:<6.2f} {corrected_8bit.min():<6} {corrected_8bit.max():<6} {corrected_8bit.mean():<8.2f} {corrected_8bit.std():<8.2f}")

plt.tight_layout()
plt.savefig('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/anfield_gamma_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✓ Saved: anfield_gamma_comparison.png")

# Apply optimal gamma
best_gamma = 0.67
corrected_image = gamma_correction(image, c, best_gamma)
corrected_8bit = (corrected_image * 255).astype(np.uint8)

print(f"\n" + "-"*70)
print(f"OPTIMAL CHOICE: γ = {best_gamma}")
print("-"*70)
print(f"Original: min={image.min()}, max={image.max()}, mean={image.mean():.2f}")
print(f"Corrected: min={corrected_8bit.min()}, max={corrected_8bit.max()}, mean={corrected_8bit.mean():.2f}")
print(f"\nReasoning: γ = 0.67 provides good brightness enhancement")
print(f"while preserving details and natural appearance.")

# Save result
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 6))
axes2[0].imshow(image, cmap='gray')
axes2[0].set_title('Original Image', fontsize=13, fontweight='bold')
axes2[0].axis('off')

axes2[1].imshow(corrected_8bit, cmap='gray')
axes2[1].set_title(f'Gamma Corrected (γ = {best_gamma})', fontsize=13, fontweight='bold')
axes2[1].axis('off')

plt.tight_layout()
plt.savefig('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/anfield_gamma_result.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved: anfield_gamma_result.png")

output_path = "/Users/muhammadjonparpiyev/Documents/DIP/Week 4/anfield_gamma_corrected.jpg"
cv2.imwrite(output_path, corrected_8bit)
print(f"✓ Saved: anfield_gamma_corrected.jpg")

# ====================================================================
# TASK 2: CONTRAST STRETCHING
# ====================================================================

print("\n" + "="*70)
print("TASK 2: CONTRAST STRETCHING")
print("="*70)

# Part 1: Non-normalized (smax=255, smin=0)
print(f"\nPART 1: Non-normalized Contrast Stretching")
print(f"Parameters: smax=255, smin=0")

stretched_255_0 = contrast_stretching(image.astype('float32'), 255, 0)
stretched_255_0_8bit = stretched_255_0.astype(np.uint8)

print(f"  Original: range={image.min()}-{image.max()}, mean={image.mean():.2f}")
print(f"  Stretched: range={stretched_255_0_8bit.min()}-{stretched_255_0_8bit.max()}, mean={stretched_255_0_8bit.mean():.2f}")

# Part 2: Normalized (smax=1, smin=0)
print(f"\nPART 2: Normalized Contrast Stretching")
print(f"Parameters: smax=1, smin=0")

normalized_image = image.astype('float32') / 255
stretched_norm = contrast_stretching(normalized_image, 1.0, 0.0)
stretched_norm_8bit = (stretched_norm * 255).astype(np.uint8)

print(f"  Normalized range: {normalized_image.min():.4f}-{normalized_image.max():.4f}")
print(f"  After stretching: {stretched_norm.min():.4f}-{stretched_norm.max():.4f}")
print(f"  As 8-bit: range={stretched_norm_8bit.min()}-{stretched_norm_8bit.max()}, mean={stretched_norm_8bit.mean():.2f}")

# Part 3: Comparison
print(f"\nPART 3: Normalized vs Non-normalized Comparison")

difference = np.abs(stretched_255_0_8bit.astype(float) - stretched_norm_8bit.astype(float))
max_diff = np.max(difference)
mean_diff = np.mean(difference)

print(f"  Max difference: {max_diff:.2f}")
print(f"  Mean difference: {mean_diff:.4f}")
print(f"  Result: {'IDENTICAL' if max_diff < 1 else 'Similar'} outputs")
print(f"  Conclusion: Both methods produce equivalent results.")
print(f"  Normalized approach preferred for mathematical precision.")

fig3, axes3 = plt.subplots(1, 3, figsize=(16, 5))

axes3[0].imshow(image, cmap='gray')
axes3[0].set_title('Original Image', fontsize=13, fontweight='bold')
axes3[0].axis('off')

axes3[1].imshow(stretched_255_0_8bit, cmap='gray')
axes3[1].set_title('Non-normalized\n(smax=255, smin=0)', fontsize=13, fontweight='bold')
axes3[1].axis('off')

axes3[2].imshow(stretched_norm_8bit, cmap='gray')
axes3[2].set_title('Normalized\n(smax=1, smin=0)', fontsize=13, fontweight='bold')
axes3[2].axis('off')

plt.tight_layout()
plt.savefig('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/anfield_normalized_vs_nonnormalized.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved: anfield_normalized_vs_nonnormalized.png")

# Part 4: Different parameter combinations
print(f"\nPART 4: Different Parameter Combinations")

param_combinations = [
    (255, 0),
    (255, 50),
    (255, 100),
    (160, 100),
    (200, 50),
]

results_dict = {}

print(f"\n{'smax':<6} {'smin':<6} {'Min':<6} {'Max':<6} {'Mean':<8} {'Std':<8}")
print("-" * 50)

for smax, smin in param_combinations:
    stretched = contrast_stretching(image.astype('float32'), smax, smin)
    stretched_8bit = stretched.astype(np.uint8)
    results_dict[(smax, smin)] = stretched_8bit
    
    print(f"{smax:<6} {smin:<6} {stretched_8bit.min():<6} {stretched_8bit.max():<6} {stretched_8bit.mean():<8.2f} {stretched_8bit.std():<8.2f}")

print(f"\nObservations:")
print(f"  1. smin ↑ → Image brightens (blacks lifted)")
print(f"  2. smax ↓ → Peak brightness reduced")
print(f"  3. Narrower range → Lower contrast")
print(f"  4. [0, 255] → Maximum contrast")
print(f"  5. Custom ranges → Fine-tuned control")

# Visualization
fig4, axes4 = plt.subplots(2, 3, figsize=(16, 11))
axes4 = axes4.flatten()

axes4[0].imshow(image, cmap='gray')
axes4[0].set_title('Original Image', fontsize=12, fontweight='bold')
axes4[0].axis('off')

for idx, (smax, smin) in enumerate(param_combinations, 1):
    if idx < len(axes4):
        stretched = results_dict[(smax, smin)]
        axes4[idx].imshow(stretched, cmap='gray')
        axes4[idx].set_title(f'smax={smax}, smin={smin}\nMean={stretched.mean():.0f}', fontsize=11, fontweight='bold')
        axes4[idx].axis('off')

plt.tight_layout()
plt.savefig('/Users/muhammadjonparpiyev/Documents/DIP/Week 4/anfield_contrast_stretching_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved: anfield_contrast_stretching_comparison.png")

# Save final result
output_path = '/Users/muhammadjonparpiyev/Documents/DIP/Week 4/anfield_contrast_stretched.jpg'
cv2.imwrite(output_path, stretched_255_0_8bit)
print(f"✓ Saved: anfield_contrast_stretched.jpg")

# ====================================================================
# SUMMARY
# ====================================================================

print("\n" + "="*70)
print("LAB 4 COMPLETED - ALL TASKS FINISHED")
print("="*70)

print(f"""
SUMMARY OF RESULTS:

TASK 1 - GAMMA CORRECTION:
  ✓ Function: gamma_correction(image, c, gamma)
  ✓ Formula: T(r) = c × r^γ
  ✓ Optimal γ: {best_gamma}
  ✓ Effect: Moderate brightness enhancement
  ✓ Files: gamma_comparison, gamma_result, gamma_corrected

TASK 2 - CONTRAST STRETCHING:
  ✓ Function: contrast_stretching(image, smax, smin)
  ✓ Method 1: Non-normalized (smax=255, smin=0)
  ✓ Method 2: Normalized (smax=1, smin=0) 
  ✓ Method 3: 5 parameter combinations tested
  ✓ Finding: Normalized and non-normalized produce identical results
  ✓ Files: comparison, normalized_vs_nonnormalized, stretching_comparison, stretched

KEY INSIGHTS:
  • Gamma correction: Non-linear, effective for shadow enhancement
  • Contrast stretching: Linear, useful for range adjustment
  • Both techniques can be combined for optimal results
  • Normalization improves precision without changing visual output

FILES GENERATED:
  1. anfield_gamma_comparison.png
  2. anfield_gamma_result.png
  3. anfield_gamma_corrected.jpg
  4. anfield_normalized_vs_nonnormalized.png
  5. anfield_contrast_stretching_comparison.png
  6. anfield_contrast_stretched.jpg

Lab 4 successfully completed for anfield.jpg!
""")

print("="*70)
