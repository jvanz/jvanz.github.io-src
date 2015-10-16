---
layout: post
title: Recovering missed data from stash
---

Today my colleague almost lost everything that he did during 4 days! Because  a wrong git command he dropped his changes saved on stash.
After this sad episode we looked for a way to try to recover as least part of his work... and we did it!

<!-- more -->

First of all, when you are implementing some big feature, split it in small pieces and commit it regularly. It's not a good idea stay so long time without commit your changes,  so take care.

Let's simulate a scenario to show what you can do when you lost some changes dropped from stash.
On our repository we have only one source file, main.c. We will use it to demonstrate the problem and the solution... so, our repository now is been like this:


![](/public/img/missing_data_from_stash_01.jpeg)

and he have only an commit, the initial commit:

![](/public/img/missing_data_from_stash_02.jpeg)

The first version of out file is:

![](/public/img/missing_data_from_stash_03.jpeg)

So, let's start to code something. For this example, we do not need some big change, is only something to put in the stash. For this, I just will add a new line. The git-diff output should be:

![](/public/img/missing_data_from_stash_04.jpeg)

Now, suppose that you have to pull some new changes from remote repository and you do not want to commit you changes. Thus, you decided to stashed your changes, pull the changes from remote repository
and apply your changes again on the master.  For this, you execute the following command to move your changes to stash:

```git stash```

Looking into the stash we can see our changes there:

![](/public/img/missing_data_from_stash_05.jpeg)

Now our code is in a safe place and the master branch is clean ( check with `git status`) and you can pull the changes. After pulled the changes, it's time to apply your changes again on the master.
But accidentally you execute

```git stash drop```

instead of:

```git stash pop```

and now, if you execute `git stash list` again, you can see that you dropped changes from the stash and does not apply them again on the master branch. OMG! Who can help us?
As you will seen soon git did not delete the object that contains your changes. It just remove the reference to it.
To prove this you can used the `git-fsck` command, this command verifies the connectivity and validity of the objects in the database.
On the begin of the repository I executed the `git-fsck` command and the output were:

![](/public/img/missing_data_from_stash_07.jpeg)

Basically, I asked `git-fsck` show me the objects that are unreachable ( `--unreachable` argument ). As you can see, it didn't show any unreachable object.
After I dropped the changes on my stash I executed the same command, and the output was different:

![](/public/img/missing_data_from_stash_08.jpeg)

Now, we can see 3 unreachable objects. But which is our changes? Actually, I don't know. We have to search for it, for this job you can execute the `git-show` command for visualize what are each objects.

![](/public/img/missing_data_from_stash_09.jpeg)

There it is! The ID 95ccbd927ad4cd413ee2a28014c81454f4ede82c is our changes. Ok, we found your missed changes. Let's recover it!
An possible solution is checkout the ID into a new branch or apply the commit directly. Once you have the ID of the object with your changes is up to you decide what is the best way to put changes on the master branch again.
For this example I will use the `git-stash` to apply the commit on my master branch again.

```git stash apply 95ccbd927ad4cd413ee2a28014c81454f4ede82c```

A important thing to remember, git run its garbage collector periodically. After the gc execution you cannot see more the unreachable objects using `git-fsck`. ;)


