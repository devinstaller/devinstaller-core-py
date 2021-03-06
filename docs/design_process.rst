==================
The Design process
==================

:Author: Justine Kizhakkinedath

Motivation
==========

It all began with my dotfiles, initially I started copy pasting my shell
commands in a file so that if I have reinstall my dotfiles I know how to
do it. But then it started getting really tedious, because I have to
manually copy paste into the file each time and copy paste back into the
shell when I needed.

So I transformed my file into executable shell script. But shell
scripting sucks that's when I started looking into dotfile installers.

These installers were all amazing but they were either too rigid or you
kinda end up writing lot of code.

So I came up Devinstaller.

Initial design
==============

I liked the simplicity of shell scripts but at the same time it lacked
the power of a full programming language.

So porting all the shell scripts into a programming language like Python
makes its maintenance an issue. As much as I like Python not everyone is
comfortable in it.

That's when the idea of specification file came into my mind. The
specification file should be a portable way of storing your instructions
that way if tomorrow someone smarter than me implements either a better
Python implementation of Devinstaller or just implemented in a different
programming language like Ruby etc everyone's Devinstaller specification
should run flawlessly.

The original specification file was a static file and just like your
regular config files, they defined the instructions and nothing more but
then it meant there was little to no interaction with the user once you
started the process. So you need to read and understand everything
before copying and using someone else's specification file. All of my
attempts to make the specification file itself interactive resulted in a
bad compromise.

Improved design
===============

This is when I got the idea of a 2 part "configuration system". I don't
like to call it config files, because it isn't. Config files are meant
to be static but here only one of it is. The other one (program file) is
a Python file. It has the full power of the Python programming language
and all of its library ecosystem as well as it has access to the
specification file itself.

Now it means you can have a static specification file which can be
completely overridden by the program file. I find that this is a better
compromise, of course the new "program file" faces the issue of
maintainability by non Python users but that can now easily be solved by
using some other implementation of Devinstaller supporting the
programming language of their choice.

So now everyone can use the specification file without any problem and
only the program file will be a potential pain point.

This pain point can be minimized by adding more features to the
Devinstaller application and the specification file.

At the same time I didn't wanted to reinvent the wheel.
