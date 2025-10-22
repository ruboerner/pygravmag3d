from setuptools import setup, find_packages

setup(
    name="pygravmag3d",
    version="0.1",
    packages=find_packages(),
    install_requires=["scipy"],  # list dependencies here if any
    python_requires=">=3.9",
)