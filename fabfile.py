#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import cd, env, hide, local, task
from livereload import Server, shell
from pelican.settings import read_settings
from os.path import isdir, isfile, join
from os import getcwd
import gntp.notifier
import sys

GNTP_ICON_PATH      = join(getcwd(), 'content/assets/images/terminal.png')

def notify(message, cfg='pelicanconf.py'):
    """ generate a growl notification """
    settings = read_settings(cfg)
    icon = None

    if 'GNTP_ICON' in settings:
        if isfile(join(settings['PATH'], settings['GNTP_ICON'])):
            icon = join(settings['PATH'], settings['GNTP_ICON'])

    gntp.notifier.mini(
        applicationName='pelican',
        title=settings['SITENAME'],
        noteType='fabric',
        description=message,
        applicationIcon=icon
    )

@task
def clean(cfg='pelicanconf.py'):
    """ clean the build directory """
    settings = read_settings(cfg)
    if isdir(settings['OUTPUT_PATH']):
        notify('cleaning %s' % settings['OUTPUT_PATH'])
        local("rm -rf %s" % settings['OUTPUT_PATH'] + '/*')

@task
def build(cfg='pelicanconf.py'):
    """ build the site """
    notify('building site')
    local('pelican -s %s' % cfg)

@task
def rebuild(cfg='pelicanconf.py'):
    """ rebuild the site """
    clean()
    build(cfg=cfg)

@task
def preview(cfg='publishconf.py'):
    """ preview the published site """
    clean()
    build(cfg=cfg)

@task
def devserver(host='localhost', port=8080, cfg='pelicanconf.py'):
    """ start the livereload server """
    settings = read_settings(cfg)
    content = settings['PATH']
    output = settings['OUTPUT_PATH']

    notify('starting server on %s:%s' % (host, port))
    rebuild()
    server = Server()
    server.watch(content, shell('fab rebuild'))
    server.serve(root=output, host=host, port=port)

@ task
def bs(host='localhost', port=8080, cfg='pelicanconf.py'):
    """ start the browsersync server - """
    settings = read_settings(cfg)
    content = settings['PATH']
    site = settings['OUTPUT_PATH']

    with cd(site):
        local('browser-sync start --server --files="%s/**' % content)

@task
def publish(cfg='publishconf.py'):
    """ publish content to github user page """
    settings = read_settings(cfg)
    rebuild()
    local('ghp-import -p -b master %s' % settings['OUTPUT_PATH'])

@task
def update():
    """ update git submodules """
    local("git submodule foreach 'git fetch origin; " +
          "git checkout $(git rev-parse --abbrev-ref HEAD); " +
          "git reset --hard origin/$(git rev-parse --abbrev-ref HEAD); " +
          "git submodule update")
