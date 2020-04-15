#!usr/bin/pthon3
# -*- coding: UTF-8 -*-
import os
import time

from PIL import Image
from Imge.Function import imShr
from flask import Flask, jsonify, request
from flask import send_from_directory, abort
from werkzeug.utils import secure_filename

#设置路径以及上传文件后缀
app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



#下载文件
@app.route("/api/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('upload', filename)):
            return send_from_directory('upload', filename, as_attachment=True) #最后的参数是改变名称的开关
    abort(404)


# 上传文件
@app.route('/api/upload', methods=['POST'], strict_slashes=False)# 对URL最后的 / 符号是否严格要求
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])#上传文件目的路径
    hei = request.form.get('pheight')
    wid = request.form.get('pwidth')

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值

    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型

        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名

        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        ipath = file_dir + '\\' + new_filename#获取上传目的文件路径

        img = Image.open(ipath)
        oriH = img.size[0]
        oriW = img.size[1]
        if not hei.isdecimal() and wid.isdecimal():
            return '<script>alert("数据类型错误")</script>'
        elif oriH < int(hei) or oriW < int(wid):
            return '<script>alert("宽或高超出界限")</script>'
        fileName = "/api/download/" + imShr(hei, wid,ipath, file_dir)#获取图片变更后的路径+名称
        return '<br><a href=' + fileName + '>下载</a>'
    else:
        return jsonify({"code": 1001, "errmsg": "上传失败","he": request.form('pheight')})

if __name__ == '__main__':
    app.run(debug=True)
