---
Title:    Introduction to Pelican
Date:     2015-02-08 00:00
Modified: 2015-03-11 00:00
Status:   Published
Tags:     [pelican, python, fabric, gitflow, github, markdown, virtualenv, virtualenvwrapper]
---

<!-- PELICAN_SUMMARY -->
I finally decided that all these notes sitting around on my computer need to be published. I love me some python and
I've played around with [pelican][] in the past, so I figured it was time to start hacking away on it and actually set
it up. Lately I've been hacking around with [ansible][] and [fabric][], which is supported out of the box by
[pelican][], so I figured I'd blow away the Makefile setup and force myself to write some [fabric][]-based python.

My "Notebook" has thousands of notes in it on various technical subjects, written in [markdown][] format over the past
couple years - and since [pelican][] supports [markdown][], this is a relatively easy conversion.
<!-- PELICAN_END_SUMMARY -->

[pelican]:  https://github.com/getpelican/pelican
[ansible]:  https://github.com/ansible/ansible
[fabric]:   https://github.com/fabric/fabric
[markdown]:  http://daringfireball.net/projects/markdown/syntax


## Project Setup
My setup process uses the following steps:

- setup a virtual environment & install dependencies
- setup version control & configure repository to serve from github user page
- setup a premade theme (customization later)
- setup (basic) plugins
- tweak our basic configuration
- setup fabric for management

To start off, install [virtualenv][] and [virtualenvwerapper][]. You'll need to do some shell configuration to properly
setup virtualenvwrapper, which you can find in their documentation.

    :::bash
    # setup our project directory
    mkdir crunk.io && cd crunk.io

    # create the virtual environment
    mkvirtualenv crunk.io

    # install basic dependencies
    pip install pelican markdown

    # build the intial site
    pelican-quickstart

[virtualenv]:           https://github.com/pypa/virtualenv
[virtualenvwrapper]:    https://bitbucket.org/dhellmann/virtualenvwrapper

The quickstart script is much like the [sphinx quickstart][] script - it walks you through a set of prompts to build the
initial configuration files & site layout:

    > Where do you want to create your new web site? [.]
    > What will be the title of this web site? crunk.io
    > Who will be the author of this web site? Nathan Farrar
    > What will be the default language of this web site? [en]
    > Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) n
    > Do you want to enable article pagination? (Y/n) n
    > Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n)
    > Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n)
    > Do you want to upload your website using FTP? (y/N) n
    > Do you want to upload your website using SSH? (y/N) n
    > Do you want to upload your website using Dropbox? (y/N) n
    > Do you want to upload your website using S3? (y/N) n
    > Do you want to upload your website using Rackspace Cloud Files? (y/N) n
    > Do you want to upload your website using GitHub Pages? (y/N) y
    > Is this your personal page (username.github.io)? (y/N) y
    Done. Your new project is available at crunk.io/

This scaffolded our project structure for us, creating various files. Some important files to note are:

    .
    ├── Makefile
    ├── content
    ├── develop_server.sh
    ├── fabfile.py
    ├── output
    ├── pelicanconf.py
    └── publishconf.py

This adds two different ways for us to manage our site: [make][] and [fabric][]. The most common (and easiest) way is to
use the generated *Makefile*:

    make                # list the Makefile commands
    make clean          # remove the generated content
    make html           # generate the static content
    make devserver      # start the pelican's webserver, using the develop_server.sh script
    make gitHub         # publish the static content to github pages

There is also a *fabfile.py* configuration, which provides a set of tasks to run using [fabric][].  To use it, we need
to install fabric (with `pip install fabric`), which provides us with the `fab` command. The `fab` command executes
using a `fabfile.py` configuration script from the *current* directory. To list the commands provided by our default
`fabfile.py` we can use `fab --list`:

    Available commands:

        build
        cf_upload
        clean
        preview
        publish
        rebuild
        regenerate
        reserve
        serve


I'm using a heavily modified fabric setup, so I went ahead an deleted the Makefile and went to town modifying the
fabfile configuration. Making it work *properly* required a lot of hacking. More on this later.


## Version Control
A lesson I've learned the hard way: the first thing we should always do (when starting a new project) is to setup
version control - even if it's just local, we can rollback a change if we accidently delete a file or junk some content
we didn't mean to.

