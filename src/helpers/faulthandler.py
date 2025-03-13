# This module contains helper functions for faulthandler
# This file is part of NeveBit

import faulthandler
import platform
from contextlib import contextmanager

@contextmanager
def faulthandler_context(enable=True, signal_trigger=None):
    """
    Context manager to enable/disable faulthandler.
    
    Args:
        enable (bool): Whether to enable faulthandler.
        signal_trigger (int, optional): Signal to trigger faulthandler traceback.
    """
    if enable:
        faulthandler.enable()
        if signal_trigger and platform.system() != "Windows":
            faulthandler.register(signal_trigger)
    try:
        yield
    finally:
        if enable:
            faulthandler.disable()
            if signal_trigger and platform.system() != "Windows":
                faulthandler.unregister(signal_trigger)