from setuptools import setup, find_packages

setup(
    name="MAU",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "ollama",
        "pydantic",
        "prompt_toolkit",
        "rich",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "mau= mau.cli:main",
        ],
    },
)
