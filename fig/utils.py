import cv2
import numpy as np
from pygifsicle import gifsicle
from PIL import ImageFont, ImageDraw, Image
import more_itertools
from .enum import TextOverlay

class Utils(object):
    @staticmethod
    def get_video_data(cap):
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return {'fps': fps, 'frame_count': frame_count}

    @staticmethod
    def create_text_overlay(cap, caption, params):
        if caption == "":
            return

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame = np.zeros((height, width, 3), np.uint8)

        if not params["keep_width"]:
            frame = Utils.resize_frame(frame, params["width"])

        frame = Image.new('RGBA', (frame.shape[1], frame.shape[0]), (0, 0, 0, 0))
        size, caption = Utils.__calculate_font_size(frame, caption)
        font = ImageFont.truetype("impact.ttf", size)
        draw = ImageDraw.Draw(frame)

        x = frame.size[0]//2 - draw.textsize(caption, font=font)[0]//2
        y = frame.size[1] // 20
        font = ImageFont.truetype("impact.ttf", size)

        if params['caption_type'] == TextOverlay.CAPTION.value:
            top_margin = draw.textsize(caption, font=font)[1] + y
            new_frame = Image.new(frame.mode, (frame.width, frame.height + top_margin), (255, 255, 255))
            new_frame.paste(frame, (0, top_margin))
            frame = new_frame
            draw = ImageDraw.Draw(frame)
            draw.text((x, 0), caption, font=font, fill=(0, 0, 0))
            return new_frame, frame, top_margin

        if params['caption_type'] == TextOverlay.BOTTOM.value:
            y = frame.size[1] - y - draw.textsize(caption, font=font)[1]

        offset = size * 3 // 80

        draw.text((x - offset - 1, y - offset - 1), caption, font=font, fill=(0, 0, 0))
        draw.text((x + offset + 1, y - offset - 1), caption, font=font, fill=(0, 0, 0))
        draw.text((x - offset - 1, y + offset + 1), caption, font=font, fill=(0, 0, 0))
        draw.text((x + offset + 1, y + offset + 1), caption, font=font, fill=(0, 0, 0))

        draw.text((x, y), caption, font=font, fill=(255, 255, 255))
        return frame

    @staticmethod
    def cv22pil(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(frame)

    @staticmethod
    def pil2cv2(pil_image):
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    @staticmethod
    def shitty_compression(filename, params):
        if params["shit_optimize"]:
            gifsicle(sources=f"{filename}.gif", optimize=True, colors=256)

    @staticmethod
    def morb_frame(frame, params, text_overlay_image):
        if not params["keep_width"]:
            frame = Utils.resize_frame(frame, params["width"])
        frame = Utils.caption_video(frame, params, text_overlay_image)
        if params["quality"] != 100:
            frame = Utils.compress_frame(frame, params["quality"])
        return frame


    @staticmethod
    def compress_frame(frame, quality):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encframe = cv2.imencode('.jpg', frame, encode_param)
        return cv2.imdecode(encframe, 1)

    @staticmethod
    def resize_frame(frame, width):
        if (frame.shape[1] > 480) and (not width):
            return cv2.resize(frame, (480, frame.shape[0] * 480 // frame.shape[1]))
        elif width:
            return cv2.resize(frame, (width, frame.shape[0] * width // frame.shape[1]))
        return frame

    @staticmethod
    def caption_video(frame, params, text_overlay_image):
        if params['caption'] == "":
            return frame
        return Utils.__overlay_text(frame, text_overlay_image, params['caption_type'])

    @staticmethod
    def __calculate_font_size(frame, caption, depth=0):
        min_size = frame.size[0] // 32
        max_size = frame.size[0] // 16
        max_text_size = frame.size[0] - max_size

        giant_ass_font = ImageFont.truetype("impact.ttf", 10000)
        draw = ImageDraw.Draw(frame)
        size = 10000 * max_text_size // draw.textsize(caption, font=giant_ass_font)[0]
        if size < min_size:
            new_caption = caption.replace("\n", "").split(" ")
            new_caption = [list(x) for x in more_itertools.divide(depth + 2, new_caption)]
            new_caption = " \n".join(" ".join(x) for x in new_caption)
            size, caption = Utils.__calculate_font_size(frame, new_caption, depth+1)
        elif size > max_size:
            size = max_size

        return size, caption

    @staticmethod
    def __overlay_text(frame, text_overlay_image, caption_type):
        frame = Utils.cv22pil(frame)
        if caption_type == TextOverlay.CAPTION.value:
            text_overlay_image[0].paste(frame, (0, text_overlay_image[2]))
            frame = text_overlay_image[0]
            text_overlay_image = text_overlay_image[1]
        frame.paste(text_overlay_image, (0, 0), text_overlay_image)
        return Utils.pil2cv2(frame)
