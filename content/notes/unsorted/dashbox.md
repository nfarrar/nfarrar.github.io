---
Title:  Building Dashbox
Status: Draft
---


## Scaffolding
Install the global dependencies:

    brew update
    brew install nodejs npm librsvg
    npm install -g gulp bower yo generator-gulp-webapp font-awesome-svg-png favicons
    npm -g update

Scaffold the project (uncheck bootstrap when running yo):

    mkdir dashbox && cd dashbox
    yo gulp-webapp

Install project packages:

    npm install --save-dev font-awesome-svg-png gulp-filter
    bower install --save-dev font-awesome pure


[nodejs]:                   http://nodejs.org/
[npm]:                      https://www.npmjs.com/
[yeoman]:                   http://yeoman.io/
[gulpjs]:                   http://gulpjs.com/
[bower]:                    http://bower.io
[generator-gulp-webapp]:    https://github.com/yeoman/generator-gulp-webapp

[wiredep]:                  https://github.com/taptapship/wiredep
[main-bower-files]:         https://github.com/ck86/main-bower-files
[autoprefixer]:             https://github.com/postcss/autoprefixer
[jquery]:                   https://jquery.com/
[Yeoman Gulp Generator]:    http://yeoman.io/blog/gulp-explore.html


## Gulp Task Listing
By default our gulp file doesn't list it's tasks, but we can add this using [npm-task-listing][] or [npm-help][]. In
this situation, I use [npm-task-listing][] since I don't want to add descriptions to each task. Install
[npm-tasking-listing][] with:

    npm install --save-dev gulp-task-listing 

The new plugin will be automatically detected by [gulp-load-plugins][] and added to the *"bling"* (`$`). Add the
following the `gulpfile.js`: 

    gulp.task('list', $.taskListing);

... and now we can run `gulp list` from our project root to get a list of the configured tasks.


[gulp-task-listing]:        https://github.com/OverZealous/gulp-task-listing
[gulp-help]:                https://github.com/chmontgomery/gulp-help


## Webfonts
To make things a little more distinctive, we'll add some custom webfonts. I keep it pretty simple and typically use
[Google Fonts][] directly from their CDN. For this site, I'll use [Oswald][] (for headings), [Lato][] (for body text),
and [Inconsolata][] (for monospaced blocks).

The easiest way to do this, is to go to [Google Fonts][], search for each font and add them to a collection. Select use
(and in my case I'm keeping the default variations), and [Google Fonts][] provides several ways to link to them. Since
my project is using sass, I'll create a sass partial in `app/styles/` named `_typography.scss` that contains:

    @import url(http://fonts.googleapis.com/css?family=Lato|Oswald|Inconsolata);
    $font-stack-head:   'Oswald', sans-serif !default;
    $font-stack-body:   'Lato', sans-serif !default;
    $font-stack-mono:   'Inconsolata', sans-serif !default;

And add the following to `app/styles/main.scss`:

    @import 'typography';

Now to use the fonts, we only need to reference the variable, for example:

    body {

    }


    npm install -g webfont-dl
    Install our custom fonts with:

        webfont-dl "http://fonts.googleapis.com/css?family=Oswald|Lato|Inconsolata" \
            --font-out=app/fonts \
            --out=app/styles/_typography.css \
            --css-rel=/dist/fonts

    And add the following to `app/styles/main.scss` to use them:


[Google Fonts]: https://www.google.com/fonts/
[Oswald]:       https://www.google.com/fonts/specimen/Oswald
[Lato]:         https://www.google.com/fonts/specimen/Lato
[Inconsolata]:  http://www.google.com/fonts/specimen/Inconsolata

## Favicons


    npm install --save-dev gulp-favicons 

    The font-awesome icon font is awesome, but sometimes it we want to use them as actual images, and not with styling. We
    can generate the equivalent svg's and png's using [font-awesome-svg-png][]:

        mkdir app/images/fa && cd app/images/fa
        font-awesome-svg-png --color black --sizes 256
        font-awesome-svg-png --color blue --sizes 256
        font-awesome-svg-png --color red --sizes 256
        cd ../../..

    And now we can use them other ways as well - for example to generate a boilerplate favicon with [gulp-favicon][] by
    adding the following line to `app/index.html`:

        <link rel="favicons" href="images/fa/black/png/256/cog.png" />

    And this to the gulpfile: 

        gulp.task('favicons', function () {
        gulp.src('app/index.html')
            .pipe($.favicons({
            files: {
                src: 'app/images/fa/black/png/256/cog.png',
                dest: 'favicons'
            },
            settings: {
                background: '#ffffff' 
                html: null,
                manifest: null,
                callback: null
            }
            }))
            .pipe(gulp.dest('./'));
        });

[Font-Awesome-SVG-PNG]:     https://github.com/encharm/Font-Awesome-SVG-PNG
[favicons]:                 https://github.com/haydenbleasel/favicons
[webfont-dl]:               https://github.com/mmastrac/webfont-dl
[RealFaviconGenerator]:     http://realfavicongenerator.net/

[pure]:                     http://purecss.io/
- http://engineroom.teamwork.com/hassle-free-third-party-dependencies/



