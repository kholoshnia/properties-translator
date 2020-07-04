import os
import re
from utils.encoder import Encoder
from utils.proptrans import Proptrans, reformat, need_translation, get_path


def process_file(directory, file_name, src, destinations, translator, encoder, keep_format, do_encode):
    """
    Processes specified file. Translates properties file in accordance with specified parameters.

    :param directory: directory where properties files are stored
    :param file_name: name of the file
    :param src: source languages
    :param destinations: destination languages
    :param translator: concrete translator
    :param encoder: concrete encoder
    :param keep_format: whether to keep format of the specified file
    :param do_encode: whether to do encode or not
    """

    for source in src:
        if need_translation(file_name, source):
            in_path = os.path.join(directory, file_name)
            with open(in_path, 'r', encoding='utf-8') as f_in:
                for dest in destinations:
                    print('Processing file: "{}".'.format(file_name))
                    print('Translating from {} into {} language.'.format(source, dest))
                    print()

                    new_lines = []
                    for line in f_in:
                        if line.strip().startswith('#'):
                            new_line = line.strip() + '\n'
                        elif line == '\n':
                            new_line = line
                        else:
                            split = line.split('=', 1)

                            if len(split) != 2 or split[1].strip() == '':
                                new_line = re.sub('\\s+=\\s+', '=\n', line)
                            else:
                                key = split[0]
                                value = split[1].replace('\n', '')
                                value = translator.translate(value, source, dest)

                                if do_encode:
                                    value = encoder.encode(value)
                                new_line = key.strip() + '=' + value + '\n'

                        if keep_format:
                            new_line = reformat(line, new_line)
                        elif new_line.startswith('#'):
                            new_line = new_line.strip() + '\n'
                        elif new_line == '\n':
                            continue

                        new_lines.append(new_line)

                    out_path = get_path(directory, file_name, dest)
                    with open(out_path, 'w', encoding='utf-8') as f_out:
                        f_out.writelines(new_lines)

                    f_in.seek(0)
        else:
            print("File \"{}\" does not need translation, skipping.".format(file_name))


def main():
    """
    The main class that receives user input
    """

    translator = Proptrans()

    directory = input('Enter the source directory with the properties file or file paths separated by commas: ').strip()
    if os.path.isdir(directory):
        try:
            dir_list = os.listdir(directory)
        except FileNotFoundError:
            print("The entered directory was not found.")
            return
        except NotADirectoryError:
            print("The specified path is not a directory.")
            return
    else:
        dir_list = directory.split(',')
        for el in dir_list:
            el = el.strip()
            if not os.path.exists(el):
                print("File or directory path \"{}\" does not exist.".format(el))
                return

    src = input('Enter the source languages separated by commas or leave it blank for auto selection: ').strip()
    if src.strip() == '':
        src = ['auto']
    else:
        src = src.split(',')
        for el in src:
            el = el.strip()
            if not translator.check_language(el) and not translator.check_language(el.split('_')[0]):
                print('Wrong source language: {}.'.format(el))
                return

    destinations = input('Enter destination languages separated by commas: ').strip().split(',')
    if len(destinations) == 0:
        print('No destination languages found.')
        return
    destinations = [el.strip() for el in destinations]
    for dest in destinations:
        if not translator.check_language(dest) and not translator.check_language(dest.split('_')[0]):
            print('Wrong destination language: {}.'.format(dest))
            return

    keep_format = input('Keep source file format? [y/n]: ')

    if keep_format == 'y':
        keep_format = True
    else:
        keep_format = False

    do_encode = input('Encode values? [y/n]: ')

    if do_encode == 'y':
        do_encode = True

        use_unicode_escape = input('Use unicode-escape to encode values? [y/n]: ')
        if use_unicode_escape == 'y':
            use_unicode_escape = True
        else:
            use_unicode_escape = False
    else:
        do_encode = False
        use_unicode_escape = False

    print()
    encoder = Encoder(use_unicode_escape)

    for file_name in dir_list:
        file_name = file_name.strip()
        if file_name.endswith('.properties'):
            process_file(directory, file_name, src, destinations, translator, encoder, keep_format, do_encode)
        else:
            print("File \"{}\" is not a properties file, skipping.".format(file_name))
            print()

    print('All files have been processed successfully.')


if __name__ == '__main__':
    main()
