import logging, os
import sys
import logging.handlers


class Logger:
    def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        # 设置创建日志的对象
        self.logger = logging.getLogger(path)
        if logging.handlers:
            # 设置日志的最低级别低于这个级别将不会在屏幕输出，也不会保存到log文件
            self.logger.setLevel(logging.DEBUG)
            # 给这个handler选择一个格式（）
            fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
            # 设置终端日志 像终端输出的日志
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)  # 设置个终端日志的格式
            sh.setLevel(clevel)  # 设置终端日志最低等级
            # 设置文件日志 用于向一个文件输出日志信息。不过FileHandler会帮你打开这个文件。
            fh = logging.FileHandler(path)
            fh.setFormatter(fmt)  # 设置个文件日志的格式
            fh.setLevel(Flevel)  # 设置终端日志最低等级
            self.logger.addHandler(sh)  # 增加终端日志Handler
            self.logger.addHandler(fh)  # 增加文件日志Handler

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


my_log = Logger('E:\earth_python\earth_auto\earth_auto.txt', logging.ERROR, logging.DEBUG)

if __name__ == '__main__':

    my_log.debug('一个debug信息')
    my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
    my_log.war('一个warning信息')
    my_log.error('一个error信息')
    my_log.cri('一个致命critical信息')