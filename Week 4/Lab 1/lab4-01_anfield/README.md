# Lab 4-01: Image Enhancement with Anfield

**Lab Focus**: DIP (Digital Image Processing) Lab 4-01  
**Primary Notebook**: `lab4-01.ipynb`  
**Main Image**: `anfield.jpg` (Football Stadium)  
**Tasks**: Gamma Correction & Contrast Stretching  

---

## 📁 Project Structure

```
lab4-01_anfield/
├── 📂 source_images/
│   └── anfield.jpg                    # Main analysis image (482×728, color)
│
├── 📂 scripts/
│   ├── run_color_analysis.py          # Complete anfield analysis
│   └── run_student_work.py            # Student submission script
│
├── 📂 output_images/
│   ├── Gamma Correction:
│   │   ├── anfield_gamma_comparison.png        # 8 gamma values
│   │   ├── anfield_gamma_result.png            # Before/after
│   │   └── anfield_gamma_corrected.jpg         # Final corrected
│   │
│   ├── Contrast Stretching:
│   │   ├── anfield_contrast_stretching_comparison.png  # 5 parameters
│   │   └── anfield_contrast_stretched.jpg              # Stretched result
│   │
│   └── Analysis:
│       └── anfield_normalized_vs_nonnormalized.png     # Comparison
│
├── 📂 notebooks/
│   └── lab4-01.ipynb                  # Main lab notebook
│
└── 📄 README.md                       # This file
```

---

## 🎯 Quick Start

### View the Notebook
```bash
# Open in Jupyter
jupyter notebook notebooks/lab4-01.ipynb
```

### Run Analysis
```bash
# Complete color analysis on anfield.jpg
python scripts/run_color_analysis.py

# Student submission version
python scripts/run_student_work.py
```

---

## 📊 Image Information

### Source Image: anfield.jpg
| Property | Value |
|----------|-------|
| **Resolution** | 482 × 728 pixels |
| **Type** | Color (RGB) |
| **Channels** | 3 (Red, Green, Blue) |
| **Min Intensity** | 0 |
| **Max Intensity** | 255 |
| **Mean** | 109.93 |
| **Std Dev** | 71.80 |

---

## 📋 Task Details

### Task 1: Gamma Correction (Power Law Transformation)

**Objective**: Apply non-linear brightness enhancement to the image

**Mathematical Formula**:
$$T(r) = c \cdot r^{\gamma}$$

Where:
- $r$ = normalized input intensity [0, 1]
- $T(r)$ = transformed intensity
- $c$ = scaling constant (typically 1.0)
- $\gamma$ = gamma exponent

**Process**:
1. Normalize image to [0, 1]: `I_norm = I / 255`
2. Apply power transformation: `I_gamma = c * (I_norm ^ γ)`
3. Scale back to [0, 255]: `I_out = I_gamma * 255`
4. Clip to uint8: `np.clip(I_out, 0, 255)`

**Gamma Values Tested**:
| γ Value | Effect | Mean Intensity |
|---------|--------|----------------|
| 0.33 | Brighten significantly | 181.81 |
| 0.50 | Brighten moderately | 156.86 |
| **0.67** | **Optimal (good balance)** | **137.27** |
| 1.00 | No change (identity) | 109.93 |
| 1.50 | Darken moderately | 83.16 |
| 2.00 | Darken more | 67.17 |
| 3.00 | Darken significantly | 49.18 |

**Result**: 
- **Optimal γ = 0.67** selected
- Original mean: 109.93 → Corrected mean: 137.27
- **Brightness increase: +25%** with detail preservation

---

### Task 2: Contrast Stretching (Linear Intensity Mapping)

**Objective**: Expand intensity range for enhanced contrast

**Mathematical Formula**:
$$s = \frac{(s_{max} - s_{min})}{(r_{max} - r_{min})} \cdot (r - r_{min}) + s_{min}$$

Where:
- $s$ = output intensity
- $r$ = input intensity
- $r_{min}, r_{max}$ = min/max of input image
- $s_{min}, s_{max}$ = desired output range

**Process**:
1. Find input range: `r_min, r_max = np.min(I), np.max(I)`
2. Calculate scale factor: `scale = (s_max - s_min) / (r_max - r_min)`
3. Map intensities: `s = scale * (r - r_min) + s_min`
4. Clip and convert: `np.clip(s, s_min, s_max).astype(uint8)`

**Parameter Combinations Tested**:

| s_min | s_max | Range | Effect | Mean |
|-------|-------|-------|--------|------|
| 0 | 255 | Full | Maximum contrast | 109.93 |
| 50 | 255 | Limited | Brightened blacks | 137.90 |
| 100 | 255 | More limited | Further brightened | 166.34 |
| 100 | 160 | Narrow | Compressed range | 125.41 |
| 50 | 200 | Custom | Balance | 114.21 |

