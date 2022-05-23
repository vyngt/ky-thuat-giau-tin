import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "steganography.py",
        "--onefile",
        "-i=steganography.ico",
    ]
)
