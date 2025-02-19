import logging
from colorlog import ColoredFormatter
import inspect
import os

class Logger:
    def __init__(self):
        self.loggers = {}

    def get_logger(self):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        script_name = os.path.basename(module.__file__) if module and module.__file__ else None
        function_name = frame.function
        class_name = frame.frame.f_locals.get('self', None).__class__.__name__ if 'self' in frame.frame.f_locals else None

        if script_name:
            script_name = os.path.splitext(script_name)[0]

        logger_name = f"{script_name}.{class_name}.{function_name}" if class_name else f"{script_name}.{function_name}"

        if logger_name not in self.loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            # Create formatter with colors
            if script_name is None:
                formatter = ColoredFormatter(
                    '%(log_color)s %(levelname)s [%(asctime)s] [%(filename)s] %(message)s',
                    datefmt='%a %Y-%m-%d %H:%M:%S',
                    log_colors={
                        'DEBUG': 'cyan',
                        'INFO': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red',
                    }
                )
            else:
                formatter = ColoredFormatter(
                    datefmt='%a %Y-%m-%d %H:%M:%S',
                    log_colors={
                        'DEBUG': 'cyan',
                        'INFO': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'bold_red',
                    }
                )

            # Add formatter to ch
            ch.setFormatter(formatter)

            # Add ch to logger
            logger.addHandler(ch)

            self.loggers[logger_name] = logger

        return self.loggers[logger_name]