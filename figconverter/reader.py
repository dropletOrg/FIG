import cv2
from .utils import Utils
import tqdm
import imageio
import sys
from typing import Dict
from multiprocessing import Queue


class Reader:
    def __init__(self, params: Dict):
        self.filename = params["filename"]
        self.params = params
        data = Utils.get_video_data(self.filename)
        self.fps = data['fps']
        self.frame_count = data['frame_count']
        self.resolution = data['resolution']
        self.text_overlay_image = Utils.create_text_overlay(self.resolution, self.params)
        self.params["frame_count"] = self.frame_count
        self.params["fps"] = self.fps
        self.params["resolution"] = self.text_overlay_image[-1]
        self.frames = Queue(self.frame_count)

    def read_video(self) -> None:
        cap = cv2.VideoCapture(self.filename)
        if self.params['progress_bar']:
            pbar = tqdm.tqdm(total=self.frame_count, desc='Reading and processing frames', position=0)
        while cap.isOpened():
            frame = cap.read()[1]
            if frame is not None:
                frame = Utils.morb_frame(frame, self.params, self.text_overlay_image)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frames.put(frame)
                if self.params['progress_bar']:
                    pbar.update(1)
            else:
                break
        if self.params['progress_bar']:
            pbar.close()
            sys.stdout.write('\x1b[1A')
            sys.stdout.flush()
        cap.release()
