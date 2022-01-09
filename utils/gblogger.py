import os


class GBLogger:
    __names = set()

    def __init__(self, name, use_file=False, file_path=None):
        if name in self.__names:
            raise KeyError(f"duplicated logger name: {name}")
        self.__names.add(name)
        self.name = name
        self.use_file = use_file
        if use_file:
            if file_path is None:
                file_path = os.path.join(os.getcwd(), 'logs')
            os.makedirs(file_path, exist_ok=True)
            self.file = open(os.path.join(file_path, name + '.log'), 'w')
        self.allow_debug = False
        self.allow_info = True
        self.allow_warning = True
        self.allow_fatal = True

    def __log_to_file(self, msg, msg_type):
        if self.use_file:
            self.file.write(self.__prep_file(msg, msg_type))
            self.file.flush()

    def __print(self, msg, msg_type):
        print(self.__prep_print(msg, msg_type))

    def __full_proc(self, msg, msg_type, should_print):
        if should_print:
            self.__print(msg, msg_type)
        self.__log_to_file(msg, msg_type)

    def __prep_print(self, msg, msg_type):
        return f'[{self.name}:{msg_type}] {msg}'

    def __prep_file(self, msg, msg_type):
        return f'[{msg_type}] {msg}\r\n'

    def debug(self, msg):
        self.__full_proc(msg, 'DEBUG', self.allow_debug)

    def info(self, msg):
        self.__full_proc(msg, 'INFO', self.allow_info)

    def warning(self, msg):
        self.__full_proc(msg, 'WARN', self.allow_warning)

    def fatal(self, msg):
        self.__full_proc(msg, 'FATAL', self.allow_fatal)
