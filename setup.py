from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    description=(
        "Reusable maze generator developed for the 42 A-Maze-ing project"
    ),
    author="luafranc, jamsilva",
    packages=find_packages(include=["mazegen*"]),
    python_requires=">=3.10",
)
