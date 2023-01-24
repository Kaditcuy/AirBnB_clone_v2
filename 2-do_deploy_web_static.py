#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static
folder of my AirBnB Clone repo, using the function do_pack
"""
from datetime import datetime
from fabric.api import *
import os
env.hosts = ['18.207.207.11', '35.174.208.65']


def do_pack():
    """Generates a .tgz archive from the contents
    of the web_static folder of this repository.
    """
    if not os.path.exists("versions"):
        os.mkdir("versions")

    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(date_time)
    archive_path = "versions/{}".format(archive_name)

    local("tar -cvzf {} web_static".format(archive_path))

    if os.path.exists(archive_path):
        return archive_path
    return None


def do_deploy(archive_path):
    """
    distributes an archive
    to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    filename = os.path.basename(archive_path)
    filename_without_ext = os.path.splitext(filename)[0]
    tmp_dir = '/tmp/'
    releases_dir = '/data/web_static/releases/'
    releases_path = releases_dir + filename_without_ext + '/'
    symLinkCurrent_dir = '/data/web_static/current'

    put(archive_path, tmp_dir + filename)
    run('mkdir -p ' + releases_path)
    run('tar -xzf ' + tmp_dir + filename + ' -C ' + releases_path)
    run('rm ' + tmp_dir + filename)
    run('mv ' + releases_path + 'web_static/* ' + releases_path)
    run('rm -rf ' + releases_path + 'web_static')
    run('rm -rf ' + symLinkCurrent_dir)
    run('ln -s ' + releases_path + ' ' + symLinkCurrent_dir)
    return True
