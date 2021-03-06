"""
parser.py
Purpose: Conversion of RFC1459 messages to/from native objects.

Copyright (c) 2014, William Pitcock <nenolod@dereferenced.org>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""


class RFC1459Message(object):
    """
    Represents an IRC message.
    """

    def __init__(self, verb):
        self.verb = verb
        self.tags = {}
        self.source = None
        self.params = []
        self.client = None

    @classmethod
    def from_data(cls, verb, params=None, source=None, tags=None):
        """
        Create a new RFC1459Message from the given verb, parameters, and source
        having the given tags.
        """
        o = cls(verb)

        if params:
            o.params = params

        if source:
            o.source = source

        if tags:
            o.tags.update(**tags)

        return o

    @classmethod
    def from_message(cls, message):
        """
        Create a new RFC1459Message from an unparsed IRC line.
        """
        if isinstance(message, bytes):
            message = message.decode('UTF-8', 'replace')

        s = message.split(' ')

        tags = None
        if s[0].startswith('@'):
            tag_str = s[0][1:].split(';')
            s = s[1:]
            tags = {}

            for tag in tag_str:
                k, v = tag.split('=', 1)
                tags[k] = v

        source = None
        if s[0].startswith(':'):
            source = s[0][1:]
            s = s[1:]

        verb = s[0].upper()
        params = s[1:]

        for param in params:
            if param.startswith(':'):
                idx = params.index(param)
                arg = ' '.join(params[idx:])
                arg = arg[1:]
                params = params[:idx]
                params.append(arg)
                break

        return cls.from_data(verb, params, source, tags)

    def __str__(self):
        return 'RFC1459Message: verb={}, params={}, source={}'.format(self.verb, self.params, self.source)
