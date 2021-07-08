from typing import List, TypeVar

T = TypeVar('T')


def flatten(items: List[List[T]]) -> List[T]:
    res = []
    for item in items:
        res.extend(item)
    return res


def objectify(source_obj):
    if isinstance(source_obj, list):
        source_obj = [objectify(item) for item in source_obj]

    if not isinstance(source_obj, dict):
        return source_obj

    class Obj(object):
        def __getattr__(self, item):
            return None

    obj = Obj()

    for key in source_obj:
        obj.__dict__[key] = objectify(source_obj[key])

    return obj

