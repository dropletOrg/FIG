from .reader import Reader
from .writer import Writer
from .text_style import TextStyle
from .dither_type import DitherType
from multiprocessing import Process
from typing import Optional, Tuple
import os
from .utils import Utils
import subprocess

__version__ = "2.5.1"


class FileTypeError(Exception):
    pass


class FileDoesNotExistError(Exception):
    pass


def __get_reader_writer(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        quality: bool = False,
        dither: bool = False,
        shit_optimize: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        progress_bar: bool = False
) -> Tuple[Reader, Writer]:
    reader = Reader(filename, output, width, fps_reduction, dither, shit_optimize, text, text_style, progress_bar)
    writer = Writer(filename, reader.frames, reader.resolution, output, quality, fps_reduction, dither, shit_optimize,
                    progress_bar)
    return reader, writer


def video2video(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        quality: bool = False,
        dither: bool = False,
        shit_optimize: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        progress_bar: bool = False
) -> None:
    if not os.path.exists(filename):
        raise FileDoesNotExistError(f"File '{filename}' does not exist.")

    reader, writer = __get_reader_writer(filename, output, width, fps_reduction, quality, dither, shit_optimize, text,
                                         text_style, progress_bar)

    try:
        p = Process(target=reader.read_video, args=())
        p.start()
        writer.write_video()
        p.join()
    except KeyboardInterrupt:
        p.terminate()


def gif2gif(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        quality: bool = False,
        dither: bool = False,
        shit_optimize: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        progress_bar: bool = False
) -> None:
    video2gif(filename, output, width, fps_reduction, quality, dither, shit_optimize, False, text, text_style,
              progress_bar)


def video2gif(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        quality: bool = False,
        dither: bool = False,
        shit_optimize: bool = False,
        is_ffmpeg: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        progress_bar: bool = False
) -> None:
    if is_ffmpeg:
        if not output:
            output = Utils.get_output_name(filename)
        video2video(filename, "temp", width, fps_reduction, quality, False, shit_optimize, text,
                    text_style, progress_bar)
        dither_type = DitherType.BAYER
        if quality:
            dither_type = DitherType.FLOYDSTEINBERG
        subprocess.call(f'ffmpeg -i temp.mp4 -vf "split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse=dither={dither_type.value}" -y {output}.gif', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if shit_optimize:
            Utils.shit_optimize(output)
        os.remove("temp.mp4")
        return

    if not os.path.exists(filename):
        raise FileDoesNotExistError(f"File '{filename}' does not exist.")

    reader, writer = __get_reader_writer(filename, output, width, fps_reduction, quality, dither, shit_optimize, text,
                                         text_style, progress_bar)

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
        dither: bool = False,
        shit_optimize: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        progress_bar: bool = False
) -> None:
    if not os.path.exists(filename):
        raise FileDoesNotExistError(f"File '{filename}' does not exist.")
    if filename[-4:] != ".gif":
        raise FileTypeError(f"File '{filename}' is not a gif.")

    reader, writer = __get_reader_writer(filename, output, width, fps_reduction, quality, dither, shit_optimize, text,
                                         text_style, progress_bar)

    try:
        p = Process(target=reader.read_video, args=())
        p.start()
        writer.write_video()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
