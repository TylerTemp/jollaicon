jollaicon
=========

Summary
-------

`jollaicon` can convert a png file into Sailfish OS style.

Here is a Android icon set in Sailfish OS style already:
[TylerTemp-DroidSailizedIcon](https://github.com/TylerTemp/DroidSailizedIcon).
Also [here](http://talk.maemo.org/showthread.php?t=92073) and
[here](https://together.jolla.com/question/104668/custom-sailfish-os-style-icons-for-android-apps/)

It's a very little tool: it only change the shape of the icon.
You may still need to edit the file after converted.

Install
-------

It requires [python](http://python.org/) and [python-pip](https://pip.pypa.io/en/stable/installing/)

Install by:

```bash
pip install git+git://github.com/TylerTemp/jollaicon.git
```

or

```bash
git clone https://github.com/TylerTemp/jollaicon.git
cd jollaicon
pip install .
```

Then run as

```bash
jollaicon --help
```

If you're a python developer, you can use it as

```python
from jollaicon import icon
help(icon)
```

NOTE: Mac OSX need to install `cairo` separated:

```
brew install cairo
```

More about [brew command](http://brew.sh/)

Usage
---------

```
Usage:
    $ python jollaicon.py [options] <input> <output>

Options:
    -1, --top-left        make top left rectangle instead of round
    -2, --top-right       make top right rectangle instead of round
    -3, --bottom-right    make bottom right rectangle instead of round
    -4, --bottom-left     make bottom left rectangle instead of round
    -h, --help            print this screen
    -v, --version         print version of this script
    -f, --fill[=<color>]  fill color for transparent part. No effect when your
                          icon file is full-filled with color already. It
                          should in ``(r, g, b)`` or ``(r, g, b, alpha)``
                          number group. use white when this option appears but
                          no color specified.

    <input>               path to your icon file (png format only)
    <output>              output file (png format)
```

The corners of Sailfish icon are only round or rectangle.
Use `-1`, `-2`, `-3`, `-4` to set which corner is round/rectangle