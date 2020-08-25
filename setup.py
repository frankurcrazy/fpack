import setuptools

with open("README.md", "r") as fh:
    long_desc = fh.read()

setuptools.setup(
    name="fpack",
    version="1.0.0",
    author="Frank Chang",
    author_email="frank@csie.io",
    description="fpack is a simple message (de)seriealizer in pure python",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/frankurcrazy/fpack",
    packages=setuptools.find_packages(),
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet",
        "Topic :: System :: Networking",
    ],
    keywords=["serializer", "unserializer", "packer", "unpacker"],
    python_requires=">=3.7",
)
