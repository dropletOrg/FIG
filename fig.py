import click
import figconverter
from figconverter.text_style import TextStyle


@click.version_option(figconverter.__version__, "-v", "--version")
@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-o', '--output', help='Output filename')
@click.option('-g2v', '--gif2video', default=False, is_flag=True,
              help='Convert a gif to a video (options: dithering, low-quality, shit-optimize, ffmpeg are disabled)')
@click.option('-w', '--width', help='Width of the gif (must be 16 or bigger)', type=int)
@click.option('-fr', '--fps-reduction', default=1,
              help="Divide fps by this number (must be bigger than 0 and can't be bigger than the original fps)",
              type=int)
@click.option('-lq', '--low-quality', is_flag=True, default=False, help='Prioritize speed and size over quality',
              show_default=True)
@click.option('-dd', '--disable-dither', is_flag=True, default=False,
              help='Disable dither to increase quality but cause color banding (disables low-quality)')
@click.option('-so', '--shit-optimize', default=False, is_flag=True,
              help='Optimize the gif but change it to 256 colors (requires gifsicle)')
@click.option('-f', '--ffmpeg', is_flag=True, default=False, show_default=True,
              help='Use ffmpeg for higher quality conversion (requires ffmpeg) (enables dithering)')
@click.option('-t', '--text', default="", help='Text to add to the gif')
@click.option('-ts', '--text-style', default=TextStyle.TOP.value,
              type=click.Choice([TextStyle.TOP.value, TextStyle.BOTTOM.value, TextStyle.CAPTION.value]),
              help='Style of text to add to the gif')
def main(filename, gif2video, output, width, fps_reduction, low_quality, disable_dither, shit_optimize, ffmpeg, text, text_style):
    if gif2video:
        if filename[-4:] != ".gif":
            raise click.BadParameter(f"File '{filename}' is not a gif.", param_hint='FILENAME')
        figconverter.gif2video(filename, output, width, fps_reduction, text, TextStyle(text_style), True)
        return

    figconverter.video2gif(filename, output, width, fps_reduction, low_quality, disable_dither, shit_optimize, ffmpeg,
                           text, TextStyle(text_style), True)


if __name__ == '__main__':
    main()
