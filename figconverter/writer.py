import tqdm
import imageio
import sys
from typing import Tuple, Optional
from .utils import Utils
import cv2
import os
from multiprocessing import Queue
import math


class Writer:
    def __init__(
            self,
            filename: str,
            frames: Queue,
            resolution: Tuple,
            output: Optional[str] = None,
            low_quality: bool = False,
            fps_reduction: int = 1,
            disable_dither: bool = False,
            shit_optimize=False,
            progress_bar: bool = False,
    ):
        self.filename = filename
        self.frames = frames
        self.resolution = resolution
        self.low_quality = low_quality
        self.output = output
        self.disable_dither = disable_dither
        self.shit_optimize = shit_optimize
        self.progress_bar = progress_bar

        data = Utils.get_video_data(self.filename)
        self.fps = data["fps"]
        self.frame_count = data["frame_count"]
        if 0 < fps_reduction <= self.fps:
            self.fps /= fps_reduction
            self.frame_count = math.ceil(self.frame_count / fps_reduction)

        if not self.output:
            self.output = Utils.get_output_name(self.filename)

    def write_gif(self) -> None:
        quantizer = 0
        if self.low_quality and self.disable_dither:
            quantizer = 2
        with imageio.get_writer(f"{self.output}.gif", mode='I', fps=self.fps, quantizer=quantizer) as writer:
            if self.progress_bar:
                pbar = tqdm.tqdm(total=self.frame_count, desc='Writing frames', position=1)
            for i in range(self.frame_count):
                frame = self.frames.get()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                writer.append_data(frame)
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
        writer = cv2.VideoWriter(f"{self.output}.mp4", fourcc, self.fps, self.resolution)

        if self.progress_bar:
            pbar = tqdm.tqdm(total=self.frame_count, desc='Writing frames', position=1)
        for i in range(self.frame_count):
            frame = self.frames.get()
            writer.write(frame)
            if self.progress_bar:
                pbar.update(1)
        if self.progress_bar:
            sys.stdout.write('\n')
            sys.stdout.flush()
            pbar.close()
        writer.release()
