#!/usr/bin/env python

import gobject
import gtk

from gui import Gui
from player import Player

class GStream(Gui, Player):
  def __init__(self):
    Gui.__init__(self)
    Player.__init__(self)

if __name__ == '__main__':
  GStream()
  gobject.threads_init()
  gtk.main()
