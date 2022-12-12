
from django.core.serializers import serialize
from collections.abc import Iterable
from json import loads

# 序列化数据集对象
def serialize_models(modelsObj):
    try:
        # 可迭代对象是转换成列表，否则转换成字典
        if isinstance(modelsObj, Iterable):
            # 序列化成列表格式
            modelsObj = loads (serialize ("json", modelsObj))
            # 清洗列表数据(列表推导式)
            modelsObj = [{'id': item["pk"], **item["fields"]} for item in modelsObj]
        else:
            modelsObj = {key: value for key, value in modelsObj.__dict__.items () if key != '_state'}
        return modelsObj
    except Exception as e:
        print("序列化数据集对象异常",e)
        return None