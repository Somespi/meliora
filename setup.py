from setuptools import setup, find_packages

setup(
    name="meliora",
    version="1.0.0",
    packages=find_packages(),
    package_data={"meliora.includes": ["common_titles.txt"]},
)
