from setuptools import setup, find_packages
setup(
    name="llm_tree_reasoning",
    version="0.1",
    packages=find_packages(exclude=["tests", "logs"]),
)
