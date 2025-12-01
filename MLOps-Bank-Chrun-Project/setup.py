from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-BANK-CHURN",
    version="0.1",
    author="Preetham",
    packages=find_packages(),
    install_requires = requirements,
)