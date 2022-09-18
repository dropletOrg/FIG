from setuptools import setup, find_packages
from pathlib import Path
import fig

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='fig-converter',
    description='A python package and CLI to turn videos into GIFs and vice-versa.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=fig.__version__,
    license='MIT',
    author="blahberi, kamoodi",
    author_email='droplet.org@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    py_modules=["fig"],
    url='https://github.com/dropletOrg/FIG',
    install_requires=['opencv-python', 'numpy', 'Pillow', 'click', 'tqdm', 'pygifsicle', 'more-itertools', 'imageio', 'requests', 'yt-dlp', 'tldextract', 'art'],
    entry_points={'console_scripts': ['fig = fig.scripts.fig_cli:main', 'fig-download = fig.scripts.fig_download:main']},
    keywords='convert converter video gif fig pyfig figpy python-fig fig-python py-fig fig-py caption text edit editor cli package command command-line gif-convert gif-converter tool gif-tool gif-editor gif-editor-tool',
)
