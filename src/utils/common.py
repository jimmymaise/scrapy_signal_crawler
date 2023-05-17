import re
import time


def reverse_format_string(format_template, formated_string):
    reg_keys = "{([^{}:]+)[^{}]*}"
    reg_fmts = "{[^{}:]+[^{}]*}"
    pat_keys = re.compile(reg_keys)
    pat_fmts = re.compile(reg_fmts)

    keys = pat_keys.findall(format_template)
    lmts = pat_fmts.split(format_template)
    temp = formated_string
    values = []
    for lmt in lmts:
        if not len(lmt) == 0:
            value, temp = temp.split(lmt, 1)
            if len(value) > 0:
                values.append(value)
    if len(temp) > 0:
        values.append(temp)
    return dict(zip(keys, values))


class SimpleCache:
    def __init__(self):
        self.cache = {}

    def set(self, key, value, expire_time_in_sec=None):
        expire_time_in_sec = expire_time_in_sec or 0
        self.cache[key] = {"value": value, "expire_time": time.time() + expire_time_in_sec}

    def get(self, key):
        data = self.cache.get(key)
        if data and data["expire_time"] >= time.time():
            return data["value"]
        else:
            self.delete(key)

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
