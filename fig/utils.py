import random
import click
import importlib.resources as pkg_resources
from typing import Dict, Tuple, Optional
import cv2
import more_itertools
import numpy as np
import requests
import tldextract
import yt_dlp
from PIL import ImageFont, ImageDraw, Image
from pygifsicle import gifsicle
import os
import datetime
import art
import fig
from .text_style import TextStyle
from .yt_dlp_filename_collector import FilenameCollectorPP


def show_logo() -> None:
    motd = ["It's pronounced GIF",
            '"Stop misquoting me"\n -Albert Einstein',
            '"A delayed game is eventually bad, but a rushed game is forever bad. I hate games."\n -Shigeru Miyamoto',
            '"I am a fig"\n -fig',
            '"I am become fig, destroyer of ezgif.com"\n -J. Robert Oppenheimer',
            '"That’s what the kids call "epic fail""\n -Saul Goodman',
            '"Waltuh, put your dick away Waltuh. I’m not having sex with you right now."\n -Finger',
            '"You should kill yourself, NOW"\n -Dalauan Sparrow',
            "Fun Fact: Figs are very moist",
            '"That means that as a human being you should have a right to water. That’s an extreme solution."\n -Peter Brabeck-Letmathe',
            '"We will coup whoever we want! Deal with it."\n -Elon Musk',
            ]

    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'bright_red', 'bright_green', 'bright_yellow',
              'bright_blue', 'bright_magenta', 'bright_cyan']

    fig_font = art.text2art("FIG", "random")
    centered_fig_font = []
    for i in fig_font.split("\n"):
        centered_fig_font.append(i.center(40))
    centered_fig_font = "\n".join(centered_fig_font)
    logo_color = random.choice(colors)
    colors.remove(logo_color)
    click.secho(centered_fig_font, fg='bright_blue')
    click.echo(pkg_resources.read_text(__package__, "logo_ascii_art.txt"))
    click.secho(f"{random.choice(motd)}\n", fg=random.choice(colors))


def get_output_name(filename: str) -> str:
    return "".join(os.path.basename(filename).split('.')[:-1])


def get_video_data(filename: str) -> Dict:
    cap = cv2.VideoCapture(filename)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    cap.release()

    return {'fps': fps, 'frame_count': frame_count, 'resolution': resolution}


