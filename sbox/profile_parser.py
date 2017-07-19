import json


def parse_profile(path: str) -> dict:
    if path == "":
        return dict()

    with open(path) as file:
        try:
            opts = json.loads(file.read())
            return opts
        except json.JSONDecodeError:
            return dict()


def merge_dicts(low: dict, high: dict) -> dict:
    ret = dict()

    for key in low:
        ret[key] = low[key]

    for key in high:
        if isinstance(high[key], dict):
            ret[key] = merge_dicts(low[key], high[key])
        elif isinstance(high[key], list):
            ret[key] = ret[key].extend(high[key])
        else:
            ret[key] = high[key]

    return ret


def collect_options(path_sys: str, path_app: str = "") -> dict:
    opts_sys = parse_profile(path_sys)
    opts_app = parse_profile(path_app)

    if "system" in opts_sys:
        opts_sys = opts_sys["system"]
    else:
        opts_sys = dict()

    if "application" in opts_app:
        opts_app = opts_app["application"]
    else:
        opts_app = dict()

    return merge_dicts(opts_sys, opts_app)
