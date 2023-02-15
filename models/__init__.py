"""

By Allen Tao
Created at 2023/02/10 15:37
"""

from pathlib import Path

__all__ = [p.stem for p in Path(__file__).parent.glob('[!_]*.py')]


def register_all():
    import importlib
    for model in __all__:
        importlib.import_module(f'models.{model}')
