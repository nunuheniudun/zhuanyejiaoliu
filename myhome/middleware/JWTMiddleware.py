import jwt
import datetime

# 加密密钥
secret_key = 'django123456'


# 一、生成token密钥
# 传入的数据为 use_id 最好不要添加其它参数，否则会超过最大值240， 目前是 176长度
# 可修改参数：  valid_days  有效期天数可以修改，  secret_key   服务器密钥也可以修改
## data为字典数据
# 1.有效载核，存放有效信息   2.密钥字串， 服务端被重置时的合法性      3.sinature签名算法
# 返回token字符串值 和 token数据
def make_jwt(user_id):
    try:
        global secret_key
        now_time = datetime.datetime.now ()
        str_now_time = datetime.datetime.strftime (now_time, '%Y-%m-%d %H:%M:%S')
        token_input_data = {
            'user_id': user_id,  # 用户ID,或者其它参数
            'now_time': str_now_time,  ## 当前的用户登录信息, 日期字符串
            'valid_days': 15  # 天数 days
        }
        encoded_jwt = jwt.encode (token_input_data, secret_key, algorithm='HS256')
        if type (encoded_jwt) != str:  ## 转换成普通的string字符串
            encoded_jwt = str (encoded_jwt, encoding="utf-8")
        return encoded_jwt
    except Exception as e:
        print("错误是",e)
        return None


# 二、解析token密钥
## str_token 为token字符串
## 返回验证结果 user_data /  None
def parse_jwt(str_token):
    try:
        global secret_key
        if type (str_token) != bytes:
            str_token = bytes (str_token, encoding='utf8')
            # 解密token
        token_output_data = jwt.decode (str_token, secret_key, algorithms=['HS256'])
        # 检测token的有效性
        str_pass_time = token_output_data.get ('now_time', None)
        str_valid_days = token_output_data.get ('valid_days', None)
        if len (str_pass_time) == 0 or str (str_valid_days) == 0:
            raise Exception ('error')
        obj_pass_time = datetime.datetime.strptime (str_pass_time, '%Y-%m-%d %H:%M:%S')
        obj_valid_time = obj_pass_time + datetime.timedelta (days=str_valid_days)
        now_time = datetime.datetime.now ()
        if obj_valid_time < now_time:
            raise Exception ('error')
        else:
            return token_output_data
    except Exception as e:
        print("错误是",e)
        return None


# 三、jwt直接获取 user_id 参数值
# 获取 token,   META 获取数据  ”HTTP_ + header字段名称大写“
# 使用.get获取与是否在请求中使用get方法无关
def get_parse_token(request):
    try:
        global secret_key
        str_token = request.META.get ('HTTP_TOKEN',None)
        if type (str_token) != bytes:
            str_token = bytes (str_token, encoding='utf8')
            token_output_data = jwt.decode (str_token, secret_key, algorithms=['HS256'])
            return token_output_data['user_id']
    except Exception as e:
        print("错误是",e)
        return None