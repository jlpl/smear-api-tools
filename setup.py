from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()


setup(
    name="smear-api-tools",
    version="0.2.1",
    description='Utility functions for using the SmartSMEAR API',
    py_modules=["smear_api_tools"],
    package_dir={'':'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "pandas >= 1.0.0",
        "numpy >= 1.19.0"
    ],
    extras_require = {
        "dev": [
            "pytest>=3.6",
        ],
    },
    url="https://github.com/jlpl/smear-api-tools",
    author="Janne Lampilahti",
    author_email="janne.lampilahti@helsinki.fi",
)
