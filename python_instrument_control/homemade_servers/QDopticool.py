# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 16:37:09 2025

@author: Prof. Wang
"""

import MultiPyVu as mpv
import sys

class Opticool(mpv.Client):
    def __init__(self, host='169.254.170.239', port=5000):
        super().__init__(host, port)
        self._connected = False
        self.connect()

    def connect(self):
        if not self._connected:
            try:
                super().__enter__()
                self._connected = True
            except Exception as e:
                super().__exit__(*sys.exc_info())
                raise ConnectionError(f"Failed to connect: {e}")

    def close(self):
        if self._connected:
            try:
                super().__exit__(None, None, None)
            finally:
                self._connected = False

    def __del__(self):
        # Ensure cleanup if disconnect wasn't called
        if self._connected:
            try:
                self.disconnect()
            except Exception:
                pass
