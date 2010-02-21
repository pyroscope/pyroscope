# -*- coding: utf-8 -*-
""" PyroScope - Python Torrent Tools.

    PyroScope is a collection of tools for the BitTorrent protocol and especially the rTorrent client.

    It offers the following components:
     * a modern and versatile rTorrent web interface
     * rTorrent extensions like a queue manager and statistics
     * command line tools for automation of common tasks, like metafile creation 

    Copyright (c) 2009 The PyroScope Project <pyroscope.project@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import os

from paver.easy import *
from paver.setuputils import setup

from setuptools import find_packages


#
# Project Metadata
#

name, version = open("../debian/changelog").readline().split(" (", 1)
version, _ = version.split(")", 1)

project = dict(
    # egg
    name = name,
    version = version,
    packages = find_packages(exclude = ["tests"]),
    entry_points = {
        "console_scripts": [
            "mktor = pyroscope.scripts.mktor:run",
            "lstor = pyroscope.scripts.lstor:run",
        ],
        "paste.app_factory": [
            "main = pyroscope.web.config.middleware:make_app",
        ],
        "paste.app_install": [
            "main = pylons.util:PylonsInstaller",
        ],
    },
    include_package_data = True,
    zip_safe = False,
    data_files = [
        ("EGG-INFO", [
            "README", "../LICENSE", "../debian/changelog", 
            "pyroscope/web/config/paste_deploy_config.ini_tmpl",
        ]),
    ],
    paster_plugins = ["PasteScript", "Pylons"],

    #package_data={"pyroscope.web": ["i18n/*/LC_MESSAGES/*.mo"]},
    #message_extractors={"pyroscope.web": [
    #        ("**.py", "python", None),
    #        ("templates/**.mako", "mako", {"input_encoding": "utf-8"}),
    #        ("public/**", "ignore", None)]},

    # dependencies
    install_requires = [
        "Pylons==0.9.7",
    ],
    setup_requires = [
        "PasteScript>=1.7.3",
    ],

    # tests
    test_suite = "nose.collector",

    # cheeseshop
    author = "The PyroScope Project",
    author_email = "pyroscope.project@gmail.com",
    description = __doc__.split('.', 1)[0].strip(),
    long_description = __doc__.split('.', 1)[1].strip(),
    license = [line.strip() for line in __doc__.splitlines()
        if line.strip().startswith("Copyright")][0],
    url = "http://code.google.com/p/pyroscope/",
    keywords = "bittorent rtorrent cli webui python",
    classifiers = [
        # see http://pypi.python.org/pypi?:action=list_classifiers
        "Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Paste",
        "Framework :: Pylons",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.5",
        "Topic :: Communications :: File Sharing",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)

#
# Build
#

@task
@needs(["setuptools.command.egg_info", "svg2png"])
def bootstrap():
    links = []
    for egg_info in (i[1] for i in project["data_files"] if i[0] == "EGG-INFO").next():
        links.append((
            "../" + egg_info, 
            "%s.egg-info/%s" % (project["name"], os.path.basename(egg_info))
        ))

    for link_pair in links:
        if not os.path.exists(link_pair[1]):
            print "%s <- %s" % link_pair
            os.symlink(*link_pair)


@task
def svg2png():
    """ Convert SVG icons to PNG icons.
    """
    grad_sizes = (
        100, 
        (160,80), # icon boxes
        (160, 32), (160, 48),         
        (320, 32), (320, 48), 
        (1920, 16), (1920, 24), (1920, 32),  (1920, 48), 
        (1920, 96), (1920, 360),
    )
    grad_colors = {
        "black": lambda s: s,
        "grey": lambda s: s
            .replace("#000000", "#808080"),
        "white": lambda s: s
            .replace("#000000", "#FFFFFF"),
        "half-black": lambda s: s
            .replace("stop-opacity:1", "stop-opacity:0.5"),
        "half-grey": lambda s: s
            .replace("#000000", "#808080")
            .replace("stop-opacity:1", "stop-opacity:0.5"),
        "half-white": lambda s: s
            .replace("#000000", "#FFFFFF")
            .replace("stop-opacity:1", "stop-opacity:0.5"),
        "ff9": lambda s: s
            .replace("#000000", "#FFFF99"),
        "ffc": lambda s: s
            .replace("#000000", "#FFFFCC"),
    }
    icon_sizes = (12, 16, 24, 32, 48)
    img_path = path("pyroscope/web/public/img")
    svg_path = img_path / "svg"
    build_dir = path("build")

    def grad_transform(svg_file, color):
        tmp_file = build_dir / ("%s-%s.svg" % (color, svg_file.namebase))
        tmp_file.write_bytes(grad_colors[color](svg_file.bytes()))
        tmp_file.utime((svg_file.atime, svg_file.mtime))
        return tmp_file
    
    def make_png(svg_file, size):
        try:
            w, h = size
            szdir = "%dx%d" % size
        except TypeError:
            w, h = size, size
            szdir = str(size)
        png_path = img_path / "png" / szdir
        png_path.exists() or png_path.makedirs()
        png_file = png_path / svg_file.namebase + ".png"
        if not png_file.exists() or png_file.mtime < svg_file.mtime:
            sh("inkscape -z -e %(png_file)s -w %(w)d -h %(h)d %(svg_file)s" % locals())

    build_dir.exists() or build_dir.makedirs()

    icon_files = (svg_path / "icons").files("*.svg")
    for size in icon_sizes:
        for svg_file in icon_files:
            make_png(svg_file, size)

    grad_files = (svg_path / "gradients").files("*.svg")
    for svg_file in grad_files:
        for color in grad_colors:
            tmp_file = grad_transform(svg_file, color)
            for size in grad_sizes:
                make_png(tmp_file, size)
            os.remove(tmp_file)

    # Project logo for Google Code & the UI
    make_png(svg_path / "logo-wide.svg", (150, 55))
    make_png(svg_path / "logo-wide.svg", (200, 100))
    make_png(svg_path / "icons" / "logo.svg", 150)


def _screenshots():
    """ Make thumbnails for the screenshots.
    """
    # developers need to checkout the wiki in read/write mode using
    #  svn co https://pyroscope.googlecode.com/svn/wiki
    gallery_file = "wiki/ScreenShotGallery.wiki"
    gallery_text = [
        "#summary Screenshots of different browser views",
        "",
        "Click on a thumbnail to see a larger version...",
        "",
    ]
    gallery_width = 2
    thumb_size = "300x200"
    img_path = "docs/media/screens"
    svn_base = "http://pyroscope.googlecode.com/svn/trunk/pyroscope/" + img_path

    def make_thumb(img_file, thumb_size=thumb_size):
        thumb_file = img_file.dirname() / img_file.namebase + "-thumb.jpg"
        if not thumb_file.exists() or thumb_file.mtime < img_file.mtime:
            sh("convert -geometry %(thumb_size)s %(img_file)s %(thumb_file)s" % locals())
        return thumb_file

    counter = 0
    img_files = path(img_path).files()
    for img_file in img_files:
        if img_file.ext in (".jpg", ".png",) and "-thumb" not in img_file.namebase:
            thumb_file = make_thumb(img_file)

            if counter % gallery_width == 0:
                gallery_text.append("|| ")
            counter += 1

            gallery_text[-1] += '<a title="%s" href="%s/%s"><img src="%s/%s" /></a> ||' % (
                img_file.namebase, svn_base, img_file.basename(),
                svn_base, thumb_file.basename(),
            )
        
    path(gallery_file).write_lines(gallery_text)
    sh('svn stat %s' % gallery_file)
    print "Use this command to check-in the new gallery if changed..."
    print '    svn ci -m "Auto-generated ScreenShotGallery" %s' % gallery_file


@task
def docs():
    """ Create documentation.
    """
    _screenshots()


#
# Testing
#

@task
@needs("setuptools.command.build")
def serve():
    """ Start the web server in DEVELOPMENT mode.
    """
    sh("bin/paster setup-app development.ini")
    ##sh("bin/paster serve --reload --monitor-restart development.ini")
    sh("bin/paster serve --reload development.ini")


@task
@needs("setuptools.command.build")
def functest():
    """ Functional test of the command line tools.
    """


#
# Project Management
#

@task
@consume_args
def controller(args):
    links = [
        ("web/controllers", "%s/controllers" % project["name"]),
        ("../tests/web", "%s/tests" % project["name"]),
    ]
    for link_pair in links:
        if not os.path.exists(link_pair[1]):
            #print "%s <- %s" % link_pair
            os.symlink(*link_pair)
    try:
        sh("paster controller %s" % " ".join(args))
    finally:
        for _, link in links:
            os.remove(link)


#
# Web Server Control
#

PASTER_CMD =  " ".join([
    "paster serve %s",
    "--pid-file ~/.pyroscope/web.pid",
    "--log-file ~/.pyroscope/log/web.log",
    "~/.pyroscope/web.ini",
])

@task
def start():
    """ Start the PRODUCTION web server.
    """
    sh("paster setup-app ~/.pyroscope/web.ini")
    sh(PASTER_CMD % ("--daemon")) # --monitor-restart makes --stop-daemon fail


@task
def stop():
    """ Start the PRODUCTION web server.
    """
    sh(PASTER_CMD % ("--stop-daemon"))


@task
def status():
    """ Check status of the PRODUCTION web server.
    """
    sh(PASTER_CMD % ("--status"))


setup(**project)

