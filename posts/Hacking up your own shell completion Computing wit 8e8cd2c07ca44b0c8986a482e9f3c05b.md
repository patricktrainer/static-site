# Hacking up your own shell completion | Computing with Jeremy

Created: Mar 6, 2020 8:31 PM
URL: https://feltrac.co/environment/2020/01/18/build-your-own-shell-completion.html

In this post I’ll be walking through a simple hack I added to my shell that I think makes me more productive (if nothing else it makes me happy).

Note that all this applies to most common shells, but my examples will be using `[fish](https://fishshell.com/)` since that’s what I’ve been using as of late.

I’ll also be talking about using [fzf](https://github.com/junegunn/fzf) as a part of this hack. You can use `fzf` or not with this idea, but I like the feel of it :).

## Introducing: My Problems

As a full-stack (frontend, backend, and firmware) software engineer, I use quite a few tools to build, test, run, version control, and style check the code I write.

At my company we built this pretty simplistic go program that is really a collection of scripts for building and testing out parts of our application.

We’ll call the tool `doer` for fun.

Those things can be listed using the command `doer -list`.

No one really bothered making autocompletion scripts for 3+ shells used across the company for an internal tool, but I was having trouble remembering the exact abbreviations involved in the command I wanted to run.

## Script It!

Some people at my company use `fzf`. For the uninitiated, `fzf` is a program that lets you select from multiple options using a fuzzy find search.

The cool thing about `fzf` is that you can send it a newline separated list of items, and it’ll handle all the user interaction to select one and return the selected item.

Here’s an example of using `fzf` to choose a line from a file and echo it.

I’ve often used `fzf` as a file finder, you can simply run something like `git ls-files | fzf`, and pass the output to your editor, and you’ve already made a git aware fuzzy file finder, running this inside your editor like [fzf-vim](https://github.com/junegunn/fzf.vim) makes this even more powerful.

One quick solution to our `doer` problem is to write a bash script like this:

```
#!/bin/bash
doer $(doer -list | fzf)
```

Here we just use command substitution to run `doer`’s list command, pass it to `fzf`, then run doer with the result.

Here’s it in action:

This works *really* well, but unfortunately you lose shell history when you run this command.

For example, lets say I finally figure out through the fuzzy completion version of `doer` that I really want to run `doer gen/other_thing`, because it generates a file based on one I’m currently modifying.

So I run the command once, fuzzy selecting my option, modify some code, then return to my shell to quickly repeat the command I had just tried.

After a quick `CTRL-P` (or up arrow), or `CTRL-R`, I find that the only thing in my history is `doer-fuzzy`. That means I have to fuzzy find my option again and rerun, and it means I don’t have a great history of what I’ve run in the past. What a drag!

## Maintaining History

My first thought here was to somehow append the underlying command being run by `doer-fuzzy` to my shell history, but I quickly found out that this is hard, hacky, and no one really does this.

So really what we want is to trigger argument completion in the shell, so that by the time I hit return to trigger the command, the full command I’m interested in is on the shell already.

Oh wait… that sounds like just normal shell completion, you the know, the tab-tab-tab-tab-tab approach.

Okay fine, I guess I can add proper shell completion to the command using `fish`’s built in `complete` command, add it to the repo, and set up an install script. But now that I think about it, I have several commands I use that don’t support completion (not just `doer`), or complete too much stuff for my 90% use case, or just support so many options its a bit painful to autocomplete through tab key wear out.

What if there was a way to strap an `fzf` completion thing into my shell, that I fully control through just a couple lines of `fish` script, that doesn’t interfere with built-in completion, and allows me to quickly add bindings to any command I frequently run?

## Introducing Personalized FZF Completion!

`fzf` already sort of does this type of thing when you install the `fzf` bindings to your shell. Regardless of your currently typed command, you can hit `CTRL-T` to search for a list of files in your current directory. For example, lets say we’re trying to open a file in `nvim`.

What if we could copy how `CTRL-T` works, but replace the hardcoded `fzf` command with a contextual one that we control?

Here’s a basic `fish` script to accomplish the core part of this. Basically we just match on any commands that are prefixed with `doer`, and return an appropriate autocompletion function for that command.

```
function get-completion-command
	set -l cmd (commandline)
	switch $cmd
		case 'doer *'
			echo 'doer -list'
		case '*'
			return 1
	end
end
```

This function gets called in a skeleton version of `fzf`’s `CTRL-T` command.

```
function fzf-smart-completion -d "List files and folders"
	set -l commandline (__fzf_parse_commandline)
	set -l dir $commandline[1]
	set -l fzf_query $commandline[2]

	# use our cool new completion checker
	set -l FZF_CMD (get-completion-command); or return

	# fzf edge case and formatting (prevents fzf from taking up the whole screen)
	set FZF_HEIGHT 40%
	begin
	  set -lx FZF_DEFAULT_OPTS "--height $FZF_HEIGHT --reverse $FZF_DEFAULT_OPTS $FZF_CMD[2]"
	  eval "$FZF_CMD[1] | "(__fzfcmd)' -m --query "'$fzf_query'"' | while read -l r; set result $result $r; end
	end
	if [ -z "$result" ]
	  commandline -f repaint
	  return
	else
	  # Remove last token from commandline.
	  commandline -t ""
	end
	for i in $result
	  commandline -it -- (string escape $i)
	  commandline -it -- ' '
	end
	commandline -f repaint
end

bind -M insert \et fzf-smart-completion
bind \et fzf-smart-completion
```

With this little bit of `fish` scripting, we now have a pretty cool `ALT-T` command that runs our own fuzzy autocomplete like so.

This got me thinking, what other commands could benefit from this type of completion?

One example is `go test`, which for my use cases, should only run on source controlled files ending in `_test.go`. There’s no reason to autocomplete every file in my repo, just the test ones is perfect!

The same idea applies to our frontend test runner, if I’m typing `yarn test`, I probably only want to see typescript files ending with our `.test` convention.

```
function get-completion-command
	set -l cmd (commandline)
	switch $cmd
		case 'doer *'
			echo 'doer -list'
		case 'go test *'
			echo 'git ls-files | grep _test.go'
		case 'yarn test *'
			echo 'git ls-files | grep .test.ts'
		case '*'
			return 1
	end
end
```

You can see the go tester in action here:

Another useful thing I’ve found is automating some routine `git` commands.

Obviously there exist quite a few `git` UIs that try to allow you to use `git` more quickly than the CLI interface, but I have always come back to the CLI because frankly (1) there’s more documentation, and (2) it doesn’t have performance issues on massive monorepos that I’ve seen in every `git` UI (cough cough [magit](https://magit.vc/manual/magit/Performance.html#Performance)).

Good `git` autocomplete is awesome and likely used by everyone, but we can extend it using this same interface.

Simply adding the following gives you a `git add` command that completes only changed files and allows showing a toggleable preview of the file changes.

```
case 'git add *'
	echo 'git diff --name-only'
	echo '--bind='ctrl-space:toggle-preview' --preview 'git diff --color=always {}' -m'
```

If you look hard enough at these scripts, you’ll find there are flaws or gaps in this completion system.

A common example for me is my `git checkout` completion. I simply list local branches as targets. This obviously ignores a lot of different targets to the `git checkout` command including commits, specific files, remote branches, and tags, but for me, > 90% of the time I’m using it to just switch branches.

On top of that, using this new framework doesn’t break or invalidate any other tool you have, I frequently fall back to `fish`’s `git` completion when I’m doing something more specific, but I’m happy that my most common access patterns are now a bit faster.

This pattern also doesn’t add a layer of abstraction over the CLI tools you use, your shell history still is useful, you use the same CLI tools as everyone else, you just hopefully save yourself a bit of typing.

I’m quite sure this sort of thing would be pretty trivial to get working in both `bash` and `zsh` since they support `fzf`’s `CTRL-T` command as well. If I get a lot of long term use out of this maybe I’ll try getting a similar idea running in a few shells and share those scripts.