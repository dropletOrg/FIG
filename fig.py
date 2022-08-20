import click
import sys
import cv2
import fig
from fig.utils import Utils
from fig.enum import TextOverlay


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-q', '--quality', default=100, help='Quality of the gif', show_default=True, type=click.IntRange(0, 100))
@click.option('-o', '--output', help='Output filename')
@click.option('-w', '--width', help='Width of the gif', show_default=True, type=click.IntRange(1, sys.maxsize))
@click.option('-so', '--shit-optimize', default=False, is_flag=True, help='Optimize the gif but change it to 8 bit')
@click.option('-kw', '--keep-width', default=False, is_flag=True, help='Keep the width of the gif')
@click.option('-c', '--caption', default="", help='Caption to add to the gif')
@click.option('-ct', '--caption-type', default=TextOverlay.TOP.value, type=click.Choice([TextOverlay.TOP.value, TextOverlay.BOTTOM.value, TextOverlay.CAPTION.value]), help='Type of caption to add to the gif')
@click.option('-g2v', '--gif2video', default=False, is_flag=True, help='Convert gif to video')
def main(filename, quality, output, width, shit_optimize, keep_width, caption, caption_type, gif2video):
    params = {"filename": filename,
              "quality": quality,
              "output": output,
              "width": width,
              "shit_optimize": shit_optimize,
              "keep_width": keep_width,
              "caption": caption,
              "caption_type": caption_type,
              "progress_bar": True
              }
    if gif2video:
        fig.gif2video(params)
        return
    fig.video2gif(params)


if __name__ == '__main__':
    main()
