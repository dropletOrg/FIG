from .reader import Reader
from .writer import Writer
from multiprocessing import Process
from typing import Optional


def video2gif(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        quality: int = 100,
        shit_optimize: bool = False,
        text: str = "",
        text_style: str = "top",
        progress_bar: bool = False
) -> None:
    reader = Reader(filename, output, width, quality, shit_optimize, text, text_style, progress_bar)
    writer = Writer(reader.frames, filename, output, shit_optimize, progress_bar)

    p = Process(target=reader.read_video, args=())
    p.start()
    writer.write_gif()
    p.join()


def gif2video(filename: str,
              output: Optional[str] = None,
              width: Optional[int] = None,
              quality: int = 100,
              shit_optimize: bool = False,
              text: str = "",
              text_style: str = "top",
              progress_bar: bool = False
) -> None:
    reader = Reader(filename, output, width, quality, shit_optimize, text, text_style, progress_bar)
    writer = Writer(reader.frames, filename, output, shit_optimize, progress_bar)

    p = Process(target=reader.read_video, args=())
    p.start()
    writer.write_video()
    p.join()
