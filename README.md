# openHAB Material Design Icons

This project creates a set of icons for use with [openHAB 2](https://www.openhab.org) from the [Material Design Icons](https://www.materialdesignicons.com) (MDI).

## Pre-requisites

Install the required libraries:
```
pip3 install -r requirements.txt
```

Download this repository with
```
git clone --recursive https://github.com/metbril/openhab-mdi.git
```


## Design

The icon set is built around default colors.

Icon colors follow the dynamic state or value when possible. For example:

- Switch ON = green
- Switch OFF = red
- Contact CLOSED = green
- Contact OPEN = red

Gradients, for example for the dimmed `light` states, can be computed with tools like the [color gradient table generator](http://www.herethere.net/~samson/php/color_gradient/) or [RGB Color Gradient Maker](http://www.perbang.dk/rgbgradient/).

## Configuration

The script parses a YAML configuration file `mdi.yaml`. This file parses (a selected part of) the MDI library and creates a set of .svg icons from the source.

You can specify the source icon, the destination icon, the color of the destination icon and any alias for the icon.
The color must be a string and defined in mdi.py.

## Building the iconset

To build the iconset:

1. Run `python3 mdi.py` from the command line to create the .svg icons in a subfolder `iconset`.
2. Run the `_icon_convert.sh` script to create the corresponding .png files.

## Using the iconset

That's easy. Just copy all files from the `iconset` folder to your openHAB configuration in the folder `icons/classic`.
