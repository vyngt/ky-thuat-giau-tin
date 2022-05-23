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
        Mỗi pixel ảnh gồm 3 giá trị RGB, để lưu được 1 ký tự cần 8 bit nhị phân,
        nghĩa là cần 8 giá trị RGB, cho nên phải dùng 3 pixel ảnh để lưu trữ 1 ký tự.
        - B3: Chỉnh sửa giá trị RGB tương ứng với ký tự ở dạng nhị phân.
        Mỗi bit nhị phân là 0 hoặc 1, ta sẽ chỉnh sửa tương ứng như sau:
                - Chỉnh giá trị RGB thành số chẵn nếu bit nhị phân là 0. (Có thể +1 hoặc -1 hoặc để yên)
                - Chỉnh giá trị RGB thành số lẻ nếu bit nhị phân là 1. (Có thể +1 hoặc -1 hoặc để yên)
        - B4: Sau khi lưu trữ xong 1 ký tự, còn 1 giá trị RGB:
                - Nếu còn dữ liệu thì chỉnh thành số chẵn, quay lại B2
                - Nếu không còn dữ liệu thì chỉnh thành số lẻ, sang B5.
        - B5: Xuất ảnh có thông điệp.

    ---
    Lưu ý về ảnh:
        - Một ảnh số được cấu tạo từ các pixel ảnh
        - Mỗi pixel ảnh bao gồm 3 giá trị: red(đỏ), green(xanh lá), blue(xanh trời) hay được biết đến là các giá trị RGB
        - Mỗi giá trị RGB thuộc [0, 255] nghĩa là: 0 <= x <= 255"""

    def __init__(self, message: str, image: str):
        self.__message = message
        self.__image_path = image
        self.__m_8b: list[str] = self.__convert_to_8bit()
        self.__m_image = self.__get_copy_image(image)

    def __repr__(self):
        return "<%s.%s message=%s... image=%s at 0x%X>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.__message[:3],
            self.__image_path,
            id(self),
        )

    def __convert_to_8bit(self):
        """Chuyển đổi các ký tự của thông điệp sang dạng 8bit."""
        return ["{0:08b}".format(ord(c), "b") for c in self.__message]

    def __get_copy_image(self, image_path: str):
        """Lấy 1 bản sao của ảnh gốc, để tránh chỉnh sửa ảnh gốc."""
        return Image.open(image_path, "r").copy()

    def __get_new_image_name(self):
        """Tên ảnh sau khi chỉnh sửa, là các ký tự ngẫu nhiên."""
        return (
            "".join(choices(ascii_letters, k=10))
            + f".{self.__image_path.split('.')[-1]}"
        )

    def __modify_pixels(self):
        """Điều chỉnh các pixel ảnh"""
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

            # Điều chỉnh 8 giá trị RGB trong 3 pixels.
            for j in range(0, 8):
                if self.__m_8b[i][j] == "0" and _3p[j] % 2 != 0:
                    _3p[j] -= 1

                elif self.__m_8b[i][j] == "1" and _3p[j] % 2 == 0:
                    if _3p[j] != 0:
                        _3p[j] -= 1
                    else:
                        _3p[j] += 1

            # Điều chỉnh giá trị RGB thứ 9.
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

        for pixel in self.__modify_pixels():

            # Áp pixel đã được điều chỉnh vào ảnh mới.
            self.__m_image.putpixel((x, y), pixel)
            if x == w - 1:
                x = 0
                y += 1
            else:
                x += 1

    def __save(self):
        """Xuất ra ảnh mới."""
        output = self.__get_new_image_name()
        self.__m_image.save(output, str(output.split(".")[-1].upper()))
        return output

    def encode(self):
        self.__encode()
        return self.__save()
