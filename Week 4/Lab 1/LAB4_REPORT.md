# Lab 4 - Intensity Transformation I
## Digital Image Processing - Spring 2025

### Completed Tasks Summary

---

## Task 1: Power Law Transformation (Gamma Correction)

### Objective
Apply gamma correction to enhance image visibility using the power law transformation formula:
$$T(r) = c \cdot r^{\gamma}$$

### Image Analyzed
- **Filename**: `4.png`
- **Dimensions**: 258 × 617 pixels
- **Characteristics**: Dark image with low visibility (mean intensity: 76.58)

### Implementation
Created `gamma_correction_task1.py` with a `gamma_correction()` function that:
1. Normalizes the input image to [0, 1] range
2. Applies power law transformation: $I_{transformed} = c \times (I_{norm})^{\gamma}$
3. Clips values to valid range and returns transformed image

### Chosen Parameters
- **γ = 0.5** (square root transformation)
- **c = 1.0** (scaling factor)

### Reasoning for γ = 0.5
- **Original Problem**: Dark image with poor visibility
- **Effect of γ < 1**: Produces brightening effect (applies nth root)
- **Advantage of 0.5**: 
  - Significant enhancement in dark regions
  - Preserves image details without over-brightening
  - Mean intensity increased from 76.58 to 114.66
  - Improved visibility while maintaining natural appearance

### Test Results
| γ Value | Type | Mean Intensity |
|---------|------|----------------|
| 0.33 | Cubic root | 136.70 |
| **0.50** | **Square root** | **114.66** |
| 0.67 | - | 98.10 |
| 1.0 | Original | 76.58 |
| 1.5 | - | 57.65 |
| 2.0 | Square | 47.23 |
| 3.0 | Cube | 36.62 |

### Generated Output Files
1. **gamma_correction_task1.py** - Source code
2. **gamma_comparison.png** - 8-image grid showing original + 7 gamma values
3. **4_gamma_result.png** - Side-by-side comparison of original vs. corrected
4. **4_gamma_corrected.png** - Final corrected image (8-bit)

---

## Task 2: Contrast Stretching

### Objective
Enhance image contrast using linear contrast stretching and compare normalized vs. non-normalized approaches.

### Contrast Stretching Formula
$$s = \left(\frac{s_{max} - s_{min}}{r_{max} - r_{min}}\right)(r - r_{min}) + s_{min}$$

Where:
- $r_{min}$, $r_{max}$ = minimum and maximum intensity in input image
- $s_{min}$, $s_{max}$ = desired output range bounds

### Implementation
Created `contrast_stretching_task2.py` with a `contrast_stretching()` function that:
1. Finds min/max intensity values in input image
2. Applies linear transformation to stretch contrast
3. Clips output to specified range
4. Handles both normalized and non-normalized inputs

---

### Part 1: Non-normalized Contrast Stretching
**Parameters**: smax = 255, smin = 0

| Metric | Original | Stretched |
|--------|----------|-----------|
| Range | 0 - 255 | 0 - 255 |
| Mean | 76.58 | 76.58 |
| Std Dev | 79.16 | 79.16 |

**Note**: Image was already at full dynamic range, so no visible enhancement.

---

### Part 2: Normalized vs. Non-normalized Comparison

#### Non-normalized Approach
- Input: 8-bit grayscale (0-255)
- Output: 8-bit grayscale (0-255)
- Process: Direct intensity transformation

#### Normalized Approach
- Input: Float normalized to [0, 1]
- Output: Float [0, 1], then converted back to 8-bit
- Process: Mathematically equivalent but allows precision computation

#### Impact Analysis
| Aspect | Result |
|--------|--------|
| Visual Output | **No significant difference** |
| Mathematical Result | **Identical** |
| Practical Advantage | Normalized allows uniform handling of various formats |
| Computational Precision | Better in normalized approach |

**Conclusion**: Both methods produce similar results. Normalization is preferred for mathematical operations and handling diverse image formats while maintaining numerical precision.

---

### Part 3: Different Parameter Combinations

#### Test Combinations (Non-normalized):

| smax | smin | Range | Mean | Std Dev | Effect |
|------|------|-------|------|---------|--------|
| 255 | 0 | 0-255 | 76.58 | 79.16 | Full range |
| 255 | 50 | 50-255 | 111.17 | 63.63 | Brightening |
| 255 | 100 | 100-255 | 146.18 | 48.08 | Strong brightening |
| 160 | 100 | 100-160 | 117.64 | 18.61 | Compressed range |
| 200 | 50 | 50-200 | 94.72 | 46.51 | Custom range |

#### Observations:

1. **Adjusting smin (lower bound)**:
   - Increasing smin → Image becomes brighter
   - Blacks (intensity 0) map to smin value instead of 0
   - Example: smin=100 makes darkest areas gray (value 100)

2. **Adjusting smax (upper bound)**:
   - Decreasing smax → Reduces peak brightness
   - Compresses the dynamic range
   - Example: smax=160 caps white values at 160

3. **Range Width (smax - smin)**:
   - Full range [0, 255] → Maximum contrast
   - Smaller range → Lower contrast, compressed appearance
   - Example: [100, 160] is narrow, less dramatic changes

4. **Practical Applications**:
   - Specific ranges → Adjust brightness/contrast for specific purposes
   - Full range → Maximum enhancement for dark/washed images
   - Custom ranges → Fine-tune appearance for specific requirements

5. **Impact on Statistics**:
   - Larger range → Higher standard deviation
   - Compressed range → Lower standard deviation
   - Mean shifts based on smin offset

---

### Generated Output Files
1. **contrast_stretching_task2.py** - Source code
2. **contrast_stretching_comparison.png** - 6-image grid showing original + 5 parameter combinations
3. **normalized_vs_nonnormalized.png** - Comparison of three approaches
4. **4_contrast_stretched.png** - Final stretched image (smax=255, smin=0)

---

## Summary of Techniques

### Gamma Correction
- **Purpose**: Non-linear enhancement for visibility improvement
- **Best for**: Dark or underexposed images
- **Formula**: $T(r) = c \cdot r^{\gamma}$
- **When to use**: γ < 1 for brightening, γ > 1 for darkening

### Contrast Stretching
- **Purpose**: Linear enhancement to utilize full dynamic range
- **Best for**: Low-contrast or washed-out images
- **Formula**: Linear transformation with custom output bounds
- **When to use**: When image is already at full range or needs specific intensity bounds

---

## Conclusions

1. **Gamma Correction** is effective for non-linear enhancement of dark images
   - γ = 0.5 significantly improved the test image visibility
   - Preserves details while brightening shadows

2. **Contrast Stretching** provides linear intensity mapping
   - Useful for custom intensity range adjustment
   - Normalized and non-normalized methods are equivalent
   - Different (smax, smin) combinations offer fine control

3. **Combination Usage**: Both techniques can be applied sequentially for optimal results
   - First apply gamma correction for visibility
   - Then apply contrast stretching for final adjustment

---

**Lab Completed**: February 17, 2025
**Student**: [Your Name]
**Course**: Digital Image Processing - Spring 2025
