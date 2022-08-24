import click
import sys
import figconverter
from figconverter.textstyle import TextStyle

@click.version_option(figconverter.__version__, "-v", "--version")
@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-g2v', '--gif2video', default=False, is_flag=True, help='Convert a gif to a video')
@click.option('-q', '--quality', is_flag=True, default=False, help='priorotize quality over speed and size', show_default=True)
@click.option('-o', '--output', help='Output filename')
@click.option('-w', '--width', help='Width of the gif (must be 16 or bigger)', type=int)
@click.option('-fr', '--fps-reduction', default=1, help="devide fps by thiss number (must be bigger than 0 and can't be bigger than the original fps)", type=int)
@click.option('-d', '--dither', is_flag=True, default=False, help='Apply dither to increase quality increase quality')
@click.option('-so', '--shit-optimize', default=False, is_flag=True, help='Optimize the gif but change it to 256 colors (requires gifsicle)')
@click.option('-t', '--text', default="", help='Text to add to the gif')
@click.option('-ts', '--text-style', default=TextStyle.TOP.value, type=click.Choice([TextStyle.TOP.value, TextStyle.BOTTOM.value, TextStyle.CAPTION.value]), help='Style of text to add to the gif')
def main(filename, gif2video, quality, output, width, fps_reduction, dither, shit_optimize, text, text_style):
    if gif2video:
        if filename[-4:] != ".gif":
            raise click.BadParameter(f"File '{filename}' is not a gif.", param_hint='FILENAME')
        figconverter.gif2video(filename, output, width, fps_reduction, quality, dither, shit_optimize, text, TextStyle(text_style), True)
        return

    figconverter.video2gif(filename, output, width, fps_reduction, quality, dither, shit_optimize, text, TextStyle(text_style), True)


if __name__ == '__main__':
    main()
