from setuptools import setup, find_packages

setup(
    name="strongly",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    author="StronglyAI, Inc.",
    author_email="info@strongly.ai",
    description="A Python client for the Strongly.AI API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/strongly-ai/strongly",
)
