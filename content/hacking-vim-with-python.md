Title: Hacking your vim with python
Date: 2017-01-10 22:55
Tags: vim, python
Author: José Guilherme Vanz

I'm happy vim user for a while now. After learned the basics I started customize
the editor to my needs/preferences and for a long time everything were well. I
did not face anything that I could not do and this is still true. However, when
I became a more advanced user and decide to create more complex functions to help
me while I work in my source code files, something discouraged me go ahead: the
vim language (VimL). Don't judge me, I could study it but I do not have time and
desire to do that. So, for some time I do not create more interesting stuff because
of that. But a short time ago I discovered that I could write python script to
interact with vim, like buffer, windows, tabs and so on! That's great!

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

The first option is useful if you want to execute a single python statement.
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

Last but not least is the `:[range]pyf[ile] {file}` command. It allows load a
separated python file and call its function with `:py` command. This is the
command used to load the python script in the following example.


### Vim module

To make possible the integration between python and vim there is a python module.
This module gives you the ability to interact with buffers, windows, tabs,
execute vim commands and so on. This module has a bunch of methods, constants
and objects that might used for the scripts. This article will use just a few
of the features available in the module. They are: `vim.command(str)`;
`vim.current`; and `Buffer.mark()`.

You can see a better documentation of the module typing `:help python` in you
vim editor.

### Let's hack!

Let's dive deeper in the example. In this example the author of the script is
a guy that has the boring job to write the current weather of bunch of cities
sitting in some file. Wisely he/she decided automate that process. (Yes, it is not
the ideal real life use case but I am not a creative person, sorry... xD). So, after
some time reading the documentation a python script was born:

[gist:id=b02e61147a7f05a2a308b3d5b1d0d382,file=weather.py]

It has the following features:

- function that will iterate over all rows of the current buffer
and append the current weather for the city (the row's content is used as city's
name)
- function that will use the selected text as city's and append the weather in
the row of the selection

Okay, let's take a closer look... The method `get_weather()` allow the user gets
the weather for city names sitting on each line of the current buffer. It's nice
to highlight the `vim.current` object. This object provides access to
various objects in vim. That is:

- `vim.current.line`: current line (string)
- `vim.current.buffer`: current buffer (Buffer object)
- `vim.current.window`: current window (Window object)
- `vim.current.tabpage`: current tab page (TabPage object)
- `vim.current.range`: current line range (Range object)

That been said, the line `buff = vim.current.buffer` is getting the current buffer
to iterate and update it. After that, the script iterate over all buffer's rows
calls the Open Weather API to get the weather using the row's content as city's
name and update the row with the current value appended with the weather.

The `get_weather_selection()` is the method that uses the selected text as city
to call the weather API. In this method, again, a reference to the current
buffer is gotten and used the `buf.mark()` method of the `Buffer` object to get
the line and column of the start and end of the selection. In vim the marks "<"
and ">" is used to define the beginning and end of the selected text respectively.

Once we have the marks values the script calls a helper function who extract the
selected text from the buffer and returns it. After that, the weather API is called
and the weather is appended after the selection

The `get_text(start, end)` and `get_openweather(city)` methods are helper methods.
First one is able to extract text from the buffer using tuples of (line, column)
passed as arguments to delimitate the text should be returned. The second one
is just a call to the Open Weather API using the python request module.

Once the script is done it can be loaded with the `pyf {file}` command.
As the script in discussion is a python3 code, it has to be load using the
equivalent command to python3, that is: `py3file $HOME/.vim/weather.py`. After
added this line in the vimrc, it is ready to go and the methods can be called
with:

`py3 get_weather()` or `:'<,'>py3 get_weather_selection()`.

NOTE: be aware that there are equivalent commands, `py3`, `py3do` and `py3f` to
run/load python3 code. See more in the python3 section in the vim documentation

#### Buffer

The most important object in the example is Buffer. Buffer objects can be treat
as sequence object. Thus, they act like lists and are mutable and to update
a row it is necessary just assign the new value,
`vim.current.buffer[1] = "new value for the line 2"`. Remember, lists
indexing start with 0 and the lines in a vim buffer with 1. In the script is
possible see the lines being updated at lines 14 and 26.

It is also possible delete lines, `:py del vim.current.buffer[1]` (delete the second
row). Append new lines, `:py vim.current.buffer.append("bottom")`. Assign variables,
`:py vim.current.buffer.vars["foo"] = "bar"`, and so on. You can see a complete
description with all methods and attribute with `:help python`

### Your turn

This is a very, very simple example of how you can start script vim with python.
I encourage you to read the vim documentation, play with it and create crazy
stuff! =)

If you need more info take a look in the references, send me an e-mail or leave
a comment. Thanks you!

#### References

`:help python` in your vim editor

[weather.py](https://github.com/jvanz/dotfiles/blob/master/.vim/weather.py)

[Scripting Vim with Python](http://old.orestis.gr/blog/2008/08/10/scripting-vim-with-python/)



