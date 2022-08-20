# FIG (Format Interchange Graphics)
A [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software) python package and CLI to turn videos into GIFs and vice-versa.

## Usage

You can use FIG's built-in CLI to convert videos to GIFs through the Command-Line.

```terminal
Usage: fig FILENAME [OPTIONS]

Options:
  -q, --quality INTEGER RANGE     Quality of the gif (applies jpeg lossy
                                  compression to the gif, 100 - no
                                  compression, 0 - shitloads of compression)
                                  [default: 100; 0<=x<=100]
  -o, --output TEXT               Output filename
  -w, --width INTEGER RANGE       Width of the gif
                                  [1<=x]
  -so, --shit-optimize            Optimize the gif but change it to 256 colors
                                  (requires gifsicle)
  -kw, --keep-width               Keep the width of the gif
  -t, --caption TEXT              Text to add to the gif
  -ts, --text-style [top|bottom|caption]
                                  Style of text to add to the gif
  -g2v, --gif2video               Convert a gif to video (other options are
                                  ignored)
  --help                          Display all options for the CLI

  -v, --version                   Display the version of FIG
```
Or you could use FIG as a Python package

```python
import fig

fig.video2gif("myvideo.mp4")  # Convert video to GIF
fig.gif2video("myvideo.gif")  # Convert GIF to video
```

## About Us
We are a duo of independent university students and professional programmers who love contributing to the world of [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software). Our goal is to improve our skills as developers and to make the world a better place by replacing [shitty online GIF conversion tools](https://www.onlineconverter.com/) with [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software).

## Credits
- https://github.com/opencv/opencv-python (Special Thanks! Super Fast 💨)
- https://github.com/pallets/click (Special Thanks! Made Our CLI Amazing 🎉)
- https://github.com/numpy/numpy (Special Thanks! Awsome Work 👍🏻)
- https://github.com/LucaCappelletti94/pygifsicle
- https://github.com/python-pillow/Pillow (Special Thanks! Great Project 🔥)
- https://github.com/more-itertools/more-itertools (Special Thanks! Keep Up The Good Work 🤟🏻)
- https://github.com/tqdm/tqdm (Special Thanks! Made Our CLI SOO Much Better 🙏🏻)
- https://github.com/imageio/imageio (Special Thanks! Cheers 🍻)
- https://github.com/python/cpython (Special Thanks! Couldn't Have Done This Without You ❤)
- https://github.com/dropletOrg/FIG (Super Mega Special Special Thanks!!! One Of the Best [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software) Projects Out There🔥❤✔)