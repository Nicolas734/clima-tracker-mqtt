from os import getcwd
from time import sleep
from threading       import Lock
from sys             import exc_info
from traceback       import format_exc
from datetime        import datetime



class Logger():
    DEFAULT_LOG = "clima-tracker.log"
    def __init__(self, log_file: bool = True, log_dir: str = getcwd()+"/log/") -> None:
        self._log_dir = log_dir
        self._log_file = log_file
        self._console = None
        self._lock = Lock()


    def _build_message(self, txt):
        """Build the standard log message."""
        now = datetime.now()
        msg = '[{0}.{1:3.0f}] {2}\n'.format(now.strftime('%Y-%m-%d %H:%M:%S'), now.microsecond / 1000, txt)
        return msg

    def log(self, txt: str, arq: str=DEFAULT_LOG, flush: bool=False):
        """Guarantee the log and print, if need."""
        msg = None
        if self._log_file:
            if self._lock.acquire(timeout=30):
                try:
                    msg = self._send_to_file(self._build_message(txt), arq, flush)
                except Exception as e:
                    _line = exc_info()[2].tb_lineno
                    msg = '[EXCEPTION] - Logger >> on Debug log txt print \n Line: {} Error: {}\n{}'.format( _line, e, format_exc())
                    if self._console:
                        self._console(str(msg).encode('utf-8'))
                finally:
                    self._lock.release()
            else:
                if self._console:
                    self._console(self._build_message(txt))
        else:
            msg = self._build_message(txt)
        if msg is not None:
            if self._console:
                self._console(str(msg))

    def _send_to_file(self, txt: str, arq: str=DEFAULT_LOG, flush: bool=False):
        """Define a common point of file record."""
        with open(self._log_dir + arq, 'a', encoding='UTF-8') as _f:
            _f.write(txt)
            _f.flush()
            sleep(1)
        return txt