""" 全局基础配置
json_dumps: 不同类型数据在序列化成 json 字符串时的格式化方法
log:        日志配置
"""

from . import json_dumps, log
from .config import Config

config = Config()
log.remove_config('DEBUG' if config.DEBUG else 'INFO')

__all__ = ['config']