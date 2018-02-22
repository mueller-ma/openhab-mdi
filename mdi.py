#!/usr/bin/env python3

import sys
import os
from os.path import expanduser
from shutil import copyfile
import fileinput
import ruamel.yaml as yaml

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

def empty_folder(folder_path, verbose):
    if verbose:
        print('Deleting all files from ' + folder_path + '...')
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)

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
                        action="store",
                        dest="filename",
                        type=lambda x: is_valid_file(parser, x),
                        default=pwd + "/mdi.yaml",
                        metavar="FILE",
                        help="get input/output mapping from FILE")
    parser.add_argument("-i", "--input-path",
                        dest="input_path",
                        type=lambda x: is_valid_file(parser, x),
                        default=pwd + "/download/MaterialDesign-master/icons/svg",
                        metavar="INPUT-PATH",
                        help="read icons from INPUT-PATH")
    parser.add_argument("-o", "--output-path",
                        dest="output_path",
                        type=lambda x: is_valid_file(parser, x),
                        default=pwd+"/iconset",
                        metavar="OUTPUT-PATH",
                        help="write icons to OUTPUT-PATH")
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

    args.output_path = args.output_path + "/" + os.path.splitext(os.path.basename(args.filename))[0]

    if (args.empty):
        # remove all files in output folder
        if (args.dryrun):
            print('All files in ' + args.output_path + ' would have been deleted.')
        else:
            empty_folder(args.output_path, args.verbose)

    # fill sample variable with the created icons, to be output for documentation purposes.
    sample = ""
    sample += "# Icons sample\n\n"
    sample += "Icon | Sample\n"
    sample += " --- | --- \n"

    with open(args.filename) as f:
        try:
            doc = yaml.safe_load(f)
            f.close()
            for mdi in doc['mdi']:
                for sourcename in mdi:
                    for destname in mdi[sourcename]:

                        srcfile = args.input_path + '/' + sourcename + '.svg'
                        dstfile = args.output_path + '/' + destname['dest'] + '.svg'

                        # copy file
                        if args.dryrun:
                            print('File ' + srcfile + ' would have been copied to ' + dstfile)
                        else:
                            if args.verbose:
                                print('Copy ' + srcfile + ' to ' + dstfile)
                            svg_copy(srcfile, dstfile)
                            sample +=  destname['dest'] + " | ![" + destname['dest'] + "](file://" + dstfile +") \n"

                        # modify color of destination file
                        if 'color' in destname:
                            if args.dryrun:
                                print('Color of file ' + dstfile + ' would have been replaced with ' + destname['color'])
                            else:
                                if args.verbose:
                                    print('Replace icon color with ' + destname['color'])
                                svg_replace_fill(dstfile, '#000000', destname['color'])

                        # create aliases
                        if 'alias' in destname:
                            for alias in destname['alias']:
                                srcfile = args.output_path + '/' + destname['dest'] + '.svg'
                                dstfile = args.output_path + '/' + alias + '.svg'
                                if args.dryrun:
                                    print('Alias ' + dstfile + ' would have been created for ' + srcfile)
                                else:
                                    if args.verbose:
                                        print('Create alias ' + dstfile)
                                    svg_copy(srcfile, dstfile)
                                    sample +=  alias + " | ![" + alias + "](file://" + dstfile +") \n"

            # future feature: print iconset sample as md document
            # print(sample)

        except yaml.YAMLError as exc:
            print(exc)

if __name__ == "__main__":
    main(sys.argv)
