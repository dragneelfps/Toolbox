from setuptools import setup, find_packages

setup(
    name="toolbox",
    version="0.2.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "box = toolbox.app:cli"
        ]
    }
)
