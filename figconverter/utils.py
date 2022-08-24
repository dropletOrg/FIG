import fractions
import cv2
import numpy as np
from pygifsicle import gifsicle
from PIL import ImageFont, ImageDraw, Image
import more_itertools
from .textstyle import TextStyle
from typing import Dict, Tuple, Optional


class Utils(object):
    @staticmethod
    def get_video_data(filename: str) -> Dict:
        cap = cv2.VideoCapture(filename)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        cap.release()

        return {'fps': fps, 'frame_count': frame_count, 'resolution': resolution}

    @staticmethod
    def create_text_overlay(
        resolution: Tuple,
        text: str,
        width: Optional[int] = None,
        text_style: TextStyle = TextStyle.TOP
    ) -> Optional[Tuple]:
    
        frame = np.zeros((resolution[1], resolution[0], 3), np.uint8)

        if width:
            frame = Utils.resize_frame(frame, width)

        if text == "":
            return frame, text_style, ((frame.shape[1], frame.shape[0]),)

        if text == "":
            return frame, (frame.shape[1], frame.shape[0])

        frame = Image.new('RGBA', (frame.shape[1], frame.shape[0]), (0, 0, 0, 0))
        size, text = Utils.__calculate_font_size(frame, text)
        font = ImageFont.truetype("impact.ttf", size)
        draw = ImageDraw.Draw(frame)

        x = frame.size[0] // 2 - draw.textsize(text, font=font)[0] // 2
        y = frame.size[1] // 20
        font = ImageFont.truetype("impact.ttf", size)

        if text_style == TextStyle.CAPTION:
            top_margin = draw.textsize(text, font=font)[1] + y*2
            new_resolution = (frame.width, frame.height + top_margin)
            new_frame = Image.new(frame.mode, new_resolution, (255, 255, 255))
            new_frame.paste(frame, (0, top_margin))
            frame = new_frame
            draw = ImageDraw.Draw(frame)
            draw.text((x, y//2), text, font=font, fill=(0, 0, 0))
            return frame, text_style, (new_resolution, top_margin)

        if text_style == TextStyle.BOTTOM:
            y = frame.size[1] - y - draw.textsize(text, font=font)[1]

        offset = size * 3 // 80

        draw.text((x - offset - 1, y - offset - 1),
                  text, font=font, fill=(0, 0, 0))
        draw.text((x + offset + 1, y - offset - 1),
                  text, font=font, fill=(0, 0, 0))
        draw.text((x - offset - 1, y + offset + 1),
                  text, font=font, fill=(0, 0, 0))
        draw.text((x + offset + 1, y + offset + 1),
                  text, font=font, fill=(0, 0, 0))

        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        new_resolution = (frame.width, frame.height)
        return frame, text_style, (new_resolution,)

    @staticmethod
    def cv22pil(frame: np.ndarray) -> Image.Image:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(frame)

    @staticmethod
    def pil2cv2(pil_image: Image.Image) -> np.ndarray:
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    @staticmethod
    def morb_frame(
        frame: np.ndarray,
        text_overlay_image: Optional[Image.Image],
        width: Optional[int] = None,
        text: str = "",
        dither: bool = False,
    ) -> np.ndarray:

        if width:
            frame = Utils.resize_frame(frame, width)
        if text != "":
            frame = Utils.caption_video(frame, text_overlay_image)
        if dither:
            frame = Utils.quantize_dither_frame(frame)
        return frame

    @staticmethod
    def quantize_dither_frame(frame: np.ndarray) -> np.ndarray:
        frame = Utils.cv22pil(frame)
        frame = frame.convert('P', colors=256, palette=Image.Palette.WEB, dither=Image.Dither.FLOYDSTEINBERG)
        frame = frame.convert("RGB")
        frame = Utils.pil2cv2(frame)
        return frame
                
    
    @staticmethod
    def shit_optimize(filename: str) -> None:
        gifsicle(sources=f"{filename}.gif", optimize=True, colors=256)

    @staticmethod
    def resize_frame(frame: np.ndarray, width: int) -> np.ndarray:
        if width < 16:
            return frame
        return cv2.resize(frame, (width, frame.shape[0] * width // frame.shape[1]))

    @staticmethod
    def caption_video(frame: np.ndarray, text_overlay_image: Image.Image) -> np.ndarray:
        return Utils.__overlay_text(frame, text_overlay_image)

    @staticmethod
    def __calculate_font_size(frame: Image.Image, text: str = "", depth: int = 0) -> Tuple[int, str]:
        min_size = frame.size[0] // 32
        max_size = frame.size[0] // 16
        max_text_size = frame.size[0] - max_size

        giant_ass_font = ImageFont.truetype("impact.ttf", 10000)
        draw = ImageDraw.Draw(frame)
        size = 10000 * \
            max_text_size // draw.textsize(text, font=giant_ass_font)[0]
        if size < min_size:
            new_text = text.replace("\n", "").split(" ")
            new_text = [list(x)
                        for x in more_itertools.divide(depth + 2, new_text)]
            new_text = " \n".join(" ".join(x) for x in new_text)
            size, text = Utils.__calculate_font_size(
                frame, new_text, depth + 1)
        elif size > max_size:
            size = max_size

        return size, text

    @staticmethod
    def __overlay_text(frame: np.ndarray, text_overlay_image: Image.Image) -> np.ndarray:
        frame = Utils.cv22pil(frame)
        text_style = text_overlay_image[1]
        if text_style == TextStyle.CAPTION:
            top_margin = text_overlay_image[2][1]
            text_overlay_image[0].paste(frame, (0, top_margin))
            frame = text_overlay_image[0]
            return Utils.pil2cv2(frame)
        frame.paste(text_overlay_image[0], (0, 0), text_overlay_image[0])
        return Utils.pil2cv2(frame)
