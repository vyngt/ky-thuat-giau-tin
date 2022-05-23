"""
Trình giải mã.
"""

from PIL import Image
from .cryptor import decrypt_message
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken


class Decoder:
    """
    ---
    Trình giải mã: Giải mã ảnh số và lấy thông điệp.

    ---
        - B1: Trích xuất bản mã từ ảnh.
        - B2: Dùng `key` để trích xuất thông điệp từ bản mã.
        - B3: Xuất thông điệp(hay có thể gọi là bản rõ).
    """

    def __init__(self, key: str, image: str):
        self.__image_path = image
        self.__key = key
        self.__ciphertext = ""
        self.__data = ""

    def __repr__(self):
        return "<%s.%s image=%s at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.__image_path,
            id(self),
        )

    def __get_image(self):
        return Image.open(self.__image_path, "r")

    def __extract_data_from_image(self):
        img = self.__get_image()
        img_data = iter(img.getdata())

        while True:
            pixels = [
                value
                for value in img_data.__next__()[:3]
                + img_data.__next__()[:3]
                + img_data.__next__()[:3]
            ]

            # string of binary data
            bin_str = ""

            for i in pixels[:8]:
                if i % 2 == 0:
                    bin_str += "0"
                else:
                    bin_str += "1"

            self.__ciphertext += chr(int(bin_str, 2))
            if pixels[-1] % 2 != 0:
                return self.__ciphertext

    def __decode(self):
        self.__extract_data_from_image()
        try:
            self.__data = decrypt_message(
                self.__ciphertext.encode(), self.__key
            ).decode()
        except (InvalidSignature, InvalidToken):
            raise Exception("Sai key hoặc dữ liệu bị hỏng hoặc chương trình có vấn đề.")
        return self.__data

    def decode(self, force=False):
        if force or not self.__ciphertext or not self.__data:
            return self.__decode()

        if self.__data:
            raise Exception("Đã giải mã, thay vào đó hãy dùng get_data()")
        return self.__decode()

    def get_data(self):
        if self.__data:
            return self.__data

        return "Không có dữ liệu hoặc chưa decode."
