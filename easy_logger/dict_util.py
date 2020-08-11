from collections.__init__ import OrderedDict


def add_prefix(log_dict: OrderedDict, prefix: str):
    with_prefix = OrderedDict()
    for key, val in log_dict.items():
        with_prefix[prefix + key] = val
    return with_prefix


def append_log(log_dict, to_add_dict, prefix=None):
    if prefix is not None:
        to_add_dict = add_prefix(to_add_dict, prefix=prefix)
    return log_dict.update(to_add_dict)