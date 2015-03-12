---
Title:  Building a Custom Pelican Theme
Status: Draft
---

<!--
Date: 2015-02-10
-->

# Introduction
<!--PELICAN_BEGIN_SUMMARY -->
**DRAFT:** Building a custom pelican theme.
<!-- PELICAN_END_SUMMARY -->

After playing around a little bit with a fork of the [pelican-pure][] theme, I decided to try to create my own from
scratch, so I started googling around for *modern* best practices. There's tons of information out there, so I tried to
pick and choose a few things that made sense for me - and in the process spent way to much time learning how to do some
stuff that's completely unrelated to what I normally do. Good times. ;) I kept notes during the process to build this
guide.

[pelican-pure]: https://github.com/PurePelicanTheme/pure-single

## Contents

[TOC]

## Overview

I'm not a web designer, and I know nothing of this stuff. So there was a bunch of reading and mucking around to figure
it out. Each time I read about one thing, it seemed that there was something else to check out. For someone who normally
does this, this is probably all *really* basic, however it took me awhile to figure out.

I've broken this down into four sections:

1. Overview - an introduction to the 'frontend web development' technologies I used to build the theme.
2. Resources - an overview of the tools & resources I used to build the theme.
3. Assets - the packaged resources (webassets) I used to build the theme.
4. Development - the process I used to actually build the template.

### Assets


[HTML5 Boilerplate]: https://html5boilerplate.com/
[PureCSS]: http://purecss.io/

[pelican-assets]: https://github.com/getpelican/pelican-plugins/tree/master/assets
[python-webassets]: https://github.com/miracle2k/webassets

[Web Assets Tips for Better Organization and Performance]: http://code.tutsplus.com/articles/web-assets-tips-for-better-organization-and-performance--net-33950


### Dynamic Stylesheets


<!-- Guides:CSS3 -->
[Beginner's Guide to CSS3]: http://www.hongkiat.com/blog/beginners-guide-to-css3/
[Power of HTML5-CSS3]: http://perishablepress.com/power-of-html5-css3/
[Beginners Guide to CSS3]: http://www.hongkiat.com/blog/beginners-guide-to-css3/
[Using CSS Variables]: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_variables

<!-- LESS:Tools -->
[lesscss]: http://lesscss.org/
[lessjs]: https://github.com/less/less.js/
[colors.less]: https://github.com/jking90/colors.less

<!-- LESS:Tutorials -->
[Using LESS as a Live CSS Engine]: http://css-tricks.com/using-less-as-a-live-css-engine/
[Introduction to RGBA Opacity]: http://www.css3.info/introduction-opacity-rgba/
[DON’T READ this Less CSS tutorial]: http://verekia.com/less-css/dont-read-less-css-tutorial-highly-addictive
[Less Color Functions]: http://www.hongkiat.com/blog/less-color-functions/
[10 LESS CSS Examples You Should Steal for Your Projects]: http://designshack.net/articles/css/10-less-css-examples-you-should-steal-for-your-projects/
[Creating a Colour Palette with LESS]: http://mattlambert.ca/blog/creating-a-colour-palette-with-less/
[LESS CSS for Color Palette Picking (Similar Colors)]: http://morecaffeinestudio.com/blog/less-css-for-color-palette-picking-like-colors/
[Using Less.js to Simplify Your CSS3]: http://designshack.net/articles/css/using-less-js-to-simplify-your-css3
[MoreCSS]: http://morecss.org/

[Dynamic Variable Names with Less]: http://stackoverflow.com/q/28426067/212343
[seven-phases-max-gist]: https://gist.github.com/seven-phases-max/92531212a4cb365539ae#file-28426067-less

### Webfonts

[Google Fonts]: https://www.google.com/fonts
[CSS Font Stack]: http://www.cssfontstack.com/

### Favicons

[Real Favicon Generator]: http://realfavicongenerator.net/

### Icon Fonts

[We Love Icon Fonts]: http://weloveiconfonts.com/

### JavaScript

[jQuery]: https://jquery.com/
[AngularJS]: https://angularjs.org/


### Syntax Highlighting

[PrismJS]: http://prismjs.com/

### Patterns

[Subtle Patterns]: http://subtlepatterns.com/

## Resources

## Assets

## Pelican

[Pelican Themes]: http://docs.getpelican.com/en/latest/themes.html

[Ipsum Generator]: http://www.ipsum-generator.com/
[CSS Tricks]: http://css-tricks.com/

<!-- Tutorials -->
[Build a Modular Dashboard Interface with Pure]: http://webdesign.tutsplus.com/tutorials/build-a-modular-dashboard-interface-with-pure--webdesign-13314
[Working with Pure CSS Modules, Part 1]: http://www.techrepublic.com/blog/web-designer/working-with-pure-css-modules-part-1/

http://www.paulirish.com/2010/the-protocol-relative-url/

## Development


### Colour

    Black    rgb(59,59,59)     #3b3b3b
    Red      rgb(207,106,76)   #cf6a4c
    Green    rgb(153,173,106)  #99ad6a
    Yellow   rgb(216,173,76)   #d8ad4c
    Blue     rgb(89,123,197)   #597bc5
    Magenta  rgb(160,55,176)   #a037b0
    Cyan     rgb(113,185,248)  #71b9f8
    White    rgb(173,173,173)  #adadad

<!-- Tools -->
[Jellybeans.vim]: https://github.com/nanotech/jellybeans.vim/blob/master/ansi-term-colors.txt
[Colour Lovers]: http://www.colourlovers.com/
[Color Hex]: http://www.color-hex.com/
[colors.css]: http://clrs.cc/
[CSS3 Please]: http://css3please.com/


