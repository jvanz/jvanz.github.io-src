Title: malloc/free implementation. Just4Fun!
Date: 2015-11-26 00:08
Modified: 2016-01-24 22:22
Tags: c, tlpi, glibc, memory
Author: José Guilherme Vanz

Some time ago I bought the The Linux Programming Interface book, one of the best books I have acquired.
One of the first chapters I read were about memory allocation. At the end of the chapter, author offers some exercises
to the reader. Among them there is a challenging one. He suggests to implement the equivalent to the malloc and free
functions. The challenge has been accepted!

First of all, this implementation is just for study purposes. It means you should NOT start to implement your malloc and
free functions for production programs. Do not reinvent the wheel! The glibc are being improved for decades for many
great guys. You probably will take more time to do the equivalent excellent work! ;)

I assume that you know a little bit about how a process and its segments works. It is nice remember this code does not
cover all details. As any software it can be improved (a lot).


### System calls

There are two system calls allows the program to increase the program break, `brk` and `sbrk`. The program break defines
where is the end of process's data segment. It means if the program increases the program break, memory is allocated.
Otherwise, it deallocate memory. In this code only `sbrk` is used, its only parameter defines the amount of memory program wants
to increase. If the program break has being increased successfully, a pointer to the beginning of the allocated memory is
returned. Otherwise, (void*) -1 is returned. `brk` is not being used. It allows the program set the end of data segment to
the pointer passed in the functions arguments. I think this function is not being in use because the code does not decrease
the program break. Maybe in the future I implement this feature and use the `brk` system call.

For more details, take a look in the man page. ;)

### Code

[gist:id=869420fb87353049d4d7,file=memory.c]

The cornerstone of the code is a linked list, called `free_list`. It stores all available memories blocks. Each element is
composed for a header and the memory itself. The header is a structure that contains two metadata. The first field of the
struct is block's size and the second is a pointer to next memory block in the `free_list`. The first thing necessary
when a program request some memory is check if the `free_list` is already initialized (line 29). If not, it is initiated
with a block of 0 size (lines 29 ~ 36). This is done to keep the first element in the list always the same. Thus, it is more easy to know
when stop a loop through the list and reduce the code complexity.

![]({filename}/images/mem_init.png)

Once `free_list` initiated, a search in the list is performed. Looking for a memory block with enough size to attempt the
request. The algorithm follows the 'first fit' approach. It means that the first memory block found with enough size is
split and returned a pointer to the memory to the caller (lines 38 ~ 53). If any block has enough size, the heap is increased and the
new memory is returned (line 55). The pointer returned to the user is a pointer to the memory block itself. It is
not include the header. Does not make sense give to caller  access to the control structures. This structure is used only
for memory management and to know what is the memory block size when the program wants to frees it.

![]({filename}/images/one_mem_allocate.png)

As you can see between lines 26 and 28, all memory blocks are multiple of the header size. It means the minimum
memory size allocated is the HEADER_SIZE * 2 (with the header). This approach facilitate the pointer arithmetic and avoid
counting every single byte. In other words, even if the user requests less memory, the allocated memory will be always
multiple of the HEADER_SIZE.

When the user wants to free a pointer, another search in the `free_list` is performed. This time, looking for a memory block
next the to the block is being freed. If a block is found, the two blocks are merged into one (lines 64 ~ 77). Otherwise,
the block is appended in the list (lines 78 ~ 80). The goal of merge close blocks is avoid memory fragmentation. ;)

According to my weak skill in asymptotic analysis, both functions have running time of O(n). Since each functions performed
a search in the `free_list`. Please, tell me if I am wrong. I will study more about this topic and correct if I wrote
bullshit. The following sources are the header and a test program.

[gist:id=869420fb87353049d4d7,file=memory.h]

[gist:id=869420fb87353049d4d7,file=sample.c]

Feel free to ask me in the comments. =]

#### References

[brk, sbrk](http://linux.die.net/man/2/sbrk)

[The Linux Programing Interface](http://www.amazon.com/Linux-Programming-Interface-System-Handbook/dp/1593272200/ref=sr_1_1?s=books&ie=UTF8&qid=1448501399&sr=1-1&keywords=the+linux+programming+interface)

[The C Programming Language](http://www.amazon.com/Programming-Language-Brian-W-Kernighan/dp/0131103628/ref=sr_1_1?s=books&ie=UTF8&qid=1448501445&sr=1-1&keywords=the+c+programming+language)

[Repository](https://github.com/jvanz/tlpi)
