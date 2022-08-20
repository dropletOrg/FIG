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

    read_thread = threading.Thread(target=reader.read_video)
    read_thread.start()
    writer.write_gif()


def gif2video(filename: str, progress_bar: bool = False) -> None:
    params = {"filename": filename,
              "progress_bar": progress_bar
              }
    reader = Reader(params)
    params = reader.params
    writer = Writer(reader.frames, params)

    read_thread = threading.Thread(target=reader.read_gif)
    read_thread.start()
    writer.write_video()
