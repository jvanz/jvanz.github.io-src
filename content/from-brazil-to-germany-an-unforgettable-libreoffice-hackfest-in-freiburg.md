Title: From Brazil to Germany, an Unforgettable LibreOffice Hackfest in Freiburg
Date: 2014-01-24 00:00
Tags: hackfest, libreoffice, travel, germany
Author: José Guilherme Vanz


While I have not decided what it will be my first post about development stuff I'll post the text that me and my friend wrote to the The Document Foundation's blog. In that text we talked about out trip to LibreOffice hackfest in freiburg.
From Brazil to Germany, an Unforgettable LibreOffice Hackfest in Freiburg

José Guilherme Vanz and Marcos Souza, LibreOffice development in Brazil

Our first contact with the LibreOffice was in FISL 2012 (International Forum of Free Software, held in Porto Alegre, Brazil). Since then, we got quickly involved with the LibreOffice development community. Now we attend events in Brazil advocating to people about the better office suite ever done!
Months ago, after some time contributing to the project and participating in LibreOffice community, we, José Guilherme Vanz and Marcos Paulo de Souza were invited to participate in the Freiburg LibreOffice Hackfest. We were very happy and very excited! This invitation showed us that we were recognized for our humble work in the project and because this is a unique opportunity to work with people that we just know by mailing or IRC chats. So, we started the preparations of travel, such as paperwork, funds and a negotiation with our employers.

![]({filename}/images/hackfest_01.jpg)

We arrived in Germany thinking about how to learn more about LibreOffice code base, and learn some tips and tricks to code while contributing with the project. The guys at the hackfest work full time in the project, so we were very excited to improve our skills, including stuffs about how to make a nice hackfest and try setup one in Brazil!
Our journey in Germany began in the beautiful city of Munich, where we stayed for two days. We met Christian Lohmaier, the current release engineer of LibreOffice project. He and Florian Effenberger were patient and generous to show Munich to us and all nice places of this nice city! Thanks a lot guys!
Then we went to Freiburg, where the Hackfest was to start. The event took three days. We had the opportunity to meet some of the most famous mega developers! It was a very nice experience to link faces and names to IRC nicks, and of course, to question the “pythons” of the project in real time! Surely, we learned a lot in these 3 days!
Marcos did some work in LibreOffice Math. The first was about including tooltips in the new Elements Dock. To solve this bug, we basically need to create some strings with the descriptions of each element in the Elements Dock. These strings are stored inside “.src” files. These files are “compiled” and used by translators to translate each string to a specific language used in the user interface of LibreOffice. This fix was not difficult, just painful!
The second bug that Marcos worked was about to implement a scrollbar in the Elements Dock. We did not finish this fix because he had some doubts and some points that need some other fixes. Still in the event, we talked with some others hackers about other issues.
I was focused trying to execute a static checker to detect some error prone code and fix them

![]({filename}/images/hackfest_02.jpg)

After three days of hackfest, we started the “Hamburg Home Hacking Marathon”! We stayed four days in Hamburg, coding in the house of LibreOffice enginners! Again, we had the pleasure to work with Eike Ratke, Michael Stahl, Stephan Bergmann and Bjoern Michaelsen. All of them willing to help us teaching about the code base and showing some tips.
Using our precious time with them, Marcos worked in the issue 60698 (https://bugs.freedesktop.org/show_bug.cgi?id=60698). This bug is about unify some shared libraries that are built by few files. Doing this we get a smaller library because these libraries are compiled and built just once, and by this we avoid the dispersion of shared libraries. Working in this bug, Marcos unified all shared libraries of IO module.
Marcos tried yet to solve a bug in Calc, with the help of Eike as mentor. This bug was about ODS files using link to another sheets. By changing the referenced files, Calc was not allowed to update the data inside the file that was referencing. But, this bug was not so easy, and the problem was bigger than we thought. So we couldn’t solve this bug in that time, and Eike removed the bug from the easy hacks.
And I was still working in static checker. I started to look to a bug of Math, about the user interface. After some work, I fixed that bug!
In the third day, we went back to Stephan’s place, trying to solve bugs and learn more! This day Bjoern went to Stephan’s house too, totaling six guys programming in the same table! In this day Marcos worked in a bug(https://bugs.freedesktop.org/show_bug.cgi?id=63020) indicated by Bjoern. That bug was related to removing a class from LibreOffice. With Stephan’s help, Marcos could remove that class and use a better approach in the code.
And in the last day, we went again to Eike’s home, where we enjoyed to last moments with the great developers of LibreOffice! We talked a little about their work and how they work daily.

![]({filename}/images/hackfest_02.jpg)

For sure, these days were very fruitful, and we learned a lot of things that we’ll use in the future.
We came back to Brazil and we want to say a big THANK YOU for all of you guys! To the  Brazilian community, that welcomed us and keeps helping us. To The Document Foundation, who gave us this opportunity. To all developers that are helping us since we started in the project, specially YOU we met this wonderful German journey, and all people involved directly or indirectly in this amazing project!

Source: http://blog.documentfoundation.org/2013/12/04/from-brazil-to-germany-an-unforgettable-libreoffice-hackfest-in-freiburg/

Portuguese version: http://blog.pt-br.libreoffice.org/2013/12/09/do-brasil-para-a-alemanha-um-inesquecivel-hackfest-em-freiburg/
