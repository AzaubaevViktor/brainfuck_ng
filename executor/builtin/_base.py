from typing import Dict, Type


class BaseModule:
    NAME = None
    about = "This is base module, please inherit from them"

    modules: Dict[str, Type["BaseModule"]] = {}

    dependencies = None

    def __init_subclass__(cls, **kwargs):
        print("Register this please:", cls, kwargs)
        if cls.NAME:
            cls.modules[cls.NAME] = cls

    def __call__(self, variables):
        raise NotImplementedError()

    def shutdown(self):
        # Not realized in executor, sorry
        raise NotImplementedError()
