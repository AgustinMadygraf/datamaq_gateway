"""
Path: interface_adapters/controllers/static_controller.py
"""

import os

from interface_adapters.presenters.static_presenter import present_static_file, present_not_found
from interface_adapters.gateway.file_gateway import get_file
from shared.config import get_static_path

def get_index_html():
    "Obtiene el archivo index.html"
    index_path = os.path.join(get_static_path(), "datam.html")
    content = get_file(index_path)
    if content is not None:
        return present_static_file(content, "text/html")
    return present_not_found()

def get_favicon():
    "Obtiene el archivo favicon.ico"
    favicon_path = os.path.join(get_static_path(), "favicon.ico")
    content = get_file(favicon_path)
    if content is not None:
        return present_static_file(content, "image/x-icon")
    return present_static_file(b"", "image/x-icon", 204)

def get_datamaq_gateway():
    "Obtiene el archivo datamaq_gateway.html"
    datamaq_gateway_path = os.path.join(get_static_path(), "datamaq_gateway.html")
    content = get_file(datamaq_gateway_path)
    if content is not None:
        return present_static_file(content, "text/html")
    return present_not_found()
