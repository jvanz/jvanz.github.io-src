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

### Scripting

There are some way you can execute a python code in vim. You can use the commands:
`:py[thon]`, `:pydo`, `:pyfile`. In this article I'll do a short description of
them, but I'll use just `:pyfile` in the example.

When you decide write the python script you can write it in a separated file
or embedded it in your vimrc. If you do not want write file for you script you
can use the `:[range]python` or

```
:[range]py[thon] << {endmarker}
{script}
{endmarker}
```

The fist option is useful if you want to execute a single python statement.
For example: `:python print "Python rocks!"`. The second way is more interesting,
it is allows embedded the python code inside vim script. Take a look:

```
function! IcecreamInitialize()
python3 << EOF
class StrawberryIcecream:
    def __call__(self):
        print('EAT ME')
ice = StrawberryIcecream()
ice()
EOF
endfunction
```

Another option is the `[range]pydo {body}` command. It is a good option if the
script should be executed in each line of the range. In this command the `{body}`
is executed as `def _vim_pydo(line, linenr) {body}`. Thus, the body script can
get the line text and number from arguments. The function should return a string
or None. If a string is returned the line is updated to that value. A possible
example is `:pydo return "%s\t%d" % (line[::-1], len(line))`


### Vim python module

The vim integration with python is done via a python module. This module gives
you the ability to interact with buffers, windows, tabs, execute vim commands
and so on.


#### References

`:help python`



