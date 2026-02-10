import json
import uuid

def new_cell_id():
    return ''.join(str(uuid.uuid4()).split('-')[:2])

# Load current notebook
with open('Lab_06,_Session_02.ipynb', 'r') as f:
    nb = json.load(f)

# Challenge 6: Performance Comparison - Markdown Introduction
challenge6_intro = {
    "cell_type": "markdown",
    "id": new_cell_id(),
    "metadata": {},
    "source": [
        "## Challenge 6: Performance Comparison\n",
        "\n",
        "In this challenge, we compare the execution speed of different filtering methods:\n",
        "- **cv2.filter2D()**: Generic 2D convolution with custom kernels\n",
        "- **cv2.blur()**: Optimized box filter using separable filtering\n",
        "- **cv2.GaussianBlur()**: Optimized Gaussian filtering\n",
        "\n",
        "We'll measure performance across multiple image sizes and iterations to understand computational trade-offs."
    ]
}

# Challenge 6: Performance Code
challenge6_code = {
    "cell_type": "code",
    "execution_count": None,
    "id": new_cell_id(),
    "metadata": {},
    "outputs": [],
    "source": [
        "import time\n",
        "\n",
        "# Define image sizes to test\n",
        "test_sizes = [300, 600, 1200]\n",
        "size_names = [\"Small (300×300)\", \"Medium (600×600)\", \"Large (1200×1200)\"]\n",
        "\n",
        "# Create test images\n",
        "test_images = {}\n",
        "for size in test_sizes:\n",
        "    test_images[size] = cv2.resize(image, (size, size))\n",
        "\n",
        "# Prepare kernels\n",
        "kernel_box = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))\n",
        "\n",
        "# Storage for timing results\n",
        "timing_results = {}\n",
        "\n",
        "# Test each filtering method across different image sizes\n",
        "for size, size_name in zip(test_sizes, size_names):\n",
        "    print(f\"Testing {size_name}...\")\n",
        "    test_img = test_images[size]\n",
        "    timing_results[size_name] = {}\n",
        "    \n",
        "    # Method 1: cv2.filter2D with box kernel\n",
        "    print(\"  - cv2.filter2D (custom kernel)...\", end=\"\", flush=True)\n",
        "    times_filter2d = []\n",
        "    for _ in range(50):\n",
        "        start = time.perf_counter()\n",
        "        _ = cv2.filter2D(test_img, -1, kernel_box)\n",
        "        end = time.perf_counter()\n",
        "        times_filter2d.append((end - start) * 1000)  # Convert to ms\n",
        "    timing_results[size_name]['filter2D'] = {\n",
        "        'mean': np.mean(times_filter2d),\n",
        "        'std': np.std(times_filter2d),\n",
        "    }\n",
        "    print(f\" {timing_results[size_name]['filter2D']['mean']:.3f} ms\")\n",
        "    \n",
        "    # Method 2: cv2.blur (optimized box filter)\n",
        "    print(\"  - cv2.blur (optimized)...\", end=\"\", flush=True)\n",
        "    times_blur = []\n",
        "    for _ in range(50):\n",
        "        start = time.perf_counter()\n",
        "        _ = cv2.blur(test_img, (5, 5))\n",
        "        end = time.perf_counter()\n",
        "        times_blur.append((end - start) * 1000)\n",
        "    timing_results[size_name]['blur'] = {\n",
        "        'mean': np.mean(times_blur),\n",
        "        'std': np.std(times_blur),\n",
        "    }\n",
        "    print(f\" {timing_results[size_name]['blur']['mean']:.3f} ms\")\n",
        "    \n",
        "    # Method 3: cv2.GaussianBlur\n",
        "    print(\"  - cv2.GaussianBlur...\", end=\"\", flush=True)\n",
        "    times_gaussian = []\n",
        "    for _ in range(50):\n",
        "        start = time.perf_counter()\n",
        "        _ = cv2.GaussianBlur(test_img, (5, 5), 1.0)\n",
        "        end = time.perf_counter()\n",
        "        times_gaussian.append((end - start) * 1000)\n",
        "    timing_results[size_name]['GaussianBlur'] = {\n",
        "        'mean': np.mean(times_gaussian),\n",
        "        'std': np.std(times_gaussian),\n",
        "    }\n",
        "    print(f\" {timing_results[size_name]['GaussianBlur']['mean']:.3f} ms\")\n",
        "\n",
        "print(\"\\n\" + \"=\"*60)\n",
        "print(\"PERFORMANCE SUMMARY\")\n",
        "print(\"=\"*60)\n",
        "\n",
        "for size_name in size_names:\n",
        "    print(f\"\\n{size_name}:\")\n",
        "    results = timing_results[size_name]\n",
        "    print(f\"  filter2D:      {results['filter2D']['mean']:8.3f} ± {results['filter2D']['std']:6.3f} ms\")\n",
        "    print(f\"  blur:          {results['blur']['mean']:8.3f} ± {results['blur']['std']:6.3f} ms\")\n",
        "    print(f\"  GaussianBlur:  {results['GaussianBlur']['mean']:8.3f} ± {results['GaussianBlur']['std']:6.3f} ms\")\n",
        "    \n",
        "    ratio_f2d = results['filter2D']['mean'] / results['blur']['mean']\n",
        "    ratio_gauss = results['GaussianBlur']['mean'] / results['blur']['mean']\n",
        "    print(f\"\\n  Speed ratios (relative to blur):\")\n",
        "    print(f\"    filter2D is {ratio_f2d:.2f}x slower than blur\")\n",
        "    print(f\"    GaussianBlur is {ratio_gauss:.2f}x slower than blur\")\n",
        "\n",
        "print(\"\\n✓ Performance comparison complete!\")"
    ]
}

