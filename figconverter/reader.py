import cv2
from .utils import Utils
import tqdm
import sys
from typing import Optional
from multiprocessing import Queue
import math
from .text_style import TextStyle


class Reader:
    def __init__(
        self, 
        filename: str,
        output: Optional[str] = None,
        width: Optional[int] = None,
        fps_reduction: int = 1,
        disable_dither: bool = False,
        shit_optimize: bool = False,
        text: str = "",
        text_style: TextStyle = TextStyle.TOP,
        progress_bar: bool = False
    ):
        self.filename = filename
        self.output = output
        self.width = width
        self.fps_reduction = fps_reduction
        self.disable_dither = disable_dither
        self.shit_optimize = shit_optimize
        self.text = text
        self.text_style = text_style
        self.progress_bar = progress_bar

        data = Utils.get_video_data(self.filename)
        self.frame_count = data['frame_count']
        self.resolution = data['resolution']

        if self.fps_reduction <= 0 or self.fps_reduction > data["fps"]:
            self.fps_reduction = 1
        self.frame_count = math.ceil(self.frame_count / self.fps_reduction)

        self.text_overlay_image = Utils.create_text_overlay(self.resolution, text, width, text_style)
        self.resolution = self.text_overlay_image[2][0]

        self.frames = Queue(self.frame_count)

    def read_video(self) -> None:
        cap = cv2.VideoCapture(self.filename)
        if self.progress_bar:
            pbar = tqdm.tqdm(total=self.frame_count, desc='Reading and processing frames', position=0)
        i = -1
        while cap.isOpened():
            frame = cap.read()[1]
            if frame is not None:
                i += 1
                if i % self.fps_reduction != 0:
                    continue

                frame = Utils.morb_frame(  # process frames
                    frame, 
                    self.text_overlay_image, 
                    self.width, 
                    self.text,
                    self.disable_dither
                )

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

        return
