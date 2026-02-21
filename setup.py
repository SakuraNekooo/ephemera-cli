from setuptools import setup
with open("README.md") as f: long_description = f.read()
setup(
    name="ephemera-cli",
    version="1.1.0",
    author="柏喵Atri",
    author_email="atri@example.com",
    description="CLI for Alice EVO Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SakuraNekooo/ephemera-cli",
    py_modules=["ephemera_cli"],
    entry_points={"console_scripts": ["ephemera=ephemera_cli:main"]},
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
