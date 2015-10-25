# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jos\xe9 Guilherme Vanz'
SITENAME = u'vanz'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_RSS = None
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
SOCIAL = (('twitter', 'https://twitter.com/vanzstuff'),
	('linkedin', 'https://br.linkedin.com/in/joseguilhermevanz'),
	('github', 'https://github.com/jvanz'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATH = ['images']

# Theme stuff
THEME = "vanz-theme"

BIO = "I'm José Guilherme Vanz, from south Brazil. Working as Software Engineer. I love Open Source and programming"
PROFILE_IMAGE = "avatar.jpg"

DISQUS_SITENAME = "jvanz"
