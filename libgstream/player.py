#!/usr/bin/env python

import urllib

import gobject
import gst

class Player(object):
  def __init__(self):
    self._source = gst.element_factory_make('playbin2')
    bus = self._source.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect('message', self.message_cb)
    self._tag = []
    self._uri = []
    self._index = -1

  def message_cb(self, bus, message):
    type = message.type
    if type == gst.MESSAGE_TAG:
      self.tag = message.parse_tag()
    elif type == gst.MESSAGE_ERROR:
      print message.parse_error()
      self.index += 1

  def play(self):
    self._source.set_state(gst.STATE_PLAYING)

  def stop(self):
    self._source.set_state(gst.STATE_NULL)

  @property
  def tag(self):
    return self._tag

  @tag.setter
  def tag(self, value):
    tag = []
    for attr in ['artist', 'title']:
      if attr in value:
        tag.append(value[attr])
    if tag:
      self._tag = tag
      if hasattr(self, 'tooltip'):
        self.tooltip = ' - '.join(tag)

  @property
  def uri(self):
    return self._uri

  @uri.setter
  def uri(self, value):
    uri = []
    if value.endswith('.pls') or value.endswith('.m3u'):
      for line in urllib.urlopen(value).readlines():
        url = line[line.find('http://'):]
        url = url[:url.find(' ')]
        if url:
          uri.append(url.strip())
    else:
      uri.append(value)
    self._uri = uri
    self.index = 0

  @property
  def index(self):
    return self._index

  @index.setter
  def index(self, value):
    value = value % len(self._uri)
    self._index = value
    self._source.set_property('uri', self._uri[self._index])
