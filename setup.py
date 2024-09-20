from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pypelineer",  # Replace with the name of your package
    version="0.0.1",  # Update this version as necessary
    author="Sadig Akhund",  # Replace with your name
    author_email="sadigaxund@gmail.com",  # Replace with your email
    description="Simplistic library for building pipelines efficiently and fast.",  # A short summary of your package
    long_description=long_description,  # This is your README file content
    long_description_content_type="text/markdown",  # Use 'text/markdown' for Markdown files
    url="https://github.com/sadigaxund/pypeliner",  # URL of your package's homepage
    packages=find_packages(),  # Automatically find all packages in your project
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    install_requires=[
        # List of dependencies your package requires (e.g. 'requests>=2.20.0')
    ],
    classifiers=[
        "Programming Language :: Python :: 3",  # Indicate supported versions
        "License :: OSI Approved :: Apache Software License",  # Indicate license
        "Operating System :: OS Independent",  # Indicate compatibility
    ],
    python_requires=">=3.8",  # Minimum Python version
    keywords="your keywords here",  # Add relevant keywords to help users find your package
    project_urls={  # Additional URLs relevant to your project
        "Bug Tracker": "https://github.com/sadigaxund/pypeliner/issues",
        "Documentation": "https://github.com/sadigaxund/pypeliner/README.md",  # If you have documentation
        "Source Code": "https://github.com/sadigaxund/pypeliner/src",
    },
)
