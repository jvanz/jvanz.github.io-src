#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://jvanz.github.com'
RELATIVE_URLS = False

AUTHOR = u'Jos\xe9 Guilherme Vanz'
SITENAME = u'vanz'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('email', 'guilherme.sft@gmail.com'),
	('twitter', 'https://twitter.com/vanzstuff'),
	('linkedin', 'https://br.linkedin.com/in/jvanz'),
	('github', 'https://github.com/jvanz'))

DEFAULT_PAGINATION = 10

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

# Theme stuff
THEME = "pelican-hyde"

BIO = "I'm José Guilherme Vanz, from south Brazil. Working as Software Engineer. I love Open Source and programming"
PROFILE_IMAGE = "avatar.jpg"

PLUGINS = ['pelican_gist']

DISQUS_SITENAME = "jvanz"
GOOGLE_ANALYTICS = "UA-73126405-1"
