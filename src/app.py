import os
from tqdm import tqdm
from googletrans import Translator


def process_file(file_name, source, destinations, translator, replace_format, do_encode, use_unicode_escape):
    for destination in destinations:
        path, name = os.path.split(file_name)
        print('\nProcessing file: {}'.format(name))
        name = os.path.splitext(name)[0]
        new_name = '{}_{}.properties'.format(name, destination)
        new_path = os.path.join(path, new_name)

        f_in = open(file_name, 'r')
        f_out = open(new_path, 'w')

        for line in tqdm(f_in):
            if line.startswith('#'):
                new_line = line
            elif line == '\n':
                new_line = '\n'
            else:
                line = line.split('=', 1)
                new_line = line[0] + '= '
                result = translator.translate(line[1], src=source, dest=destination).text

                if replace_format:
                    result = result.replace('% s', ' %s')

                if use_unicode_escape:
                    result = str(result.encode('unicode-escape'), 'utf-8')
                elif do_encode:
                    result = ''.join(["\\u%s" % hex(ord(i))[2:].zfill(4) for i in result])

                new_line += result + '\n'

            f_out.write(new_line)


def main():
    path = input('Input source properties file path: ').strip()
    source = input('Input source language: ').strip()
    destinations = input('Input destination languages: ').split()
    destinations = [i.strip() for i in destinations]
    replace_format = input('Replace string format characters after google translate (\'% s\' -> \' %s\')? [y/n]: ')

    if replace_format == 'y':
        replace_format = True
    else:
        replace_format = False

    do_encode = input('Encode? [y/n]: ')

    if do_encode == 'y':
        use_unicode_escape = input('Use unicode-escape? [y/n]: ')
        if use_unicode_escape == 'y':
            use_unicode_escape = True
        else:
            use_unicode_escape = False
        do_encode = True
    else:
        do_encode = False
        use_unicode_escape = False

    translator = Translator()
    dir_list = os.listdir(path)
    for file_name in dir_list:
        if 'properties' in file_name:
            file_name = os.path.join(path, file_name)
            process_file(file_name, source, destinations, translator, replace_format, do_encode, use_unicode_escape)


if __name__ == '__main__':
    main()
