from cx_Freeze import setup, Executable

packages = ["os", "pytube", "tkinter", "moviepy", "PIL", "threading", "tqdm"]
include_files = ["D:/Projetos_Python/down-youtube/IA-Image.jpg"]

setup(
    name = "Downloader_Gle",
    version = "1.0",
    description = "Programa para download de videos do Youtube",
    options = {
        'build_exe': {
            'packages': packages,
            'include_files': include_files,
        },
    },
    executables = [Executable("downloader.py", base="Win32GUI")],
)