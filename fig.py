import click
import sys
import figconverter
from figconverter.enum import TextOverlay


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-q', '--quality', default=100, help='Quality of the gif (applies jpeg lossy compression to the gif, 100 - no compression, 0 - shitloads of compression)', show_default=True, type=click.IntRange(0, 100))
@click.option('-o', '--output', help='Output filename')
@click.option('-w', '--width', help='Width of the gif', show_default=True, type=click.IntRange(1, sys.maxsize))
@click.option('-so', '--shit-optimize', default=False, is_flag=True, help='Optimize the gif but change it to 256 colors (requires gifsicle)')
@click.option('-kw', '--keep-width', default=False, is_flag=True, help='Keep the width of the gif')
@click.option('-t', '--text', default="", help='Text to add to the gif')
@click.option('-ts', '--text-style', default=TextOverlay.TOP.value, type=click.Choice([TextOverlay.TOP.value, TextOverlay.BOTTOM.value, TextOverlay.CAPTION.value]), help='Style of text to add to the gif')
@click.option('-g2v', '--gif2video', default=False, is_flag=True, help='Convert a gif to video (other options are ignored)')
def main(filename, quality, output, width, shit_optimize, keep_width, text, text_style, gif2video):
    if gif2video:
        figconverter.gif2video(filename, True)
        return
    figconverter.video2gif(filename, output, width, quality, shit_optimize, keep_width, text, text_style, True)


if __name__ == '__main__':
    main()
