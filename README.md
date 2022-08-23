# FIG (Format Interchange Graphics)
A [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software) python package and CLI to turn videos into GIFs and vice-versa.

## Usage

You can use FIG's built-in CLI to convert videos to GIFs through the Command-Line.

```
Usage: fig.py [OPTIONS] FILENAME

Options:
  -q, --quality                   priorotize quality over speed and size
  -o, --output TEXT               Output filename
  -w, --width INTEGER             Width of the gif (must be 16 or bigger)
  -so, --shit-optimize            Optimize the gif but change it to 256 colors
                                  (requires gifsicle)
  -t, --text TEXT                 Text to add to the gif
  -ts, --text-style [top|bottom|caption]
                                  Style of text to add to the gif
  -g2v, --gif2video               Convert a gif to a video
  -fr, --fps-reduction INTEGER    devide fps by thiss number (must be bigger
                                  than 0 and can't be bigger than the original
                                  fps)
  -v, --version                   Show the version and exit.
```
Or you could use FIG as a Python package.

```python
import figconverter

figconverter.video2gif("myvideo.mp4")  # Convert video to GIF
figconverter.gif2video("myvideo.gif")  # Convert GIF to video
```

## Installation
```shell
pip install fig-converter
```
in order to use the -so option (or shit_optimize if you're using the package) you'll need to install gifsicle:

While running the installation, on **MacOS** the setup will automatically install **gifsicle** using [Brew](https://brew.sh/).

On Linux you will need to install **gifsicle** using apt-get as follows:
```shell
sudo apt-get install gifsicle
```
On Windows you will need to download and install the [correct port of the library](https://eternallybored.org/misc/gifsicle/) for your OS.
## About Us
We are a duo of independent university students and professional programmers who love contributing to the world of [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software). Our goal is to improve our skills as developers and to make the world a better place by replacing [shitty online GIF conversion tools](https://www.onlineconverter.com/) with [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software).

## Credits
- https://github.com/opencv/opencv-python (Special Thanks! Super Fast)
- https://github.com/pallets/click (Special Thanks! Made Our CLI Amazing)
- https://github.com/numpy/numpy (Special Thanks! Awesome Work)
- https://github.com/LucaCappelletti94/pygifsicle
- https://github.com/python-pillow/Pillow (Special Thanks! Great Project)
- https://github.com/more-itertools/more-itertools (Special Thanks! Keep Up The Good Work)
- https://github.com/tqdm/tqdm (Special Thanks! Made Our CLI SOO Much Better)
- https://github.com/imageio/imageio (Special Thanks! Cheers)
- https://github.com/python/cpython (Special Thanks! Couldn't Have Done This Without You)
- https://github.com/dropletOrg/FIG (Super Mega Special Special Thanks!!! One Of The Best [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software) Projects Out There)
