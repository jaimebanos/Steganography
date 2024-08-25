from os import write
from PIL import Image
import numpy as np
import os

MARK = "11110000111100001111000011110000"


def resize_image(image_path: str, output_path: str, new_size: tuple):
    img = Image.open(image_path)
    resized_img = img.resize(new_size)
    resized_img.save(output_path)


def encode_message(image_path: str, file_path: str, output_image_path: str):
    img = Image.open(image_path)
    with open(file_path, "rb") as file:
        file_data = file.read()

    file_name, file_extension = os.path.splitext(file_path)
    file_type = file_extension[1:]  # Quitar el punto del inicio

    file_type_bits = "".join(format(ord(c), "08b") for c in file_type) + MARK
    file_name_bits = "".join(format(ord(c), "08b") for c in file_name) + MARK
    file_bits = "".join(format(byte, "08b") for byte in file_data) + MARK

    bits_to_encode = file_type_bits + file_name_bits + file_bits

    img_data = np.array(img)
    flat_img_data = img_data.flatten()

    if len(bits_to_encode) > len(flat_img_data):
        raise ValueError("Message is too long to encode in the image.")

    for i, bit in enumerate(bits_to_encode):
        flat_img_data[i] = (flat_img_data[i] & 0xFE) | int(bit)

    img_data = flat_img_data.reshape(img_data.shape)
    img = Image.fromarray(img_data.astype(np.uint8))

    img.save(output_image_path)
    print(f"Imagen con archivo oculto guardada en {output_image_path}")


def decode_message(image_path: str):
    img = Image.open(image_path)
    img_data = np.array(img)
    flat_img_data = img_data.flatten()

    bits = "".join(str(pixel & 1) for pixel in flat_img_data)

    parts = bits.split(MARK)

    if len(parts) < 3:
        raise ValueError("Not have any message")

    file_type_bits = parts[0]
    file_name_bits = parts[1]
    file_bits = parts[2]
    print(len(parts))

    def bits_to_string(bits):
        return "".join(chr(int(bits[i : i + 8], 2)) for i in range(0, len(bits), 8))

    file_type = bits_to_string(file_type_bits)
    file_name = bits_to_string(file_name_bits)
    file_data_bits = file_bits

    file_data = bytearray()
    for i in range(0, len(file_data_bits), 8):
        byte = file_data_bits[i : i + 8]
        if len(byte) < 8:
            break
        file_data.append(int(byte, 2))

    with open(f"decoders/extracted_{file_name}.{file_type}", "wb") as file:
        file.write(file_data)
