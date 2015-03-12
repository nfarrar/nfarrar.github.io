Title: Tintin Modules, Standards & Testing
Date: 2014-08-19
Category: tintin
Tags: tintin, mud
Status: draft

For quite a long time, I've been working on methods to bring the TinTin++ community into the current era of software development, by building methods for making TinTin++ scripts portable, implementing some standards, and building a testing framework. I've attacked this problem over and over and have approximately three separate codebases with modules using different methods for achieving these ends. I've migrated that code in the [TTUG Modules Repository](https://github.com/tintinplusplus/tintinplusplus-modules) and written up some basic information on my though process.

Two of the primary "modules" I've built, which I can't imaging playing without are my 'module manager' and my 'session manager'.

## Module Manager
The module manager essentially finds all the TinTin++ command files in a directory structure, strips the .tin extension and beginning of the path off which is used as a name for the module. So to summarize - it generates names for all of my command files and stores their path and a flag to identify whether or not they are loaded in a table. Each command file includes code which dynamically names the class in the command file, allowing the class to be bound to the command file so they can be loaded, unloaded, and reloaded on the fly. This also allows me to get a friendly list of the modules available to load (and which are loaded) at any time while playing, rather than having to remember paths to files and their unassociated class names, then trying to unload and load them that way. This is a much more convenient system and I can't imaging going back to the days when I didn't have it.

## Session Manager
The session manager reads a configuration file which defines a list of my sessions. The [included sample](https://github.com/tintinplusplus/tintinplusplus-modules/blob/master/cfg/sessions.tin) defines a single session - not very useful. My personal configuration file defines more than 20 - very helpful. The session manager provides an API that allows you to list the sessions, connection a session, and disconnection a session - but more importantly, it binds specific configuration files to each session for me - so that each time I load up the session, everything is configured the way I expect. I've also been planning to implement a restart session, which will cache the entire configuration from a session, write it out to disk, disconnect the session, then load back up the configuration, allowing me to continue where I left off.

Both of these are completely portable and good examples of what modules can be.

## Standards & Testing
One of the problems I've been trying to tackle with the modules is a way to implement a robust testing framework. It just occurred to me that the best way to do this is most likely to leverage the TinTin++ parser itself. My hope is that I can rewrite these modules using the exact syntax the parser uses. To test them and ensure there are no typos, an alias can be built that loads a specific command file, writes it out, then performs a diff on the file that was written out and the original command file. If the syntax is correct, then there should be no differences - if the original command file is written using the exact parser syntax. This has the added benefit of providing explicit coding standards for the modules framework, but the drawback of enforcing less than ideal (very verbose) code syntax.

I'm currently working on testing and implementing this solution.
