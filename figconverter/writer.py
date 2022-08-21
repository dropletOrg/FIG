import tqdm
import imageio
import sys
from typing import List, Dict
from .utils import Utils
import cv2
import os


class Writer:
    def __init__(self, frames: List, params: Dict):
        self.frames = frames
        self.output = params["output"]
        self.fps = params["fps"]
        self.frame_count = params["frame_count"]
        self.params = params

        if self.output is None:
            self.output = "".join(os.path.basename(params["filename"]).split('.')[:-1])

    def write_gif(self) -> None:
        i = 0
        with imageio.get_writer(f"{self.output}.gif", mode='I', fps=self.fps) as writer:
            if self.params['progress_bar']:
                pbar = tqdm.tqdm(total=self.frame_count, desc='Writing frames')
            while True:
                if self.frame_count == i:
                    break
                if self.frames:
                    writer.append_data(self.frames[0])
                    self.frames.pop(0)
                    i += 1
                    if self.params['progress_bar']:
                        pbar.update(1)
        if self.params['progress_bar']:
            pbar.close()
        Utils.shitty_compression(self.output, self.params)

    def write_video(self) -> None:
        while not self.frames:
            pass

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        size = (self.frames[0].shape[1], self.frames[0].shape[0])
        writer = cv2.VideoWriter(f"{self.output}.mp4", fourcc, self.fps, size)

        i = 0
        if self.params['progress_bar']:
            pbar = tqdm.tqdm(total=self.frame_count, desc='Writing frames')
        while True:
            if self.frame_count == i:
                break
            if self.frames:
                frame = self.frames[0]
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                writer.write(frame)
                self.frames.pop(0)
                i += 1
                pbar.update(1)
        if self.params['progress_bar']:
            pbar.close()
        writer.release()