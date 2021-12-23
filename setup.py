import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyanvil",
    version="0.1.0",
    author="Thaodan",
    description="A python library to read, write and edit Minecraft worlds.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UncleThaodan/PyAnvilEditor",
    project_urls={
        "Bug Tracker": "https://github.com/UncleThaodan/PyAnvilEditor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.9.5+",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "pyanvil"},
    py_modules=[],
    install_requires=[],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9.5,<4"
)
