# Getting ready for PyPi
# https://packaging.python.org/tutorials/packaging-projects/
# https://packaging.python.org/guides/distributing-packages-using-setuptools/
# https://packaging.python.org/guides/using-manifest-in/
############################################
import setuptools

exec(open('SunGather/version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SunGather",
    version=__version__,
    author="FSEL TEAM",
    author_email="ha-fsel@faujiposer.com",
    description="Sungrow Inverters 0x01 data collect and feed to various locations (MQTT, PVOutput, Home Assistant)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harrisjunaid/SunGrowInverters",
    packages=setuptools.find_packages(),
    install_requires=[
        'pymodbus>=2.3.0',
        'websocket-client>=1.2.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.0',
)
