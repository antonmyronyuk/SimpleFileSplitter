import os
import shutil
import re


def file_base_name(file_name):
    return file_name if '.' not in file_name\
        else file_name.rsplit('.', 1)[0]


def parts_sizes(file_size, parts_num):
    part = file_size // parts_num
    return [part for i in range(parts_num - 1)]\
        + [file_size - (part * (parts_num - 1))]  # last size


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

    # check file
    try:
        file_size = os.stat(path + '/' + file_name).st_size
    except:
        print('No such file or directory')
        return

    dir_name = file_name + '_split'
    split_file_ext = '.sfsplt'

    # make directory for split files
    try:
        # os.rmdir(path + '/' + dir_name)
        # remove non empty dir
        shutil.rmtree(path + '/' + dir_name)
        os.mkdir(path + '/' + dir_name)
        print('directory "' + dir_name + '" was replaced')
    except:
        os.mkdir(path + '/' + dir_name)
        print('directory "' + dir_name + '" was created')

    '''
    print('size: ' + str(file_size))
    print(parts_sizes(1345, 7))
    print(sum(parts_sizes(1345, 7)))
    '''
    parts = parts_sizes(file_size, parts_num)
    with open(file_name, 'rb') as f:
        for i in range(parts_num):
            chunk = f.read(parts[i])
            cur_file_path = path + '/' + dir_name + '/' + file_base + str(i) + split_file_ext
            output_file = open(cur_file_path, "wb")
            output_file.write(chunk)
            output_file.close()
            print('Part {} - ready!'.format(i + 1))

    print('That\'s all!')
    print('Check "' + dir_name + '" folder')


def merge_parts(dir_name: str):
    output_name = 'merged_' + re.sub('_split$', '', dir_name)
    output_file = open(output_name, 'wb')
    print('output file: ' + output_name)
    path = os.getcwd()  # current path
    dir_name = path + '/' + dir_name
    for ind, file in enumerate(os.listdir(dir_name), 1):
        with open(dir_name + '/' + file, 'rb') as f:
            output_file.write(f.read())
            print('Part {} - merged!'.format(ind))
    output_file.close()
    print('That\'s all!')


if __name__ == '__main__':
    # split_file(file_name='file.avi', parts_num=7)
    merge_parts('file.avi_split')