**Key Findings**:
- Normalized and non-normalized approaches are **mathematically identical**
- Normalized preferred for numerical precision and float operations
- Full range [0, 255] produces maximum contrast
- Custom ranges allow fine-tuned brightness control

---

## 🔧 Function Implementations

### `gamma_correction(I_in, c, gamma)`

```python
def gamma_correction(I_in, c, gamma):
    """Apply power law (gamma) transformation"""
    # Normalize
    I_norm = I_in.astype('float32') / 255
    # Transform
    I_gamma = c * (I_norm ** gamma)
    # Scale and clip
    I_out = np.clip(I_gamma * 255, 0, 255).astype('uint8')
    return I_out
```

### `contrast_stretching(i_in, s_min=0, s_max=255)`

```python
def contrast_stretching(i_in, s_min=0, s_max=255):
    """Apply linear contrast stretching"""
    r_min, r_max = np.min(i_in), np.max(i_in)
    if r_max == r_min:
        return np.zeros_like(i_in, dtype='uint8')
    i_out = ((s_max - s_min) / (r_max - r_min)) * (i_in - r_min) + s_min
    i_out = np.clip(i_out, s_min, s_max).astype('uint8')
    return i_out
```

---

## 📈 Results Summary

### Gamma Correction Results
- **Original Image Mean**: 109.93
- **After γ=0.67 Correction**: 137.27
- **Improvement**: +25% brightness increase
- **Quality**: Detail preserved, no over-brightening

### Contrast Stretching Results
- **Non-normalized (0-255)**: Identical to normalized approach
- **Best Range**: (255, 0) for full contrast
- **Custom Ranges**: Allow selective brightness adjustment
- **Practical Use**: (255, 50) for balanced brightness enhancement

---

## 📁 Output Images Explained

### Gamma Correction
1. **`anfield_gamma_comparison.png`** - All 7 gamma values side-by-side for comparison
2. **`anfield_gamma_result.png`** - Before/after with optimal γ=0.67
3. **`anfield_gamma_corrected.jpg`** - Final corrected image ready for use

### Contrast Stretching
1. **`anfield_contrast_stretching_comparison.png`** - 5 parameter combinations
2. **`anfield_contrast_stretched.jpg`** - Result with optimal parameters
3. **`anfield_normalized_vs_nonnormalized.png`** - Validation of both approaches

---

## 🚀 Usage Examples

### Example 1: Apply Gamma Correction
```python
import cv2
import numpy as np

# Load image
img = cv2.imread('source_images/anfield.jpg', cv2.IMREAD_COLOR)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Apply gamma correction
gamma = 0.67
img_corrected = gamma_correction(img_rgb, c=1.0, gamma=gamma)

# Save result
img_out = cv2.cvtColor(img_corrected, cv2.COLOR_RGB2BGR)
cv2.imwrite('anfield_gamma_0.67.jpg', img_out)
```

### Example 2: Apply Contrast Stretching
```python
# Apply contrast stretching
smin, smax = 50, 255
img_stretched = contrast_stretching(img_rgb.astype('float32'), 
                                    s_min=smin, s_max=smax)

# Save result
img_out = cv2.cvtColor(img_stretched, cv2.COLOR_RGB2BGR)
cv2.imwrite('anfield_contrast_stretched.jpg', img_out)
```

---

## ✅ Verification Checklist

- [x] Gamma correction applies power law correctly
- [x] Contrast stretching implements linear mapping
- [x] Color images processed in all 3 channels
- [x] Output saved with 150 DPI quality
- [x] Statistical calculations verified
- [x] Both transformations produce expected results
- [x] Notebooks are runnable and produce correct output
- [x] Scripts are executable and generate images

---

## 📝 Key Learnings

1. **Gamma Correction**: Most effective for brightness enhancement without losing details
2. **Optimal γ**: 0.67 provides best balance for this image
3. **Contrast Stretching**: Linear operation, mathematically simple but powerful
4. **Normalization**: Important for numerical precision in float operations
5. **Color Handling**: All channels transformed uniformly preserves color balance
6. **Range Selection**: Custom s_min/s_max allows fine control over output appearance

---

## 📚 References

- **Power Law Transformation**: Digital Image Processing (Gonzalez & Woods)
- **Contrast Stretching**: Standard linear remapping technique
- **Implementation**: OpenCV + NumPy + Matplotlib
- **Testing**: 7 gamma values × 2 images + 5 parameter combinations

---

## 📞 Notes

- **Image Color**: Anfield is naturally muted (football stadium colors)
- **Processing**: All float32 precision maintained during calculations
- **Backend**: Matplotlib using 'Agg' for headless execution
- **Format**: PNG images saved at 150 DPI for quality preservation
- **Reproducibility**: All scripts and notebooks fully documented

---

**Last Updated**: February 17, 2026  
**Lab**: DIP Week 4 - Image Enhancement  
**Status**: ✅ Complete and Organized
