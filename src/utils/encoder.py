class Encoder(object):
    """
    Encoder class is responsible for encoding
    """

    def __init__(self, use_unicode_escape):
        """
        One can specify weather to use unicode-escape encoding or not.

        :param use_unicode_escape: True to use unicode-escape else False
        """
        self.use_unicode_escape = use_unicode_escape

    def encode(self, string):
        """
        Encodes specified string.

        :param string: concrete string to encode
        :return: encoded string
        """

        if self.use_unicode_escape:
            return str(string.encode('unicode-escape'), 'utf-8')
        return ''.join(["\\u%s" % hex(ord(i))[2:].zfill(4) for i in string])
