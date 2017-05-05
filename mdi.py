#!/usr/local/bin/python3

import sys
import os
from os.path import expanduser
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

def is_valid_file(parser, arg):
    """
    Check if arg is a valid file that already exists on the file system.

    Parameters
    ----------
    parser : argparse object
    arg : str

    Returns
    -------
    arg
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_parser():
    """Get parser object for script """

    # home = expanduser("~")
    #pwd = os.path.realpath(__file__)
    pwd = os.path.abspath(os.path.dirname(__file__))

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    # parser.add_argument("-c", "--config",
    #                     dest="config",
    #                     type=lambda x: is_valid_file(parser, x),
    #                     help="get configration from CONFIG",
    #                     metavar="CONFIG",
    #                     default=home + "/.config/mdi.conf")
    parser.add_argument("-f", "--file",
                        dest="filename",
                        action="store",
                        type=lambda x: is_valid_file(parser, x),
                        metavar="FILE",
                        default=pwd + "/mdi.yaml",
                        help="get input/output mapping from FILE")

    parser.add_argument("-i", "--input",
                        dest="input_path",
                        type=lambda x: is_valid_file(parser, x),
                        help="read icons from INPUT PATH",
                        metavar="INPUT PATH")

    parser.add_argument("-o", "--output",
                        dest="output_path",
                        type=lambda x: is_valid_file(parser, x),
                        metavar="OUTPUT PATH",
                        default=pwd+"/iconset",
                        help="write icons to OUTPUT PATH")
    parser.add_argument("-n", "--dry-run",
                        action="store_true",
                        dest="dryrun",
                        default=False,
                        help="parse yaml file for errors")
    parser.add_argument("-q", "--quiet",
                        action="store_false",
                        dest="verbose",
                        default=True,
                        help="don't print status messages to stdout")
    parser.add_argument("-e", "--empty",
                        action="store_true",
                        dest="empty",
                        default=False,
                        help="empty output folder first")

    return parser

def main(argv):

    args = get_parser().parse_args()

    if (args.empty):
        # remove all files in output folder
        folder_path = args.output_path

        if args.verbose:
            print('Deleting all files from ' + folder_path + '...')

        for file_object in os.listdir(folder_path):
            file_object_path = os.path.join(folder_path, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)

    file = args.filename
    with open(file) as f:
        try:
            doc = yaml.safe_load(f)
            f.close()
            for mdi in doc['mdi']:
                for source in mdi:
                    for dest in mdi[source]:

                        # copy source to destination
                        srcfile = srcpath + '/' + source + '.svg'
                        dstfile = dstpath + '/' + dest['dest'] + '.svg'

                        if (not args.dryrun):

                            # copy file
                            if args.verbose:
                                print('Copy ' + srcfile + ' to ' + dstfile)
                            svg_copy(srcfile, dstfile)

                            #modify color of destination file
                            if 'color' in dest:
                                if args.verbose:
                                    print('Replace icon color with ' + dest['color'])
                                svg_replace_fill(dstfile, '#000000', dest['color'])

                            # create aliases
                            if 'alias' in dest:
                                for alias in dest['alias']:
                                    srcfile = dstpath + '/' + dest['dest'] + '.svg'
                                    dstfile = dstpath + '/' + alias + '.svg'
                                    if args.verbose:
                                        print('Create alias ' + dstfile)
                                    svg_copy(srcfile, dstfile)

        except yaml.YAMLError as exc:
            print(exc)

if __name__ == "__main__":
    main(sys.argv)
