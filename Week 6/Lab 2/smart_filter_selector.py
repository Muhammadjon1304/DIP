"""
Smart Filter Selector Module

A reusable, well-structured filter selector for image processing.
Supports multiple filter types with parameter validation and visualization.

Author: DIP Lab Course
Date: March 2026
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt


class SmartFilterSelector:
    """
    A reusable, well-structured filter selector for image processing.
    Supports multiple filter types with parameter validation and visualization.
    
    Attributes:
        image (np.ndarray): Input grayscale image
        filtered_image (np.ndarray): Filtered output image
        filter_type (str): Type of filter applied ('uniform' or 'gaussian')
        parameters (dict): Filter parameters (kernel_size, sigma, etc.)
    
    Example:
        >>> selector = SmartFilterSelector(image)
        >>> selector.select_filter('gaussian', kernel_size=7, sigma=1.0)
        >>> selector.apply_filter()
        >>> selector.compare_side_by_side()
        >>> selector.compute_statistics()
    """
    
    def __init__(self, image):
        """
        Initialize the filter selector with an image.
        
        Args:
            image (np.ndarray): Input grayscale image (numpy array)
        
        Raises:
            ValueError: If image is not a 2D numpy array
        """
        if not isinstance(image, np.ndarray) or image.ndim != 2:
            raise ValueError("Image must be a 2D numpy array (grayscale)")
        
        self.image = image
        self.filtered_image = None
        self.filter_type = None
        self.parameters = {}
        
    def validate_kernel_size(self, size):
        """
        Validate kernel size (must be positive odd integer).
        
        Args:
            size (int): Kernel size to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(size, int):
            print(f"❌ Error: Kernel size must be an integer, got {type(size)}")
            return False
        if size < 1:
            print(f"❌ Error: Kernel size must be positive, got {size}")
            return False
        if size % 2 == 0:
            print(f"⚠️  Warning: Kernel size must be odd, got {size}. Using {size+1} instead.")
            return False
        return True
    
    def validate_sigma(self, sigma):
        """
        Validate sigma value (must be positive).
        
        Args:
            sigma (float): Sigma value to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            sigma_val = float(sigma)
        except (ValueError, TypeError):
            print(f"❌ Error: Sigma must be a number, got {type(sigma)}")
            return False
        
        if sigma_val <= 0:
            print(f"❌ Error: Sigma must be positive, got {sigma_val}")
            return False
        return True
    
    def select_filter(self, filter_type, kernel_size, sigma=None):
        """
        Select and configure a filter.
        
        Args:
            filter_type (str): 'uniform' or 'gaussian'
            kernel_size (int): Size of the kernel (must be odd)
            sigma (float, optional): Sigma for Gaussian filter (required if Gaussian)
            
        Returns:
            bool: True if configuration successful, False otherwise
        
        Raises:
            ValueError: If filter_type is not recognized
        """
        # Validate kernel size
        if not self.validate_kernel_size(kernel_size):
            return False
        
        # Make kernel size odd if even
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        self.filter_type = filter_type.lower()
        self.parameters['kernel_size'] = kernel_size
        
        if self.filter_type == 'uniform':
            print(f"✓ Selected: Uniform filter (Box Blur)")
            print(f"  └─ Kernel size: {kernel_size}×{kernel_size}")
            
        elif self.filter_type == 'gaussian':
            if sigma is None:
                print("❌ Error: Gaussian filter requires sigma parameter")
                return False
            if not self.validate_sigma(sigma):
                return False
            self.parameters['sigma'] = float(sigma)
            print(f"✓ Selected: Gaussian filter")
            print(f"  ├─ Kernel size: {kernel_size}×{kernel_size}")
            print(f"  └─ Sigma: {self.parameters['sigma']}")
            
        else:
            raise ValueError(f"Unknown filter type '{filter_type}'. Use 'uniform' or 'gaussian'")
        
        return True
    
    def apply_filter(self):
        """
        Apply the selected filter to the image.
        
        Returns:
            np.ndarray: Filtered image, or None if filter not configured
        
        Raises:
            RuntimeError: If no filter has been selected
        """
        if self.filter_type is None:
            raise RuntimeError("No filter selected. Call select_filter() first.")
        
        kernel_size = self.parameters['kernel_size']
        
        try:
            if self.filter_type == 'uniform':
                self.filtered_image = cv2.blur(self.image, (kernel_size, kernel_size))
                print(f"✓ Applied uniform filter (box blur)")
                
            elif self.filter_type == 'gaussian':
                sigma = self.parameters['sigma']
                self.filtered_image = cv2.GaussianBlur(
                    self.image, 
                    (kernel_size, kernel_size), 
                    sigma
                )
                print(f"✓ Applied Gaussian filter")
        
        except Exception as e:
            print(f"❌ Error applying filter: {e}")
            return None
        
        return self.filtered_image
    
    def compare_side_by_side(self, figsize=(14, 6), save_path=None):
        """
        Display original and filtered images side by side.
        
        Args:
            figsize (tuple, optional): Figure size (width, height). Default: (14, 6)
            save_path (str, optional): Path to save figure. If None, doesn't save.
        
        Raises:
            RuntimeError: If no filtered image is available
        """
        if self.filtered_image is None:
            raise RuntimeError("No filtered image. Call apply_filter() first.")
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Original image
        axes[0].imshow(self.image, cmap='gray')
        axes[0].set_title('Original Image', fontsize=14, fontweight='bold')
        axes[0].axis('off')
        
        # Filtered image
        axes[1].imshow(self.filtered_image, cmap='gray')
        filter_name = "Uniform Filter (Box Blur)" if self.filter_type == 'uniform' else "Gaussian Filter"
        kernel_info = f"kernel={self.parameters['kernel_size']}"
        if self.filter_type == 'gaussian':
            kernel_info += f", σ={self.parameters['sigma']}"
        
        axes[1].set_title(f'{filter_name}\n({kernel_info})', 
                         fontsize=14, fontweight='bold')
        axes[1].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"✓ Figure saved to {save_path}")
        
        plt.show()
    
    def compute_statistics(self):
        """
        Compute and display filtering statistics.
        
        Returns:
            dict: Statistics dictionary with mean, std, min, max
        
        Raises:
            RuntimeError: If no filtered image is available
        """
        if self.filtered_image is None:
            raise RuntimeError("No filtered image. Call apply_filter() first.")
        
        stats = {
            'original_mean': float(self.image.mean()),
            'filtered_mean': float(self.filtered_image.mean()),
            'original_std': float(self.image.std()),
            'filtered_std': float(self.filtered_image.std()),
            'original_min': int(self.image.min()),
            'filtered_min': int(self.filtered_image.min()),
            'original_max': int(self.image.max()),
            'filtered_max': int(self.filtered_image.max()),
        }
        
        print("\n" + "="*70)
        print("FILTERING STATISTICS")
        print("="*70)
        print(f"\n{'Metric':<25} {'Original':<20} {'Filtered':<20}")
        print("-"*70)
        print(f"{'Mean':<25} {stats['original_mean']:<20.2f} {stats['filtered_mean']:<20.2f}")
        print(f"{'Std Dev':<25} {stats['original_std']:<20.2f} {stats['filtered_std']:<20.2f}")
        print(f"{'Min':<25} {stats['original_min']:<20} {stats['filtered_min']:<20}")
        print(f"{'Max':<25} {stats['original_max']:<20} {stats['filtered_max']:<20}")
        
        # Compute difference
        diff = np.abs(
            self.image.astype(np.float32) - self.filtered_image.astype(np.float32)
        )
        print(f"\n{'Mean Absolute Diff':<25} {diff.mean():<20.2f}")
        print(f"{'Max Absolute Diff':<25} {diff.max():<20.2f}")
        print("="*70 + "\n")
        
        return stats
    
    def get_difference_map(self):
        """
        Get the absolute difference map between original and filtered images.
        
        Returns:
            np.ndarray: Absolute difference map
        
        Raises:
            RuntimeError: If no filtered image is available
        """
        if self.filtered_image is None:
            raise RuntimeError("No filtered image. Call apply_filter() first.")
        
        diff = np.abs(
            self.image.astype(np.float32) - self.filtered_image.astype(np.float32)
        )
        return diff
    
    def visualize_difference(self, figsize=(16, 5)):
        """
        Visualize original, filtered, and difference map.
        
        Args:
            figsize (tuple, optional): Figure size (width, height). Default: (16, 5)
        
        Raises:
            RuntimeError: If no filtered image is available
        """
        if self.filtered_image is None:
            raise RuntimeError("No filtered image. Call apply_filter() first.")
        
        diff = self.get_difference_map()
        
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # Original
        axes[0].imshow(self.image, cmap='gray')
        axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
        axes[0].axis('off')
        
        # Filtered
        axes[1].imshow(self.filtered_image, cmap='gray')
        axes[1].set_title('Filtered Image', fontsize=12, fontweight='bold')
        axes[1].axis('off')
        
        # Difference
        im = axes[2].imshow(diff, cmap='hot')
        axes[2].set_title('Absolute Difference Map', fontsize=12, fontweight='bold')
        axes[2].axis('off')
        plt.colorbar(im, ax=axes[2], label='Intensity Difference')
        
        plt.tight_layout()
        plt.show()
    
    def __str__(self):
        """String representation of the filter configuration."""
        if self.filter_type is None:
            return "SmartFilterSelector(no filter selected)"
        
        info = f"SmartFilterSelector(\n"
        info += f"  filter_type: {self.filter_type},\n"
        info += f"  kernel_size: {self.parameters['kernel_size']}"
        if 'sigma' in self.parameters:
            info += f",\n  sigma: {self.parameters['sigma']}"
        info += f"\n)"
        return info


if __name__ == "__main__":
    """
    Example usage of SmartFilterSelector class.
    This runs when the script is executed directly.
    """
    print("SmartFilterSelector Module")
    print("=" * 60)
    print("\nUsage Example:")
    print("-" * 60)
    print("""
    import cv2
    from smart_filter_selector import SmartFilterSelector
    
    # Load image
    image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
    
    # Create selector
    selector = SmartFilterSelector(image)
    
    # Apply uniform filter
    selector.select_filter('uniform', kernel_size=7)
    selector.apply_filter()
    selector.compare_side_by_side()
    selector.compute_statistics()
    
    # Or apply Gaussian filter
    selector.select_filter('gaussian', kernel_size=7, sigma=1.5)
    selector.apply_filter()
    selector.compare_side_by_side()
    selector.visualize_difference()
    """)
    print("-" * 60)
