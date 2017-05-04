# openHAB Material Design Icons

This project creates a set of icons for use with [openHAB 2](https://www.openhab.org) from the [Material Design Icons](https://www.materialdesignicons.com) (MDI).

## Pre-requisites

Install the required libraries:
```
pip3 install -r requirements.txt
```

The script expects the source icons in a sub folder `download` of the script location. [Download the repo as a ZIP](https://github.com/Templarian/MaterialDesign/archive/master.zip) and extract it there first.

## Design

The icon set is built around default colors.
A good overview of available colors can be found [at W3 Schools](https://www.w3schools.com/colors/colors_groups.asp).

The icon colors used are:

- green: "#32CD32"
- yellow: "#FFD700"
- red: "#DC143C"
- blue: "#0000CD"

Icon colors follow the dynamic state or value when possible. For example:

- Switch ON = green
- Switch OFF = red
- Contact CLOSED = green
- Contact OPEN = red

Gradients, for example for the dimmed `light` states, can be computed with tools like the [color gradient table generator](http://www.herethere.net/~samson/php/color_gradient/) or [RGB Color Gradient Maker](http://www.perbang.dk/rgbgradient/).

## Different sets

### Minimal set

Any icon set should at least contain an icon for [each channel category](https://www.eclipse.org/smarthome/documentation/development/bindings/thing-definition.html#channel-categories).
A minimal set is included in the project as `minimal.yaml`.

### Classic

openHAB currently includes an extended 'classic' set of icons.
The classic set `classic.yaml` includes an alternative for any of these icons.

### Extra

In addition to the classic set, some additional useful icons have been mapped as `extra.yaml`.
Mainly as an example how to extend the classic set.

### Full

The full set of mapped icons. This is the combination of both the classic as the extra set.

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
