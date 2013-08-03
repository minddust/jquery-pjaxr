# [jquery-pjaxr](https://www.minddust.com/project/jquery-pjaxr/) [![Build Status](https://secure.travis-ci.org/minddust/jquery-pjaxr.png)](http://travis-ci.org/minddust/jquery-pjaxr)

jquery-pjaxr is [jQuery](http://jquery.com/) plugin that uses ajax and pushState to deliver a fast browsing experience.

It is able to replace **multiple containers** and different **head tags** with full back-forward functionality.

For [browsers that don't support pushState](http://caniuse.com/#search=pushstate) pjaxr fully degrades.


## Why another pjax library?

Shortly after starting with pjax a ran into some limitations like:

* how to add additional head elements?
* how to update multiple containers?

I started writing a workaround which became an own library and here we are :). 

I hope pjaxr will help people who are running into the same problems like I did.


## Note

There is already an awesome plugin called [jquery-pjax](https://github.com/defunkt/jquery-pjax) on which this project is based.  For not breaking existing frontends but to support the same port to the server this library is named **pjaxr** and accepts the same header **X-PJAX**.


## Note 2

This lib is still beta.  There are no test cases yet.  Everything works as expected but for production usage - please wait until v1.1.0.


## Installation

* Download the latest release: [v1.0.0](https://github.com/minddust/jquery-pjaxr/archive/v1.0.0.zip) (NOT READY YET)
* Clone the repository: `git clone git@github.com:minddust/jquery-pjaxr.git`.
* Curl the library: `curl -O https://raw.github.com/minddust/jquery-pjaxr/master/jquery.pjaxr.min.js`
* Install with [Bower](http://bower.io): `bower install jquery-pjaxr`. (NOT READY YET)


## Dependencies

Requires jQuery 1.8.x or higher.


## Usage

``` javascript
$(document).pjaxr('a');
```

That's all you need to activate pjaxr functionality.

If you only want to bind pjaxr when it's supported by the user's browser, you can activate pjaxr like this:

``` javascript
if ($.support.pjaxr) {
    $(document).pjaxr('a');
}
```

If you are migrating an existing site you probably don't want to enable pjaxr everywhere just yet.  Instead of using a global selector like `a` try annotating pjaxrable links with `data-pjaxr`, then use `'a[data-pjaxr]'` as your selector.


## Settings

Of course there are some options which will change your pjaxr behavior:

* `timeout`: the time in ms pjaxr will wait for a server response before hard loading the page. (default: `650`)
* `push`: determines whether to push the pjaxr request or not (default: `true`)
* `replace`: determines whether to replace the history state or not. will be ignored if `push` is `true`. (default: `false`)
* `scrollTo`: position in pixel the to scroll after pjaxring. (default: `0`)
* `version`: delivered pjaxr version. used to compare with `X-PJAX-VERSION` of the response header to force hard load on mismatch. (default: `<meta http-equiv="X-PJAX-VERSION" content="...">`)

You can either pass them as a second parameter on your `pjaxr` call or override them globally via `$.fn.pjaxr.defaults`.



## Signals

jquery-pjaxr fires a number of events regardless of how its invoked.

All events are fired from the document, cause the actions concern the whole page.

### start and end

* `pjaxr:start` - Fired when a pjaxr request is made or `popstate` is triggered.
* `pjaxr:end` - Fired when a pjaxr request ends or `popstate` is triggered.
* `pjaxr:click` - Fired when a pjaxr link is clicked.

### ajax related

* `pjaxr:beforeSend` - Fired before the pjaxr request begins. Preventing this event will abort the request.
* `pjaxr:send` - Fired after the pjaxr request begins.
* `pjaxr:always` - Fired after the pjaxr request finishes.
* `pjaxr:done` - Fired after the pjaxr request succeeds.
* `pjaxr:fail` - Fired after the pjaxr request fails. Preventing this event will disable fallback redirect.
* `pjaxr:timeout` - Fired if after timeout is reached. Preventing this event will disable the fallback and will wait indefinitely until the response returns.

`send` and `complete` are a good pair of events to use if you are implementing a loading indicator. They'll only be triggered if an actual request is made, not if it's loaded from cache.

``` javascript
$(document).on('pjaxr:send', function() {
  $('#loading').show()
})
$(document).on('pjaxr:complete', function() {
  $('#loading').hide()
})
```

## Response Structure & Rules

Check if the request header have **X-PAX** set and return rendered html in like this format:

```html
<pjaxr-head>
    <title>...</title>
    <meta name="..." ...>
    <meta property="..." ...>
    <link href="..." ...>
    <script src="..."></script>
    <style>...</style>
</pjaxr-head>
<pjaxr-body>
    <... id="..." ...></...>
    <... id="..." ...></...>
    <... id="..." ...></...>
</pjaxr-body>
```

* `pjaxr-head` and `pjaxr-body` are optional but if both are missing, pjaxr will hard load the giving url.
* `pjaxr-head`
    * `title` will always be replaced if given.
    * `meta` will be replaced if `name` or `property` find a match, otherwise it will be appended.
    * `link` will be replaced if `href` finds a match, otherwise it will be appended.
    * `script` will be replaced if `href` finds a match, otherwise it will be appended.
    * `style` will always be appended.
    * `data-remove-on-pjaxr` can the written to any tag and will force the element to be removed with the next pjaxr request.
* `pjaxr-body`
    * every child must have an id.
* any other content will be ignored.


### Existing Server Side Libraries

There are many available plugins for different languages and frameworks which will lift the heavy work for you:

* Asp.Net MVC3: http://biasecurities.com/blog/2011/using-pjax-with-asp-net-mvc3/
* Aspen: https://gist.github.com/whit537/6059536
* CakePHP : https://github.com/sanojimaru/CakePjax
* Django: https://github.com/jacobian/django-pjax
* Express: https://github.com/abdelsaid/express-pjax-demo
* Flask: https://github.com/zachwill/pjax_flask
* FuelPHP: https://github.com/rcrowe/fuel-pjax
* Grails: http://www.bobbywarner.com/2012/04/23/add-some-pjax-to-grails/
* Rails: https://github.com/rails/pjax_rails


## Behavior example

Note: Each state will be called via pjaxr and is fully reversible.

* Step 1
    * **Request**: /
    * **Response**: FULL PAGE LOAD
    * **Result**:
        ```html
        <html>
        <head>
            <title>home</title>
            <meta name="author" content="minddust">
        </head>
        <body>
            <nav id="main-menu">
                <ul>
                    <li><a href="/">home</a></li>
                    <li><a href="/blog/">blog</a></li>
                    <li id="menu-extra-entry"></li>
                </ul>
            </nav>
            <div id="content"><h1>home</h1></div>
            <script>$(document).ready(function() { $(document).pjaxr('a'); } });</script>
        </body>
        </html>
        
        ```

* Step 2
    * **Request**: /blog/
    * **Response**: 
        ```html
        <pjaxr-head>
            <title>blog</title>
            <meta name="title" content="blog">
            <meta name="description" content="blog post list">
            <meta property="og:image" content="http://example.org/blog-image.png" data-remove-on-pjaxr>
            <link href="additional-blog-styles.css" rel="stylesheet" type="text/css">
            <script src="animate-something.js" data-remove-on-pjaxr></script>
        </pjaxr-head>
        <pjaxr-body>
            <div id="content"><h1>Entry X</h1><a href="/blog/entry-x/">click here to read more</a></div>
        </pjaxr-body>
              
        ```
    * **Result**:
        ```html
        <html>
        <head>
            <title>blog</title>
            <meta name="author" content="minddust">
            <meta name="title" content="blog">
            <meta name="description" content="blog post list">
            <meta property="og:image" content="http://example.org/blog-image.png" data-remove-on-pjaxr>
            <link href="additional-blog-styles.css" rel="stylesheet" type="text/css">
            <script src="animate-something.js" data-remove-on-pjaxr></script>
        </head>
        <body>
            <nav id="main-menu">
                <ul>
                    <li><a href="/">home</a></li>
                    <li><a href="/blog/">blog</a></li>
                    <li id="menu-extra-entry"></li>
                </ul>
            </nav>
            <div id="content"><h1>Entry X</h1><a href="/blog/entry-x/">click here to read more</a></div>
            <script>$(document).ready(function() { $(document).pjaxr('a'); } });</script>
        </body>
        </html>
        
        ```

* Step 3
    * **Request**: /blog/entry-x/
    * **Response**: 
        ```html
        <pjaxr-head>
            <title>entry-x</title>
            <meta name="description" content="blog post: entry-x">
        </pjaxr-head>
        <pjaxr-body>
            <li id="menu-extra-entry"><a href="/blog/entry-x/">click here for the latest shown blog entry</a></li>
            <div id="content"><h1>Entry X</h1><p>content of entry-x blog post bla..</div>
        </pjaxr-body>
              
        ```
    * **Result**:
        ```html
        <html>
        <head>
            <title>entry-x</title>
            <meta name="author" content="minddust">
            <meta name="title" content="blog">
            <meta name="description" content="blog post: entry-x">
            <link href="additional-blog-styles.css" rel="stylesheet" type="text/css">
        </head>
        <body>
            <nav id="main-menu">
                <ul>
                    <li><a href="/">home</a></li>
                    <li><a href="/blog/">blog</a></li>
                    <li id="menu-extra-entry"><a href="/blog/entry-x/">click here for the latest shown blog entry</a></li>
                </ul>
            </nav>
            <div id="content"><h1>Entry X</h1><p>content of entry-x blog post bla..</div>
            <script>$(document).ready(function() { $(document).pjaxr('a'); } });</script>
        </body>
        </html>
        
        ```
        
* Step 4
    * **Request**: /
    * **Response**: 
        ```html
        <pjaxr-head>
            <title>home</title>
            <meta name="author" content="minddust">
        </pjaxr-head>
        <pjaxr-body>
            <div id="content"><h1>home</h1></div>
        </pjaxr-body>
              
        ```
    * **Result**:
        ```html
        <html>
        <head>
            <title>home</title>
            <meta name="author" content="minddust">
            <meta name="title" content="blog">
            <meta name="description" content="blog post: entry-x">
            <link href="additional-blog-styles.css" rel="stylesheet" type="text/css">
        </head>
        <body>
            <nav id="main-menu">
                <ul>
                    <li><a href="/">home</a></li>
                    <li><a href="/blog/">blog</a></li>
                    <li id="menu-extra-entry"><a href="/blog/entry-x/">click here for the latest shown blog entry</a></li>
                </ul>
            </nav>
            <div id="content"><h1>home</h1></div>
            <script>$(document).ready(function() { $(document).pjaxr('a'); } });</script>
        </body>
        </html>
        
        ```
        
As you can see - everything went fine until we went from step 3 to step 4. Now we have unwanted meta tags and styles.  In that case you should make neat use of `data-remove-on-pjax` to prevent messing up your head.


## Sites using jquery-pjaxr

If you are using this library and want to get listed below.  Please let me know.  Just make a pull request or write me an <a href="http://www.google.com/recaptcha/mailhide/d?k=013hG570A7Q8W8N-mLwG_KYA==&amp;c=Si_w84-xzI8tECjbipjghuMGRCyZRSrgBkV5ZFp61IY=" title="Reveal my email address" target="_blank">email</a>.


## Contributing

```
$ git clone https://github.com/minddust/jquery-pjaxr.git
$ cd jquery-pjaxr/
```

> TODO: explain how to run tests etc.


## Thanks

I like to thank [Chris Wanstrath :star2:](https://github.com/defunkt) for his really awesome [jquery-pjax](https://github.com/defunkt/jquery-pjax) library.  This project wouldn't exist without his work.


## Copyright and license

Copyright 2013 Stephan Groß, under [MIT license](LICENSE).

Want to appreciate my work? [minddust at Gittip](https://www.gittip.com/minddust/)
