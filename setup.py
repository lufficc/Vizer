from distutils.core import setup

setup(
    name='Vizer',
    version='0.1.4',
    author='lufficc',
    author_email='luffy.lcc@gmail.com',
    packages=['vizer'],
    url='https://github.com/lufficc/Vizer',
    scripts=[],
    description='Boxes and masks visualization tools.',
    install_requires=[
        "opencv-python",
        "numpy",
        "Pillow",
    ],
)
