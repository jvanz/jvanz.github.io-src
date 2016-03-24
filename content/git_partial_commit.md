Title: Git: partial commit
Date: 2016-01-28 00:00
Tags: git
Author: José Guilherme Vanz

This post will demonstrate one of many cool features available in Git, partial commit. This feature allows add just
some hunk of a file leaving other ones for future commit.

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

![]({filename}/images/partial_commit_1.png)

And the first change is made:

![]({filename}/images/partial_commit_2.png)

Suppose a colleague requests another update in same file. He/She asks to change the name of the `foo()` function to
`xpto()`. So after both changes the diff is:


![]({filename}/images/partial_commit_3.png)

Nice, now it's time to commit the changes. However, it's necessary commit each hunk in different commits. Fortunately
git has a feature that will help on this situation. The commands `git add` and `git commit` allows user to select which
hunks of a file should be added. This is done by passing the `-p, --patch` option. In our example, let's use `git commit`
to choose the hunks should be added in first commit:

![]({filename}/images/partial_commit_4.png)

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

In this example, it shown the first file's hunk. In the first commit, should be
committed the changes related with function `bar()` only. The this hunk must be
ignored. Thus, the option `n` is the right one.

![]({filename}/images/partial_commit_5.png)

In the following, git shows all further changes as an unique hunk. It's necessary
split them the smaller hunks. For do that, there is two options: `s` and `e`.
The first one tells git to split the hunk into smaller pieces. The `e` option,
in the other hand, allows user choose manually each lines should added. In this
post the go with option `s`. Git should shown something similar to this:

![]({filename}/images/partial_commit_6.png)

The previous hunk has been split into 3 hunks. Git now will iterate all of them
asking the user what should be done with each one. The first hunk should also be
ignored. The second one is the first change related with the function `bar()` and
should be added. To that task, the `y` is the right command.

![]({filename}/images/partial_commit_7.png)

Third hunk should be added too

![]({filename}/images/partial_commit_8.png)

Once there are no more hunks, as we used the `git commit` command, the editor
will be open to the user insert the commit message. That's it.

![]({filename}/images/partial_commit_9.png)

Now with the first commit contains the only the changes within `bar()` function,
further hunks might be committed in the second commit:

![]({filename}/images/partial_commit_10.png)

I hope you have enjoyed the tip. ;)
