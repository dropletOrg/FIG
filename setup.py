from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='fig-converter',
    description='A python package and CLI to turn videos into GIFs and vice-versa.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.0-beta',
    license='MIT',
    author="blahberi, kamoodi",
    author_email='droplet.org@gmail.com',
    packages=["figconverter"],
    py_modules=["figconverter"],
    url='https://github.com/dropletOrg/FIG',
    install_requires=['opencv-python', 'numpy', 'pillow', 'click', 'tqdm', 'pygifsicle', 'more-itertools', 'imageio'],
    scripts=['fig.py'],
    keywords='convert converter video gif fig pyfig figpy python-fig fig-python py-fig fig-py caption text edit editor cli package command command-line gif-convert gif-converter tool gif-tool gif-editor gif-editor-tool',
)
