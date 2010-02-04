#!/usr/bin/env python

import os

import gobject
import gtk

from libgstream.gui import Gui
from libgstream.playlist import Playlist
from libgstream.player import Player

playlist_location = os.path.join('~', '.config', 'gstream', 'playlist.cfg')

class GStream(Gui, Player):
  def __init__(self, playlist):
    Gui.__init__(self, playlist)
    Player.__init__(self)

if __name__ == '__main__':
  GStream(Playlist(playlist_location))
  gobject.threads_init()
  gtk.main()
