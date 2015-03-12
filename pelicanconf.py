#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


# --- [ CORE ] -----------------------------------------------------------------

AUTHOR = u'Nathan Farrar'
SITENAME = u'crunk.io'
SITEURL = u'http://127.0.0.1:8080'
DEFAULT_LANG = u'en'
TIMEZONE = 'US/Mountain'

# --- [ MISC ] -----------------------------------------------------------------

DEFAULT_CATEGORY = u'unsorted'
DEFAULT_PAGINATION = 10


# MENUITEMS = [
#     ('Nothing Here', 'Nothing at all.'),
# ]

USE_FOLDER_AS_CATEGORY = True
# DISPLAY_PAGES_ON_MENU = True
# DELETE_OUTPUT_DIRECTORY = False
# RELATIVE_URLS = True
# SLUGIFY_SOURCE = 'title'

# --- [ LOCAL PATHS ] ----------------------------------------------------------

CACHE_PATH = '_cache'
OUTPUT_PATH = '_site'

PATH = 'content'
ARTICLE_PATHS   = [ 'posts' ]
PAGE_PATHS      = [ 'pages' ]
STATIC_PATHS    = [ 'assets' ]

EXTRA_PATH_METADATA = {
    'assets/extra/CNAME': {
        'path': 'CNAME'
    },
    'assets/extra/favicon.ico': {
        'path': 'favicon.ico'
    },
}

FAVICON_URL='/favicon.ico'

# --- [ URLS ] -----------------------------------------------------------------

# "Clean" URL setup for static serving. Works with github. No messing with
# server configs.

ARTICLE_SAVE_AS = 'post/{slug}/index.html'
ARTICLE_URL = 'post/{slug}/'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
PAGE_URL = 'page/{slug}/'
PAGE_SAVE_AS = 'page/{slug}/index.html'
TAG_URL = 'tagged/{slug}/index.html'
TAG_SAVE_AS = 'tagged/{slug}/index.html'

# --- [ DEFAULT METADATA ] -----------------------------------------------------

# Default metadata, applied globally. Three separate fucking "bugs".

from datetime import date
# DEFAULT_METADATA = (
#     ('Authors', 'Nathan Farrar'),
#     ('Status', 'draft'),
#     ('Date', date.today()),
# )

# Another attempted hack at setting default metadata, another fail. These
# settings appear to be incompatible. 

# DEFAULT_DATE = (2016, 01, 01)
# WITH_FUTURE_DATES = False

# --- [ MARKDOWN ] -------------------------------------------------------------

MD_EXTENSIONS = ([
    'codehilite(css_class=highlight)',
    'extra',
    'toc'
])

# ---[ CACHING ] ---------------------------------------------------------------

CACHE_CONTENT = False
GZIP_CACHE = False
LOAD_CONTENT_CACHE = False

# AUTORELOAD_IGNORE_CACHE = False
# CONTENT_CACHING_LAYER = 'reader'

# --- [ FEED ] -----------------------------------------------------------------

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# --- [ THEME ] ----------------------------------------------------------------

THEME='themes/pure'

SITESUBTITLE = 'gritty technology'
GITHUB_URL='http://github.com/nfarrar/nfarrar.github.io'
TWITTER_USERNAME='oxsyn'

GOSQUARED_SITENAME = None
DISQUS_SITENAME = None
GOOGLE_ANALYTICS = None
PIWIKI_URL = None
PIWIK_SSL_URL = None
PIWIK_SITE_ID = None

SOCIAL = (
    ('home', SITEURL),
    ('github', 'https://github.com/nfarrar'),
    ('linkedin', 'https://www.linkedin.com/in/nfarrar'),
    ('twitter', 'http://twitter.com/oxsyn'),
    ('rss', 'http://crunk.io/rss'),
)

# LINKS = (
#     ('Nothing', 'Nothing'),
# )

# --- [ THEME:PURE ] -----------------------------------------------------------

TAGLINE = SITESUBTITLE
COVER_IMG_URL = '/assets/images/cover/city05.jpg'
PROFILE_IMG_URL = '/assets/images/terminal.png'

# --- [ PLUGINS ] --------------------------------------------------------------

PLUGIN_PATHS = [
    'plugins/pelican-plugins',
    'plugins/pelican-md-metayaml'
]

PLUGINS = [ 'gravatar', 'sitemap', 'summary', 'md_metayaml'  ]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Tipue
# DIRECT_TEMPLATES = (
#     ('index', 'tags', 'categories', 'authors', 'archives', 'search')
# )
