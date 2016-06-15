import glob
import os
import shutil


class Files:
    def __init__(self):
        pass

    @staticmethod
    def copy(src_dir, dst_dir, suffix):
        if not os.path.isdir(src_dir):
            raise 'not a directory'

        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)

        for file in glob.iglob(os.path.join(src_dir, suffix)):
            shutil.copy(file, dst_dir)
            print('copy {0} to {1}'.format(file, dst_dir))

    @staticmethod
    def delete(dir, files):
        for f in files:
            os.remove(os.path.join(dir, f))
