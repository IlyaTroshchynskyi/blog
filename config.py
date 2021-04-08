class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/test1'
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/test1'
    # mysql -  название базы данных
    # mysqlconnector - названиедрайвера типа как мост для SQL
    # root - имя пользоветаеля базы данных
    # 12345 - пароль
    # localhost - адресс сервера
    # test1 - имя базы данных
    SECRET_KEY = 'something_very_secret'
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
