import logging
import os
import sys

from contextlib import contextmanager

def start_log(log_location, log_type, event_name=None, to_file=True, to_stream=False):
    """
    Function that creates logs for analysts or controller.

    :param log_location: Location of the log (used only if to_file=`True`).
    :type log_location: str

    :param log_type: Which level of logging to initialize, default value is `error`.
    :type log_type: str

    :param event_name: name of event assigned to the analyst
    :type event_name: str, optional

    :param to_file: Should logs be written to a file? Default `True`.
    :type to_file: bool, optional

    :param to_stream: bool, should logs be written to stdout (e.g. for Kubernetes)? Default `False`.
    :type to_stream: bool, optional

    :return: python logger instance
    """

    if not to_file and not to_stream:
        raise ValueError("At least one of to_file or to_stream must be True.")

    logger_name = f"analyst_{event_name}" if event_name is not None else "controller_log"
    log = logging.getLogger(logger_name)

    if log.handlers:
        for handler in list(log.handlers):
            if isinstance(handler, logging.FileHandler):
                handler.close()
            log.removeHandler(handler)

    log_level = logging.ERROR
    if log_type == "debug":
        log_level = logging.DEBUG
    elif log_type == "info":
        log_level = logging.INFO
    elif log_type == "error":
        log_level = logging.ERROR

    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    log.setLevel(log_level)
    log.propagate = False

    if to_stream:
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        log.addHandler(ch)

    if to_file:
        if event_name is not None:
            filename = os.path.join(log_location, f"{event_name}_analyst.log")
        else:
            filename = os.path.join(log_location, "controller.log")

        if not os.path.isdir(log_location):
            os.makedirs(log_location)
        fh = logging.FileHandler(filename, encoding="utf-8")
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    log.info("Processing started. Opened log.")

    return log


def close_log(log):
    """
    Function that closes a log.

    :param log: logger instance to close
    """

    log.info("Processing complete.\n")

    for handler in list(log.handlers):
        if isinstance(handler, logging.FileHandler):
            handler.close()
        log.removeHandler(handler)


class StreamToLogger:
    """
    Written with the help of Claude.ai.

    File-like object that redirects writes to a logging.Logger instance,
    so that `print()` calls get captured into the same log.
    Important especially for capturing fitting packages print statments that
    inform on fitting progress.

    :param log: logger instance
    :type log: logging.Logger instance

    :param log_level: logging level
    :type log_level: logging level
    """

    def __init__(self, log, log_level=logging.INFO):
        self.log = log
        self.log_level = log_level
        self._buffer = ""

    def write(self, message):
        self._buffer += message
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line.strip():
                self.log.log(self.log_level, line.rstrip())

    def flush(self):
        if self._buffer.strip():
            self.log.log(self.log_level, self._buffer.rstrip())
        self._buffer = ""

    def isatty(self):
        return False


@contextmanager
def capture_prints(log, log_level=logging.INFO, capture_stderr=False):
    """
    Written with the help of Claude.ai.

    Context manager that redirects sys.stdout (and optionally sys.stderr)
    into the given logger for the duration of the `with` block.
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = StreamToLogger(log, log_level)
    if capture_stderr:
        sys.stderr = StreamToLogger(log, log_level)

    try:
        yield log
    finally:
        sys.stdout.flush()
        sys.stdout = old_stdout
        if capture_stderr:
            sys.stderr.flush()
            sys.stderr = old_stderr
