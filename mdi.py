#!/usr/local/bin/python3

import sys
from shutil import copyfile
import fileinput
import ruamel.yaml as yaml

srcpath = "./download/MaterialDesign-master/icons/svg"
dstpath = "./iconset"

def svg_copy(src, dst):
    try:
        copyfile(src, dst)
    except IOError as err:
        print(err)

def svg_replace_fill(file, search_color, replace_color):
    search = 'fill="' + search_color + '"'
    replace = 'fill="' + replace_color + '"'
    with fileinput.FileInput(file, inplace=True) as file:
        for line in file:
            print(line.replace(search, replace), end='')

def main(argv):

    with open("mdi.yaml") as f:
        try:
            doc = yaml.safe_load(f)
            f.close()
            for mdi in doc['mdi']:
                for source in mdi:
                    for dest in mdi[source]:

                        # copy source to destination
                        srcfile = srcpath + '/' + source + '.svg'
                        dstfile = dstpath + '/' + dest['dest'] + '.svg'
                        svg_copy(srcfile, dstfile)

                        #modify color of destination file
                        if 'color' in dest:
                            svg_replace_fill(dstfile, '#000000', dest['color'])

                        # create aliases
                        if 'alias' in dest:
                            for alias in dest['alias']:
                                srcfile = dstpath + '/' + dest['dest'] + '.svg'
                                dstfile = dstpath + '/' + alias + '.svg'
                                svg_copy(srcfile, dstfile)

        except yaml.YAMLError as exc:
            print(exc)



if __name__ == "__main__":
    main(sys.argv)
