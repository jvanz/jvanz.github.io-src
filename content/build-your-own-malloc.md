Title: My own malloc/free implementation
Date: 2015-11-26 00:08
Tags: c, tlpi, glibc, memory
Author: José Guilherme Vanz

Some time ago I bought the The Linux Programming Interface book, one of the best books I have bought.
One of the first chapters I read were about memory allocation. At the end of the chapter, author offers some exercises
to the reader. Among them there is a challenging one. He suggests to implement the equivalent to the malloc and free
functions. The challenge has been accepted!

First of all, this implementation is just for study purposes. It is mean you should NOT start to implement your malloc and free functions
for production programs. Do not reinvent the wheel! The glibc are being improved for decades for many great guys. You probably
will take the same or more time to do the equivalent excellent work! ;)

I assume that you know a little bit about how a process works and its data, text, heap, stack segments.

### System calls

There are two system calls allows the program to increase the program break, `brk` and `sbrk`. The program break defines
where is the end of process's data segment. It means if the program increases the program break, memory is allocated.
Otherwise, it deallocate memory. In this code only `sbrk` is used, its only parameter defines the amount of memory program wants
to increase. If the program break has being increased successfully, a pointer to the beginning of the allocated memory is
returned. Otherwise, (void*) -1 is returned. `brk` is not being used allows the program set the end of data segment to
the pointer passed in the functions arguments. I think I did not use this function because my code do not decrease the
program break. Maybe in the future I implement this feature and use the `brk` system call.

### Code

The cornerstone of the code is a linked list, called `free_list`. It keeps all available memories blocks. Each element is
composed for a header and the memory itself. The header is a structure to store two metadata. The first field of the
struct is block's size and the second is the next memory block in the `free_list`. The first thing necessary when a program
request some memory is check if the `free_list` is already initialized. If not, it is initiated with a block of 0 size.
This is done to keep the first element in the list always the same.Thus, it is more easy to know when stop a loop through
the list and reduce the code complexity.

Once `free_list` initiated, a search in the list is performed. Looking for a memory block with enough size to attempt the
request. The algorithm follows the 'first fit' approach. It means that the first memory block found with
enough size is split  and returned a pointer to the memory to the caller. If any block
has enough size, the heap is increased and the new memory is returned. The pointer returned to the user is a pointer
to the memory block itself. It is not include the header. Does not make sense give access to the control structures for
the caller program. This structure is used only for memory management and to know what is the memory block size when the
program wants to free it.

As you will see soon in the code, all memory blocks are multiple of the header size. It means the minimum
memory size allocated is the HEADER_SIZE * 2 (with the header). This approach facilitate the pointer arithmetic and avoid
counting every single byte. In other words, even if the user requests less memory, the allocated memory will be always
multiple of the HEADER_SIZE.

When the user wants to free a pointer, another search in the free_list is performed. This time, looking for a memory block
next the to the block is being freed. If a block is found, the two blocks are merged into one. Otherwise, the block is
appended in the list. The goal of merge close blocks is avoid memory fragmentation. ;)

Well, let's take a look in the code! Thus you can see all the implementation details.

[gist:id=869420fb87353049d4d7,file=memory.h]

[gist:id=869420fb87353049d4d7,file=memory.c]

[gist:id=869420fb87353049d4d7,file=sample.c]

The last source code is a simple sample program using the functions described before.

Feel free to ask me in the comments. =]

#### References

[brk, sbrk](http://linux.die.net/man/2/sbrk)

[The Linux Programing Interface](http://www.amazon.com/Linux-Programming-Interface-System-Handbook/dp/1593272200/ref=sr_1_1?s=books&ie=UTF8&qid=1448501399&sr=1-1&keywords=the+linux+programming+interface)

[The C Programming Language](http://www.amazon.com/Programming-Language-Brian-W-Kernighan/dp/0131103628/ref=sr_1_1?s=books&ie=UTF8&qid=1448501445&sr=1-1&keywords=the+c+programming+language)
