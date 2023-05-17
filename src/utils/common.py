import re


def reverse_format_string(format_template, formated_string):
    reg_keys = '{([^{}:]+)[^{}]*}'
    reg_fmts = '{[^{}:]+[^{}]*}'
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