For my use case, I'm publishing to my github user page (http://nfarrar.github.io/), which is a little tricky. The
**published** content has to be served from the *master* branch (rather than the *gh-pages* branch. There are a couple
ways we can make this work, but the most straight-forward, is to work from a *"source"* branch and publish back
to master, and track them at the origin using the same names. The default branch that we begin working in is master (but
it's not actually created until we make a commit), so we can start by initializing the repository, then immediately
checking out our source branch, so we can begin commiting files:

    :::bash
    git init 
    git checkout -b source

Now if you look at the branches with `git branch` you'll see we've only got one branch (named source) and it's our
working branch. We can start commiting files to this branch just like normal - and now's a good time to add our
`.gitignore` and `.gitattributes` files. 

A very convenient way to generate gitignore files is via [gitiginore.io][] (you'll need to setup a simple shell alias to
use it via the cli):

    :::bash
    gi OSX,python,vim >> .gitignore.io

We'll also need to add some additional directories to the `.gitignore` file - for example the `output` directory (or
alternate directory where generated content is built).

To ensure our line endings and file types are properly handled, we can add the following to `.gitattributes`:

    # normalize line endings (LF) for text files
    * text=auto

    # text files
    *.py    text
    *.css   text
    *.html  text
    *.js    text
    
    # binary files
    *.png binary
    *.jpg binary

We'll also need to create our repository on github, and setup proper branch tracking (make sure the local source branch
is pushed to the remote source branch):

    git remote add origin git@github.com:nfarrar.github.io.git
    git push -u origin source

To publish my content, I'm using a fabric wrapper around [ghp-import][] (more on that later). To manually publish our
content, we first need to build it (`Make build` or `fab build`), install ghp-import (`pip install ghp-import`), and
then publish the content:

    :::bash
    ghp-import -p -b master output

This does a bunch of things all at once. First, the `-p` flag says that we should attempt to push the local branch
that ghp-import is importing content **to** to the origin. Second, the `-b` flags specifies the branch we want to import
our content **to**. Third, is the name of the directory we're importing content **from**. 

So essentially: Take the content from the `output` directory, import it into the root of the `master` branch, and pushes
the `master` branch to the `master` branch at the origin. And after running this command, you should be able to see your
site at `username.github.io` (and if you're using a custom domain, it should also be accessible there).

This process *is* destructive, it will destroy your current master branch - so make sure you don't have anything in
there that you're planning on saving. 

Additionally, if you're building content to an alternate directory (i build mine to `_site`, then you'll need to
specify that directory instead of `output`).

<!-- references -->
[gitignore.io]: https://www.gitignore.io/docs
[Github Pages]:     https://pages.github.com/
[Github User Page]: https://help.github.com/articles/user-organization-and-project-pages/
[ghp-import]:       https://github.com/davisp/ghp-import
[custom-domain]:    https://help.github.com/articles/setting-up-a-custom-domain-with-github-pages


## Pelican Configuration
The pelican configuration already has extensive documentation, but I've added a few notes of my own here that I didn't
find covered.

### Clean URLs
You can simulate 'clean/pretty urls' without touching apache/nginx rewrite rules, by doing some trickery with the URL
paths:

    ARTICLE_SAVE_AS = 'post/{slug}/index.html'
    ARTICLE_URL = 'post/{slug}/'
    CATEGORY_URL = 'category/{slug}/'
    CATEGORY_SAVE_AS = 'category/{slug}/index.html'
    PAGE_URL = 'page/{slug}/'
    PAGE_SAVE_AS = 'page/{slug}/index.html'
    TAG_URL = 'tagged/{slug}/index.html'
    TAG_SAVE_AS = 'tagged/{slug}/index.html'

This writes each page, post, category page, and tag page as a folder with an index.html. This makes the URLS look like
clean server rewrites, even though they aren't.

### Markdown Metadata
The metadata formatting with markdown files is handled by the python markdown library 'metadata' extension. It's built
in and pelican uses it. It also sucks. It's completely non-standard, and not *really* part of markdown. It's *so* close
to yaml, yet so far away. It broke all my code folding in vim - I was able to get it restored with a bit of hacking
around, but it was unreliable and I didn't want to spend any more time on it.

