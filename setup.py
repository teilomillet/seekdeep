from setuptools import setup, find_packages

setup(
    name="deep-research",
    version="0.1.0",
    description="A compact implementation of the DeepSearch concept using deepseek-r1 via Ollama",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "chromadb>=0.4.18",
        "requests>=2.28.0",
        "pydantic>=1.10.8",
    ],
    python_requires=">=3.8",
) 