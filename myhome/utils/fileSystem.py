import random,time

# from docx import Document
# from docx.shared import Inches

# 接收上传文件
def upload(file):
    ext = file.name.split ('.').pop ()
    name = str (random.randint (10000, 99999) + time.time ()) + '.' + ext
    try:
        # 注意，这个路径和返回的路径不太一样，是真实路径
        with open (f'./static/assets/images/{name}', 'wb+') as fp:
            ## 分块写入文件
            for chunk in file.chunks ():
                fp.write (chunk)
        filename = f'/static/assets/images/{name}'
        print ("链接是", filename)
        return filename
    except Exception as e:
        print ("error is ", e)
        return None
