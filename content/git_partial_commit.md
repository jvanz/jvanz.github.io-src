Title: Git: partial commit
Date: 2016-01-28 00:00
Tags: git
Author: José Guilherme Vanz

This post will demonstrates one of many cool features available in Git, partial commit. This feature allows commit
some hunk of a file leaving other ones for a future commit.

Let's suppose in a project there is the following source code:

```c
#include <stdio.h>

void foo(void);
void bar(int);

int main(int argc, char **argv)
{
	foo();
	bar(100);
}

void foo()
{
	printf("Hello, it's foo function here\n");
}

void bar(int x)
{
	printf("Hello, it's bar function here. Wow! You send me a %d... it's such a number! ;)\n", x);
}
```

In this brand new repository there is only one commit:

```
$ git log
commit aba1cbab0b427a9e6713f2fe563e2b14db6e51cd
Author: José Guilherme Vanz <guilherme.sft@gmail.com>
Date:   Tue Jan 26 20:45:42 2016 -0200

    Add commit.c

```

And the first change is made:

```
$ git diff
diff --git a/commit.c b/commit.c
index ce46da0..9eaf12b 100644
--- a/commit.c
+++ b/commit.c
@@ -16,5 +16,7 @@ void foo()

 void bar(int x)
 {
+       printf("--------------------------------------------------");
        printf("Hello, it's bar function here. Wow! You send me a %d... it's such a number! ;)\n", x);
+       printf("--------------------------------------------------");
 }

```

Suppose a colleague requests another update in same file. He/She asks to change the name of the `foo()` function to
`xpto()`. So after both changes the diff is:


```
diff --git a/commit.c b/commit.c
index ce46da0..8255080 100644
--- a/commit.c
+++ b/commit.c
@@ -1,20 +1,22 @@
 #include <stdio.h>

-void foo(void);
+void xpto(void);
 void bar(int);

 int main(int argc, char **argv)
 {
-       foo();
+       xpto();
        bar(100);
 }

-void foo()
+void xpto()
 {
        printf("Hello, it's foo function here\n");
 }

 void bar(int x)
 {
+       printf("--------------------------------------------------");
        printf("Hello, it's bar function here. Wow! You send me a %d... it's such a number! ;)\n", x);
+       printf("--------------------------------------------------");
 }

```

Nice, now it's time to commit the changes. However, it's necessary commit each hunk in different commits. Fortunately
git has a feature that will help on this situation. The command `git add` and `git commit` allows user to select which
hunks of a file should be added. This is done by passing the `-p, --patch` option. In our example, let's use `git commit`
to choose the hunks should be added in first commit:

```
$ git commit -p commit2.c
diff --git a/commit.c b/commit.c
index ce46da0..8255080 100644
--- a/commit.c
+++ b/commit.c
@@ -1,20 +1,22 @@
 #include <stdio.h>

-void foo(void);
+void xpto(void);
 void bar(int);

 int main(int argc, char **argv)
 {
-       foo();
+       xpto();
        bar(100);
 }

-void foo()
+void xpto()
 {
        printf("Hello, it's foo function here\n");
 }

 void bar(int x)
 {
+       printf("--------------------------------------------------");
        printf("Hello, it's bar function here. Wow! You send me a %d... it's such a number! ;)\n", x);
+       printf("--------------------------------------------------");
 }
Stage this hunk [y,n,q,a,d,/,s,e,?]?
```

As can be seen, git shows each hunk and asks the user for what should be done with it. The options are: [y,n,q,a,d,/,s,e,?].
To see help text, type `?`. The following text shall be shown:

```
y - stage this hunk
n - do not stage this hunk
q - quit; do not stage this hunk or any of the remaining ones
a - stage this hunk and all later hunks in the file
d - do not stage this hunk or any of the later hunks in the file
g - select a hunk to go to
/ - search for a hunk matching the given regex
j - leave this hunk undecided, see next undecided hunk
J - leave this hunk undecided, see next hunk
k - leave this hunk undecided, see previous undecided hunk
K - leave this hunk undecided, see previous hunk
s - split the current hunk into smaller hunks
e - manually edit the current hunk
? - print help
```

As the file is very small, all changes are shown as a unique hunk. So is necessary split it, selecting for the first
commit just the changes related if `bar()` function. For that, there are two options: `s` and `e`. In first one,
git splits the current hunk into smaller ones. The second allows user manually choose which hunk it wants. In this
sample we will use `s` options. So after select the actions, git shows:

