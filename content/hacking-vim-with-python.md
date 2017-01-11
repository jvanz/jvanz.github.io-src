Title: Hacking your vim with python
Date: 2017-01-10 22:55
Tags: vim, python
Author: José Guilherme Vanz


I'm happy vim user for a while now. After learned the basics I started customize
the editor to my needs/preferences and for a long time everything was good. I did
not face anything that I could not do and this is still true. However, when I
became a more advanced user and decide to create more complex functions
to help me while I work in my source code files I found something discouraging:
the vim language (VimL). Don't judge me, I could spend some time studying it but I do
not have this time. So, for some time I do not create more interesting stuff because
of that. But a short time ago I discovered that I could write python script to interact
with vim, like buffer, windows, tabs and so on! That's great!

This article is about how create a very simple script to read data from buffer and
update them. :-)

Before you start write python script to do the magic in your vim buffer it is
necessary take a look if you vim allow you use python. For that you can run the
`vim --version` and see if your vim has python support. The output should show
something like `+python`

### Vim python module

The vim integration with python is done via a python module. This module gives
you the ability to interact with buffers, windows, tabs, execute vim commands
and so on.


#### References

`:help python`



