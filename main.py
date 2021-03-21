import asyncio
import logging
import sys

from api import LoxApp, LoxWs
import qasync
from PyQt5 import uic
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow
from qasync import asyncSlot, asyncClose
import traceback
import json

logging.getLogger('asyncio').setLevel(logging.ERROR)
logging.getLogger('asyncio.coroutines').setLevel(logging.ERROR)
logging.getLogger('websockets.server').setLevel(logging.ERROR)
logging.getLogger('websockets.protocol').setLevel(logging.ERROR)


class LoxoneConnecionGui(QMainWindow):
    def __init__(self):
        super(LoxoneConnecionGui, self).__init__()
        uic.loadUi('Main.ui', self)
        # self.log.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        # logging.getLogger().addHandler(self.log)
        # logging.getLogger().setLevel(logging.DEBUG)

        self.api = None
        self.show()

    @asyncSlot()
    async def message_callback(self, data):
        print(data)
        if isinstance(data, dict):
            for k, v in data.items():
                self.log.appendPlainText("{} : {}".format(k, v))
        else:
            self.log.appendPlainText(str(data))

    @asyncClose
    async def closeEvent(self, event):
        try:
            await self.api.stop()
        except:
            pass
        loop = asyncio.get_running_loop()
        loop.close()

    @asyncSlot()
    async def disconnect_from_loxone(self):
        if self.api is not None and self.api.state != "CLOSED":
            await self.api.stop()

    @asyncSlot()
    async def connect_to_loxone(self):
        if self.api is not None and self.api.state == "CONNECTED":
            self.log.appendPlainText("Already connected...")
            return True

        username = self.user.text()
        password = self.password.text()
        ip = self.ip.text()
        port = self.port.text()

        lox_config = LoxApp()
        lox_config.lox_user = username
        lox_config.lox_pass = password
        lox_config.host = ip
        lox_config.port = port
        self.json_txt.clear()
        self.log.clear()
        self.log.appendPlainText("Try to connect...")

        try:
            request_code = await lox_config.getJson()
            if request_code == 200 or request_code == "200":

                self.log.appendPlainText("Got Config from Loxone. Port and Host ok.")
                self.json_txt.setText(json.dumps(lox_config.json, indent=4, sort_keys=False, ensure_ascii=False))
                self.api = LoxWs(user=username,
                                 password=password,
                                 host=ip,
                                 port=port,
                                 loxconfig=lox_config.json,
                                 loxone_url=lox_config.url)

                res = await self.api.async_init()
                self.log.appendPlainText("Res {}".format(res))
                if not res or res == -1:
                    self.log.appendPlainText("Error connecting to loxone miniserver #1")
                    return False
                self.api.message_call_back = self.message_callback
                await self.api.start()

            else:
                self.log.appendPlainText(f"Request Code {request_code}. Could not connect to Loxone.")

        except:
            traceback.print_exc()
            t = traceback.format_exc()
            self.log.appendPlainText(str(t))


async def main():
    loop = asyncio.get_running_loop()
    # app = QApplication(sys.argv)
    dark_palette = QPalette()
    # dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    # dark_palette.setColor(QPalette.WindowText, Qt.white)
    # dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    # dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    # dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    # dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    # dark_palette.setColor(QPalette.Text, Qt.white)
    # dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    # dark_palette.setColor(QPalette.ButtonText, Qt.white)
    # dark_palette.setColor(QPalette.BrightText, Qt.red)
    # dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    # dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    # dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    # app.setPalette(dark_palette)
    window = LoxoneConnecionGui()
    window.show()
    await loop.create_future()
    # app.exec_()


if __name__ == '__main__':
    qasync.run(main())
