import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or b"\xb0\xb3\n\xe1\xeep'\xdc\x9a\x1bm\xa4\xce\x81\xd5\x9fW^\xd0h"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or b'\x1c\x7f~\xe6\xb5<P3,9\x80\x15nXQEvK\x11%\xabF\x17\x8fc\xdc@2\x91\xe6'
    JWT_ERROR_MESSAGE_KEY = "error"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
