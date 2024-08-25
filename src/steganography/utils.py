from os import write
from PIL import Image
import numpy as np


def resize_image(image_path: str, output_path: str, new_size: tuple):
    img = Image.open(image_path)
    resized_img = img.resize(new_size)
    resized_img.save(output_path)


def encode_message(image_path: str, file_path: str, output_image_path: str):
    img = Image.open(image_path)
    with open(file_path, "rb") as file:
        file_data = file.read()

    file_bits = "".join(format(byte, "08b") for byte in file_data)

    img_data = np.array(img)
    flat_img_data = img_data.flatten()

    file_bits += "00000000"

    for i, bit in enumerate(file_bits):
        flat_img_data[i] = (flat_img_data[i] & 0xFE) | int(bit)

    img_data = flat_img_data.reshape(img_data.shape)
    img = Image.fromarray(img_data.astype(np.uint8))

    img.save(output_image_path)
    print(f"Imagen con archivo oculto guardada en {output_image_path}")


def decode_message(image_path: str, output_path: str):
    img = Image.open(image_path)
    img_data = np.array(img)
    flat_img_data = img_data.flatten()

    file_bits = ""
    for i in range(len(flat_img_data)):
        file_bits += str(flat_img_data[i] & 1)

    end_marker = "00000000"
    end_index = file_bits.find(end_marker)

    if end_index != -1:
        file_bits = file_bits[: end_index + 1]

    file_bytes = [int(file_bits[i : i + 8], 2) for i in range(0, len(file_bits), 8)]
    file_data = bytes(file_bytes)

    with open(output_path, "wb") as f:
        f.write(file_data)
