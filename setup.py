#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="2B1Q",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "2b1q-send=sender:send_message",
            "2b1q-receive=receiver:receive_message",
        ],
    },
    install_requires=[
        "cryptography",
        "matplotlib",
    ],
    author="Data Pulse",
    author_email="lucasyfm@hotmail.com",
    description="Projeto de envio/recebimento de código 2B1Q criptografado",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iLukSbr/2B1Q",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)