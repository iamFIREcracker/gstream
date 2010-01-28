#!/usr/bin/env python

try:
  import pynotify
  pynotify.init('Gstream')
except:
  pass

try:
  _notification = pynotify.Notification('GStream')
except:
  _notification = None

def notify(title, body):
  if not _notification:
    return
  _notification.update(title, body)
  _notification.show()
