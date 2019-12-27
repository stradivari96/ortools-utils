import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# python setup.py sdist
# twine upload --skip-existing --repository pypi dist/*

setuptools.setup(
    name="ortools-utils",
    version="0.0.20",
    author="Xiang Chen",
    author_email="xiangchenchen96@gmail.com",
    description="Python utilities for ortools",
    python_requires='>=3.6',
    install_requires=['ortools'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stradivari96/ortools-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