```
Stage this hunk [y,n,q,a,d,/,s,e,?]? s
Split into 5 hunks.
@@ -1,7 +1,7 @@
 #include <stdio.h>

-void foo(void);
+void xpto(void);
 void bar(int);

 int main(int argc, char **argv)
 {
Stage this hunk [y,n,q,a,d,/,j,J,g,e,?]?
```

The previous hunk has been split into 5 hunks. Git now will iterate all of them asking the user what should be done
with each one. The first hunk should be ignored, as it is not related with function `bar()`. Hence, the `n` option
(do not stage) is the right one.

```
Stage this hunk [y,n,q,a,d,/,j,J,g,e,?]? n
@@ -4,8 +4,8 @@
 void bar(int);

 int main(int argc, char **argv)
 {
-       foo();
+       xpto();
        bar(100);
 }

Stage this hunk [y,n,q,a,d,/,K,j,J,g,e,?]?
```

Second hunk should not be added either:

```
Stage this hunk [y,n,q,a,d,/,K,j,J,g,e,?]? n
@@ -9,10 +9,10 @@
        bar(100);
 }

-void foo()
+void xpto()
 {
        printf("Hello, it's foo function here\n");
 }

 void bar(int x)
 {
Stage this hunk [y,n,q,a,d,/,K,j,J,g,e,?]?
```
The same with third one...

```
Stage this hunk [y,n,q,a,d,/,K,j,J,g,e,?]? n
@@ -13,7 +13,8 @@
 {
        printf("Hello, it's foo function here\n");
 }

 void bar(int x)
 {
+       printf("--------------------------------------------------");
        printf("Hello, it's bar function here. Wow! You send me a %d... it's such a number! ;)\n", x);
Stage this hunk [y,n,q,a,d,/,K,j,J,g,e,?]?
```

In the fourth hunk we have the first change related with `bar()` function. As could be seen, this hunk must be in the
commit. Thus, `y` (stage this hunk) is the correct option this time.

```
Stage this hunk [y,n,q,a,d,/,K,j,J,g,e,?]? y
@@ -19,2 +20,3 @@
        printf("Hello, it's bar function here. Wow! You send me a %d... it's such a number! ;)\n", x);
+       printf("--------------------------------------------------");
 }
Stage this hunk [y,n,q,a,d,/,K,g,e,?]?

```

Again, the fifth hunk should be added. Choose `y` option...
When there are no more hunks to be analyzed git opens the editor to the user write a commit message. Once the message is
written, it's done. See:

```
$git log
commit 8f1b1bc364a8e5ea83ab43ed95c0de026263561d
Author: José Guilherme Vanz <guilherme.sft@gmail.com>
Date:   Tue Jan 26 22:43:05 2016 -0200

    Changes in bar() function

commit aba1cbab0b427a9e6713f2fe563e2b14db6e51cd
Author: José Guilherme Vanz <guilherme.sft@gmail.com>
Date:   Tue Jan 26 20:45:42 2016 -0200

    Add commit.c

$ git diff
diff --git a/commit.c b/commit.c
index 9eaf12b..8255080 100644
--- a/commit.c
+++ b/commit.c
@@ -1,15 +1,15 @@
 #include <stdio.h>

-void foo(void);
+void xpto(void);
 void bar(int);

 int main(int argc, char **argv)
 {
-       foo();
+       xpto();
        bar(100);
 }

-void foo()
+void xpto()
 {
        printf("Hello, it's foo function here\n");
 }

```

Hence, the first commit contains just the changes made with `bar()` function. The remaining changes can be committed in
second commit:

```
$git commit -a -m "Rename foo() function to xpto()"
[master c12c40a] Rename foo() function to xpto()
 1 file changed, 3 insertions(+), 3 deletions(-)

$git log
commit c12c40a83fe5295bc84ca0928182881426d9d752
Author: José Guilherme Vanz <guilherme.sft@gmail.com>
Date:   Tue Jan 26 22:48:50 2016 -0200

    Rename foo() function to xpto()

commit 8f1b1bc364a8e5ea83ab43ed95c0de026263561d
Author: José Guilherme Vanz <guilherme.sft@gmail.com>
Date:   Tue Jan 26 22:43:05 2016 -0200

    Changes in bar() function

commit aba1cbab0b427a9e6713f2fe563e2b14db6e51cd
Author: José Guilherme Vanz <guilherme.sft@gmail.com>
Date:   Tue Jan 26 20:45:42 2016 -0200

    Add commit.c
```

I hope you have enjoyed the tip. ;)
