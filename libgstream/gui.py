#!/usr/bin/env python

import time

import gobject
import gtk

from notifications import notify
from playlist import Playlist

class Gui(gtk.StatusIcon):
  def __init__(self, playlist):
    super(Gui, self).__init__()
    self.set_from_icon_name('applications-multimedia')

    self.connect('activate', self.activate_cb)
    self.connect('popup-menu', self.popup_menu_cb)
    self.set_visible(True)

    self._playlist = playlist
    self._tooltip = ''
    self._playing = False
    self._active = -1

  def select_cb(self, widget, data, index):
    self._active = index
    if self._playing:
      self.stop_cb(widget)
    if hasattr(self, 'uri'):
      self.uri = data
    self.play_cb(widget)

  def activate_cb(self, widget):
    menu = gtk.Menu()
    for (i, (name, uri)) in enumerate(self._playlist):
      item = gtk.MenuItem(name)
      if i == self._active:
        label = item.get_child()
        label.set_markup('<b>' + name + '</b>')
      item.connect('activate', self.select_cb, uri, i)
      menu.append(item)
    menu.show_all()
    menu.popup(None, None, None, 1, 0)

  def copy_cb(self, widget):
    gtk.Clipboard().set_text(self.tooltip)

  def add_cb(self, widget):
    dialog = gtk.Dialog('New radio', None, gtk.DIALOG_MODAL,
                     (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    box = dialog.get_child()
    box.pack_start(gtk.Label('Name'), False, False, 0)
    name_entry = gtk.Entry()
    box.pack_start(name_entry, False, False, 0)
    box.pack_start(gtk.Label('Url'), False, False, 0)
    url_entry = gtk.Entry()
    box.pack_start(url_entry, False, False, 0)
    dialog.show_all()
    response_id = dialog.run()
    if response_id == gtk.RESPONSE_ACCEPT:
      (name, url) = (name_entry.get_text(), url_entry.get_text()) 
      if name and url:
        self._playlist.append((name, url))
    dialog.destroy()

  def remove_cb(self, widget):
    pass

  def play_cb(self, widget):
    if self._active != -1 and not self._playing and hasattr(self, 'play'):
      self._playing = True
      self.play()

  def stop_cb(self, widget):
    if self._playing and hasattr(self, 'stop'):
      self._playing = False
      self.stop()

  def popup_menu_cb(self, widget, button, time):
    if button == 3:
      menu = gtk.Menu()

      if not self._playing:
        item = gtk.ImageMenuItem(gtk.STOCK_MEDIA_PLAY)
        item.connect('activate', self.play_cb)
      else:
        item = gtk.ImageMenuItem(gtk.STOCK_MEDIA_STOP)
        item.connect('activate', self.stop_cb)
      menu.append(item)

      item = gtk.ImageMenuItem(gtk.STOCK_COPY)
      label = item.get_child()
      label.set_text('Copy title')
      item.connect('activate', self.copy_cb)
      menu.append(item)

      item = gtk.ImageMenuItem(gtk.STOCK_ADD)
      label = item.get_child()
      label.set_text('Add radio')
      item.connect('activate', self.add_cb)
      menu.append(item)

      item = gtk.ImageMenuItem(gtk.STOCK_REMOVE)
      label = item.get_child()
      label.set_text('Remove radio')
      item.connect('activate', self.remove_cb)
      menu.append(item)

      item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
      item.connect('activate', gtk.main_quit)
      menu.append(item)

      menu.show_all()
      menu.popup(None, None, None, 3, time)
  
  @property
  def tooltip(self):
    return self._tooltip

  @tooltip.setter
  def tooltip(self, value):
    self._tooltip = value
    self.set_tooltip(value)
    notify(self._playlist[self._active][0], value)
