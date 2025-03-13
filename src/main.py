#
# This file is part of NeveBit.
# Copyright (C) 2024 SlimeCodex
#
# NeveBit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeveBit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeveBit. If not, see <https://www.gnu.org/licenses/>.
#

import sys
import asyncio
import signal
import platform

import qasync
from PyQt6.QtWidgets import QApplication

from gui.windows.win_main import MainWindow
from helpers import faulthandler_context

if __name__ == "__main__":
    # Enable faulthandler for debugging
    # Note: Disable this for production builds
    enable_faulthandler = True

    # Signal trigger for faulthandler traceback
    signal_trigger = None if platform.system() == "Windows" else signal.SIGUSR1

    # Run the application
    with faulthandler_context(enable=enable_faulthandler, signal_trigger=signal_trigger):
        cmd_args = sys.argv[1:]
        app = QApplication(sys.argv)
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)
        main_win = MainWindow(app, arguments=cmd_args)
        sys.excepthook = main_win.exception_hook
        main_win.show()
        with loop:
            sys.exit(loop.run_forever())
