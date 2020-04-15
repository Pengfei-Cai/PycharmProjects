#!usr/bin/pthon3
# -*- coding: UTF-8 -*-
#!usr/bin/pthon3
# -*- coding: UTF-8 -*-
import os
from os.path import exists as file_exists
from tkinter import messagebox

from PIL import Image

def imShr(pheight, pwidth, inpath, outpath):
    img = Image.open(inpath)
    img_resize = img.resize((int(pheight), int(pwidth)), Image.ANTIALIAS)  # 调整尺寸
    imgn = 'cp' + os.path.basename(inpath)  # 操作文件后保存的名称
    os.path.isdir(outpath) or os.mkdir(outpath)
    opath = os.path.join(outpath, imgn)
    img_resize.save(opath)
    return imgn