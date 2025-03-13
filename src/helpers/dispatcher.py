# Simple global event dispatcher for event propagation
# This file is part of NeveBit.

import logging


class GlobalEventDispatcher:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalEventDispatcher, cls).__new__(cls)
            cls._instance.logger = logging.getLogger('NeveBit')
            cls._instance.listeners = {}
            cls._instance.last_event_status = {}
        return cls._instance

    def sub(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unsub(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)
            if not self.listeners[event_type]:
                del self.listeners[event_type]

    def pub(self, event_type, *args, **kwargs):
        if args:
            self.last_event_status[event_type] = args[0]
        else:
            self.last_event_status[event_type] = None

        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                try:
                    listener(*args, **kwargs)
                except Exception as e:
                    listener_name = listener.__name__ if hasattr(listener, '__name__') else str(listener)
                    self.logger.error(f"Error dispatching to listener '{listener_name}' for event type '{event_type}'")
                    self.logger.error(f"{type(e).__name__}: {e}")
                    self.logger.debug(f"Event args: {args} Event kwargs: {kwargs}")

    def get_event(self, event_type):
        event = self.last_event_status.get(event_type, None)
        return event
