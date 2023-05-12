# Managing my personal knowledge base · tkainrad

Created: Jan 10, 2020 6:23 PM
Tags: Productivity, Self
URL: https://tkainrad.dev/posts/managing-my-personal-knowledge-base/

# Introduction

It is hard to imagine any other field where lifelong learning is more important than in software engineering. Another unique characteristic is the degree to which learning material is available for free on the internet. On top of that, we create various resources ourselves by documenting issues, submitting bug reports, writing notes, creating documentation, and many others. The sum of all these resources can be called a knowledge base. You could argue that every developer has a system to manage their personal knowledge base, whether they know it or not. In this post, I explain my knowledge management practices.

A software engineer's personal knowledge base is likely to overlap with the knowledge of their employers and project partners. Be sure to carefully study your data protection obligations. A good basis is to keep your personal knowledge base strictly technical and to never include data that is related to customers, or people in general.

I chose this topic mainly because of three reasons:

1. **Fun:** I enjoy thinking about my workflows and trying to improve them. Maybe a little too much, some friends have started to roll their eyes when I try to recommend a new tool to them.
2. **Improving my system and workflows:** Writing [a post about my Linux setup](https://tkainrad.dev/posts/setting-up-linux-workstation/) has been very rewarding for me. While documenting my configuration, especially my command-line workflows, I identified some shortcomings that I have since eliminated. After writing this article, I can already say that my knowledge management workflows have improved similarly.
3. **Relevance:** Knowledge management in all its forms is integral to software engineering.

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/is_it_worth_the_time.png](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/is_it_worth_the_time.png)

Knowledge management tasks are done frequently. It pays off to do them efficiently. (Source: xkcd.com)

Much of this post comes down to describing my usage of software tools. The stars will be

Copying all of my practices will likely not serve you well. I invite you to try out things at your own pace and revisit this post whenever you are looking for new ideas.

# Bookmarking

Even though everybody loves books, or at least says so, myself included, the reality is that we rely on digital resources most of the time. The challenge is to organize this knowledge efficiently without creating too much overhead.

There are some naive approaches that I do not deem sufficient. Until a few years ago, I relied mainly on browser bookmarks, but for some reason, browsers do not provide proper organizing features. Another way is to just copy the URLs into notes, project issues, documentation and all other kinds of manually created content. This is viable and we all do it regularly, but it has nothing to do with what I think is bookmark management.

My current setup is a little more complex, but in the end, it does not require more work than keeping bookmarks solely in the browser. I organize my bookmarks in multiple layers, depending on how often I want to access them and how long they should persist.

Maybe you are thinking of caching now, but fortunately, bookmarking layers are not caching levels. This would be hard to manage because as we all know, there are [two hard problems in computer science](https://martinfowler.com/bliki/TwoHardThings.html): cache invalidation, naming things, and off-by-1 errors. In contrast to cache entries, a bookmark is not supposed to move between layers. Instead, it gets inserted at the right place and stays there.

The following figure illustrates my layers:

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/bookmarking-layers.png](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/bookmarking-layers.png)

Bookmarking layers

## 1. Chrome bookmarks

Chrome bookmarks have some nice benefits. They are synchronized between devices, new ones can be added easily, and organizing them in folders brings at least some structure. Another advantage for me is the [Albert Chromium extension](https://albertlauncher.github.io/docs/extensions/chromium/) that lets me access and open my Chrome bookmarks from Albert:

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/albert-chrome-bookmarks.gif](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/albert-chrome-bookmarks.gif)

Searching through Chrome bookmarks directly from Albert. Pressing enter opens the selected entry in Chrome. 

Because of these advantages, Chrome bookmarks are ideal for things that I need often and want to have accessible somewhat independent of context. They are, however, not well suited for keeping extensive bookmarks libraries. There is no tagging, it is not possible to add comments, and browsers do not even save a timestamp for when a page was bookmarked. It is further not possible to filter and search Chrome bookmarks using complex queries. In my experience, browser bookmark libraries are hard to manage if they grow beyond a certain size.

Some examples of well-suited Chrome bookmarks:

