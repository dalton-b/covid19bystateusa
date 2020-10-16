import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="run",
    version="0.0.1",
    author="dalton-b",
    description="Plots of COVID19 cases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dalton-b/covid19bystateusa",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=[
        "pandas",
        "urllib3",
        "matplotlib",
        "beautifulsoup4",
        "numpy"
    ],
    entry_points = {
        'console_scripts': ['covid_update=run.driver:main'],
    }
)
