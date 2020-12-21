from jinja2 import Environment, FileSystemLoader, Template
from .cache import Cache
from config import TellusConfig

import json 

data = {}

env = Environment(
        loader=FileSystemLoader(searchpath=TellusConfig.TEMPLATE_PATH),
        bytecode_cache=Cache(TellusConfig.TEMPLATE_CACHE_PATH),
        auto_reload=True,
    )

def template(template, **kwargs):
    """Used to render templates
    """
    data["content"] = env.get_template(template).render(kwargs)
    data["content-type"] = ("Content-Type", "text/html")
    data["status"] = '200'
    return data

def as_json(content):
    """Used to return JSON data 
    """
    data["content"] = json.dumps(content)
    data["content-type"] = ("Content-Type", "text/json")
    data["status"] = "200"
    return data