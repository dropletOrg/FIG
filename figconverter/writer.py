import tqdm
import imageio
import sys
from typing import List, Dict
from .utils import Utils
import cv2
import os
from multiprocessing import Queue


class Writer:
    def __init__(self, frames: Queue, params: Dict):
        self.frames = frames
        self.output = params["output"]
        self.fps = params["fps"]
        self.frame_count = params["frame_count"]
        self.params = params

        if self.output is None:
            self.output = "".join(os.path.basename(params["filename"]).split('.')[:-1])

    def write_gif(self) -> None:
        with imageio.get_writer(f"{self.output}.gif", mode='I', fps=self.fps) as writer:
            if self.params['progress_bar']:
                pbar = tqdm.tqdm(total=self.frame_count, desc='Writing frames', position=1)
            for i in range(self.frame_count):
                writer.append_data(self.frames.get())
                if self.params['progress_bar']:
                    pbar.update(1)
        if self.params['progress_bar']:
            sys.stdout.write('\n')
            sys.stdout.flush()
            pbar.close()
        Utils.shitty_compression(self.output, self.params)

    def write_video(self) -> None:
        while not self.frames:
            pass

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        size = self.params["resolution"]
        writer = cv2.VideoWriter(f"{self.output}.mp4", fourcc, self.fps, size)

        if self.params['progress_bar']:
            pbar = tqdm.tqdm(total=self.frame_count, desc='Writing frames', position=1)
        for i in range(self.frame_count):
            frame = self.frames.get()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            writer.write(frame)
            if self.params['progress_bar']:
                pbar.update(1)
        if self.params['progress_bar']:
            sys.stdout.write('\n')
            sys.stdout.flush()
            pbar.close()
        writer.release()
