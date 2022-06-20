[![CI](https://github.com/comictagger/comicapi/actions/workflows/build.yaml/badge.svg?branch=develop&event=push)](https://github.com/comictagger/comicapi/actions/workflows/build.yaml)
[![GitHub release (latest by date)](https://img.shields.io/github/downloads/comictagger/comicapi/latest/total)](https://github.com/comictagger/comicapi/releases/latest)
[![PyPI](https://img.shields.io/pypi/v/comicapi)](https://pypi.org/project/comicapi/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/comicapi)](https://pypistats.org/packages/comicapi)
[![PyPI - License](https://img.shields.io/pypi/l/comicapi)](https://opensource.org/licenses/Apache-2.0)

[![GitHub Discussions](https://img.shields.io/github/discussions/comictagger/comicapi)](https://github.com/comictagger/comicapi/discussions)

# ComicAPI

ComicAPI is a library for **writing metadata to digital comics**, written in Python.

Archives supported:
* CBZ/Zip
* CBR/RAR (Optional needs extra dependencies)
* CB7/7zip
* CBT/Tar
* Folder (an extracted archive)

Metadata supported:
* ComicRack (CR)
* ComicBookLover (CBL)
* The Comic Metadata (CoMet)

# History
ComicAPI originates in [ComicTagger] was separated by Davide Romanini in [ComicAPI], was integrated into [ComicStreamer], was modified in [kounch]'s fork, extracted and packaged by [Iris W], maintained by [OzzieIsaacs], and now lives in this repository after merging these separate histories.

[ComicTagger]: https://github.com/comictagger/comictagger
[ComicAPI]: https://github.com/davide-romanini/comicapi
[ComicStreamer]: https://github.com/davide-romanini/ComicStreamer
[kounch]: https://github.com/kounch/ComicStreamer
[Iris W]: https://github.com/wildthyme/comicapi

## Installation

A pip package is provided, you can install it with:

```
 $ pip3 install comicapi
```

There is an optional dependency CBR. You can install it by specifying `CBR` or `all` in braces e.g. `comicapi[CBR]`

### From source

 1. Ensure you have python 3.8 or newer installed
 2. Clone this repository `git clone https://github.com/comictagger/comicapi.git`
 3. `pip3 install -r requirements_dev.txt`
 7. `pip3 install .` or `pip3 install .[CBR]`
