Title: RAII: do not touch new and delete!
Date: 2020-07-28 00:00
Tags: c++,raii
Author: José Guilherme Vanz

![]({filename}/images/giphy.gif)

Some weeks ago I finished a online course about C++. I've already programmed in the language bBut I decided to take the course to refresh my skills and have some projects in my portfolio.
I wrote this article to consolidate my memory and try to explain to myself one of the things that I've learnt. Maybe you can find useful as well. What I'll cover in this article is the modern way to handle
resource in C++. I'll focus on memory, but the same concept can be applied in other resources types like sockets, files and etc. I'll also try to show how modern C++ does not require you to use `new`/`delete` to acquire and release memory. 

Okay, let's go. Image that we are software engineers working on a project to process image. But it's not common images. They are huge images. Something like image from telescopes, satellites, [real big images](https://mars.nasa.gov/resources/curiositys-1-8-billion-pixel-panorama/?site=msl). Maybe we can image you are working for [NASA](https://www.nasa.gov/) or [ESA](https://www.esa.int/). Our job is write a program to do some kind of image processing. The "goal" of the system does not matter for this example. ;)

We start to code the program by loading the images in memory.  Let's use the following program as the first few lines that we wrote :

```cpp
#include <chrono>
#include <fstream>
#include <iostream>
#include <thread>

using namespace std::chrono_literals;

/**
 * SOME OF THE INCLUDE AND FUNCTIONS USED IN THIS PROGRAM ARE FOR DEBUG ONLY.
 */

class MyHugeImage {
public:
  MyHugeImage(const std::string filepath) : _data("") {
    // read the whole file into memory
    // open the file and seek until the end
    std::ifstream stream(filepath, std::ios::binary | std::ios::ate);
    auto size = stream.tellg();
    _data = std::string(size, '\0');
    // go back to the beginning if the file
    stream.seekg(0);
    stream.read(&_data[0], size);
    std::cout << "Image loaded into memory!" << std::endl;
  };

private:
  // just a member function to keep the file content in memory
  std::string _data;
};

int main(int argc, char **argv) {
  MyHugeImage image("myhugeimage.jpg");
  std::this_thread::sleep_for(10s);
}
```

Cool! now we have simple program to load the images and we can start to improve it. Next, we need to change our program to start doing some image processing. For that we add a new function which will do something with the image. Let's take a look in this new function:

```cpp
void SomeCrazyImageProcessing(MyHugeImage image) {
  std::cout << "Wow! Some crazy and awesome image processing" << std::endl;
  std::this_thread::sleep_for(10s);
}

int main(int argc, char **argv) {
  MyHugeImage image("myhugeimage.jpg");
  std::this_thread::sleep_for(3s);
  SomeCrazyImageProcessing(image);
}
```

But when we run the program, we notice something which should not happen. After the `SomeCrazyImageProcessing` is called, the memory consumption of the program double! Well, this happens because we are passing the image to function *by value*. Which means that your object will be copied. Leaving us with two `MyHugeImage` objects in memory. One instantiated in the `main` function and another one initialized when the function `SomeCrazyImageProcessing` is called. 

![]({filename}/images/stackmem.gif)

That's not acceptable. It's waste of resources. For fix that we can receive the image as a *reference.* This means the the object will not be copied. A reference is similar to a pointer. But it's guarantee that will be **not** null and we do not need to use the `->` operator. Let's try that:

```cpp
void SomeCrazyImageProcessing(MyHugeImage &image) {
  std::cout << "Wow! Some crazy and awesome image processing" << std::endl;
  std::this_thread::sleep_for(10s);
}

int main(int argc, char **argv) {
  MyHugeImage image("myhugeimage.jpg");
  std::this_thread::sleep_for(3s);
  SomeCrazyImageProcessing(image);
}
```

Great, we avoided the additional object in memory and save the time necessary to create it. Now when checking the system monitor, we notice that the memory consumption will stay the same. But we have another problem to solve. Our program is storing data on the stack. In C++ when we do not use the `new` operator, the object is stored in the *stack*. Which in our case seems not be the best place to store the data. For those who are not familiarize with the concepts of *stack*  and *heap*, there is a section below explaining the difference between both. Okay, come back to the problem...

Keep things in the stack has its advantages. Like the automatic deallocation of the object. However, stack has a limit in size. As we are working with big images, it seems not the best place to put the data. There is another option. Store the data in the *heap*. But this comes with a price. We need to remember to release the memory requested when we are done. For that, it's used the `delete` operator. What happen when we call the `new` operator is that a memory block necessary to store the object is instantiated in the *heap* and the constructor is called to initialize the object in that piece of memory. So, let's update our class to does that:

```cpp
#include <chrono>
#include <fstream>
#include <iostream>
#include <thread>

using namespace std::chrono_literals;

/**
 * SOME OF THE INCLUDE AND FUNCTIONS USED IN THIS PROGRAM ARE FOR DEBUG ONLY.
 */

class MyHugeImage {
public:
  MyHugeImage(const std::string filepath) : _data(nullptr) {
    // read the whole file into memory
    // open the file and seek until the end
    std::ifstream stream(filepath, std::ios::binary | std::ios::ate);
    auto size = stream.tellg();
    _data = new std::string(size, '\0');
    // go back to the beginning if the file
    stream.seekg(0);
    stream.read(_data->data(), size);
    std::cout << "Image loaded into memory!" << std::endl;
  };

  ~MyHugeImage() { delete _data; }

private:
  // just a member function to keep the file content in memory
  std::string *_data;
};

void SomeCrazyImageProcessing(MyHugeImage image) {
  std::cout << "Wow! Some crazy and awesome image processing" << std::endl;
  std::this_thread::sleep_for(10s);
}

int main(int argc, char **argv) {
  MyHugeImage image("myhugeimage.jpg");
  std::this_thread::sleep_for(3s);
  SomeCrazyImageProcessing(image);
  std::this_thread::sleep_for(90s);
}
```

Now, our class store the data in the *heap.* Because we are creating the `std::string` object using `new` and storing the pointer in the `_data` member variable*.* It's important to highlight that this version has the *destructor.* Which is called when the object run out of scope. Thus, it releases the memory which contains the image data. Avoiding memory leaks. 

Furthermore, a pointer it is very cheap to be copied. That's why the `SomeCrazyImageProcessing` now is copying the object again. But this time, the bytes from the image will not be copied. Just the pointer. It does not mean you always should copy the object. Actually, the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#main) has best practice of where and when use arguments by value or reference and much more. You definitely should check it out! ;-)

Speaking on best practice, I would like to bring our attention to something important. In our example we have a class to initialize and release the resource (memory) , to store our image data. But why not just read the whole data in the main function and pass a pointer to the `SomeCrazyImageProcessing` function? Well, in this very simple and small program is easy to know where the resource is initialized and where it should be released. But imagine this program grow and hundreds of new functions are added and some parallelism and concurrency features are added as well... Who is the owner of the pointer? If we have a lot of different places pointing to the same resource, who is responsible to released? When it should be released? Things can get worst fast and this kind of raw pointer management can be a root of a lot of problems. This is where the `MyHugeImage` class comes to play. This is a very simple and naive implementation of what we call *Resource Acquisition Is Initialization.* 

*Resource Acquisition Is Initialization* (a.k.a. RAII) is a power concept in C++ to manage all kind of resources. Memory, files, sockets, you named it. Actually, this is a best practice of how to implement resource management in C++. Take a look in the [Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii). When we use RAII the acquisition and release of a resource happens automatically. C++ guarantees that an object will be initialized using its constructors and the destructor will be called when the object goes out of scope. That's why we can see the `delete` call in the class's destructor. When the object `image` in the function `main` goes out of the scope everything is clean up and we have no resources leaks. 

But as I sad before, our class is very bad implemented, it does not follow the [rule of five](https://en.cppreference.com/w/cpp/language/rule_of_three). So, we have the option to implement the rule of five or using something from the standard library. Let's do the former option. To archive this, we will use *smart pointers*. A cool thing about *smart pointers* is that they make explicit who are the owner of the pointer/resource. There are two main types of smart pointers. The `std::shared_ptr` and `std::unique_prt`. As you can probably guess, the first one allow a shared ownership of the resource. The former one allow only one owner. In both cases when every pointer instance is destroyed, the resources is released/deallocated. How does it work? Let's adapt our program to use some of the *smart pointer* as the resource manager for our data. 

```cpp
#include <chrono>
#include <fstream>
#include <iostream>
#include <thread>

using namespace std::chrono_literals;

/**
 * SOME OF THE INCLUDE AND FUNCTIONS USED IN THIS PROGRAM ARE FOR DEBUG ONLY.
 */

std::shared_ptr<std::string> LoadImage(std::string filepath) {
  std::ifstream stream(filepath, std::ios::binary | std::ios::ate);
  auto size = stream.tellg();
  auto data = std::make_shared<std::string>(size, '\0');
  // go back to the beginning if the file
  stream.seekg(0);
  stream.read(data->data(), size);
  std::cout << "Image loaded into memory!" << std::endl;
  return data;
}

void SomeCrazyImageProcessing(std::shared_ptr<std::string> image) {
  std::cout << "Wow! Some crazy and awesome image processing. There are "
            << image.use_count() << " owners of the pointer object"
            << std::endl;
  std::this_thread::sleep_for(10s);
}

int main(int argc, char **argv) {
  auto image = LoadImage("myhugeimage.jpg");
  std::this_thread::sleep_for(3s);
  SomeCrazyImageProcessing(image);
  std::cout << "Processing done! Now there are " << image.use_count()
            << " owners." << std::endl;
  std::this_thread::sleep_for(10s);
}
```

If we run the program, the output will be something like this:

```bash
Image loaded into memory!
Wow! Some crazy and awesome image processing. There are 2 owners of the pointer object
Processing done! Now there are 1 owners.
```

Notice the change in the owners count. When the object is passed to the `SomeCrazyImageProcessing` the argument object is a copy of the object passed by the caller. When this happen a counter inside the smart pointer object is incremented and the pointer to the resource copied. This is a very simple representation of what's going on:

![]({filename}/images/shared_ptr.gif)

When the function returns its pointer object decreases the owners count and it is destroyed. But as the counter is different from `0` the resource is **not** deallocated yet. This will happens when the last owner goes out of scope. In our example, that happens when the pointer object living inside the `main` function goes out of scope as well. It's good to mention that passing a smart pointer to function as an argument it is not a best practice. If the function just need to access the resource underneath  you should pass a [reference or a raw pointer](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-smartptrparam). But remember, references and raw pointer does not mean pointer ownership. 

Another smart pointer option is the `std::unique_ptr`. Different from the shared version, this one does not allow multiple owners. This means that when the pointer object is passed to another object/function, the previous one lost the ownership and the access to the resource. Let's update our program to does that. 

```cpp
#include <chrono>
#include <fstream>
#include <iostream>
#include <thread>

using namespace std::chrono_literals;

/**
 * SOME OF THE INCLUDE AND FUNCTIONS USED IN THIS PROGRAM ARE FOR DEBUG ONLY.
 */

std::unique_ptr<std::string> LoadImage(std::string filepath) {
  std::ifstream stream(filepath, std::ios::binary | std::ios::ate);
  auto size = stream.tellg();
  auto data = std::make_unique<std::string>(size, '\0');
  // go back to the beginning if the file
  stream.seekg(0);
  stream.read(data->data(), size);
  std::cout << "Image loaded into memory!" << std::endl;
  return data;
}

void SomeCrazyImageProcessing(std::unique_ptr<std::string> image) {
  std::cout << "Wow! Some crazy and awesome image processing." << std::endl;
  std::this_thread::sleep_for(10s);
}

int main(int argc, char **argv) {
  auto image = LoadImage("myhugeimage.jpg");
  std::this_thread::sleep_for(3s);
  SomeCrazyImageProcessing(image);
  std::cout << "Processing done!" << std::endl;
  std::this_thread::sleep_for(10s);
}
```

But there is a problem in the program. Take a look in the compiler output:

```cpp
main6.cc: In function ‘int main(int, char**)’:
main6.cc:31:33: error: use of deleted function ‘std::unique_ptr<_Tp, _Dp>::unique_ptr(const std::unique_ptr<_Tp, _Dp>&) [with _Tp = std::__cxx11::basic_string<char>; _Dp = std::default_delete<std::__cxx11::basic_string<char> >]’
   SomeCrazyImageProcessing(image);
                                 ^
In file included from /usr/include/c++/7/memory:80:0,
                 from /usr/include/c++/7/thread:39,
                 from main6.cc:4:
/usr/include/c++/7/bits/unique_ptr.h:383:7: note: declared here
       unique_ptr(const unique_ptr&) = delete;
       ^~~~~~~~~~
main6.cc:23:6: note:   initializing argument 1 of ‘void SomeCrazyImageProcessing(std::unique_ptr<std::__cxx11::basic_string<char> >)’
 void SomeCrazyImageProcessing(std::unique_ptr<std::string> image) {
      ^~~~~~~~~~~~~~~~~~~~~~~~
```

The compiler try to use the copy constructor of the `std::unique_ptr` class to copy the object from the caller (`main`) and initialize the argument of the function. But if that happen  there will be two objects pointing to the same resource. Which is what we do not want. The reason of why the compiler cannot access the copy constructor is because it does not exist. It is deleted. You can see that in the error message:  `use of deleted function ...`. This is how the `std::unique_ptr` class guarantee only one owner. The programmer **cannot** copy the object, just move it. Move semantics is another very powerful C++ feature and deserves a whole article for it. It allow the programmer to move object around scopes and objects without copy them. It is faster and more efficient. So, let's update our program to use `std::unique_ptr`. 

```cpp
#include <chrono>
#include <fstream>
#include <iostream>
#include <thread>

using namespace std::chrono_literals;

/**
 * SOME OF THE INCLUDE AND FUNCTIONS USED IN THIS PROGRAM ARE FOR DEBUG ONLY.
 */

std::unique_ptr<std::string> LoadImage(std::string filepath) {
  std::ifstream stream(filepath, std::ios::binary | std::ios::ate);
  auto size = stream.tellg();
  auto data = std::make_unique<std::string>(size, '\0');
  // go back to the beginning if the file
  stream.seekg(0);
  stream.read(data->data(), size);
  std::cout << "Image loaded into memory!" << std::endl;
  return data;
}

void Processing1(std::string &image) {
  std::cout << "Processing1" << std::endl;
}

void Processing2(std::string &image) {
  std::cout << "Processing2" << std::endl;
}

void SomeCrazyImageProcessing(std::unique_ptr<std::string> image) {
  std::cout << "Wow! Some crazy and awesome image processing." << std::endl;
  Processing1(*image);
  Processing2(*image);
  std::cout << "Processing done!" << std::endl;
}

int main(int argc, char **argv) {
  auto image = LoadImage("myhugeimage.jpg");
  SomeCrazyImageProcessing(std::move(image));
}
```

We take the opportunity to update the processing function adding more processing features ;-). Also we start to use raw pointer to give access to the function which just need access to the resource and does not need to manage the pointer object itself, as defined in the [C++ Core guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r-resource-management). In this version the image data is released after we are done with the processing. In other words, when the `SomeCrazyImageProcessing` returns. 

![]({filename}/images/unique_ptr.gif)

Another way to thing about smart pointer, as said by Bjarne Stroupstrup (C++ creator), is like a garbage collection mechanism. They clean stuff that you do not want to remember to clean. But it's important to highlight that this can be use for any kind of resource which requires some kind of *pair of functions,* like `open` and `close`. ;)

### Final thoughts

That's all I have to you now. I hope this superficial article helps you understand what RAII is and how it can help you to handle resources properly in your C++ programs. I believe this is a very powerful concept which you should use in your C++ program right away. However, I do not think you should rewrite all your applications in C++ just because you just learnt classes which release resources "automatically" for you. As I've listened from one engineer, programming languages are a tools. Each tool has your goal. Do you not paint a wall with a hammer, don't you?

If you would like to know more or if the article is confuse, let me know. Furthermore, there are more material in the references section.

### Stack and  heap

Every program running in your computer consumes memory. This memory is split in 2 main parts. All leave in your RAM, but it's used differently by the running program. The most important ones are *stack* and *heap* (a.k.a. free store). In C++ memory model has other types of memory. But they are not important for this article. So, let's ignore them for now.

When a program are running, every time a function is called a new *stack* frame is created. This *stack* frame has the functions arguments and the local variables used in the function scope. Once the function returns that memory is released. In the other hand, when the memory is allocated in the heap, it sits there until the memory is released by the program. If you have never worried about release memory is because your programming language has a mechanism to clean the memory automatically for you.

In C++ is up to the programmer decide if the object will live on *stack* or *heap*. It's quite simple. If the object is allocated using the `new` operator, it will be stored in the *heap*. Which means that programmer must call `delete` to release that memory.  The `new` operator returns a pointer to the object initialized in the `heap`. Another option is instantiate the object on the *stack*. Here's an example of both methods:

```cpp
#include <iostream>

class MyClass {
public:
  int intMemeber;
  float floatMember;
};

int main(int argc, char **argv) {
  // alloc the object in the stack
  MyClass myClassObj;
  myClassObj.intMemeber = 1;
  myClassObj.floatMember = 2.0;
  std::cout << "int: " << myClassObj.intMemeber
            << ", float: " << myClassObj.floatMember << std::endl;
  // alloc the object in the heap
  MyClass myClassObj2 = new MyClass();
  myClassObj2->intMemeber = 1;
  myClassObj2->floatMember = 2.0;
  std::cout << "int: " << myClassObj2->intMemeber
            << ", float: " << myClassObj2->floatMember << std::endl;
  delete myClassObj2;
}
```

### References

---

[CppCon 2019: Arthur O'Dwyer "Back to Basics: Smart Pointers"](https://www.youtube.com/watch?v=xGDLkt-jBJ4)

[CppCon 2019: Arthur O'Dwyer "Back to Basics: RAII and the Rule of Zero"](https://www.youtube.com/watch?v=7Qgd9B1KuMQ)

[C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

---
