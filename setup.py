import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deluge-slackr",
    version="0.0.1",
    author="Andrew Cole",
    author_email="andrew.cole@illallangi.com",
    description="A utility to post notifications about events to Slack from Deluge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/illallangi/DelugeSlackr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts':
            [
                'deluge-slackr=deluge_slackr:__main__.main',
                'deluge-slackr-added=deluge_slackr:__main__.added',
                'deluge-slackr-complete=deluge_slackr:__main__.complete'
            ]
    },
    install_requires=[
        'Click',
        'loguru',
        'notifiers'
    ]
)
