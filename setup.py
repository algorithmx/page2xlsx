from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="page2xlsx",
    version="0.1",
    install_requires=requirements,
    entry_points=f"""
        [console_scripts]
        page2xlsx=page2xlsx.main:get_page
    """,
)
