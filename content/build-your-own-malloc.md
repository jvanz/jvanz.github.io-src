Title: cgo: Go lang with C
Date: 2015-11-19 00:00
Tags: c, tlpi, glibc, memory
Author: José Guilherme Vanz

Some time ago I bought the The Linux Programming Interface, one of the best books I have bought.
One of the first chapters I read were about memory allocation. At the end of the chapter author offers some exercises to the reader.
Among them there is one more challenged. Implement the equivalent to the malloc and free functions. The challenge has been accepted!

First of all, this implementation has only study purposes. It is mean you SHOULD not start to implement your malloc and free functions.
Do not reinvent the wheel! The glibc are being improved for decades for many great guys. ;)

Theory
------

Before show the code, I will explain how and what I use to create my own memory allocator. For this, I assume that you have a background of how a process works
and its data, text, heap, stack segments. If you do not have this acknowledgement, I will give some references in the end of this post.

- System calls
- free list
- avoid memory fragmentation

Code
----

TODO
memory.c
sample program

References
----------

- The Linux Programing Interface
- man pages
- some good link about process memory layout
