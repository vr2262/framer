#!/usr/bin/env python3
"""
Framer is a module for dealing with frames in a video. It provides just a few
key capabilities:

- Given a video file, extract some frames as images.
- Given some image files, combine them into one image.
"""

import os
import time
from vlc import vlc
from PIL import Image
import fnmatch


class Video():
    """The Video class provides methods for taking snapshots of a video."""

    def __init__(self, file_name: str, snapshot_path: str, scale: float=None,
                 width: int=None, height: int=None,
                 snapshot_format: str='png'):
        """
        Everything but the snapshot file name prefix and position values
        are video properties.
        """

        self.snapshot_format = snapshot_format
        self.snapshot_path = snapshot_path
        self.file_name = file_name
        # --vout=dummy means the video does not display
        # I can't figure out how to silence VLC warnings though...
        instance = vlc.Instance('''--vout=dummy --no-audio --play-and-exit
                              --snapshot-format={}'''.format(snapshot_format))
        self._player = instance.media_player_new()
        self._player.set_media(instance.media_new(file_name))
        # the state of the player needs to be Playing or Paused... so here we
        # go...
        self._player.play()
        while self._player.get_state() in range(3):
            time.sleep(0.1)
        self._player.pause()

        self.height = 0
        # if the dimensions are specified they take precedence over a scaling
        # ratio
        # a value of 0 for a dimension means auto-scale
        if width is not None or height is not None:
            self.width = width if width is not None else 0
            if height is not None:
                self.height = height
        elif scale is not None:
            self.width = scale * self._player.video_get_width()
        else:
            self.width = 0

    def take_snapshots(self, file_name_prefix: str, *positions: float):
        """Save snapshots for the given positions (between 0 and 1)."""
        file_name_prefix = file_name_prefix.replace(' ', '_')  # .\
                                            # replace('-', '')
        for old_snapshot in fnmatch.filter(os.listdir(self.snapshot_path),
                            file_name_prefix + '*.' + self.snapshot_format):
            os.remove(self.snapshot_path + os.sep + old_snapshot)
        for index, position in enumerate(positions):
            # The file name looks like
            # <path>/<name>_i.<ext>
            # where i is the index of the image.
            snap_name = '{0}{1}{2}_{3:0>2}.{4}'.format(self.snapshot_path,
                            os.sep, file_name_prefix, str(index),
                            self.snapshot_format)
            self._player.set_position(position)
            self._player.video_take_snapshot(0, snap_name, int(self.width),
                                             int(self.height))
            # sometimes taking a snapshot fails inexplicably... so try a few
            # times
            for i in range(4):
                if os.path.exists(snap_name):
                    break
                self._player.video_take_snapshot(0, snap_name, int(self.width),
                                             int(self.height))
            if i == 3:
                raise vlc.VLCException("Couldn't grab {}".format(snap_name))
            yield snap_name
        self._player.stop()
        return

    def take_snapshots_from_iterable(self, file_name_prefix: str,
                                     positions: float):
        """
        Save snapshots for the given iterable of positions (between 0 and 1).

        """

        return self.take_snapshots(file_name_prefix, *positions)

    def convert_times_to_positions(self, times):
        """
        Convert an iterable of times (milliseconds) to positions (between 0 and
        1).
        """

        return (time / self._player.get_media().get_duration() for time \
                                                               in  times)

    def take_snapshots_times(self, file_name_prefix, *times):
        """Save snapshots for the given times (milliseconds)."""
        return self.take_snapshots_from_iterable(file_name_prefix,
                                    self.convert_times_to_positions(times))

    def take_snapshots_times_from_iterable(self, file_name_prefix, times):
        """Save snapshot for the given iterable of times (milliseconds)."""
        return self.take_snapshots_from_iterable(file_name_prefix,
                                        self.convert_times_to_positions(times))


def is_url(path):
    """Return whether a path is a URL or a local file."""
    return path.find(':') > 0  # VLC media_new() logic


def combine_vertical(*images):
    """Make a vertical image from the given images."""
    _, _, width, height = Image.open(images[0]).getbbox()
    result = Image.new('RGB', (width, height * len(images)))
    for multiplier, image in enumerate(images):
        result.paste(Image.open(image), (0, multiplier * height))
    return result


def combine_vertical_from_iterable(images):
    """Make a vertical image from a list of images."""
    return combine_vertical(*images)
