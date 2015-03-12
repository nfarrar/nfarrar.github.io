---
Title:    Building an MDWiki Pelican Plugin
Status:   Draft
---



## Setup
There are three basic ways to deploy mdwiki:

1. We can fork and deploy the [mdwiki-seed](https://github.com/Dynalon/mdwiki-seed) repository.
2. We can download a [distribution release](https://github.com/Dynalon/mdwiki/releases) and add it to our own repository.
3. We can download the [source](https://github.com/Dynalon/mdwiki), [build](https://github.com/Dynalon/mdwiki#how-to-build-from-source), and add to own our repository.

I'm pressed for time right now, so I'm going to use the easiest option (#2). This method does not allow us to merge updates or customize the theme or parsing engine, so we'll looking into those in a future article.

First, clone the minimized mdwiki index file:

    wget https://github.com/Dynalon/mdwiki/releases/download/0.6.2/mdwiki-0.6.2.zip -O /tmp/mdwiki.zip
    cd ~/Documents/Projects/crunk.io/content
    nzip /tmp/mdwiki.zip "*mdwiki-slim.html" -j -d wiki
    mv wiki/mdwiki-slim.html wiki/index.html
    rm /tmp/mdwiki.zip

Next, add the supporting files:

    touch wiki/config.json
    touch wiki/index.md
    touch wiki/navigation.md

Add configuration options to [config.json](https://dynalon.github.io/mdwiki/#!customizing.md):

    {
        "useSideMenu": true,
        "lineBreaks": "gfm",
        "additionalFooterText": "",
        "anchorCharacter": "#"
    }

... and some menu items to [navigation.md](https://dynalon.github.io/mdwiki/navigation.md:

    # crunk.io

    [Blog](http://crunk.io)

Now modify the static paths in pelicanconf.py to copy the wiki content when publishing:

    STATIC_PATHS = [
        ...
        'wiki',
        ...
    ]
    EXTRA_PATH_METADATA = {
        ...
        'wiki': {'path': 'wiki'},
        ...
    }

I like to keep a tmp directory, where I can stage raw, unsorted notes:

    mkdir wiki/tmp


http://docs.getpelican.com/en/3.4.0/internals.html?highlight=internals
