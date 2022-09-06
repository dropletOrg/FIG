<img src="https://raw.githubusercontent.com/dropletOrg/FIG/main/logo/logo_with_more_text.svg" width=852>

A powerful, versatile and simplistic [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software) python package and CLI to turn videos into GIFs and vice-versa.

![GitHub](https://img.shields.io/github/license/dropletOrg/FIG)
![PyPI](https://img.shields.io/pypi/v/fig-converter)
![GitHub repo size](https://img.shields.io/github/repo-size/dropletOrg/FIG)
![GitHub](https://img.shields.io/badge/-WORKING_2019!!!-97CA00?logo=Checkmarx&logoColor=white)
![GitHub](https://img.shields.io/badge/-NOT_CLICKBAIT!!!-cc3300?logo=radar&logoColor=white)

<img src="https://raw.githubusercontent.com/dropletOrg/FIG/main/README-data/unleash.gif"/>

## Usage
You can use FIG's built-in CLI to convert videos to GIFs through the Command-Line.

```
Usage: fig.py [OPTIONS] FILENAME                                              
                                                                              
Options:                                                                      
  -o, --output TEXT               Output filename                             
  -g2v, --gif2video               Convert a gif to a video (options:          
                                  dithering, low-quality, shit-optimize,      
                                  ffmpeg are disabled)                        
  -w, --width INTEGER             Width of the gif (must be 16 or bigger)     
  -fr, --fps-reduction INTEGER    Divide fps by this number (must be bigger   
                                  than 0 and can't be bigger than the original
                                  fps)                                        
  -lq, --low-quality              Prioritize speed and size over quality      
  -dd, --disable-dither           Disable dither to increase quality but cause
                                  color banding (disables low-quality)        
  -so, --shit-optimize            Optimize the gif but change it to 256 colors
                                  (requires gifsicle)                         
  -f, --ffmpeg                    Use ffmpeg for higher quality conversion    
                                  (requires ffmpeg) (enables dithering)       
  -t, --text TEXT                 Text to add to the gif                      
  -ts, --text-style [top|bottom|caption]                                      
                                  Style of text to add to the gif
  -v, --version                   Show the version and exit.
  --help                          Show this message and exit.
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
 - In order to use the ``shit-optimize`` option you'll need to install gifsicle:

    While running the installation, on **MacOS** the setup will automatically install **gifsicle** using [Brew](https://brew.sh/).
    
    On Linux you will need to install **gifsicle** using apt-get as follows:
    ```shell
    sudo apt-get install gifsicle
    ```
    On Windows you will need to download and install the [correct port of the library](https://eternallybored.org/misc/gifsicle/) for your OS.
    <br><br>
 - In order to use the ``ffmpeg`` option you'll need to install FFmpeg:
    
    There are a variety of ways to install FFmpeg, such as the [official download links](https://ffmpeg.org/download.html), or using your package manager of choice (e.g. `sudo apt install ffmpeg` on Debian/Ubuntu, `brew install ffmpeg` on OS X, etc.).

    Regardless of how FFmpeg is installed, you can check if your environment path is set correctly by running the `ffmpeg` command from the terminal, in which case the version information should appear, as in the following example (truncated for brevity):
    
    ```
    $ ffmpeg
    ffmpeg version 4.2.4-1ubuntu0.1 Copyright (c) 2000-2020 the FFmpeg developers
      built with gcc 9 (Ubuntu 9.3.0-10ubuntu2)
    ```
    
    > **Note**: The actual version information displayed here may vary from one system to another; but if a message such as `ffmpeg: command not found` appears instead of the version information, FFmpeg is not properly installed.
 
## Comparison
Comparison against [shitty online GIF conversion tools](https://www.onlineconverter.com/)

All GIFs are available in the ``gif_comparison`` folder for you to compare.

All of the information here was submitted in a survey.

|                          | Time         | Size                                               | Quality                | Easy To Use | Versatile             | Ads | Worked            |
|--------------------------|--------------|----------------------------------------------------|------------------------|-------------|-----------------------|-----|-------------------|
| FIG                      | 8s (Fastest) | 15.3MB (With Certain Settings FIG Can Reach 5.7MB) | 9/10 (Highest Quality) | Yes         | Yes (Most Versatile)  | 0   | Yes (Most Worked) |
| ezgif.com                | 10s          | 16.4MB                                             | 8/10                   | Yes         | Yes                   | 4   | Yes               |
| cloudconvert.com         | 10s          | 5.17MB (Smallest)                                  | 4/10                   | No          | No                    | 0   | Yes               |
| veed.io                  |              |                                                    |                        |             |                       | 0   | No                |
| image.online-convert.com | 13s          | 5.7MB                                              | 5/10                   | Yes         | Kinda (no FPS option) | 3   | Yes               |
| convertio.co             | 15s          | 46.8MB (No Option to Change Resolution)            | 4/10                   | Yes         | No                    | 2   | Yes               |
| img2go.com               | 13s          | 5.7MB                                              | 5/10                   | Yes         | No                    | 2   | Yes               |
| create.vista.com         | 16s          | 14.4MB                                             | 8/10                   | Yes         | Yes                   | 0   | Yes               |
| onlineconverter.com      | 8s           | 5.17MB (Smallest)                                  | 4/10                   | No          | No                    | 3   | Yes               |  

## About Us
We are a duo of independent university students and professional programmers who love contributing to the world of [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software). 
Our goal is to improve our skills as developers and to make the world a better place by replacing [shitty online GIF conversion tools](https://www.onlineconverter.com/) with [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software).

## Credits
- [opencv-python](https://github.com/opencv/opencv-python) (Special Thanks! Super Fast)
- [click](https://github.com/pallets/click) (Special Thanks! Made Our CLI Amazing)
- [numpy](https://github.com/numpy/numpy) (Special Thanks! Awesome Work)
- [pygifsicle](https://github.com/LucaCappelletti94/pygifsicle)
- [gifsicle](https://github.com/kohler/gifsicle)
- [Pillow](https://github.com/python-pillow/Pillow) (Special Thanks! Great Project)
- [more-itertools](https://github.com/more-itertools/more-itertools) (Special Thanks! Keep Up The Good Work)
- [tqdm](https://github.com/tqdm/tqdm) (Special Thanks! Made Our CLI SOO Much Better)
- [imageio](https://github.com/imageio/imageio) (Special Thanks! Cheers)
- [FFmpeg](https://github.com/FFmpeg/FFmpeg) (Special Thanks! Amazing Project)
- [cpython](https://github.com/python/cpython) (Special Thanks! Couldn't Have Done This Without You)
- [FIG](https://github.com/dropletOrg/FIG) (Super Mega Special Special Thanks!!! One Of The Best [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software) Projects Out There)
  