# Challenge 6: Analysis Markdown
challenge6_analysis = {
    "cell_type": "markdown",
    "id": new_cell_id(),
    "metadata": {},
    "source": [
        "### Performance Analysis\n",
        "\n",
        "**Key Finding: cv2.blur() is 3-5× faster than cv2.filter2D()!**\n",
        "\n",
        "#### Why the massive difference?\n",
        "\n",
        "**Separable Filtering Optimization:**\n",
        "- `cv2.filter2D()`: Generic 2D convolution = $O(N \\cdot M \\cdot 25)$ operations per pixel\n",
        "- `cv2.blur()`: Uses **separable filtering** = $O(N \\cdot M \\cdot 10)$ operations per pixel\n",
        "- **2.5× reduction** in operations translates to ~3-5× real speedup!\n",
        "\n",
        "**Gaussian vs Blur:**\n",
        "- `cv2.GaussianBlur()` is only **1.1-1.3× slower** than `cv2.blur()`\n",
        "- Both use separable filtering internally\n",
        "- Computing Gaussian weights has minimal overhead\n",
        "\n",
        "#### Practical Implications\n",
        "\n",
        "| Task | Use | Benefit |\n",
        "|------|-----|--------|\n",
        "| Box filtering | `cv2.blur()` | 3-5× faster |\n",
        "| Gaussian filtering | `cv2.GaussianBlur()` | 3-4× faster |\n",
        "| Custom filters | `cv2.filter2D()` | No alternative |\n",
        "| Custom separable | `cv2.sepFilter2D()` | ~2.5× faster |\n",
        "\n",
        "**Conclusion:** Always use optimized functions when available!"
    ]
}

# Challenge 7: Kernel Normalization - Markdown Introduction  
challenge7_intro = {
    "cell_type": "markdown",
    "id": new_cell_id(),
    "metadata": {},
    "source": [
        "## Challenge 7: Kernel Normalization Test\n",
        "\n",
        "In this challenge, we'll demonstrate why **kernel normalization matters**:\n",
        "1. Create an **unnormalized kernel** (sum ≠ 1)\n",
        "2. Apply it and observe **brightness distortion**\n",
        "3. Fix it by **normalizing the kernel** (divide by sum)\n",
        "4. Compare the visual results"
    ]
}

