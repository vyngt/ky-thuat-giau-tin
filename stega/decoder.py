from PIL import Image


class Decoder:
    """
    ---
    Trình giải mã: Giải mã ảnh số và lấy thông điệp.

    """

    def __init__(self, image_path: str):
        self.__image_path = image_path
        self.__data = ""

    def __str__(self):
        return f"Decoder(image={self.__image_path} at {hex(id(self))}"

    def __repr__(self):
        return self.__str__()

    def __get_image(self):
        return Image.open(self.__image_path, "r")

    def __decode(self):
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

            self.__data += chr(int(bin_str, 2))
            if pixels[-1] % 2 != 0:
                return self.__data

    def decode(self, force=False):
        if force or not self.__data:
            return self.__decode()
        return self.__decode()

    def get_data(self):
        if self.__data:
            return self.__data

        return "None"
