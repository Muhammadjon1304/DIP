#!/usr/bin/env python3
"""
Smart Filter Selector - Example Script

This script demonstrates how to use the SmartFilterSelector module
with the Roberto Firmino Liverpool image.

Run: python3 example_usage.py
"""

import sys
import cv2
import numpy as np
from smart_filter_selector import SmartFilterSelector


def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def example_1_basic_uniform():
    """Example 1: Basic uniform (box) filter."""
    print_header("EXAMPLE 1: Basic Uniform Filter")
    
    # Load image
    image = cv2.imread('roberto-firmino-liverpool.avif', cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("❌ Error: Could not load image")
        return
    
    print(f"Image shape: {image.shape}")
    
    # Create selector and apply filter
    selector = SmartFilterSelector(image)
    selector.select_filter('uniform', kernel_size=7)
    selector.apply_filter()
    selector.compare_side_by_side()
    selector.compute_statistics()


def example_2_gaussian():
    """Example 2: Gaussian filter with different parameters."""
    print_header("EXAMPLE 2: Gaussian Filter (medium)")
    
    image = cv2.imread('roberto-firmino-liverpool.avif', cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("❌ Error: Could not load image")
        return
    
    selector = SmartFilterSelector(image)
    selector.select_filter('gaussian', kernel_size=9, sigma=1.5)
    selector.apply_filter()
    selector.compare_side_by_side()
    selector.compute_statistics()


def example_3_strong_gaussian():
    """Example 3: Strong gaussian filter."""
    print_header("EXAMPLE 3: Strong Gaussian Filter")
    
    image = cv2.imread('roberto-firmino-liverpool.avif', cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("❌ Error: Could not load image")
        return
    
    selector = SmartFilterSelector(image)
    selector.select_filter('gaussian', kernel_size=15, sigma=3.0)
    selector.apply_filter()
    selector.compare_side_by_side()
    selector.compute_statistics()


def example_4_difference_visualization():
    """Example 4: Detailed difference visualization."""
    print_header("EXAMPLE 4: Difference Visualization")
    
    image = cv2.imread('roberto-firmino-liverpool.avif', cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("❌ Error: Could not load image")
        return
    
    selector = SmartFilterSelector(image)
    selector.select_filter('gaussian', kernel_size=11, sigma=2.0)
    selector.apply_filter()
    selector.visualize_difference()


def example_5_comparison():
    """Example 5: Compare uniform vs gaussian."""
    print_header("EXAMPLE 5: Uniform vs Gaussian Comparison")
    
    image = cv2.imread('roberto-firmino-liverpool.avif', cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("❌ Error: Could not load image")
        return
    
    print("\n📊 Comparing filters on same image...")
    
    # Uniform filter
    print("\n1️⃣  Uniform Filter (kernel=7):")
    selector1 = SmartFilterSelector(image)
    selector1.select_filter('uniform', kernel_size=7)
    selector1.apply_filter()
    stats1 = selector1.compute_statistics()
    
    # Gaussian filter
    print("\n2️⃣  Gaussian Filter (kernel=7, sigma=1.5):")
    selector2 = SmartFilterSelector(image)
    selector2.select_filter('gaussian', kernel_size=7, sigma=1.5)
    selector2.apply_filter()
    stats2 = selector2.compute_statistics()
    
    # Compare visually
    print("\n3️⃣  Visual comparison (side-by-side):")
    selector1.compare_side_by_side(figsize=(16, 6))


def example_6_parameter_tuning():
    """Example 6: Explore different kernel sizes."""
    print_header("EXAMPLE 6: Parameter Tuning")
    
    image = cv2.imread('roberto-firmino-liverpool.avif', cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("❌ Error: Could not load image")
        return
    
    print("\nTesting different kernel sizes...")
    
    kernel_sizes = [3, 7, 11, 15]
    selectors = []
    
    for size in kernel_sizes:
        print(f"\n→ Kernel size: {size}")
        selector = SmartFilterSelector(image)
        selector.select_filter('gaussian', kernel_size=size, sigma=1.0)
        selector.apply_filter()
        selectors.append(selector)
        print(f"  Mean pixel value: {selector.filtered_image.mean():.2f}")
    
    print("\n✓ All filters applied successfully!")
    print(f"  Total selectors created: {len(selectors)}")


def main():
    """Main function to run all examples."""
    print("\n" + "🎬 "*35)
    print("SMART FILTER SELECTOR - EXAMPLE SCRIPT")
    print("🎬 "*35)
    
    print("\nThis script demonstrates various features of the SmartFilterSelector module.")
    print("Make sure 'roberto-firmino-liverpool.avif' is in the current directory.")
    
    # Run examples
    try:
        example_1_basic_uniform()
        example_2_gaussian()
        example_3_strong_gaussian()
        example_4_difference_visualization()
        example_5_comparison()
        example_6_parameter_tuning()
        
        print_header("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("✓ SmartFilterSelector module is working correctly!")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the image file exists in the current directory.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
