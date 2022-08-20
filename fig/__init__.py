from .reader import Reader
from .writer import Writer
import threading


def video2gif(params):
    reader = Reader(params)
    params = reader.params
    writer = Writer(reader.frames, params)

    read_thread = threading.Thread(target=reader.read_video)
    read_thread.start()
    writer.write_gif()

def gif2video(params):
    reader = Reader(params)
    params = reader.params
    writer = Writer(reader.frames, params)

    read_thread = threading.Thread(target=reader.read_gif)
    read_thread.start()
    writer.write_video()
