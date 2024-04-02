import os
import shutil
from glob import glob


def shorten(target_directory, target_length=256):
    absolute_target_directory = os.path.abspath(target_directory)
    glob_str = os.path.join(absolute_target_directory, '**/*')
    files = glob(glob_str, recursive=True)
    print('Shortening {} filenames... Please wait...'.format(len(files)))
    unshortenable_files = []
    for file in files:
        if os.path.isdir(file):
            continue
        filepath, filename_ext = os.path.split(file)
        filename, ext = os.path.splitext(filename_ext)
        total_length = len(file)
        if total_length <= target_length:
            continue
        else:
            length_difference = total_length - target_length
            filename_length = len(filename)
            if length_difference >= filename_length:
                unshortenable_files.append(file)
            else:
                new_filename = filename[:(filename_length-length_difference)]
                new_filename_ext = '{}{}'.format(new_filename, ext)
                new_file = os.path.join(filepath, new_filename_ext)
                optional_number = 0
                while os.path.exists(new_file):
                    optional_number += 1
                    optional_number_str = str(optional_number)
                    optional_number_str_length = len(optional_number_str)
                    new_filename = filename[:(filename_length-(length_difference + optional_number_str_length + 1))]
                    new_filename_ext = '{}_{}{}'.format(new_filename, optional_number_str, ext)
                    new_file = os.path.join(filepath, new_filename_ext)
                shutil.move(file, new_file)
    if len(unshortenable_files) > 0:
        print('Unable to shorten:')
        for unshortenable_file in unshortenable_files:
            print(unshortenable_file)
    print('Done.')


if __name__ == '__main__':
    shorten("/home/alex/Documents/test", 50)
