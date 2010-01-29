#!/usr/bin/env python

import os
from ConfigParser import ConfigParser

class Playlist(object):
  def __init__(self, location):
    dir = os.path.expanduser(os.path.dirname(location))
    if not os.path.exists(dir):
      os.mkdir(dir)

    self._config = ConfigParser()
    self._config.optionxform = str

    self._file = os.path.expanduser(location)
    if os.path.exists(self._file):
      self._config.read(self._file)
    else:
      self._config.add_section('Playlist')
      self.save()

  def save(self):
    self._config.write(open(self._file, 'wb'))

  def append(self, item):
    self._config.set('Playlist', *item)
    self.save()

  def remove(self, option):
    self._config.remove_option('Playlist', option)
    self.save()

  def __getitem__(self, item):
    return self._config.items('Playlist')[item]

  def __iter__(self):
    return iter(self._config.items('Playlist'))
