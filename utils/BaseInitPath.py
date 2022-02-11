import os


class InitPath:

    @classmethod
    def get_root_path(cls):
        return os.path.dirname(os.path.dirname(__file__))

    @classmethod
    def set_report_path(cls, report_path):
        cls.report_path = os.path.abspath(os.path.join(cls.get_root_path(), 'report', report_path))

    @classmethod
    def get_report_path(cls, report_path=''):
        return os.path.abspath(os.path.join(cls.get_root_path(), 'report', report_path))

    # @classmethod
    # def set_log_path(cls, log_path):
    #     cls.log_path = os.path.abspath(os.path.join(cls.get_root_path(), 'log', log_path))

    @classmethod
    def get_log_path(cls, log_path):
        return os.path.abspath(os.path.join(cls.get_root_path(), 'log', log_path))

    @classmethod
    def get_file_path(cls, file_path):
        return os.path.abspath(os.path.join(cls.get_root_path(), file_path))

    @classmethod
    def get_config_path(cls, filepath=''):
        return os.path.abspath(os.path.join(cls.get_root_path(), 'config', filepath))

    @classmethod
    def get_data_path(cls, filepath=''):
        return os.path.abspath(os.path.join(cls.get_root_path(), 'data', filepath))

    @classmethod
    def get_mitm_path(cls, filepath=''):
        return os.path.abspath(os.path.join(cls.get_root_path(), 'mitm', filepath))

    @classmethod
    def get_screen_path(cls, filepath=''):
        return os.path.abspath(os.path.join(cls.get_root_path(), 'screen', filepath))


if __name__ == '__main__':
    print(InitPath.get_root_path())
    print(InitPath.get_file_path('data\\data.cvs'))
    print(InitPath.get_config_path('config.ini'))
