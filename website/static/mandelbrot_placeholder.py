from PIL import Image
import numpy as np

def mandelbrot(width, height, max_iter):
    # Create a blank white image
    img = Image.new('RGB', (width, height), color='white')
    pixels = img.load()

    # Define the region of the complex plane to display
    x_min, x_max, y_min, y_max = -2.0, 1.0, -1.5, 1.5

    # Scale the pixels to the complex plane
    for x in range(width):
        for y in range(height):
            zx, zy = x * (x_max - x_min) / (width - 1) + x_min, y * (y_max - y_min) / (height - 1) + y_min
            c = complex(zx, zy)
            z = 0.0j
            iter_count = 0

            # Iterate to determine the pixel color based on convergence
            while abs(z) <= 2 and iter_count < max_iter:
                z = z * z + c
                iter_count += 1

            # Assign color based on the number of iterations
            color = (iter_count * 10) % 256  # Just an example of coloring
            pixels[x, y] = (color, color, color)

    return img

# Create the Mandelbrot image
image = mandelbrot(1200, 1000, 512)
# image.show()  # Display the image

# Save the image if you'd like
image.save("mandelbrot_placeholder.png")
