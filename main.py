import math
import os
import re
import shutil
from time import time


def file_base_name(file_name):
    return file_name if '.' not in file_name\
        else file_name.rsplit('.', 1)[0]


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def split_file(file_name: str, parts_num: int):
    # check parts_num
    try:
        parts_num = int(parts_num)
        if parts_num < 1 or parts_num > 10:
            raise BaseException
    except:
        print('Wrong number of parts. Choose number in range [1, 10]')
        return

    path = os.getcwd()  # current path
    file_base = file_base_name(file_name)

    # check file size (if it exists)
    try:
        file_size = os.stat(path + '/' + file_name).st_size
    except:
        print('No such file or directory')
        return

    dir_name = file_name + '_split'
    split_file_ext = '.sfsplt'

    # make directory for split files
    try:
        # remove non empty dir
        shutil.rmtree(path + '/' + dir_name)
    except:
        print('directory "' + dir_name + '" was created')
    else:
        print('directory "' + dir_name + '" was replaced')
    finally:
        os.mkdir(path + '/' + dir_name)

    time_start = time()
    with open(file_name, 'rb') as input_file:
        chunk_size = 1024
        pieces_in_file = math.ceil((file_size / chunk_size) / parts_num)
        piece_ind = 0
        file_ind = 1

        # TODO: optimize there
        for piece in read_in_chunks(input_file, chunk_size=chunk_size):
            if piece_ind > pieces_in_file:
                print('Part {} - ready!'.format(file_ind))
                file_ind += 1
                piece_ind = 0
            cur_file_path = path + '/' + dir_name + '/' + file_base \
                            + str(file_ind) + split_file_ext

            # splitting is really slow because of opening and
            # closing of this file for every 1-kilobyte chunk
            # f. e. merging is almost two times faster
            # TODO: move opening/closing out of here
            output_file = open(cur_file_path, "ab")
            output_file.write(piece)
            output_file.close()
            piece_ind += 1
        print('Part {} - ready!'.format(file_ind))

    print('That\'s all!')
    print('Check "' + dir_name + '" folder')
    print('Time elapsed: {:0.3f}s'.format(time() - time_start))


def merge_parts(dir_name: str):
    output_name = 'merged_' + re.sub('_split$', '', dir_name)
    output_file = open(output_name, 'wb')
    path = os.getcwd()  # current path
    dir_name = path + '/' + dir_name
    time_start = time()
    for ind, file_name in enumerate(sorted(os.listdir(dir_name)), 1):
        with open(dir_name + '/' + file_name, 'rb') as input_file:
            for piece in read_in_chunks(input_file, chunk_size=1024):
                output_file.write(piece)
            print('Part {} - merged!'.format(ind))
    output_file.close()
    print('That\'s all!')
    print('output file: ' + output_name)
    print('Time elapsed: {:0.3f}s'.format(time() - time_start))


if __name__ == '__main__':
    merge_parts('file.mkv_split')
    # split_file(file_name='file.mkv', parts_num=9)
