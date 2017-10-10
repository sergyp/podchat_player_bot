# -*- coding: utf-8 -*-
from __future__ import print_function


import requests
import BeautifulSoup as bs
from collections import namedtuple


class PodcastException(Exception):
    pass


class Message(namedtuple('BaseMessage', 't author text')):

    def __new__(cls, raw_message):
        t, name, text = raw_message.findChildren('td')
        t = t.text
        name = name.text
        text = u"".join(map(unicode, text.contents))
        return Message.__bases__[0].__new__(cls, t, name, text)


class Podcast(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.start_time = None

        req = requests.get("https://chat.radio-t.com/logs/radio-t-{self.id}.html".format(self=self))

        if req.status_code != 200:
            raise PodcastException("Can't get podcast metadata: {req.status_code} {req.content}".format(**locals()))

        self.doc = bs.BeautifulSoup(req.content)

        self.chat = chat = []
        for raw_msg in self.doc.body.table.findAll('tr'):
             chat.append(Message(raw_msg))
             print(raw_msg)



if __name__ == '__main__':
    p = Podcast(id=566)


