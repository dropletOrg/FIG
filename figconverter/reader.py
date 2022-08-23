import cv2
from .utils import Utils
import tqdm
import imageio
import sys
from typing import Optional
from multiprocessing import Queue


class Reader:
    def __init__(
        self, 
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        quality: int = 100,
        shit_optimize: bool = False,
        text: str = "",
        text_style: str = "top",
        progress_bar: bool = False
    ):
        self.filename = filename
        self.output = output
        self.width = width
        self.quality = quality
        self.shit_optimize = shit_optimize
        self.text = text
        self.text_style = text_style
        self.progress_bar = progress_bar

        data = Utils.get_video_data(self.filename)
        self.frame_count = data['frame_count']
        self.resolution = data['resolution']

        self.text_overlay_image = Utils.create_text_overlay(self.resolution, text, width, text_style)

        self.frames = Queue(self.frame_count)

    def read_video(self) -> None:
        cap = cv2.VideoCapture(self.filename)
        if self.progress_bar:
            pbar = tqdm.tqdm(total=self.frame_count, desc='Reading and processing frames', position=0)
        while cap.isOpened():
            frame = cap.read()[1]
            if frame is not None:
                frame = Utils.morb_frame(  # process frames
                    frame, 
                    self.text_overlay_image, 
                    self.width, 
                    self.text, 
                    self.quality, 
                )
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert frame from BGR to RGB
                self.frames.put(frame)

                if self.progress_bar:
                    pbar.update(1)
            else:
                break
        if self.progress_bar:
            pbar.close()
            sys.stdout.write('\x1b[1A')
            sys.stdout.flush()
        cap.release()
