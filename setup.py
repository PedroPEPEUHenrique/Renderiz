from setuptools import setup, find_packages

setup(
    name="renderiz",
    version="0.1.0",
    description="Framework Python para renderização de alta performance em Web e Mobile",
    packages=find_packages(include=["renderiz", "renderiz.*"]),
    python_requires=">=3.10",
)
