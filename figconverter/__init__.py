from .reader import Reader
from .writer import Writer
import threading
from typing import Optional


def video2gif(
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        quality: int = 100,
        shit_optimize: bool = False,
        keep_width: bool = False,
        text: str = "",
        text_style: str = "top",
        progress_bar: bool = False
) -> None:

    params = {"filename": filename,
              "quality": quality,
              "output": output,
              "width": width,
              "shit_optimize": shit_optimize,
              "keep_width": keep_width,
              "text": text,
              "text_style": text_style,
              "progress_bar": progress_bar
              }
    reader = Reader(params)
    params = reader.params
    writer = Writer(reader.frames, params)

    reader.read_video()
    writer.write_gif()


def gif2video(filename: str, output: Optional[str] = None, progress_bar: bool = False) -> None:
    params = {  
        "filename": filename,
        "output": output,
        "progress_bar": progress_bar
    }
    reader = Reader(params)
    params = reader.params
    writer = Writer(reader.frames, params)

    reader.read_gif()
    writer.write_video()
