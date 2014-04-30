#!/usr/bin/env python3
"""The command-line entry point for taking snapshots of a video."""

from framer import Video, is_url
import argparse
import os


def main():
    """Create snapshots from a video based on command line arguments."""
    parser = argparse.ArgumentParser(description='''Get frames from a video.
                Specify either a scaling ratio or the height/width. If nothing
                is specified, the default is the full size of the video. If
                both the scale and at least one of the dimensions are
                specified, the dimension(s) take precedence. If only one
                dimension is specified, the other will scale to preserve the
                aspect ratio of the video file.''')
    parser.add_argument('file',
                        help='''The path to the video file. Can be a URL in
                        which case --path must be specified.''')
    parser.add_argument('positions', nargs='+', type=float,
                        help='''The positions in the video at which to take the
                        snapshots. Give the positions as numbers between 0
                        (start of video) and 1 (end of video) unless the -m
                        flag is specified, in which case give the times in
                        milliseconds.''')
    parser.add_argument('-p', '--path',
                        help='''Snapshot path. The default is the path of the
                        video file (must be specified for a URL).''')
    parser.add_argument('-m', '--milliseconds', action='store_true',
                        help='''Flag to interpret the positions as times in
                        milliseconds.''')
    parser.add_argument('-n', '--name',
                        help='''The filename prefix for each of the resultant
                        snapshot image files. The default is the name of the
                        video file without its file extension.''')
    parser.add_argument('-s', '--scale', type=float,
                        help='''The scaling ratio for the snapshots. A ratio of
                        1 means the full size of the video.''')
    parser.add_argument('-w', '--width', type=int,
                        help='The width in pixels of each snapshot.')
    parser.add_argument('-l', '--length', type=int,
                        help='The length (height) in pixels of each snapshot.')
    parser.add_argument('-t', '--type', choices=['png', 'jpg'], default='png',
                        help='The file type of the snapshots. ')

    args = parser.parse_args()

    path = args.path if args.path is not None \
                     else os.path.dirname(args.file)

    if is_url(args.file) and args.path is None:
        parser.error("You must specify --path for a web video.")

    if is_url(args.file):
        print('You put in a URL? Good luck!')

    name = args.name if args.name is not None \
                     else os.path.splitext(os.path.basename(args.file))[0]

    results = []
    video = Video(args.file, path, args.scale, args.width, args.length,
                  args.type)
    snapshot = video.take_snapshots_times_from_iterable \
              if args.milliseconds \
              else video.take_snapshots_from_iterable
    for file in snapshot(name, args.positions):
        print('Created ' + file)
        results.append(file)

    print('--------------------')
    print('\n'.join(results))

if __name__ == '__main__':
    main()
