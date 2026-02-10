import cv2
import numpy as np

# Check both images
for fname in ['4.png', 'anfield.jpg']:
    path = f'/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/{fname}'
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is not None:
        print(f"\n{fname}:")
        print(f"  Shape: {img.shape}")
        if len(img.shape) == 3:
            b, g, r = cv2.split(img)
            print(f"  B mean: {b.mean():.2f}, G mean: {g.mean():.2f}, R mean: {r.mean():.2f}")
            color_diff = abs(int(r.mean()) - int(g.mean())) + abs(int(g.mean()) - int(b.mean()))
            print(f"  Color variance: {color_diff} (higher = more colorful)")
