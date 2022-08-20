from importlib.metadata import entry_points
from setuptools import setup, find_packages


setup(
    name='fig-converter',
    version='1.0',
    license='MIT',
    author="blahberi, kamoodi",
    author_email='droplet.org@gmail.com',
    packages=find_packages('fig'),
    url='https://github.com/dropletOrg/FIG',
    description='A python package and CLI to turn videos into GIFs and vice-versa.',
    install_requires=['opencv-python', 'numpy', 'pillow', 'click', 'tqdm', 'pygifsicle', 'more-itertools', 'imageio'],
    entry_points={
        'console_scripts': [
            'fig = fig.__main__:main',
        ],
    },
    keywords='convert converter video gif fig pyfig figpy python-fig fig-python py-fig fig-py caption text edit editor cli package command command-line gif-convert gif-converter tool gif-tool gif-editor gif-editor-tool',
)