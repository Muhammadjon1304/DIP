#!/usr/bin/env python3
"""
Smart Filter Selector - Interactive Demo
Demonstrates the Smart Filter Selector module with sample filters
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from smart_filter_selector import SmartFilterSelector

def load_image(image_path):
    """Load image from file path"""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Could not load image from {image_path}")
    return image

def main():
    # Image path
    image_path = '/Users/muhammadjonparpiyev/Documents/DIP/Week 6/Lab 2/roberto-firmino-liverpool.avif'
    
    print("=" * 70)
    print("SMART FILTER SELECTOR - INTERACTIVE DEMO")
    print("=" * 70)
    print()
    
    try:
        # Load image
        print("[1/5] Loading image...")
        image = load_image(image_path)
        print(f"✓ Image loaded: Shape={image.shape}, Dtype={image.dtype}")
        print(f"  Image stats: Min={image.min()}, Max={image.max()}, Mean={image.mean():.1f}")
        print()
        
        # Demo 1: Uniform Filter
        print("[2/5] Demo 1: Uniform Filter (Kernel Size=7)")
        print("-" * 70)
        selector_uniform = SmartFilterSelector(image)
        selector_uniform.select_filter('uniform', kernel_size=7)
        selector_uniform.apply_filter()
        print(f"✓ Uniform filter applied")
        print(f"  Filtered image: Min={selector_uniform.filtered_image.min()}, Max={selector_uniform.filtered_image.max()}, Mean={selector_uniform.filtered_image.mean():.1f}")
        selector_uniform.compare_side_by_side()
        print()
        
        # Demo 2: Gaussian Filter
        print("[3/5] Demo 2: Gaussian Filter (Kernel Size=7, Sigma=1.5)")
        print("-" * 70)
        selector_gaussian = SmartFilterSelector(image)
        selector_gaussian.select_filter('gaussian', kernel_size=7, sigma=1.5)
        selector_gaussian.apply_filter()
        print(f"✓ Gaussian filter applied")
        print(f"  Filtered image: Min={selector_gaussian.filtered_image.min()}, Max={selector_gaussian.filtered_image.max()}, Mean={selector_gaussian.filtered_image.mean():.1f}")
        selector_gaussian.compare_side_by_side()
        print()
        
        # Demo 3: Difference Visualization
        print("[4/5] Demo 3: Difference Map (Uniform vs Original)")
        print("-" * 70)
        selector_uniform.visualize_difference()
        print("✓ Difference visualization created")
        print()
        
        # Demo 4: Statistics Comparison
        print("[5/5] Demo 4: Statistics Comparison")
        print("-" * 70)
        stats_uniform = selector_uniform.compute_statistics()
        stats_gaussian = selector_gaussian.compute_statistics()
        
        print("\n--- UNIFORM FILTER STATISTICS ---")
        for key, value in stats_uniform.items():
            print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
        
        print("\n--- GAUSSIAN FILTER STATISTICS ---")
        for key, value in stats_gaussian.items():
            print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
        
        print("\n" + "=" * 70)
        print("✓ ALL DEMOS COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
        plt.show()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
