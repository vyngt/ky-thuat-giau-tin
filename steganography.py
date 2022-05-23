"""
The art of Image Steganography
"""

## Tài liệu tham khảo
# https://betterprogramming.pub/image-steganography-using-python-2250896e48b9   <--
# https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password <--
# https://dev.to/erikwhiting88/let-s-hide-a-secret-message-in-an-image-with-python-and-opencv-1jf5
# https://gist.github.com/erik-whiting/d9988122b5e94b1db4c15236b6d86975

import argparse
import sys
from stega import Encoder, Decoder

OPTIONS = {"encode", "decode"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="steganography",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Ẩn thông tin trong ảnh số",
        epilog="""
        Ví dụ:
            steganography -m "my secret data" -k mykey -i "images/original.png"
            steganography -k mykey -i "images/modified.png" --option "decode"
        """,
    )
    parser.add_argument("-m", type=str, help="message: thông điệp muốn giấu trong ảnh.")

    parser.add_argument(
        "-k",
        type=str,
        help="key: khóa dùng để mã hóa hoặc giải mã.",
    )

    parser.add_argument(
        "-i",
        type=str,
        help="image: Đường dẫn đến ảnh.",
    )

    parser.add_argument(
        "--option",
        type=str,
        default="encode",
        help="`encode`: mã hóa và nhúng thông điệp vào ảnh, `decode`: giải mã và trích xuất thông điệp từ ảnh.",
    )

    parser_args = parser.parse_args()
    message: str | None = parser_args.m
    key: str | None = parser_args.k
    image: str | None = parser_args.i
    option: str = parser_args.option

    if key and image and option in OPTIONS:
        output = ""
        if option == "encode":
            if message:
                print("Đang nhúng thông điệp vào ảnh.")
                output = f"Ảnh mới: '{Encoder(message, key, image).encode()}'"
            else:
                print("Thiếu 'thông điệp'.")
                sys.exit(1)

        elif option == "decode":
            print("Đang giải mã và trích xuất thông điệp.")
            output = (
                f"Thông điệp được giấu trong ảnh là: '{Decoder(key, image).decode()}'"
            )

        print(output)
    elif option not in OPTIONS:
        print(f"option '{option}' không có sẵn.")
    else:
        print("Thiếu 'khóa' và 'ảnh'.")
