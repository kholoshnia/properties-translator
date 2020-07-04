import os
import re
import googletrans
from googletrans import Translator


def reformat(before, after):
    """
    Formats new line from old line format. Keeps track of spaces near "=" and new lines. Also adds spaces at the
    beginning of the line.

    :param before: old line
    :param after: new line
    :return: new line with format of old one
    """

    search = re.search('^\\s+', before)
    if search:
        after = search.group() + after

    search = re.search('(?<!^)\\s+=', before)
    if search:
        after = after.replace('=', search.group())

    search = re.search('=\\s+(?!$)', before)
    if search:
        after = after.replace('=', search.group())

    if before == '\n':
        after = before

    return after


def need_translation(file_name, src):
    """
    Checks if a translation is needed for the file with the specified name.

    :param file_name: name of the file
    :param src: source language
    :return: True if file needs to be translated else False
    """

    file_name = os.path.splitext(file_name)[0]

    if file_name.endswith('_' + src) or src == 'auto':
        return True
    return False


def get_path(directory, file_name, dest):
    """
    Returns output path with file name including destination language suffix.

    :param directory: input directory
    :param file_name: name of the file
    :param dest: destination language
    :return: output path
    """

    out_name = re.sub('_.{2}(?:_.{2})?$', '', os.path.splitext(file_name)[0])
    out_name = '{}_{}.properties'.format(os.path.splitext(out_name)[0], dest)
    out_path = os.path.join(directory, out_name)

    return out_path


class Proptrans(object):
    """
    Proptrans class is responsible for actions connected with languages or Google API usage.
    """

    def __init__(self):
        """
        Setups translator from Google API and receives all supported languages.
        """

        self.translator = Translator()
        self.languages = googletrans.LANGUAGES

    def check_language(self, language):
        """
        Checks if Google Translate API supports specified language.

        :param language: concrete language
        :return: True if language is supported by Google API else False
        """

        if language in self.languages:
            return True
        return False

    def translate(self, value, src='auto', dest='en'):
        """
        Translates value of properties file line. Also keeps track of incorrect sentence capitalization after
        translation and adds trailing spaces to the result in accordance with the source value. Also, replaces all
        string format special symbols such as "% s" with "% s".

        :param value: value of properties file line
        :param src: source language
        :param dest: destination language
        :return: translated and formatted value
        """

        string = value.strip()
        result = self.translator.translate(string, src=src, dest=dest).text

        result = result.strip().lower().replace('% d', ' %d')
        result = result.strip().lower().replace('% s', ' %s')
        result = result.strip().lower().replace('% f', ' %f')
        result = result.strip().lower().replace('% x', ' %x')
        result = result.strip().lower().replace('% c', ' %c')
        result = result.strip().lower().replace('% o', ' %o')

        if string[0].isupper():
            result = result.capitalize()
        else:
            result = result[0].lower() + result[1:]

        if re.search('\\.$', string):
            if not re.search('\\.$', result):
                result += '.'
        else:
            result = re.sub('\\.$', '', result)

        search = re.search('\\s+$', value)
        if search:
            result = result.strip() + search.group()

        return result
