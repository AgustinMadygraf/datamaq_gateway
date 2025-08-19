"""
Path: interface_adapters/controllers/static_controller.py
"""

import os

from interface_adapters.presenters.static_presenter import present_static_file, present_not_found
from interface_adapters.gateway.file_gateway import get_file

def get_index_html():
    "Obtiene el archivo index.html"
    index_path = os.path.join(os.path.dirname(__file__), '../../static/index.html')
    content = get_file(index_path)
    if content is not None:
        return present_static_file(content, "text/html")
    return present_not_found()

def get_favicon():
    "Obtiene el archivo favicon.ico"
    favicon_path = os.path.join(os.path.dirname(__file__), '../../static/favicon.ico')
    content = get_file(favicon_path)
    if content is not None:
        return present_static_file(content, "image/x-icon")
    return present_static_file(b"", "image/x-icon", 204)
