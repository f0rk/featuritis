featuritis
==========

`featuritis` is a tool that allows you to incorporate ticket information into
your codebase. In this way, you can then produce during your build, incorporate
into an API, etc. which features are in your codebase.

Features, generally, are tied to specific tickets or user stories, but could be
anything you can imagine a "feature" to be tracked by.

Every must have a unique id.

Usage
=====

Featuritis writes the feature tracking information into a folder named
featuritis. To create this folder, you should run:

```!sh
$ featuritis init
```

To add a new feature, run the add command:
```!sh
$ featuritis add ABC-123 -d "here's a nifty description"
feature added /home/jimmy/projects/rustlers/featuritis/features/20200703023344_ABC-123_heres_a_nifty_description.py
```

To view the list of all features:
```!sh
$ featuritis list
id: timestamp author: description
ABC-123: 2020-07-03 Jimmy Rustle <jimmy@jimmyrustle.guru>: here's a nifty description
```
