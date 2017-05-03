# openHAB Material Design Icons

This project creates a set of icons for use with [openHAB 2](https://www.openhab.org) from the [Material Design Icons](https://www.materialdesignicons.com) (MDI).

## Pre-requisites

Install the required libraries:
```
pip3 install -r requirements.txt
```

The script expects the source icons in a sub folder `download` of the script location. [Download the repo as a ZIP](https://github.com/Templarian/MaterialDesign/archive/master.zip) and extract it there first.

## Configuration

The script parses a YAML configuration file `mdi.yaml`. This file parses (a selected part of) the MDI library and creates a set of .svg icons from the source.

You can specify the source icon, the destination icon, the color of the destination icon and any alias for the icon.
The color should be a valid HTML RGB code (e.g. `#FF00FF`).

## Building the iconset

To build the iconset:

1. Run `python3 mdi.py` from the command line to create the .svg icons in a subfolder `iconset`.
2. Run the `_icon_convert.sh` script to create the corresponding .png files.

## Using the iconset

That's easy. Just copy all files from the `iconset` folder to your openHAB configuration in the folder `icons/classic`.
