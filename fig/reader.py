import cv2
from fig.utils import Utils
import tqdm
import imageio
import sys
from typing import Dict


class Reader:
    def __init__(self, params: Dict):
        self.filename = params["filename"]
        self.params = params
        self.frames = []

        self.cap = cv2.VideoCapture(self.filename)
        data = Utils.get_video_data(self.cap)
        self.fps = data['fps']
        self.frame_count = data['frame_count']
        self.params["frame_count"] = self.frame_count
        self.params["fps"] = self.fps

        self.text_overlay_image = Utils.create_text_overlay(self.cap, self.params)

    def read_video(self) -> None:
        if self.params['progress_bar']:
            pbar = tqdm.tqdm(total=self.frame_count, desc='Reading and processing frames')
        while self.cap.isOpened():
            frame = self.cap.read()[1]
            if frame is not None:
                frame = Utils.morb_frame(frame, self.params, self.text_overlay_image)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frames.append(frame)
                if self.params['progress_bar']:
                    pbar.update(1)
            else:
                break
        if self.params['progress_bar']:
            pbar.close()
            sys.stdout.write('\x1b[1A')
            sys.stdout.flush()
        self.cap.release()

    def read_gif(self) -> None:
        with imageio.get_reader(self.filename) as reader:
            if self.params['progress_bar']:
                pbar = tqdm.tqdm(total=reader.get_length(), desc='Reading frames')
            for i, frame in enumerate(reader):
                if i == self.frame_count:
                    break
                self.frames.append(frame)
                if self.params['progress_bar']:
                    pbar.update(1)
            if self.params['progress_bar']:
                pbar.close()
                sys.stdout.write('\x1b[1A')
                sys.stdout.flush()
