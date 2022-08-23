from .reader import Reader
from .writer import Writer
from multiprocessing import Process
from typing import Optional
import os

__version__ = "2.0.0-beta"

class FileTypeError(Exception):
    pass


class FileDoesNotExistError(Exception):
    pass


def video2gif(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        quality: bool = False,
        shit_optimize: bool = False,
        text: str = "",
        text_style: str = "top",
        progress_bar: bool = False
) -> None:

    if not os.path.exists(filename):
        raise FileDoesNotExistError(f"File '{filename}' does not exist.")
        
    reader = Reader(filename, output, width, fps_reduction, shit_optimize, text, text_style, progress_bar)
    writer = Writer(filename, reader.frames, reader.resolution, quality, output, fps_reduction, shit_optimize, progress_bar)
    
    try:
        p = Process(target=reader.read_video, args=())
        p.start()
        writer.write_gif()
        p.join()
    except KeyboardInterrupt:
        p.terminate()


def gif2video(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        quality: bool = False,
        shit_optimize: bool = False,
        text: str = "",
        text_style: str = "top",
        progress_bar: bool = False
) -> None:

    if not os.path.exists(filename):
        raise FileDoesNotExistError(f"File '{filename}' does not exist.")
    if filename[-4:] != ".gif":
        raise FileTypeError(f"File '{filename}' is not a gif.")

    reader = Reader(filename, output, width, fps_reduction, shit_optimize, text, text_style, progress_bar)
    writer = Writer(filename, reader.frames, reader.resolution, quality, output, fps_reduction, shit_optimize, progress_bar)

    try:
        p = Process(target=reader.read_video, args=())
        p.start()
        writer.write_video()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
