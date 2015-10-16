---
layout: post
title: "cgo: Go lang with C"
---
Some weeks ago I had to customize the [Docker](https://www.docker.com/) to integrate it with some libraries written and C.
Maybe you already know Docker is written in Go language and to do this task was used [cgo](https://golang.org/cmd/cgo/)
Cgo enables integrate Go code with C. It shows itself easier and smooth comparing with my past experiences with JNI

<!-- more -->

Hello World!
------------

To start let's code the old but gold hello world program. In the first example the program will just print a string that is returned by a C function.
As you can see in the following snippet, cgo allows to put C code inside the Go source code. The only thing has to do is import the pseudo-package `C`.
The comments before this import is a C code that will be compiled as a header.

```go
package main

//char* get_msg(){
//      return "Hello Go!";
//}
import "C"
import "fmt"

func main() {
	var msg = C.get_msg()
	fmt.Println(C.GoString(msg))
}
```

More funny program
------------------

To make the things more funny, the next program will write the command line arguments to a file. Take a look the code:

```go
/*
#include <stdio.h>

FILE *file;

int finish() {
	fflush(file);
	fclose(file);
}

int init(const char* file_name) {
	if (file){
		finish();
	}
	file = fopen(file_name, "w+");
}

int write_file(const char* data, size_t len) {
	if (!file){
		printf("File is not open");
		return 1;
	}
	if (fwrite(data, sizeof(char), len, file)) {
		return 0;
	}
	printf("Error on writing...");
	return 1;

}
*/
import "C"
import "os"
import "unsafe"

func main() {
	C.init(C.CString(os.Args[1]))
	for _, a := range os.Args[2:] {
		cs := C.CString(a + "\n")
		C.write_file(cs, C.size_t(len(a)+1))
		C.free(unsafe.Pointer(cs))
	}
	C.finish()
}
```

The program requires at least two arguments. The first one is the path for a file where the program will write the other arguments.
The code is quite simple. Go code uses three C functions to create, write and close a file. The C functions are:

  - `init(const char* file_name)`: function creates the file
  - `finish()`: function flushes the data and closes the file
  - `write_file(const char* data, size_t len)`: writes `len` chars from string `data` in the file

In the beginning the Go code uses the `init` function to create the file. After that, the program walks through other arguments writing each of them
in a file line. In the end, the program calls `finish` function to close the file. Nothing so special, but illustrate how you can use cgo.
The C code written inside Go source code is used as a header. You can see the static library within `$GOPATH/pkg/<package name>`

It is important to remember that Go memory manager does not knows C variables and its allocated memory blocks. Thus, the programmer must to remember to free the allocated C string. Like it is being
doing in the lines `C.free(unsafe.Pointer(cs))`. Otherwise, you will have memory leak issues.

Furthermore, when some Go source file contains the special import "C" the Go tool looks for .c, .cpp, .cc and others files types in the same source code file directory. Then it compiles them with the default C/C++ compiler.
So you might do this:

writer.go:

```go
package main

/*
#include <stdio.h>

extern int finish();
extern int init(const char* file_name);
extern int write_file(const char* data, size_t len);
*/
import "C"
import "os"

func main() {
	C.init(C.CString(os.Args[1]))
	for _, a := range os.Args[2:] {
		C.write_file(C.CString(a+"\n"), C.size_t(len(a)+1))
	}
	C.finish()
}
```

writer.c:

```c
#include <stdio.h>

FILE *file;

int finish() {
	fflush(file);
	fclose(file);
}

int init(const char* file_name) {
	if (file){
		finish();
	}
	file = fopen(file_name, "w+");
}

int write_file(const char* data, size_t len) {
	if (!file){
		printf("File is not open");
		return 1;
	}
	if (fwrite(data, sizeof(char), len, file)) {
		return 0;
	}
	printf("Error on writing...");
	return 1;

}
```

#### Note

This post is very, very, very simple. If you would like know more see the references below.

##### References

[cgo](https://golang.org/cmd/cgo/)

[C? Go? Cgo!](http://blog.golang.org/c-go-cgo)


