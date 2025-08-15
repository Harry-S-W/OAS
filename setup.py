from setuptools import setup, find_packages

setup(
    name="oas",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas", "numpy", "matplotlib", "tqdm", "six"],  # etc.
    entry_points={
        "console_scripts": [
            "oas=oas.oas:main",  # maps `oas` in terminal to your main()
        ],
    },
)