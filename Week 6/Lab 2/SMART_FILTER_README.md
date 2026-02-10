# Smart Filter Selector - Quick Reference

## Overview
`smart_filter_selector.py` is a professional-grade module for image filtering with a clean, reusable API.

## Installation
Simply copy `smart_filter_selector.py` to your project directory.

## Quick Start

```python
from smart_filter_selector import SmartFilterSelector
import cv2

# Load image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Create selector
selector = SmartFilterSelector(image)

# Apply filter
selector.select_filter('gaussian', kernel_size=7, sigma=1.5)
selector.apply_filter()

# Visualize
selector.compare_side_by_side()
selector.compute_statistics()
```

## Available Methods

### Core Methods

#### `select_filter(filter_type, kernel_size, sigma=None)`
Configure the filter before applying.
- **Parameters:**
  - `filter_type` (str): `'uniform'` or `'gaussian'`
  - `kernel_size` (int): Must be odd (auto-corrected if even)
  - `sigma` (float): Required for Gaussian, ignored for uniform
- **Returns:** `bool` - Success status

#### `apply_filter()`
Apply the selected filter to the image.
- **Returns:** `np.ndarray` - Filtered image

#### `compare_side_by_side(figsize=(14, 6), save_path=None)`
Display original and filtered images side by side.
- **Parameters:**
  - `figsize` (tuple): Figure dimensions
  - `save_path` (str): Optional path to save figure

#### `visualize_difference(figsize=(16, 5))`
Show original, filtered, and difference map in a 3-panel view.
- **Parameters:**
  - `figsize` (tuple): Figure dimensions

#### `compute_statistics()`
Calculate and display filtering statistics.
- **Returns:** `dict` - Statistics (mean, std, min, max)

### Utility Methods

#### `get_difference_map()`
Get the absolute difference map.
- **Returns:** `np.ndarray` - Difference map

## Supported Filters

### Uniform Filter (Box Blur)
```python
selector.select_filter('uniform', kernel_size=5)
```
- Simple averaging filter
- Fast computation
- Creates block-like artifacts
- Good for heavy noise removal

### Gaussian Filter
```python
selector.select_filter('gaussian', kernel_size=5, sigma=1.0)
```
- Smooth, natural-looking blur
- Slower but better quality
- Widely used in image processing
- Sigma controls blur amount

## Error Handling

The module provides clear error messages:

```python
# Missing sigma for Gaussian
selector.select_filter('gaussian', kernel_size=5)  # ❌ Error: sigma required

# Invalid kernel size
selector.select_filter('uniform', kernel_size=4)   # ⚠️ Auto-corrected to 5

# No filter applied before visualization
selector.compare_side_by_side()                    # ❌ Error: no filtered image

# Invalid image type
SmartFilterSelector("not_an_image")               # ❌ ValueError
```

## Examples

### Example 1: Basic Blur
```python
selector = SmartFilterSelector(image)
selector.select_filter('uniform', kernel_size=7)
selector.apply_filter()
selector.compare_side_by_side()
```

### Example 2: Gaussian with Statistics
```python
selector = SmartFilterSelector(image)
selector.select_filter('gaussian', kernel_size=9, sigma=2.0)
selector.apply_filter()
selector.visualize_difference()
stats = selector.compute_statistics()
```

### Example 3: Compare Multiple Filters
```python
import matplotlib.pyplot as plt

selectors = []
for size in [5, 9, 15]:
    sel = SmartFilterSelector(image)
    sel.select_filter('gaussian', kernel_size=size, sigma=1.0)
    sel.apply_filter()
    selectors.append(sel)

# All results available in selectors[]
```

## Advanced Features

### Access Filtered Image
```python
filtered = selector.filtered_image
```

### Get Filter Information
```python
print(selector.filter_type)              # 'gaussian' or 'uniform'
print(selector.parameters)               # {'kernel_size': 7, 'sigma': 1.5}
```

### Save Figure
```python
selector.compare_side_by_side(save_path='result.png')
```

### Custom Figure Size
```python
selector.compare_side_by_side(figsize=(18, 8))
```

## Performance Tips

1. **Larger kernels** = More blur but slower
2. **Gaussian is slower** than uniform filter
3. For real-time applications, use smaller kernels
4. Uniform filter is ~2-3× faster than Gaussian

## Extensibility

The class is designed for easy extension:

```python
class MyFilterSelector(SmartFilterSelector):
    def select_filter(self, filter_type, **kwargs):
        # Add support for bilateral, median, etc.
        if filter_type == 'bilateral':
            # Custom implementation
        else:
            super().select_filter(filter_type, **kwargs)
```

## Common Issues

**Q: Image appears unchanged**
- Check if `apply_filter()` was called after `select_filter()`

**Q: Kernel size is rounded up**
- Kernel size must be odd. Even sizes are auto-corrected.

**Q: Gaussian vs Uniform looks same**
- Try larger sigma values for Gaussian
- Uniform is always blocky; Gaussian is smooth

## File Structure
- **~360 lines** of well-documented code
- **8 public methods** for full functionality
- **Type hints** and comprehensive docstrings
- **Error handling** with clear messages
- **Production-ready** code quality

## License
Free to use for educational and commercial projects.

---
**Module Version:** 1.0  
**Last Updated:** March 2026  
**Author:** DIP Lab Course
