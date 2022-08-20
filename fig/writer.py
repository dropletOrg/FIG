import tqdm
import imageio
import sys

from fig.utils import Utils


class Writer:
    def __init__(self, frames, params):
        self.frames = frames
        self.output = params["output"]
        self.fps = params["fps"]
        self.frame_count = params["frame_count"]
        self.params = params

        if self.output is None:
            self.output = "".join(params["filename"].split('.')[:-1])

    def write_gif(self):
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
            sys.stdout.write('\n')
            sys.stdout.flush()
            pbar.close()
        Utils.shitty_compression(self.output, self.params)

    def write_video(self):
        i = 0
        with imageio.get_writer(f"{self.output}.mp4", mode='I', fps=self.fps) as writer:
            if self.params['progress_bar']:
                pbar = tqdm.tqdm(total=self.frame_count, desc='Writing frames')
            while True:
                if self.frame_count == i:
                    break
                if self.frames:
                    writer.append_data(self.frames[0])
                    self.frames.pop(0)
                    i += 1
                    pbar.update(1)
            if self.params['progress_bar']:
                sys.stdout.write('\n')
                sys.stdout.flush()
                pbar.close()
        Utils.shitty_compression(self.output, self.params)