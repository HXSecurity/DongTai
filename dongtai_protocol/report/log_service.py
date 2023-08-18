import logging
import socket

logger = logging.getLogger("dongtai.openapi")


class LogService:
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None

    def create_socket(self):
        if self.socket:
            return None

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((self.host, self.port))
            sock.setblocking(False)
            self.socket = sock
        except OSError:
            logger.exception(f"failed to connect log service {self.host}:{self.port}")
            self.socket = None
            sock.close()
            return False
        else:
            return True

    def __del__(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def send(self, message):
        try:
            if not self.socket:
                self.create_socket()
            if self.socket:
                self.socket.sendall(bytes(message + "\n", encoding="utf-8"), socket.MSG_DONTWAIT)
                return True
        except Exception as e:
            logger.exception("failed to send message to log service", exc_info=e)
            if self.socket:
                self.socket.close()
            self.socket = None
            return False
