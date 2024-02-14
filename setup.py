from setuptools import setup, find_packages

setup(
    name="pequena-arana",
    version="1.0",
    packages=find_packages(),
    install_requires=["networkx", "pytest", "npyscreen"],
    license="MIT",
    long_description=open("README.md").read(),
)
