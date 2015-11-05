from setuptools import setup

setup(
    name="pyskype",
    version="0.1",
    description="Skype Automation",
    author="Source Simian",
    url='https://github.com/sourcesimian/pySkype',
    license='MIT',
    packages=['skype'],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "skype=skype.cli:skype",
        ]
    },
    download_url="https://github.com/sourcesimian/pySkype/tarball/master",
)
