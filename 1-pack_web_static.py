#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static folder
of the Airbnb clone, using do_pack function
"""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """Generates a .tgz archive from the contents
    of the web_static folder of this repo.
    """
    if not os.path.exists("versions"):
        os.mkdir("versions")

    date_time = datetime.now().strfttime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(date_time)
    archive_path = "versions/{}".format(archive_name)

    local("tar -cvzf {} web_static".format(archive_path))

    if os.path.exists(archive_path):
        return archive_path
    return None