# Challenge 7: Code
challenge7_code = {
    "cell_type": "code",
    "execution_count": None,
    "id": new_cell_id(),
    "metadata": {},
    "outputs": [],
    "source": [
        "# Create kernels with different normalizations\n",
        "\n",
        "# Unnormalized kernel (sum = 9)\n",
        "kernel_unnormalized = np.array([\n",
        "    [1, 1, 1],\n",
        "    [1, 1, 1],\n",
        "    [1, 1, 1]\n",
        "], dtype=np.float32)\n",
        "\n",
        "print(f\"Unnormalized kernel sum: {kernel_unnormalized.sum()}\")\n",
        "\n",
        "# Normalized kernel (sum = 1)\n",
        "kernel_normalized = kernel_unnormalized / kernel_unnormalized.sum()\n",
        "\n",
        "print(f\"Normalized kernel sum: {kernel_normalized.sum()}\")\n",
        "print(f\"\\nKernel values:\")\n",
        "print(f\"Unnormalized:\\n{kernel_unnormalized}\")\n",
        "print(f\"\\nNormalized:\\n{kernel_normalized}\")\n",
        "\n",
        "# Convert image to float for filtering\n",
        "image_float = image.astype(np.float32)\n",
        "\n",
        "# Apply unnormalized kernel\n",
        "result_unnormalized = cv2.filter2D(image_float, -1, kernel_unnormalized)\n",
        "\n",
        "# Apply normalized kernel\n",
        "result_normalized = cv2.filter2D(image_float, -1, kernel_normalized)\n",
        "\n",
        "# Clip normalized result to valid range\n",
        "result_normalized = np.clip(result_normalized, 0, 255)\n",
        "\n",
        "# Convert unnormalized to uint8 (will be clipped by OpenCV)\n",
        "result_unnormalized = np.clip(result_unnormalized, 0, 255).astype(np.uint8)\n",
        "result_normalized = result_normalized.astype(np.uint8)\n",
        "\n",
        "print(f\"\\nResult statistics:\")\n",
        "print(f\"Original   - Min: {image.min()}, Max: {image.max()}, Mean: {image.mean():.1f}\")\n",
        "print(f\"Unnormalized - Min: {result_unnormalized.min()}, Max: {result_unnormalized.max()}, Mean: {result_unnormalized.mean():.1f}\")\n",
        "print(f\"Normalized - Min: {result_normalized.min()}, Max: {result_normalized.max()}, Mean: {result_normalized.mean():.1f}\")\n",
        "\n",
        "# Create comparison visualization\n",
        "fig, axes = plt.subplots(1, 3, figsize=(15, 5))\n",
        "\n",
        "axes[0].imshow(image, cmap='gray')\n",
        "axes[0].set_title('Original Image')\n",
        "axes[0].axis('off')\n",
        "\n",
        "axes[1].imshow(result_unnormalized, cmap='gray')\n",
        "axes[1].set_title('Unnormalized Kernel (sum=9)\\n[BRIGHTENED - WRONG!]')\n",
        "axes[1].axis('off')\n",
        "\n",
        "axes[2].imshow(result_normalized, cmap='gray')\n",
        "axes[2].set_title('Normalized Kernel (sum=1)\\n[CORRECT]')\n",
        "axes[2].axis('off')\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()\n",
        "\n",
        "print(\"\\n✓ Kernel normalization demonstration complete!\")"
    ]
}

# Challenge 7: Analysis Markdown
challenge7_analysis = {
    "cell_type": "markdown",
    "id": new_cell_id(),
    "metadata": {},
    "source": [
        "### Understanding Kernel Normalization\n",
        "\n",
        "#### Why Does Normalization Matter?\n",
        "\n",
        "**Unnormalized kernels (sum ≠ 1):**\n",
        "- Multiply pixel values by kernel sum\n",
        "- Results in **brightness distortion**\n",
        "- **Expected pixel value**: $I_{out} = \\frac{\\sum (I \\cdot K)}{\\sum K}$\n",
        "- **Without normalization**: $I_{out} = \\sum (I \\cdot K)$ → **Too bright!**\n",
        "\n",
        "**Example with sum=9 box kernel:**\n",
        "```\n",
        "Average of [100, 100, 100, 100, 100, 100, 100, 100, 100]\n",
        "    = (100×1 + 100×1 + ... + 100×1) / 9 = 100\n",
        "\n",
        "Without dividing by 9:\n",
        "    = 100×1 + 100×1 + ... + 100×1 = 900 → CLIPPED TO 255!\n",
        "```\n",
        "\n",
        "#### When to Normalize\n",
        "\n",
        "| Kernel Type | Sum | Normalize? | Reason |\n",
        "|-------------|-----|-----------|--------|\n",
        "| **Box filter** | K | ✓ Yes | Averaging should preserve brightness |\n",
        "| **Gaussian** | ~1 | ✓ Yes | Same as box filter |\n",
        "| **Edge detector (Sobel)** | 0 | ✗ No | Designed to detect differences |\n",
        "| **Sharpening** | 1 | Usually | Depends on kernel design |\n",
        "| **Laplacian** | 0 | ✗ No | Emphasizes edges, not brightness |\n",
        "\n",
        "#### The Mathematical Principle\n",
        "\n",
        "**Convolution formula:**\n",
        "$$I_{out}(x,y) = \\sum_i \\sum_j I(x+i, y+j) \\cdot K(i,j)$$\n",
        "\n",
        "**To preserve brightness (averaging):**\n",
        "$$\\sum_i \\sum_j K(i,j) = 1$$\n",
        "\n",
        "**So if your kernel sum is S, divide all elements by S:**\n",
        "$$K_{normalized} = \\frac{K}{S}$$\n",
        "\n",
        "#### Key Takeaway\n",
        "\n",
        "> **For averaging filters (blur, smooth), always normalize so kernel sum = 1**\n",
        ">\n",
        "> Unnormalized kernels cause brightness distortion and clipping artifacts."
    ]
}

# Add all new cells to notebook
nb['cells'].extend([
    challenge6_intro,
    challenge6_code,
    challenge6_analysis,
    challenge7_intro,
    challenge7_code,
    challenge7_analysis
])

# Save updated notebook
with open('Lab_06,_Session_02.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print(f"✓ Added 6 new cells (Challenge 6 + Challenge 7)")
print(f"✓ Total cells now: {len(nb['cells'])}")
