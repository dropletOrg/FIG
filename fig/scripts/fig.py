import click
import fig
from fig.text_style import TextStyle
import random
import importlib.resources as pkg_resources

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


@click.version_option(fig.__version__, "-v", "--version")
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
def main(filename, gif2video, output, width, fps_reduction, low_quality, disable_dither, shit_optimize, ffmpeg, text,
         text_style):
    fig_font = pkg_resources.read_text(__package__, "fig_ascii_font.txt")
    centered_fig_font = []
    for i in fig_font.split("\n"):
        centered_fig_font.append(i.center(40))
    centered_fig_font = "\n".join(centered_fig_font)
    click.secho(centered_fig_font, fg='bright_blue')
    click.echo(pkg_resources.read_text(__package__, "logo_ascii_art.txt"))
    click.secho(f"{random.choice(motd)}\n", fg=random.choice(['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta', 'bright_cyan']))
    if gif2video:
        if filename[-4:] != ".gif":
            raise click.BadParameter(f"File '{filename}' is not a gif.", param_hint="'FILENAME'")
        fig.gif2video(filename, output, width, fps_reduction, text, TextStyle(text_style), True)
        return

    fig.video2gif(filename, output, width, fps_reduction, low_quality, disable_dither, shit_optimize, ffmpeg,
                  text, TextStyle(text_style), True)


if __name__ == '__main__':
    main()
