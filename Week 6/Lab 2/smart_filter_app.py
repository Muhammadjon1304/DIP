"""
Smart Filter Selector - Interactive Application

An interactive command-line application for exploring image filters.
Run this in a Jupyter notebook for full functionality with visualizations.
"""

import sys
import os

# Try to import required modules
try:
    import numpy as np
    import cv2
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"❌ Error: Missing required module: {e}")
    print("   Please install: pip install numpy opencv-python matplotlib")
    sys.exit(1)

# Import the SmartFilterSelector
try:
    from smart_filter_selector import SmartFilterSelector
except ImportError:
    print("❌ Error: Could not import SmartFilterSelector")
    print("   Make sure smart_filter_selector.py is in the current directory")
    sys.exit(1)


class SmartFilterApp:
    """Interactive Smart Filter Selector Application."""
    
    def __init__(self, image_path='roberto-firmino-liverpool.avif'):
        """Initialize the app with an image."""
        self.image_path = image_path
        self.image = None
        self.selector = None
        self.history = []
        
        self.load_image()
    
    def load_image(self):
        """Load the image from file."""
        if not os.path.exists(self.image_path):
            print(f"❌ Error: Image file not found: {self.image_path}")
            print("   Available files:")
            for f in os.listdir('.'):
                if f.endswith(('.jpg', '.png', '.avif', '.jpeg')):
                    print(f"   - {f}")
            sys.exit(1)
        
        self.image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            print(f"❌ Error: Could not load image from {self.image_path}")
            sys.exit(1)
        
        print(f"✓ Image loaded: {self.image_path}")
        print(f"  Shape: {self.image.shape}")
        print(f"  Data type: {self.image.dtype}")
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("SMART FILTER SELECTOR - INTERACTIVE APPLICATION")
        print("="*60)
        print("\nChoose an option:")
        print("  1. Apply Uniform (Box) Filter")
        print("  2. Apply Gaussian Filter")
        print("  3. Compare Filters")
        print("  4. View Statistics")
        print("  5. Show Image Info")
        print("  6. Exit")
        print("-"*60)
    
    def apply_uniform_filter(self):
        """Apply uniform filter with user input."""
        print("\n📌 Uniform Filter (Box Blur)")
        print("-"*60)
        
        try:
            kernel_size = int(input("Enter kernel size (odd number, e.g., 5, 7, 9): "))
            
            self.selector = SmartFilterSelector(self.image)
            if not self.selector.select_filter('uniform', kernel_size=kernel_size):
                return
            
            self.selector.apply_filter()
            self.selector.compare_side_by_side()
            
            print("\nDo you want to see statistics? (y/n): ", end="")
            if input().lower() == 'y':
                self.selector.compute_statistics()
            
            self.history.append(('uniform', kernel_size, None))
            print("✓ Filter applied and saved to history")
            
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def apply_gaussian_filter(self):
        """Apply Gaussian filter with user input."""
        print("\n📌 Gaussian Filter")
        print("-"*60)
        
        try:
            kernel_size = int(input("Enter kernel size (odd number, e.g., 5, 7, 9): "))
            sigma = float(input("Enter sigma value (e.g., 1.0, 1.5, 2.0): "))
            
            self.selector = SmartFilterSelector(self.image)
            if not self.selector.select_filter('gaussian', kernel_size=kernel_size, sigma=sigma):
                return
            
            self.selector.apply_filter()
            self.selector.compare_side_by_side()
            
            print("\nDo you want to see statistics? (y/n): ", end="")
            if input().lower() == 'y':
                self.selector.compute_statistics()
            
            self.history.append(('gaussian', kernel_size, sigma))
            print("✓ Filter applied and saved to history")
            
        except ValueError:
            print("❌ Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def compare_filters(self):
        """Compare uniform and gaussian filters side by side."""
        print("\n📌 Compare Filters")
        print("-"*60)
        
        try:
            kernel_size = int(input("Enter kernel size (odd number, e.g., 5, 7, 9): "))
            sigma = float(input("Enter sigma for Gaussian (e.g., 1.5): "))
            
            print("\nApplying Uniform Filter...")
            sel1 = SmartFilterSelector(self.image)
            sel1.select_filter('uniform', kernel_size=kernel_size)
            sel1.apply_filter()
            
            print("Applying Gaussian Filter...")
            sel2 = SmartFilterSelector(self.image)
            sel2.select_filter('gaussian', kernel_size=kernel_size, sigma=sigma)
            sel2.apply_filter()
            
            # Create comparison visualization
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            
            axes[0].imshow(self.image, cmap='gray')
            axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
            axes[0].axis('off')
            
            axes[1].imshow(sel1.filtered_image, cmap='gray')
            axes[1].set_title(f'Uniform Filter (k={kernel_size})', fontsize=12, fontweight='bold')
            axes[1].axis('off')
            
            axes[2].imshow(sel2.filtered_image, cmap='gray')
            axes[2].set_title(f'Gaussian Filter (k={kernel_size}, σ={sigma})', fontsize=12, fontweight='bold')
            axes[2].axis('off')
            
            plt.tight_layout()
            plt.show()
            
            print("✓ Comparison displayed")
            
        except ValueError:
            print("❌ Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def view_statistics(self):
        """View statistics from last filter."""
        print("\n📊 Statistics")
        print("-"*60)
        
        if self.selector is None or self.selector.filtered_image is None:
            print("ℹ️  No filter applied yet. Apply a filter first.")
            return
        
        self.selector.compute_statistics()
    
    def show_image_info(self):
        """Display image information."""
        print("\n📋 Image Information")
        print("-"*60)
        print(f"File: {self.image_path}")
        print(f"Shape: {self.image.shape}")
        print(f"Data type: {self.image.dtype}")
        print(f"Min value: {self.image.min()}")
        print(f"Max value: {self.image.max()}")
        print(f"Mean value: {self.image.mean():.2f}")
        print(f"Std deviation: {self.image.std():.2f}")
        
        if self.history:
            print("\n📜 Filter History:")
            for i, (ftype, kernel, sigma) in enumerate(self.history, 1):
                if sigma is None:
                    print(f"  {i}. {ftype.upper()} (kernel={kernel})")
                else:
                    print(f"  {i}. {ftype.upper()} (kernel={kernel}, σ={sigma})")
    
    def run(self):
        """Run the interactive application."""
        print("\n" + "🎬 "*30)
        print("SMART FILTER SELECTOR APPLICATION")
        print("🎬 "*30)
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (1-6): ").strip()
                
                if choice == '1':
                    self.apply_uniform_filter()
                elif choice == '2':
                    self.apply_gaussian_filter()
                elif choice == '3':
                    self.compare_filters()
                elif choice == '4':
                    self.view_statistics()
                elif choice == '5':
                    self.show_image_info()
                elif choice == '6':
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-6.")
            
            except KeyboardInterrupt:
                print("\n\n👋 Application interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main entry point."""
    try:
        app = SmartFilterApp()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
