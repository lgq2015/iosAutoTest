import logging
from utils.BaseInitPath import InitPath


def singleton(cls):
    instances = {}

    def _singleton(filename, **kw):
        key = filename + str(kw)
        print(key)
        if key not in instances.keys():
            instances[key] = cls(filename, **kw)
        return instances[key]

    return _singleton


@singleton
class Log:
    fh = st = None
    logger = logging.getLogger()
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }

    def __init__(self, filename, level='debug', show='all'):
        self.filename = filename
        self.level = level
        self.logger.setLevel(self.levels[level])  # Log等级总开关

        if show == 'stream':
            self.log_stream()
        elif show == 'file':
            self.log_file()
        else:
            self.log_file()
            self.log_stream()

    def log_file(self):
        log_path = InitPath().get_log_path(self.filename)
        if log_path is None:
            raise Exception('日志文件路径未找到')
        # 创建一个handler，用于写入日志文件
        self.fh = logging.FileHandler(filename=log_path, encoding='utf-8')
        self.fh.setLevel(self.levels[self.level])  # 输出到file的log等级的开关
        # 定义handler的输出格式
        formatter = logging.Formatter(f'%(asctime)s %(levelname)s : %(message)s')
        self.fh.setFormatter(formatter)
        # self.logger.addHandler(self.fh)  # 将logger添加到handler里面

    def log_stream(self):
        # 创建一个handler，用于输出到控制台
        self.st = logging.StreamHandler()
        self.st.setLevel(logging.DEBUG)
        formatter = logging.Formatter(f'%(asctime)s %(levelname)s : %(message)s')
        self.st.setFormatter(formatter)
        # self.logger.addHandler(self.st)

    def c(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def e(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def w(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def i(self, msg, *args, **kwargs):
        self.logger.addHandler(self.st)
        self.logger.addHandler(self.fh)

        self.logger.info(msg, *args, **kwargs)

        self.logger.removeHandler(self.st)
        self.logger.removeHandler(self.fh)

    def d(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)


if __name__ == '__main__':
    serial = 'infinix'
    # InitPath.set_log_path(log_path=serial)

    log = Log('infinix', level='info')
    log.i('log info')
    log2 = Log(filename='infinix2', level='info')
    log2.i('log2 debug')
    log.i('log info2')
    log3 = Log('infinix', level='info')
    log3.i('log3 info')

    print(id(log), id(log2), id(log3))
