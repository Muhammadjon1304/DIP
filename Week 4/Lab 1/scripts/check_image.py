import cv2
import numpy as np

path = '/Users/muhammadjonparpiyev/Documents/DIP/Week 4/Lab 1/anfield.jpg'
img = cv2.imread(path, cv2.IMREAD_COLOR)

print(f"Shape: {img.shape}")
print(f"Channels: {img.shape[2] if len(img.shape) == 3 else 1}")

if len(img.shape) == 3:
    b, g, r = cv2.split(img)
    print(f"B mean: {b.mean():.2f}, G mean: {g.mean():.2f}, R mean: {r.mean():.2f}")
    print(f"B==G: {np.array_equal(b, g)}, G==R: {np.array_equal(g, r)}")
    if np.array_equal(b, g) and np.array_equal(g, r):
        print("-> Image is GRAYSCALE (all channels identical)")
    else:
        print("-> Image is COLOR")
