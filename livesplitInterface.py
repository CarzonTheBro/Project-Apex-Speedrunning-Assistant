import socket

class LiveSplitInterface:
    def __init__(self, host="127.0.0.1", port=16834):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        if self.socket is not None:
            return True

        try:
            self.socket = socket.create_connection(
                (self.host, self.port),
                timeout=5
            )
            print("[LiveSplitInterface] Connected.")
            return True

        except Exception as err:
            print(f"[LiveSplitInterface] Connection failed: {err}")
            self.socket = None
            return False

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            print("[LiveSplitInterface] Disconnected.")

    def _send(self, command):
        if not self.socket and not self.connect():
                return False

        try:
            self.socket.sendall(f"{command}\r\n".encode())
            return True

        except Exception as err:
            print(f"[LiveSplitInterface] Failed to send '{command}': {err}")
            self.disconnect()
            return False

    def start(self):
        return self._send("starttimer")

    def reset(self):
        return self._send("reset")

    def finish(self):
        return self._send("split")