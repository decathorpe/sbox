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


def collect_options(path_sys: str, path_app: str = "") -> dict:
    opts_sys = parse_profile(path_sys)
    opts_app = parse_profile(path_app)

    options = dict()

    if "system" in opts_sys:
        for key in opts_sys["system"]:
            options[key] = opts_sys["system"][key]
    if "application" in opts_app:
        for key in opts_app["application"]:
            options[key] = opts_app["application"][key]

    return options
