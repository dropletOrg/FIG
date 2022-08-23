from tkinter import E
import tqdm
import imageio
import sys
from typing import Tuple, Optional
from .utils import Utils
import cv2
import os
from multiprocessing import Queue


class Writer:
    def __init__(
        self, 
        filename: str,
        frames: Queue,
        resolution: Tuple,
        output: Optional[str] = None, 
        shit_optimize = False, 
        progress_bar: bool = False
    ):
        self.filename = filename
        self.frames = frames
        self.resolution = resolution
        self.output = output
        self.shit_optimize = shit_optimize
        self.progress_bar = progress_bar

        data = Utils.get_video_data(self.filename)
        self.fps = data["fps"]
        self.frame_count = data["frame_count"]

        if self.output is None:
            self.output = "".join(os.path.basename(self.filename).split('.')[:-1])

    def write_gif(self) -> None:
        with imageio.get_writer(f"{self.output}.gif", mode='I', fps=self.fps) as writer:
            if self.progress_bar:
                pbar = tqdm.tqdm(total=self.frame_count, desc='Writing frames', position=1)
            for i in range(self.frame_count):
                writer.append_data(self.frames.get())
                if self.progress_bar:
                    pbar.update(1)
        if self.progress_bar:
            sys.stdout.write('\n')
            sys.stdout.flush()
            pbar.close()
        
        if self.shit_optimize: 
            Utils.shit_optimize(self.output)

    def write_video(self) -> None:
        while not self.frames:
            pass

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        size = self.resolution
        writer = cv2.VideoWriter(f"{self.output}.mp4", fourcc, self.fps, size)

        if self.progress_bar:
            pbar = tqdm.tqdm(total=self.frame_count, desc='Writing frames', position=1)
        for i in range(self.frame_count):
            frame = self.frames.get()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            writer.write(frame)
            if self.progress_bar:
                pbar.update(1)
        if self.progress_bar:
            sys.stdout.write('\n')
            sys.stdout.flush()
            pbar.close()
        writer.release()
