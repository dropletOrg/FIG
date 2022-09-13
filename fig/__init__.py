from .reader import Reader
from .writer import Writer
from .text_style import TextStyle
from multiprocessing import Process
from typing import Optional, Tuple
import os
import fig.utils
import subprocess
import click

__version__ = "2.9.5"


class FileTypeError(Exception):
    pass


class FileDoesNotExistError(Exception):
    pass


class NoResults(Exception):
    pass


def __get_reader_writer(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        low_quality: bool = False,
        disable_dither: bool = False,
        shit_optimize: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        verbose: bool = False
) -> Tuple[Reader, Writer]:
    reader = Reader(filename, output, width, fps_reduction, disable_dither, shit_optimize, text, text_style,
                    verbose)
    writer = Writer(filename, reader.frames, reader.resolution, output, low_quality, fps_reduction, disable_dither,
                    shit_optimize,
                    verbose)
    return reader, writer


def download2gif(
        search: str,
        service: str = "tenor",
        output: Optional[str] = None,
        api_key: Optional[str] = "AIzaSyC3EOB__h0pNIWlPTh8MaunVK4McfErjfo",
        width: Optional[int] = None,
        fps_reduction: int = 1,
        low_quality: bool = False,
        disable_dither: bool = False,
        shit_optimize: bool = False,
        is_ffmpeg: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        verbose: bool = False
) -> None:
    if output is None:
        output = search
    if verbose:
        click.echo("Downloading gif...")
    fig.utils.download(search, "temp", service, api_key, "fig")
    video2gif("temp", output, width, fps_reduction, low_quality, disable_dither, shit_optimize, is_ffmpeg, text, text_style, verbose)
    os.remove("temp")


def download2video(
        search: str,
        service: str = "tenor",
        output: Optional[str] = None,
        api_key: Optional[str] = "AIzaSyC3EOB__h0pNIWlPTh8MaunVK4McfErjfo",
        width: Optional[int] = None,
        fps_reduction: int = 1,
        low_quality: bool = False,
        disable_dither: bool = True,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        verbose: bool = False
) -> None:
    if output is None:
        output = search
    if verbose:
        click.echo("Downloading gif...")
    fig.utils.download(search, "temp", service, api_key, "fig")
    video2video("temp", output, width, fps_reduction, low_quality, disable_dither, text, text_style, verbose)
    os.remove("temp")


def video2video(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        low_quality: bool = False,
        disable_dither: bool = True,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        verbose: bool = False
) -> None:
    if not os.path.exists(filename):
        raise FileDoesNotExistError(f"File '{filename}' does not exist.")

    reader, writer = __get_reader_writer(filename, output, width, fps_reduction, low_quality, disable_dither,
                                         False, text,
                                         text_style, verbose)

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
        low_quality: bool = False,
        disable_dither: bool = False,
        shit_optimize: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        verbose: bool = False
) -> None:
    video2gif(filename, output, width, fps_reduction, low_quality, disable_dither, shit_optimize, False, text,
              text_style,
              verbose)


def video2gif(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        low_quality: bool = False,
        disable_dither: bool = False,
        shit_optimize: bool = False,
        is_ffmpeg: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        verbose: bool = False
) -> None:
    if is_ffmpeg:
        if not output:
            output = fig.utils.get_output_name(filename)

        video2video(filename, "temp", width, fps_reduction, low_quality, True, text,
                    text_style, verbose)

        command = f'ffmpeg -i temp.mp4 -y {output}.gif'
        if not low_quality:
            command = f'ffmpeg -i temp.mp4 -vf "split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse=dither=floyd_steinberg" -y "{output}.gif"'
        if verbose:
            click.echo("Converting video to gif...")
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if shit_optimize:
            if verbose:
                click.echo("Optimizing gif...")
            fig.utils.shit_optimize(output)

        os.remove("temp.mp4")
        return

    if not os.path.exists(filename):
        raise FileDoesNotExistError(f"File '{filename}' does not exist.")

    reader, writer = __get_reader_writer(filename, output, width, fps_reduction, low_quality, disable_dither,
                                         shit_optimize, text,
                                         text_style, verbose)

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
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        verbose: bool = False
) -> None:
    if not os.path.exists(filename):
        raise FileDoesNotExistError(f"File '{filename}' does not exist.")
    if filename[-4:] != ".gif":
        raise FileTypeError(f"File '{filename}' is not a gif.")

    reader, writer = __get_reader_writer(filename, output, width, fps_reduction, False, True, False, text,
                                         text_style, verbose)

    try:
        p = Process(target=reader.read_video, args=())
        p.start()
        writer.write_video()
        p.join()
    except KeyboardInterrupt:
        p.terminate()
