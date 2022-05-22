"""
encoder module
"""
from typing import Iterator
from PIL import Image
from string import ascii_letters
from random import choices


class Encoder:
    """
    ---
    Trình mã hóa: Mã hóa và nhúng thông điệp vào trong ảnh số.

    ---
    Cách hoạt động:
        - B1: Chuyển đổi các ký tự của thông điệp sang dạng 8-bit nhị phân
        - B2: Đọc 3 pixels ảnh.
        Mỗi pixel ảnh gồm 3 giá trị RGB, để lưu được 1 ký tự cần 8 bit nhị phân, nghĩa là cần 8 giá trị RGB,
        cho nên phải dùng 3 pixel ảnh để lưu trữ 1 ký tự.
        - B3: Chỉnh sửa giá trị RGB tương ứng với ký tự ở dạng nhị phân.
        Mỗi bit nhị phân là 0 hoặc 1, ta sẽ chỉnh sửa tương ứng như sau: RGB => chẵn nếu bit nhị phân là 0 và ngược lại.
        - B4: Sau khi lưu trữ xong 1 ký tự, còn 1 giá trị RGB, nếu còn dữ liệu thì chỉnh => chẵn, ngược lại => lẻ.

    ---
    Lưu ý về ảnh:
        - Một ảnh số được cấu tạo từ các pixel ảnh
        - Mỗi pixel ảnh bao gồm 3 giá trị: red(đỏ), green(xanh lá), blue(xanh trời) hay được biết đến là các giá trị RGB
        - Mỗi giá trị RGB thuộc [0, 255] nghĩa là: 0 <= x <= 255"""

    def __init__(self, message: str, image_path: str):
        self.__message = message
        self.__image_path = image_path
        self.__m_8b: list[str] = self.__convert_to_8bit()
        self.__m_image = self.__get_copy_image(image_path)
        self.__output_name: str = self.__get_new_image_name(image_path)

    def __str__(self):
        return f"Encoder(data={self.__message} image={self.__image_path}) at {hex(id(self))}"

    def __repr__(self):
        return self.__str__()

    def __convert_to_8bit(self):
        return ["{0:08b}".format(ord(c), "b") for c in self.__message]

    def __get_copy_image(self, image_path: str):
        return Image.open(image_path, "r").copy()

    def __get_new_image_name(self, image_path: str):
        return "".join(choices(ascii_letters, k=10)) + f".{image_path.split('.')[-1]}"

    def __pixels_modifier(self):
        len_data = len(self.__m_8b)
        pixels: Iterator[tuple[int]] = iter(self.__m_image.getdata())

        for i in range(len_data):

            # Lấy 3 pixels
            _3p = [
                value
                for value in pixels.__next__()[:3]
                + pixels.__next__()[:3]
                + pixels.__next__()[:3]
            ]

            for j in range(0, 8):
                if self.__m_8b[i][j] == "0" and _3p[j] % 2 != 0:
                    _3p[j] -= 1

                elif self.__m_8b[i][j] == "1" and _3p[j] % 2 == 0:
                    if _3p[j] != 0:
                        _3p[j] -= 1
                    else:
                        _3p[j] += 1

            # ...
            if i == len_data - 1:
                if _3p[-1] % 2 == 0:
                    if _3p[-1] != 0:
                        _3p[-1] -= 1
                    else:
                        _3p[-1] += 1
            else:
                if _3p[-1] % 2 != 0:
                    _3p[-1] -= 1

            pix = tuple(_3p)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def __encode(self):
        w = self.__m_image.size[0]
        (x, y) = (0, 0)

        for pixel in self.__pixels_modifier():

            # Putting modified pixels in the new image
            self.__m_image.putpixel((x, y), pixel)
            if x == w - 1:
                x = 0
                y += 1
            else:
                x += 1

    def encode(self):
        self.__encode()

        # Saving
        self.__m_image.save(
            self.__output_name, str(self.__output_name.split(".")[-1].upper())
        )
        return self.__output_name
