from distutils.core import setup

setup(
    name='Vizer',
    version='0.1.2',
    author='lufficc',
    author_email='luffy.lcc@gmail.com',
    packages=['vizer'],
    url='https://github.com/lufficc/Vizer',
    scripts=[],
    description='Boxes and masks visualization tools.',
    install_requires=[
        "opencv-python>=3.4.2.17",
        "numpy",
        "Pillow",
    ],
)
