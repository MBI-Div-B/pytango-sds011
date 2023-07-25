from setuptools import setup, find_packages

setup(
    name="tangods_sds011",
    version="0.0.1",
    description="tango device to get dust density from sds011 sensor",
    author="Leonid Lunin",
    author_email="lunin.leonid@gmail.com",
    python_requires=">=3.10",
    entry_points={"console_scripts": ["SDS011 = tangods_sds011:main"]},
    license="MIT",
    packages=["tangods_sds011"],
    install_requires=[
        "pytango",
        "simple-sds011",
    ],
    url="https://github.com/lrlunin/pytango-moenchZmqServer",
    keywords=[
        "tango device",
        "tango",
        "pytango",
        "sds011",
    ],
)
