# [jquery-pjaxr](https://www.minddust.com/project/jquery-pjaxr/) [![Bower version](https://badge.fury.io/bo/jquery-pjaxr.png)](http://badge.fury.io/bo/jquery-pjaxr) [![Build Status](https://secure.travis-ci.org/minddust/jquery-pjaxr.png)](http://travis-ci.org/minddust/jquery-pjaxr) [![devDependency Status](https://david-dm.org/minddust/jquery-pjaxr/dev-status.png)](https://david-dm.org/minddust/jquery-pjaxr#info=devDependencies)

[![Selenium Test Status](https://saucelabs.com/browser-matrix/minddust.svg)](https://saucelabs.com/u/minddust)

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

> There are still many testcases missing but the most signicant are setup. PR's are welcome.


## Installation

* Download the latest release: [v1.2.0](https://github.com/minddust/jquery-pjaxr/archive/v1.2.0.zip)
* Clone the repository: `git clone git@github.com:minddust/jquery-pjaxr.git`.
* Curl the library: `curl -O https://raw.github.com/minddust/jquery-pjaxr/master/jquery.pjaxr.min.js`
* Install with [Bower](http://bower.io): `bower install jquery-pjaxr`.


## Dependencies

Requires jQuery 1.9.x or higher.


## Usage

```javascript
$(document).pjaxr('a');
```

That's all you need to activate pjaxr functionality.

If you only want to bind pjaxr when it's supported by the user's browser, you can activate pjaxr like this:

```javascript
if ($.support.pjaxr) {
    $(document).pjaxr('a');
}
```

Or you can call the click handler by yourself and wrap it with some additional start functionality like this:

```javascript
if ($.support.pjaxr) {
    $('#some-menu').on('click', 'a[data-pjaxr]', function(event) {
        $(document).pjaxr.click(event);
    });
}
```

Or you can make a pjaxr request by pure calling:

```javascript
$(document).pjaxr.request('/about/', {timeout: 1337});
```

If you are migrating an existing site you probably don't want to enable pjaxr everywhere just yet.  Instead of using a global selector like `a` try annotating pjaxrable links with `data-pjaxr`, then use `'a[data-pjaxr]'` as your selector.

### data-pjaxr-namespace

There is also the possibility to add a `data-pjaxr-namespace` to the body which will then be set as `X-PJAX-NAMESPACE` in the request header.  This is just for initialising the namespace - Any further values should come from pjaxr responses via `<pjaxr-namespace>`.

By passing the namespace it's possible to limit the replacement area on the server side.  Checkout existing pjaxr libraries below.


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
* `pjaxr:success` - Fired after the pjaxr request succeeds.
* `pjaxr:done` - Fired after the pjaxr request is processed successfully.
* `pjaxr:fail` - Fired after the pjaxr request fails. Preventing this event will disable fallback redirect.
* `pjaxr:timeout` - Fired if after timeout is reached. Preventing this event will disable the fallback and will wait indefinitely until the response returns.

`send` and `complete` are a good pair of events to use if you are implementing a loading indicator. They'll only be triggered if an actual request is made, not if it's loaded from cache.

```javascript
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
<pjaxr-namespace>...</pjaxr-namespace>
```

* `pjaxr-head` and `pjaxr-body` are optional but if both are missing, pjaxr will hard load the giving url.
* `pjaxr-head`
    * `title` will always be replaced if given.
    * `meta` will be replaced if `name` or `property` find a match, otherwise it will be appended.
    * `link` will be replaced if `href` finds a match, otherwise it will be appended.
    * `script` will be replaced if `href` finds a match, otherwise it will be appended.
    * `style` will always be appended.
    * `data-remove-on-pjaxr` can the written to any tag and will force the element to be removed with the next pjaxr request and restored on popstate.
* `pjaxr-body`
    * every child must have an id.
* `pjaxr-namespace` is optional but when given - it's value will be passed on further request via `X-PJAX-NAMESPACE`.
* any other content will be ignored.


### Existing Pjaxr Server Side Libraries

These libs are making use of the advanced pjaxr namespacing functionality:

* Django: https://github.com/iekadou/django-pjaxr


### Existing Pjax Server Side Libraries

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


## Testing

As noted above: the testcases are **incomplete**

The main reason for this is that it's really hard to simulate complex page transitions. If you want to support this project - you can take a look at the structure of the existing ones an write some additional tests. Help is always welcome!

To run the tests locally you have to follow these steps:

1. clone the repository

    ```
git clone git@github.com:minddust/jquery-pjaxr.git
    ```
2. install python dependencies for test suite

    ```
pip install Django==1.6.6
pip install django-pjaxr==1.1.1
pip install selenium==2.42.1
    ```
3. install node dependencies for test suite

    ```
npm install
    ```
4. copy pjaxr js into test_app

    ```
npm run-script prepare-tests
    ```
5. install node dependencies for test_app (bower)

    ```
cd test_app
npm install
    ```
6. install bower dependencies for test_app

    ```
npm run-script bower-install
    ```
7. run the tests

    ```
cd ..
python test_app/tests/runtests.py
    ```
    
Note: you may need to download the [ChromeDriver](http://chromedriver.storage.googleapis.com/index.html) if it's not already installed. 

## Sites using jquery-pjaxr

If you are using this library and want to get listed below.  Please let me know.  Just make a pull request or write me an [email](http://www.google.com/recaptcha/mailhide/d?k=011zym_c1aKrhZC1K3TKFvVQ==&c=fPxx09KG4QgsFYu7CWApi-ZBAupHsLalyCVJ_Vogc8g= "Reveal my email address").

* https://www.socialfunders.org
* http://www.noxic-action.de/page/


## Contributing

Help is appreciated!


## Thanks

I like to thank [Chris Wanstrath](https://github.com/defunkt) for his really awesome [jquery-pjax](https://github.com/defunkt/jquery-pjax) library.  This project wouldn't exist without his work.


## Copyright and license

Copyright 2013-2015 Stephan Groß, under [MIT license](https://github.com/minddust/jquery-pjaxr/blob/master/LICENSE).

Want to appreciate my work? [minddust at Gittip](https://www.gittip.com/minddust/)
