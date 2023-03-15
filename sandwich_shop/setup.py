from setuptools import setup, find_packages
import os

os.environ["API_KEY"] = "N1N5YKSR"

with open("requirements.txt", encoding="utf-16") as f:
    requirements = f.read().splitlines()

setup(
    name="code",
    version="1.0",
    packages=find_packages(),
    install_requires=requirements
)