def create_text_overlay(
        resolution: Tuple,
        text: str,
        width: Optional[int] = None,
        text_style: TextStyle = TextStyle.TOP
) -> Optional[Tuple]:
    frame = np.zeros((resolution[1], resolution[0], 3), np.uint8)

    if width:
        frame = resize_frame(frame, width)

    if text == "":
        return frame, text_style, ((frame.shape[1], frame.shape[0]),)

    if text == "":
        return frame, (frame.shape[1], frame.shape[0])

    frame = Image.new('RGBA', (frame.shape[1], frame.shape[0]), (0, 0, 0, 0))
    size, text = __calculate_font_size(frame, text)
    font = ImageFont.truetype("impact.ttf", size)
    draw = ImageDraw.Draw(frame)

    x = frame.size[0] // 2 - draw.textsize(text, font=font)[0] // 2
    y = frame.size[1] // 20
    font = ImageFont.truetype("impact.ttf", size)

    if text_style == TextStyle.CAPTION:
        top_margin = draw.textsize(text, font=font)[1] + y * 2
        new_resolution = (frame.width, frame.height + top_margin)
        new_frame = Image.new("RGB", new_resolution, (255, 255, 255))
        new_frame.paste(frame, (0, top_margin))
        frame = new_frame
        draw = ImageDraw.Draw(frame)
        draw.text((x, y // 2), text, font=font, fill=(0, 0, 0))
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


def cv22pil(frame: np.ndarray) -> Image.Image:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame)


def pil2cv2(pil_image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def morb_frame(
        frame: np.ndarray,
        text_overlay_image: Optional[Image.Image],
        width: Optional[int] = None,
        text: str = "",
        disable_dither: bool = False,
) -> np.ndarray:
    if width:
        frame = resize_frame(frame, width)
    if text != "":
        frame = caption_video(frame, text_overlay_image)
    if not disable_dither:
        frame = quantize_dither_frame(frame)
    return frame


def quantize_dither_frame(frame: np.ndarray) -> np.ndarray:
    frame = cv22pil(frame)
    frame = frame.convert('P', colors=256, palette=Image.Palette.WEB, dither=Image.Dither.FLOYDSTEINBERG)
    frame = frame.convert("RGB")
    frame = pil2cv2(frame)
    return frame


def shit_optimize(filename: str) -> None:
    gifsicle(sources=f"{filename}.gif", optimize=True, colors=256)


def resize_frame(frame: np.ndarray, width: int) -> np.ndarray:
    if width < 16:
        return frame
    return cv2.resize(frame, (width, frame.shape[0] * width // frame.shape[1]))


def caption_video(frame: np.ndarray, text_overlay_image: Image.Image) -> np.ndarray:
    return __overlay_text(frame, text_overlay_image)


def __calculate_font_size(frame: Image.Image, text: str = "", depth: int = 0) -> Tuple[int, str]:
    min_size = frame.size[0] // 32
    max_size = frame.size[0] // 16
    max_text_size = frame.size[0] - max_size

    giant_ass_font = ImageFont.truetype("impact.ttf", 10000)
    draw = ImageDraw.Draw(frame)
    size = 10000 * max_text_size // draw.textsize(text, font=giant_ass_font)[0]
    if size < min_size:
        new_text = text.replace("\n", "").split(" ")
        new_text = [list(x)
                    for x in more_itertools.divide(depth + 2, new_text)]
        new_text = " \n".join(" ".join(x) for x in new_text)
        size, text = __calculate_font_size(
            frame, new_text, depth + 1)
    elif size > max_size:
        size = max_size

    return size, text


def __overlay_text(frame: np.ndarray, text_overlay_image: Image.Image) -> np.ndarray:
    frame = cv22pil(frame)
    text_style = text_overlay_image[1]
    if text_style == TextStyle.CAPTION:
        top_margin = text_overlay_image[2][1]
        text_overlay_image[0].paste(frame, (0, top_margin))
        frame = text_overlay_image[0]
        return pil2cv2(frame)
    frame.paste(text_overlay_image[0], (0, 0), text_overlay_image[0])
    return pil2cv2(frame)


def download_video(url: str, filename: str) -> None:
    content_type = requests.head(url).headers.get("content-type")
    if content_type.split('/')[0] != "video":
        raise fig.FileTypeError("File in url is not a video")
    with open(f"{filename}", "wb") as f:
        f.write(requests.get(url).content)


def download_youtube(search: str, filename: str, verbose: bool = False) -> None:
    filename_collector = FilenameCollectorPP()
    with yt_dlp.YoutubeDL({'quiet': True, 'default_search': 'auto', 'outtmpl': filename, 'noprogress': True}) as ydl:
        if verbose:
            info_dict = ydl.extract_info(search, download=False)
            if 'entries' in info_dict:
                if info_dict['entries']:
                    title = info_dict['entries'][0]['title']
                    duration = info_dict['entries'][0]['duration']
                else:
                    raise fig.NoResults("No results found")
            else:
                title = info_dict['title']
                duration = info_dict['duration']
            click.secho(f"Downloading {title}, Duration {datetime.timedelta(seconds=duration)}", fg="yellow")
        ydl.add_post_processor(filename_collector)
        ydl.download(search)
    if not filename_collector.filenames:
        raise fig.NoResults("No results found")
    if os.path.isfile(filename):
        os.remove(filename)
    os.rename(filename_collector.filenames[0], filename)


def download_tenor_search(search: str, filename: str, api_key: str, client_key: str) -> None:
    r = requests.get(
        f"https://tenor.googleapis.com/v2/search?q={search}&key={api_key}&client_key={client_key}&limit=1&media_filter=mp4")
    if r.status_code == 200:
        r = r.json()
        if r["results"]:
            download_video(r['results'][0]['media_formats']['mp4']['url'], filename)
            return
    raise fig.NoResults("No results found")


def download_tenor_url(url: str, filename: str, api_key: str, client_key: str) -> None:
    r = requests.get(
        f"https://tenor.googleapis.com/v2/posts?ids={url.split('-')[-1]}&key={api_key}&client_keys={client_key}&limit=1&media_filter=mp4")
    if r.status_code == 200:
        r = r.json()
        if r["results"]:
            download_video(r['results'][0]['media_formats']['mp4']['url'], filename)


def download(search: str, output: str, service: str, api_key: str, client_key: str, verbose) -> None:
    if service == "tenor":
        if tldextract.extract(search).domain == "tenor":
            download_tenor_url(search, output, api_key, client_key)
        else:
            download_tenor_search(search, output, api_key, client_key)
    elif service == "youtube":
        download_youtube(search, output, verbose)
    else:
        download_video(search, output)
