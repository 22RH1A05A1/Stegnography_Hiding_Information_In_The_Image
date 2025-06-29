import cv2
import numpy as np

def message_to_binary(message):
    return ''.join([format(ord(char), '08b') for char in message])

def binary_to_message(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars if int(char, 2) != 0])

def encode_message(image_path, secret_message, output_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found. Check the path.")

    binary_msg = message_to_binary(secret_message) + '1111111111111110'  # EOF marker

    flat_image = img.flatten()
    if len(binary_msg) > len(flat_image):
        raise ValueError("Message is too large to hide in the image.")

    # Modify the least significant bit of each pixel
    for i in range(len(binary_msg)):
        flat_image[i] = (int(flat_image[i]) & ~1) | int(binary_msg[i])

    # Ensure correct type
    flat_image = flat_image.astype(np.uint8)

    # Reshape and save
    encoded_img = flat_image.reshape(img.shape)
    cv2.imwrite(output_path, encoded_img)
    print(f"Message encoded and saved to: {output_path}")

def decode_message(encoded_image_path):
    img = cv2.imread(encoded_image_path)
    if img is None:
        raise FileNotFoundError("Image not found. Check the path.")

    flat_image = img.flatten()
    binary_msg = ''

    for value in flat_image:
        binary_msg += str(value & 1)
        if binary_msg[-16:] == '1111111111111110':  # EOF marker
            break

    return binary_to_message(binary_msg[:-16])  # Remove EOF marker

# ========== 🔧 MAIN ==========
if __name__ == "__main__":
    image_path = "sample.png"
    secret_message = "Hello from Steganography!"
    output_image = "encoded_sample.png"

    # Encode
    encode_message(image_path, secret_message, output_image)

    # Decode
    hidden = decode_message(output_image)
    print("Hidden Message:", hidden)
