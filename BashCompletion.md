

# Using completion #
In case you don't know what `bash` completion looks like, watch this...

| ![https://pyroscope.googlecode.com/svn/trunk/pyrocore/docs/videos/bash-completion.gif](https://pyroscope.googlecode.com/svn/trunk/pyrocore/docs/videos/bash-completion.gif) |
|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Every time you're unsure what options you have, you can press TAB twice to get a menu of choices, and if you already know roughly what you want, you can start typing and save keystrokes by pressing TAB once, to complete whatever you provided so far.

So for example, enter a partial command name like `rtco` and TAB to get "`rtcontrol `", then type `--` and TAB twice to get a list of possible command line options.

# Activating completion #
To add `pyrocore`'s completion definitions to your shell, call these commands:
```
pyroadmin --create-config 
touch ~/.bash_completion
grep /\.pyroscope/ ~/.bash_completion >/dev/null || \
    echo >>.bash_completion ". ~/.pyroscope/bash-completion.default"
. /etc/bash_completion
```
After that, completion should work, see the above section for things to try out.