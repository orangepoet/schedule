# -*- coding: utf-8 -*-
# -*- coding: uft-8 -*-

import glob
import os
import shutil


def copy(src_dir, dst_dir, suffix):
    if not os.path.isdir(src_dir):
        raise ValueError('not a directory')

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    for f in glob.iglob(os.path.join(src_dir, suffix)):
        shutil.copy(f, dst_dir)
        print('copy {0} to {1}'.format(f, dst_dir))


def delete(dir, files):
    for f in files:
        os.remove(os.path.join(dir, f))
