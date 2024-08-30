from typing import List

import numpy as np
from PIL import Image


class ImageService:
    MAX_HEIGHT_PIXELS = 224
    MAX_WIDTH_PIXELS = 224
    RGBA_CHANNELS = 4
    RGB_CHANNELS = 3

    @staticmethod
    def is_valid_image(image: List[List[int]]) -> bool:
        try:
            image = np.array(image, dtype=np.uint8)
            Image.fromarray(image)
            expected_size = ImageService.MAX_HEIGHT_PIXELS * ImageService.MAX_WIDTH_PIXELS * ImageService.RGBA_CHANNELS
            if len(image.flatten()) != expected_size:
                raise ValueError(
                    f"El tamaño del array es incorrecto. Se esperaban "
                    f"{expected_size} elementos, pero se obtuvieron "
                    f"{len(image.flatten())} elementos.")
            return True
        except Exception as err:
            print(err)
            return False

    @staticmethod
    def convert_list_to_numpy_array(image: List[List[int]]) -> np.ndarray:
        image = np.array(image, dtype=np.uint8)
        rgba_image = image.reshape(
            (ImageService.MAX_HEIGHT_PIXELS * ImageService.MAX_WIDTH_PIXELS, ImageService.RGBA_CHANNELS))
        bgr_array = rgba_image[:, [2, 1, 0]]
        bgr_image = bgr_array.reshape(
            (ImageService.MAX_HEIGHT_PIXELS, ImageService.MAX_WIDTH_PIXELS, ImageService.RGB_CHANNELS))
        return bgr_image

    @staticmethod
    def convert_to_binary(image: List[List[int]]) -> bytes:
        np_image = np.array(image, dtype=np.uint8)
        return np_image.tobytes()

    @staticmethod
    def convert_to_array(image: bytes) -> List[List[int]]:
        array = np.frombuffer(image, dtype=np.uint8)
        list = (array.reshape(
            (ImageService.MAX_HEIGHT_PIXELS * ImageService.MAX_WIDTH_PIXELS, ImageService.RGBA_CHANNELS))).tolist()
        return list

    @staticmethod
    def convert_to_numpy_for_deepface(image: bytes) -> np.ndarray:
        array = np.frombuffer(image, dtype=np.uint8)
        expected_size = ImageService.MAX_HEIGHT_PIXELS * ImageService.MAX_WIDTH_PIXELS * ImageService.RGBA_CHANNELS
        if len(array) != expected_size:
            raise ValueError(
                f"El tamaño del array es incorrecto. Se esperaban "
                f"{expected_size} elementos, pero se obtuvieron "
                f"{len(array)} elementos.")

        rgba_image = array.reshape(
            (ImageService.MAX_HEIGHT_PIXELS * ImageService.MAX_WIDTH_PIXELS, ImageService.RGBA_CHANNELS))
        bgr_array = rgba_image[:, [2, 1, 0]]
        bgr_image = bgr_array.reshape(
            (ImageService.MAX_HEIGHT_PIXELS, ImageService.MAX_WIDTH_PIXELS, ImageService.RGB_CHANNELS))
        return bgr_image
