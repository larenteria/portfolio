from PIL import Image
import numpy as np

# Load the image
image_path = 'images/doggy.jpeg'
image = Image.open(image_path)


def grey_scale(image):
    width, height = image.size

    # Convert the image to RGB mode if it's not already
    image = image.convert('RGB')

    # Initialize an empty list to store RGB values
    rgb_values = []

    # Iterate through each pixel and get the RGB values
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            rgb_values.append((r, g, b))

    # Modify the RGB values as needed (in this example, we are converting to grayscale)
    gray_values = []
    for r, g, b in rgb_values:
        gray = int((r + g + b) / 3)
        gray_values.append((gray, gray, gray))

    # Create a new image with the same dimensions
    grey_image = Image.new('RGB', (width, height))

    # Set the pixels of the new image
    for y in range(height):
        for x in range(width):
            grey_image.putpixel((x, y), gray_values[y * width + x])
    return grey_image


def encrypt(image, password):
    # Get image data as numpy array
    data = np.array(image)

    # Flatten image data
    flat_data = data.flatten()

    # Generate permutation based on password
    password_bytes = password.encode()  # to bytes
    np.random.seed(sum(password_bytes))  # Seed
    permutation = np.random.permutation(len(flat_data))

    # Rearrange image data according to permutation
    encrypted_data = flat_data[permutation]  # Numpy rearrange feature

    # Reshape encrypted data to original image shape
    encrypted_image = encrypted_data.reshape(data.shape)

    # Convert numpy array back to image
    encrypted_image = Image.fromarray(encrypted_image)

    return encrypted_image


def decrypt(image, password):
    # Get image data as numpy array
    data = np.array(image)

    # Flatten image data
    flat_data = data.flatten()

    # Generate the same permutation based on password
    password_bytes = password.encode()
    np.random.seed(sum(password_bytes)) 
    permutation = np.random.permutation(len(flat_data))

    # Inverse permutation to decrypt the data
    decrypted_data = flat_data[np.argsort(permutation)]  # argsort() --> inverse permutation

    # Reshape to original image shape
    decrypted_image = decrypted_data.reshape(data.shape)

    # Convert to image
    decrypted_image = Image.fromarray(decrypted_image)

    return decrypted_image


# Test the functions
new_image = encrypt(image, "ryder")
new_image2 = decrypt(new_image, "ryder")

# Show the images
image.show()
image4 = grey_scale(image)
image4.show()
new_image.show()
new_image2.show()
