#!/usr/bin/env python3
"""The command-line entry point for combining images into a single image."""

from framer import combine_vertical_from_iterable
from PIL import Image
import argparse
import os


def main():
    """Combine images vertically given file names on the command line."""
    parser = argparse.ArgumentParser(description='''Make a vertical image from
                a series of images. They better have the same dimensions...''')
    parser.add_argument('images', nargs='+',
                        help='''The file paths of the images to combine.''')
    parser.add_argument('-n', '--name',
                        help=""""The resultant image's file name. Defaults to
                        the name of the first image plus '_vertical'""")
    parser.add_argument('-d', '--delete', action='store_true',
                        help='Set this flag to delete the component images.')
    parser.add_argument('-t', '--type', choices=['png', 'jpg'], default='png',
                        help='The file type of the snapshots. ')

    args = parser.parse_args()
    result = combine_vertical_from_iterable(args.images)
    if args.delete:
        for image in args.images:
            os.remove(image)
    fmt = args.type if args.type is not None \
                     else Image.open(args.images[0]).format
    name = args.name if args.name is not None \
                else os.path.splitext(args.images[0])[0] + \
                     '_vertical.' + fmt
    result.save(name, format=args.type)

if __name__ == '__main__':
    main()