- AWS EC2 dashboard
- Google cloud platform console
- Slack workspaces
- GitLab boards

Examples of things that **should not be** Chrome bookmarks:

- Blog posts to be read later
- Links to Open Source Projects
- Stack Overflow questions

## 2. Workona

Workona is a relatively new addition to my toolbox. I have mixed feelings about it, mainly because it can feel a little slow at times. There are some things it does very well though.

Workona lets you create browser workspaces that come with their own list of bookmarks. This works nicely when you have multiple projects that you work on for longer periods. It will also remember which tabs you had open in a specific workspace and synchronize this information across devices. It is, therefore, a nice place for things that I need often *dependent* on context.

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/workona-workspace.jpg](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/workona-workspace.jpg)

Screenshot of a Workona Workspace (Source)

Workona further allows you to add apps and will then collect links and even features for those apps to be quickly accessible. For example, I use it to access my different GitLab and GitHub projects, Slack Workspaces, and sometimes even StackOverflow questions. These entries are automatically created by Workona and therefore I do not see them as bookmarks. It is also possible to access features of these apps directly from Workona, mainly to create new resources, such as GitLab/GitHub projects, Google Docs, DropBox Files and so on. It feels a little bit like [Station](https://getstation.com/) built directly into the browser.

The selling point for me is that Workona **lets me do all of the described things via shortcuts** and it is even possible to customize these shortcuts at `chrome://extensions/shortcuts`.

## 3. Notion

Finally, we arrive at the layer that is suited for maintaining a large library of bookmarks. For this, and many other use cases, I use [Notion](https://www.notion.so/?r=cb45b9cefd824015a044b3336009be32). It has become the core of my personal knowledge base.

Notion's free tier comes with a hard limit on the number of blocks you can create. This means that you will have to switch to the paid version if you use it seriously for a while. It is free for [students and teachers](https://www.notion.so/Notion-for-students-teachers-adc631df15ee4ab9a7a33dd50f4c16fe). All links to Notion in this post are affiliate links. If you sign up for an account through these links, you will get 10$ of free Notion credit and I will get 5$. This works even if you create a free account.

The killer feature for me is the database. It is amazingly flexible and is single-handedly able to replace multiple other tools for me. For my bookmark collection, I use a single large database. Adding new items can be done via the [Notion Web Clipper](https://chrome.google.com/webstore/detail/notion-web-clipper/knheggckgoiihginacbkhaalnibhilkk). I am a little annoyed that the web clipper doesn't let me add properties and tags directly, but other than that, it works well. Previously, I used Trello, which was also quite good at keeping bookmarks. However, to limit the number of different tools I use, I replaced it with Notion.

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-bookmark-database.png](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-bookmark-database.png)

My bookmarks database filtered to show only entries related to this post.

The goal with this database is that I can find something years from now with only a vague memory that it should be there. This is possible because Notion automatically stores metadata, such as a creation timestamp. Even more important, I can add tags and arbitrary properties.

Things get really exciting once you use relations between different Notion databases. As an example, I have a database of my blog posts that has a relation to my bookmarks. I can now filter my bookmarks by blog posts and quickly see which sources influenced a particular post.

I cannot cover all Notion database features in this post. I think this is something you have to see for yourself. The [Notion docs page about the topic](https://www.notion.so/Intro-to-databases-fd8cd2d212f74c50954c11086d85997e) might give you some further impressions though.

The downside of this rich feature palette is that it requires some discipline. I tag and annotate new entries, that I added via the web clipper, about twice a month. Often, I just delete new items because they do not seem important anymore. If I can not think of appropriate tags or relations for an item, this often means that it is not very relevant to me.

Another important lesson I had to learn the hard way: Do not use too many databases in parallel. Notion provides excellent methods for filtering, and searching tables. You can even define different views onto the same database that only shows a specific part of the data. It is therefore not required to separate all kinds of things into different databases. For example, at first, I had three different databases for Python resources, Django resources, and Wagtail resources. This was a bad solution. Now, these all live in the same database with appropriate tags.

I hope that someday I will be able to search through my Notion databases from [Albert](https://github.com/albertlauncher/albert). Maybe I will build an extension myself once the Notion API is finally released.

To illustrate what I have described in probably too many words, you can have a look at a [public fraction of my bookmarks database](https://www.notion.so/tkpersonal/047517457f70471a91a9dac793b8d51b?v=802c2ec373fa43d0b7caf16ed8bfccda) containing all the resources that were helpful for writing this post. The post-column in this public database appears empty because the related table is not public.

## 4. Native Bookmark Sources

The last layer does not require any work at all. It only means to be aware of native bookmark sources when trying to find something, and also when thinking about adding new bookmarks. For example, it is quite easy to search through questions you have answered on Stack Overflow. It is also not a problem to go back to your Hacker News posts or search through projects you starred on GitHub. Keeping those things in your own bookmark sources adds redundancy and noise. These are some of my most commonly used native bookmark sources:

## Summary

I am aware that this sounds immensely complicated. However, I stick to my statement that it does not actually require more work than keeping all bookmarks in the browser. You still have to add every bookmark only once. If you internalize your system, you will not have problems searching for bookmarks as it will be quite obvious where a specific resource could be. Admittedly, it does require some maintenance to keep a large bookmark collection in Notion, but it pays off soon and the pay-off accumulates over time.

# Organizing Self-Written Resources

Having a proper system for external resources is great, but it does not help much if everything you write yourself is a mess. Therefore, it is essential to organize self-written resources.

## Blog Posts

My most successful blog post is about [how I run and host this website for free](https://tkainrad.dev/posts/using-hugo-gitlab-pages-and-cloudflare-to-create-and-run-this-website/). However, the post does not cover the most work-intensive part about running this site: Writing and maintaining blog posts. For this, I heavily rely on Notion. I have a database with all my past blog posts and ideas for future posts. It is simple to add tags like `done`, `doing`, `idea`, and to view the database as a kanban board with lanes based on those tags.

All posts that are published on this blog have been drafted in [Notion](https://www.notion.so/?r=cb45b9cefd824015a044b3336009be32). When they are more or less finished, I use the markdown export and copy the content into a new text file in my [Hugo](https://gohugo.io/) project. There are some minor issues with this. Usually, I have to adjust code formattings and links, but overall it works very well and has some nice benefits:

- **Edit on all devices** Using notion, I can easily edit my drafts on all devices, even on my phone when I am moving.
- **Use existing notion content** I can quickly add code snippets, links, and other stuff that I keep in Notion. This can be done via database relations or just by dragging the respective blocks into the draft page.
- **Lightweight version control** As developers, we love GIT. However, for adding a couple of lines to a blog post, it is an overkill. Notion has versioning features build-in and keeps track of all changes automatically. Naturally, it does not offer sophisticated merging options, but it's easy to stay clear of conflicts when you are writing a personal blog.

Once a post is released, I move the post from `doing` to `released`.

### Keeping Track of Update Ideas

You may have noticed that some of my blog posts are quite long. Keeping them up-to-date is a little challenging. Fortunately, I have Notion to assist me with this. I have a database where I add proposals for updating my existing posts. Using a relation, I link these ideas to the respective posts in my posts database:

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-blog-update-proposals.png](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-blog-update-proposals.png)

It is hard to know when you are finished setting up the perfect Linux workstation.

To keep track of third-party resources that were helpful in creating a post, I add them to my bookmarks database and link them to my posts database.

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-blog-sources.png](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-blog-sources.png)

My bookmarks database filtered to show only entries related to this post.

You can also have a look at the full list of sources for this post via a [public fraction of my bookmarks database](https://www.notion.so/tkpersonal/047517457f70471a91a9dac793b8d51b?v=802c2ec373fa43d0b7caf16ed8bfccda).

## Taking Notes

I suppose every software engineer takes notes to some extent, even if they do not have a system and just casually write stuff into text files. There is also a large amount of free and paid software for taking and organizing notes. Some people even like to use physical paper with the [BuJo](https://en.wikipedia.org/wiki/Bullet_Journal) system.

No matter which method you prefer, you have to think about when, why, and how to take notes.

### When to take Notes

I thought quite a bit about this question, and previously I did not adhere to any predefined rules regarding this matter. To gain a better understanding of my habits and to decide what worked best in the past, I looked through my notes from the last years that were spread over multiple applications and lots of files. I tried to find common patterns:

- **Capturing information from audio sources** I am a visual learner and prefer written content over audio. However, there are many types of audio sources that everybody encounters:
    - Meetings
    - Presentations
    - Meetups
    - Conferences
    - Informal Discussions
    - Videos
    - Podcasts
- **Preserving information that is often needed but doesn't fit in any proper documentation project** In my case, these are things like the following:
    - Command-lines with multiple parameters, complex options, and paths. I keep them in my notes so that I can quickly copy-paste them in the potentially distant future.
    - Instructions for tasks that will likely have to be repeated in the future, for example
        - setting up a development environment for a specific tech stack
        - deploying a project on a specific hosting service.
- **Questions** Sometimes I think of a question that I would like to ask someone specific, who is not available at the moment. The question and its eventual answer are a nice use case for a note.

Thanks to a more sophisticated command-line setup with Zsh and various plugins for auto-completion and history-search, preserving command-lines has become much less important for me. If you are still using Bash with its default `Ctl` - `r` search, I think you would profit from my [post on setting up a Linux workstation](https://tkainrad.dev/posts/setting-up-linux-workstation/).

On the other hand, it is important to make clear also what **should not be a note** in this system:

- **Project-specific knowledge** Everything that is directly related to a specific software project, should not be a note in your personal knowledge base. Instead, it should go into whichever system is used to keep track of issues, merge requests, documentation, and so on. This post includes a [separate section on this below](https://tkainrad.dev/posts/managing-my-personal-knowledge-base/).
- **Information that is needed for a very short time** Sometimes I need to take notes during a conversation that I will need only immediately afterward. For this, I just open VSCode and type ahead. Once the information is no longer needed, the file can be deleted completely.

In general, don't overdo and don't underdo it. If you take notes all the time, you create overhead and redundancy. If you never take notes, well, you will not have notes.

The obvious answer is to remember things. This does not mean that note-taking should replace your memory. To the contrary, taking notes provides structure and context and therefore helps your brain build up a map of your knowledge. I believe that taking notes *increases* the amount of data that you can recall from memory.

Additionally, some things are just very hard to remember, such as complex tech stacks presented at meetups, command-lines with several opaque options, numbers, and so on. Writing these things down can extend your knowledge base significantly. Notes are also very helpful when writing documentation in the future, or for writing blog posts like this one ;-)

### How to Take Notes

It can be tempting to just type ahead during a talk. Noting down whatever seems interesting at the moment. However, you should meet basic formal requirements and write down some context. Otherwise, you will have trouble extracting useful information from your notes in the future. If you take notes regularly, it is also important to organize them by assigning tags and properties, having a creation date, being able to filter and search through them, and so on. Software can help with these things.

Until about a year ago I kept notes mainly on my local machines, syncing them with Dropbox. Applications that focus almost exclusively on note-taking, such as [Evernote](https://evernote.com/), never had that much appeal to me, even though I used Google Keep/Notes. It is not so bad, supports e.g. labeling and works with little friction on mobile. However, there is not even basic formatting support, let alone markdown formatting or code syntax highlighting.

Then, I discovered [Notion](https://www.notion.so/?r=cb45b9cefd824015a044b3336009be32). At first, It wasn't really about note-taking for me. I liked it mainly because of its database concept and for organizing third-party resources as described in the [bookmarking section](https://tkainrad.dev/posts/managing-my-personal-knowledge-base/). However, by now, I use it heavily for almost all of my notes and other types of self-written content. I think Notion's mix of markdown syntax support, slash commands, and WYSIWYG makes for a great writing experience.

I strongly recommend organizing all your notes in a single database with appropriate tags, such as `meeting`, `presentation`, `tc`, and `question`. Similar to the bookmarks database described above, Notion will automatically provide a column with the creation time of the note. If you have frequent meetings with the same people, you can think about adding a *Participants* column.

A notes database is the perfect use case for another great Notion feature: [Templates](https://www.notion.so/Database-templates-454ed5ab5bd24226b58d176697bd7e10). This feature will allow you to created templates for your different types of notes and then, for example, add a new meeting note with one click. Depending on the template, the new note comes with a pre-defined layout and might include fields for the meeting's participants and agenda. This is what opens when I click to add new meeting notes in my database:

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-meeting-notes.png](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-meeting-notes.png)

My basic meeting notes template.

# Project-specific Knowledge

In my experience, it is best to keep project information as closely together as possible. For me, this means that issue tracking, merge requests (i.e. pull requests), documentation and everything else that comes with a software project should live alongside the source code.

This practice guarantees that anyone who works on the code now, or in the future, has access to all the information. My solution for this is to use GitLab for everything related to a specific project. This includes pretty much everything except some quick notes that I sometimes write in Notion because I do not want anyone else to see them.

To do this, GitLab offers a lot of project management and documentation features, such ass issue management, a project wiki, a Code snippet space for all projects and accounts, and more. A project wiki is a great place for all documentation that is not specific to an issue. This can include the following:

- Instructions for setting up the development environment
- Instructions for manual deployment
- Architecture descriptions and diagrams. I am a big fan of [mermaid](https://mermaidjs.github.io/#/), which allows creating UML diagrams with Markdown and is supported by GitLab.
- Guidelines regarding naming conventions, design paradigms, etc.

If you have read my post on [running and hosting this website](https://tkainrad.dev/posts/using-hugo-gitlab-pages-and-cloudflare-to-create-and-run-this-website/), you know that I use GitLab also for this personal blog project. Nevertheless, I use Notion for much of the project documentation and management tasks, because it comes with some unique benefits for this use case, as described [above](https://tkainrad.dev/posts/managing-my-personal-knowledge-base/).

Of course, there are alternatives. GitHub has caught up in the past and offers a very similar feature set. I have only limited experience with Atlassian products, but I suppose you can achieve the same thing by using a mix of BitBucket, Confluence, and Jira. On a side note, writing in Confluence feels a lot like writing in Notion. Both recognize markdown syntax and offer slash commands to quickly insert complex content types.

# Managing Files

This one is relatively straightforward. I think the most important thing is to use some form of cloud storage. Personally, I use Dropbox. Next, you should think about a proper folder structure. Finally, you should be able to search for your files quickly.

I use [Linux](https://tkainrad.dev/posts/setting-up-linux-workstation/) and rely on Albert for searching through files. If this doesn't work I use [the `locate` command](https://linuxize.com/post/locate-command-in-linux/) and, my last resort are command-line tools, such as `find`, and `grep`. They are still king for complex search requirements, such as regex matching and including also file content.

If you can tick the three boxes

1. availability on all devices
2. structure
3. searchable

you should be all set.

Notion databases support file columns. This means you can upload a different file to each cell. I have not yet found a use case related directly to software engineering for this. However, it is great for managing invoices.

# Additional Use Cases

In this section, I want to present some special kinds of knowledge management use cases that are unique to software engineering. Most of them I have picked up properly only after starting to use [Notion](https://www.notion.so/?r=cb45b9cefd824015a044b3336009be32). By no means, I want to say that you should copy all of them, but you are very welcome to try out what you think looks interesting.

## Code Snippets

Currently, I have two ways of collecting code snippets. I hope I can eventually integrate them somehow.

### VSCode User Snippets

The first one are [VSCode](https://code.visualstudio.com/) User Snippets. VSCode does many things right and snippet management is one of them. It is very easy to define new snippets and use them by typing a predefined string. Simply press `Ctrl`-`Shift`-`p` and choose *Preferences: Configure User Snippets*. Then, you can split your snippets into multiple files or just put all of them together in the `global-snipptes.code-snippets` file. These are some of my snippets for writing blog posts with markdown and Hugo:

[Untitled](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/Untitled%20Database%20d7f5c457cda2401489584661262f6813.csv)

The snippets can then be used by typing the prefix and pressing `Ctrl`+`Space`:

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/vscode-insert-snippet.gif](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/vscode-insert-snippet.gif)

### Notion Snippet database

The second use case concerns small pieces of code that I have written myself and that I would like to remember. This is not necessarily for productivity reasons, but rather for nostalgia. It is ideal for small algorithms, for example when you manage to substantially increase the performance of something by applying some clever technique.

I keep those snippets in a Notion database, which works great because I can tag them and add arbitrary properties. A nice benefit of this habit is that it's not a problem if you don't do it for a while. Your database will not look messy all of a sudden.

![Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-snippet.database.png](Managing%20my%20personal%20knowledge%20base%20%C2%B7%20tkainrad%20f62c7c9ae3cd4e5cb98610b8925d60e1/notion-snippet.database.png)

An exemplary entry of my code snippets database in Notion.

## Shortcut Database

I believe that typing proficiency is important for a software engineer. It is easier to stay in flow if you can type fast and navigate around your IDE and tools with shortcuts. As my set of tools grew, I realized that I have a hard time to keep track of which shortcuts I am using, which of them work in which application, and whether I can change them so that they work across as many tools as possible.

Therefore, I started to keep track of some shortcuts I would like to use everywhere. These are things like creating new tabs, creating new windows, opening the respective tool's search feature and more.

This database helps me identify overlaps and motivates me to think about which task could fit for a specific key-combination that I use often. For example, I use `Ctrl` - `Shift` - `T` in IDEs to search for type definitions and `Ctrl` - `Shift` - `R` to search for resources in general. Since I have these key combinations memorized for years and can use it very quickly, I want to make use of it wherever possible. Therefore, I try to set up my applications so that some kind of search opens whenever I use one of these combinations. My Notion database makes it easy to see which applications offer search features and which of them I can modify.

For example, my Browser now forwards `Ctrl` - `Shift` - `T` / `R` to [Workona](https://code.visualstudio.com/) and allows me to switch/search workspaces or use the general search, respectively.

Screenshot of my Notion shortcut database 

Notion's filtering and search capabilities are great for identifying problems with your setup. For me, a problem is when two applications use different shortcuts for a very similar operation. Unfortunately, Notion is negative example of an application that doesn't let you customize its shortcuts and therefore reduces the usefulness of my database. If someone from the Notion team reads this at some point, I kindly ask you to lobby on my behalf to prioritize personalized keyboard shortcuts.

I am excited about this use case and will talk about it in much more detail in a future blog post.

## Tools Database

I also have a Notion database to keep track of small web tools that I use. This serves little purpose for things that are used frequently as you will remember them anyway. However, for minor things that are only needed once in a while, such as color palette generators, detecting handwriting as LaTeX symbols, and checking SSL certificates this is quite handy. Usually, you can find these tools via google, but sometimes there are many tools for a task and it is nice to keep track of the ones that work best.

Screenshot of my software tools database in Notion. 

Again, the important thing here is to not overdo it. There are extensive publicly available lists of such tools. Your list should not be a copy of those but rather a small collection of the things you like and need from time to time.

## Collecting Ideas for new Projects

Like many software engineers in these golden times, I sometimes think about starting new software projects, maybe even bootstrapping a small business. You probably guessed it already, I keep ideas for possible projects in a Notion database. The main benefit is, once again, that it allows me to easily link it with other databases, such as my bookmarks.

# Conclusion

Similar posts often conclude with warnings that you should be very careful not to spend too much time on organizing and maintaining your knowledge and workflows. In principle, I agree with this sentiment. After all, you want to *increase* your productivity.

I do believe, however, that it is worth it to spend some time thinking about your knowledge management *system*. The most important part about conceptualizing a system is to decide exactly which types of information you want to maintain in your knowledge base. If you get this right you will benefit for the rest of your career. Even if the tools might change in the future, the system will stay.

Please don't hesitate to share your own experiences in the comments below. I am sure that my workflows are not perfect, but they might get closer with your tips.

This post is released together with [a new post in my *Reading List* series](https://tkainrad.dev/posts/reading-list-organizing-knowledge/), which lists related resources. If you want to dive even deeper into knowledge management concepts, you might want to have a look.