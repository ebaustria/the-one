import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open("requirements.txt", "r") as fh:
#    requirements = [line.strip() for line in fh.readlines()]

setuptools.setup(
    name="regiaoSul",
    version="0.0.1",
    author="Eric Bush",
    author_email="ericbushmerp@gmail.com",
    #description=(
    #    "A Python module providing functions for the representation of DTNs "
    #    "based on time-varying network graphs. "
    #    "Supports Python 2.7 and Python 3.4+."
    #),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebaustria/regiaoSul",
    packages=setuptools.find_packages(),
    # install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

