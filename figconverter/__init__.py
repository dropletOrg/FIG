from .reader import Reader
from .writer import Writer
from multiprocessing import Process
from typing import Optional


def video2gif(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        quality: int = 100,
        shit_optimize: bool = False,
        text: str = "",
        text_style: str = "top",
        progress_bar: bool = False
) -> None:
    params = {"filename": filename,
              "quality": quality,
              "output": output,
              "width": width,
              "shit_optimize": shit_optimize,
              "text": text,
              "text_style": text_style,
              "progress_bar": progress_bar
              }
    reader = Reader(params)
    params = reader.params
    writer = Writer(reader.frames, params)

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
    params = {"filename": filename,
              "quality": quality,
              "output": output,
              "width": width,
              "shit_optimize": shit_optimize,
              "text": text,
              "text_style": text_style,
              "progress_bar": progress_bar
              }
    reader = Reader(params)
    params = reader.params
    writer = Writer(reader.frames, params)

    p = Process(target=reader.read_video, args=())
    p.start()
    writer.write_video()
    p.join()