Fortunately, there's a yaml extension for pelican - which was easy to get working with markdown syntax & folding in vim.

### Default Metadata
Messing arround with the default metadata settings ended with a world of hurt. Essentially, I wanted to setup my posts
so with a couple settings:

- Set myself as the default author, since I'm the only one writing on this site.
- If the article status isn't defined, have it set to 'published' in pelicanconf.py.
- If the article status isn't defined, have it set to 'draft' in publishconf.py.
- If the date isn't defined,  set it to today's date by default (so the content reader doesn't break).

This way, when working locally - I can have my drafts get built, but when publishing, they'll be omitted. There's
even a `DEFAULT_METADATA` setting already built into pelican, that I attempted to use:

    :::python
    DEFAULT_METADATA = (
        ('Authors', 'Nathan Farrar'),
        ('Status', 'draft'),
        ('Date', date.today()),
    )

Easy, right? Way wrong. I actually found three separate bugs (I consider them bugs).

Setting the author this way exposes a unicode string handling error. It's been reported, but not fixed.

The metadata for pages and posts are different, but this setting applies to both. Setting a default value for status
either causes your pages to be skipped by the reader, or the posts to be skipped by the reader.
    
    :::python
    ERROR: Unknown status 'draft' for file pages/about.md, skipping it.
    Done: Processed 1 article(s), 1 draft(s) and 0 page(s) in 0.32 seconds.

And the reader completely chokes out (at least the yaml reader does), with `tzdata` errors, all day long when we try
to set a default date:

    ERROR: Could not process posts/every-single-post.md
    | 'datetime.date' object has no attribute 'tzinfo'
    ERROR: Could not process pages/every-single-page.md
    | 'datetime.date' object has no attribute 'tzinfo'
    CRITICAL: 'datetime.date' object has no attribute 'tzinfo'

As an alternative to the default metadata setting, I tried to set a default time, then switch on the `WITH_FUTURE_DATES` 
flag in `pelicanconf.py` and off in `publishconf.py`, but this *also* chokes:

    :::python
    # pelicanconf.py
    DEFAULT_DATE = (2016, 01, 01)
    WITH_FUTURE_DATES = True

    :::python
    # publishconf.py
    WITH_FUTURE_DATES = False

Again with critical errors in the page reader:

    ERROR: Could not process pages/about.md
    | can't compare offset-naive and offset-aware datetimes
    CRITICAL: can't compare offset-naive and offset-aware datetimes

I posted an issue on the [pelican issue tracker][issue-1620] regarding the issues with the `DEFAULT_METADATA` setting,
but the response was a blanket "manually set the status" response. I haven't had any time to dig further into these, so
I don't have a working solution yet. 

But the moral of this story is - don't fuck with the default metadata unless you *really* want to feel the pain.

[issue-1620]: https://github.com/getpelican/pelican/issues/1620


### Typogrify
[Typogrify][] is a python library that fixes up some of our ugly typographical elements and ensures everything is
*web-safe*. Pelican includes support for it out the box, it just needs to be installed & enabled.

Install typogrify in our virtual environment:

    :::bash
    pip install typogrify 

And enable it in our pelican configuration:

    :::python
    # Markup
    TYPOGRIFY = True

[typogrify]: https://code.google.com/p/typogrify/


### Markdown
Out of the box, pelican is setup to process markdown documents using the [Python Markdown Library][]. This includes
additional extensions that can be enabled via our pelican configuration. By default, the [code-hilite][] extension is
enabled, which uses the [pygments][] library to generate the HTML for highlighted source code:

    :::python
    # default MD_EXTENSIONS setting
    'MD_EXTENSIONS': ['codehilite(css_class=highlight)', 'extra'],

There are several other extensions we can enable, including the `TOC` extension, by modifying our configuration with:

    :::python
    PYGMENTS_STYLE = 'monokai'
    MD_EXTENSIONS = ([
        'codehilite(css_class=highlight)',
        'extra',
        'toc',
    ])

<!-- references -->
[Python Markdown Library]: https://pythonhosted.org/Markdown/
[code-hilite]: https://pythonhosted.org/Markdown/extensions/code_hilite.html
[pygments]: http://pygments.org/


## Themes
Pelican provides a consolidated themes repository that we can use. I add them to my project as a submodule, so that
they're all available. To do this, I create a 'themes' directory, then clone them into a subfolder - this way I have
room to add additional themes in the same folder, that aren't part of the repository. This also allows me to add them
directly to my project in case the version in the themes repository isn't updated:

    :::bash
    mkdir themes
    git submodule add https://github.com/getpelican/pelican-themes.git themes/pelican-themes
    git submodule add https://github.com/PurePelicanTheme/pure-single themes/pure
    git submodule update --init --recursive

And now we can use any of our themes by setting it in our pelican configuration:

    :::python
    THEME = "themes/pelican-themes/svbtle"


## Plugins
Pelican provides a consolidated repository of [plugins][pelican-plugins]. We can add these as a submodule as well, just
like the themes:

    :::bash
    mkdir plugins
    git submodule add https://github.com/getpelican/pelican-plugins plugins/pelican-plugins plugins/pelican-plugins
    git submodule update --init --recursive

And in pelicanconf.py, we need to provide the path to our plugins and what plugins to load:

    :::python
    PLUGIN_PATHS = [ 'plugins/pelican-plugins' ]
    PLUGINS = [ 'gravatar', 'sitemap', 'summary' ]

Some of these plugins also need additional configuration in `pelicanconf.py`:

    :::python
    SITEMAP = {
        'format': 'xml',
        'priorities': {
            'articles': 0.5,
            'indexes': 0.5,
            'pages': 0.5
        },
        'changefreqs': {
            'articles': 'monthly',
            'indexes': 'daily',
            'pages': 'monthly'
        }
    }

Unfortunately, this method doesn't work will all the plugins.  Because we're dealing with python runtime imports things
have to be structured in a specific way. I've stumbled across a couple plugins that don't properly account for this and
will fail to work with this kind of setup.

A specific example is the [python-md-metayaml][] extension - and I've posted a description of the problem to the
author's issue tracker [here][md-metayaml-issue]. If we try to add it to our plugins, we'll get an import error when
attempting to build the site.

To summarize the issue - we can't import the plugin becaues of the way that it's structured without renaming the
directory - which breaks the purpose of adding the plugins directory as a submodule - so we need to add the plugin as
a separate submodule in a nested directory, inside our plugins directory, with a specific name:

    :::bash
    mkdir -p plugins/pelican-md-metayaml
    git submodule add https://github.com/joachimneu/pelican-md-metayaml.git plugins/pelican-md-metayaml/md_metayaml
    git submodule update --init --recursive

We need to add the additional plugin path, and then we can import it correctly:

    :::python
    PLUGIN_PATHS = [
        'plugins/pelican-plugins',
        'plugins/pelican-md-metayaml'
    ]
    PLUGINS = ['gravatar', 'sitemap', 'summary', 'md_metayaml']

<!-- references -->
[pelican-plugins]: https://github.com/getpelican/pelican-plugins
[pelican-plugins-docs]: http://docs.getpelican.com/en/latest/plugins.html
[pelican-md-metayaml]: https://github.com/joachimneu/pelican-md-metayaml
[md-metayaml-issue]: https://github.com/joachimneu/pelican-md-metayaml/issues/6
[pelican-sitemap]: https://github.com/getpelican/pelican-plugins/tree/master/sitemap
[gravatar]: https://github.com/getpelican/pelican-plugins/tree/master/gravatar


## Fabric
Using fabric instead of the Makefile to a little bit of learning - but was well worth it. The final result is more
robust and is very extensible. I even added a bit of fine tuning to my configuring to make it easier for others to use
as well.

I've got through several iterations of the code - and no doubt I'll go through some more - so I'm not going to document
it all here. Instead - just checkout the [source][fabfile.py]. It's documented.

A couple of highlights though:

- There are no hardcoded settings in my [fabfile.py][] (they're loaded with `pelican.settings.read_settings()`).
- I'm using [python-livereload][] for my development server.
- I'm generating notifications using [gntp][] (python growl library).
- I'm using [ghp-import][] wrapped in a python task to publish my content.

<!-- references -->
[fabfile.py]:           http://git.io/p6oi
[python-livereload]:    https://github.com/lepture/python-livereload
[gntp]:                 https://github.com/kfdm/gntp/ 
[ghp-import]:           https://github.com/davisp/ghp-import
