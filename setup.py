# This file is placed in the Public Domain.


"write your own commands"


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


def uploadlist(dir):
    upl = []
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl


setup(
    name="modz",
    version="1",
    author="B.H.J. Thate",
    author_email="thatebhj@gmail.com",
    url="http://github.com/thatebhj/modz",
    description="write your own commands",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    install_requires=["cmdz"],
    packages=["modz"],
    include_package_data=True,
    data_files=[
                ("modz", uploadlist("modz")),
                ("share/mozz", uploadlist("extra")),
                ("share/doc/modz", ("README.rst",))
               ],
    scripts=["bin/modz"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python",
        "Intended Audience :: System Administrators",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
