from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ephemera-cli",
    version="1.0.0",
    author="柏喵Atri",
    author_email="atri@example.com",
    description="CLI for Alice EVO Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SakuraNekooo/ephemera-cli",
    py_modules=["ephemera_cli"],
    entry_points={
        "console_scripts": [
            "ephemera=ephemera_cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
