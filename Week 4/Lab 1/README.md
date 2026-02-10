# Lab 1 - Organized Project Structure

## Overview
This directory contains organized code, images, and notebooks for DIP Lab 4 (Image Enhancement: Gamma Correction & Contrast Stretching).

---

## 📁 Folder Structure

```
Lab 1/
├── 📂 source_images/          # Original input images
│   ├── 4.png                  # Sample image (colorful)
│   └── anfield.jpg            # Main image (football stadium)
│
├── 📂 scripts/                # Python scripts and executables
│   ├── run_color_analysis.py           # Main analysis on anfield.jpg
│   ├── run_4png_color.py               # Color analysis on 4.png
│   ├── run_student_work.py             # Student submission script
│   ├── gamma_correction_task1.py       # Task 1 implementation
│   ├── contrast_stretching_task2.py    # Task 2 implementation
│   ├── compare_images.py               # Image comparison utility
│   └── check_image.py                  # Image property checker
│
├── 📂 output_images/          # Generated output images
│   ├── Gamma Correction Results:
│   │   ├── anfield_gamma_comparison.png
│   │   ├── anfield_gamma_result.png
│   │   ├── anfield_gamma_corrected.jpg
│   │   ├── 4_gamma_comparison_color.png
│   │   ├── 4_gamma_result_color.png
│   │   └── 4_gamma_corrected_color.jpg
│   │
│   ├── Contrast Stretching Results:
│   │   ├── anfield_contrast_stretching_comparison.png
│   │   ├── anfield_contrast_stretched.jpg
│   │   ├── 4_contrast_stretching_comparison_color.png
│   │   └── 4_contrast_stretched.png
│   │
│   └── Analysis Comparisons:
│       ├── anfield_normalized_vs_nonnormalized.png
│       ├── normalized_vs_nonnormalized.png
│       ├── contrast_stretching_comparison.png
│       └── gamma_comparison.png
│
├── 📂 notebooks/              # Jupyter notebooks
│   ├── Week 04, Lab 01 (1).ipynb    # Student submission notebook
│   └── lab4-01.ipynb                # Comprehensive analysis notebook
│
├── 📄 Lab 4 - 01.pdf          # Lab requirements and guidelines
├── 📄 LAB4_REPORT.md          # Lab report documentation
└── 📄 README.md               # This file

```

---

## 🚀 Quick Start

### Run Analysis on anfield.jpg (COLOR)
```bash
python scripts/run_color_analysis.py
```

### Run Analysis on 4.png (ENHANCED COLOR)
```bash
python scripts/run_4png_color.py
```

### Run Student Submission Script
```bash
python scripts/run_student_work.py
```

---

## 📊 Key Tasks

### Task 1: Gamma Correction
- **Function**: `gamma_correction(I_in, c, gamma)`
- **Formula**: T(r) = c × r^γ
- **Tested Values**: γ = 0.33, 0.5, 0.67, 1.0, 1.5, 2.0, 3.0
- **Optimal**: γ = 0.67 (provides good brightness enhancement)

### Task 2: Contrast Stretching
- **Function**: `contrast_stretching(i_in, s_min, s_max)`
- **Formula**: s = ((s_max - s_min) / (r_max - r_min)) × (r - r_min) + s_min
- **Parameter Combinations Tested**:
  - (255, 0) - Full range (max contrast)
  - (255, 50) - Brightened blacks
  - (255, 100) - More brightened blacks
  - (160, 100) - Narrow range
  - (200, 50) - Custom range

---

## 📋 Image Specifications

### Source Images
| Image | Resolution | Channels | Type |
|-------|-----------|----------|------|
| 4.png | 258×617 | 3 (RGB) | Colorful |
| anfield.jpg | 482×728 | 3 (RGB) | Football Stadium |

### Output Images
- **Gamma Correction**: 3 images per input (comparison, result, corrected)
- **Contrast Stretching**: 2 images per input (comparison, stretched)
- **Total Output Files**: 16+ images across both tasks

---

## 💻 Scripts Overview

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `run_color_analysis.py` | Complete analysis on anfield.jpg | anfield.jpg | 6 images + statistics |
| `run_4png_color.py` | Complete analysis on 4.png enhanced | 4.png | 6 images + statistics |
| `gamma_correction_task1.py` | Task 1 implementation | Image file | Gamma corrected images |
| `contrast_stretching_task2.py` | Task 2 implementation | Image file | Contrast stretched images |
| `check_image.py` | Verify image properties | Image file | Channel statistics |
| `compare_images.py` | Compare multiple images | Multiple images | Color variance analysis |

---

## 📝 Key Findings

### Gamma Correction (anfield.jpg)
- **Original Mean**: 109.93 → **Corrected (γ=0.67) Mean**: 137.27
- **Effect**: 25% brightness increase with preserved details

### Contrast Stretching
- **Finding**: Normalized and non-normalized approaches produce mathematically identical results
- **Best Practice**: Use normalized approach for mathematical precision

---

## ✅ Verification

All scripts have been tested and verified to produce correct output images:
- ✓ Gamma correction applies power law transformation correctly
- ✓ Contrast stretching implements linear intensity mapping
- ✓ Color images processed in all 3 channels uniformly
- ✓ Output images saved with 150 DPI quality

---

## 📌 Notes

- **Color Enhancement**: 4.png saturation boosted by 1.5x for better visibility
- **Image Format**: Output images saved as PNG (lossless) with 150 DPI
- **Matplotlib Backend**: Set to 'Agg' for headless execution
- **All calculations use float32** for numerical precision

---

**Last Updated**: February 17, 2026  
**Lab**: DIP Week 4 - Image Enhancement  
**Instructor**: Digital Image Processing Course
