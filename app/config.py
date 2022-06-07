DB = {
    'host': "localhost",
    'user': "root",
    'passwd': "",
    'database': "ordenes",
}

class Configuration:
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB['user']}:{DB['passwd']}@{DB['host']}/{DB['database']}"