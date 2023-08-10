import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name = "univk_audio",
    version = "1.0.1",
    author = "Unik",
    description = "An easy-to-use library that allows you to search and download audio from VK, bypassing the restriction on obtaining a token to use the VK audio API.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Exponefrv1/univk_audio",
    install_requires = [
        "aiofiles",
        "aiohttp",
        "beautifulsoup4",
        "httpx",
        "lxml",
    ],
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.7",
    keywords='vk audio music songs search download free univk vk_audio',
    project_urls={
        "Homepage": "https://github.com/Exponefrv1/univk_audio",
        "Issues": "https://github.com/Exponefrv1/univk_audio/issues",
        "Author": "https://t.me/AnemoneSong",
    },
)
