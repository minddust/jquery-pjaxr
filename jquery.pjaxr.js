/*!
* jquery.pjaxr.js v1.0.4 by @minddust
* Copyright (c) 2013 Stephan Gross
*
* https://www.minddust.com/jquery-pjaxr
*
* Licensed under the MIT license:
* http://www.opensource.org/licenses/MIT
*/
(function($) {
    'use strict';

    function fnPjaxR(selector, options) {
        return this.on('click.pjaxr', selector, function(event) {
            handleClick(event, options);
        });
    }

    function handleClick(event, options) {
        var link = event.currentTarget;

        if (link.tagName.toUpperCase() !== 'A') {
            throw '$.fn.pjaxXR requires an anchor element';
        }

        // middle click, cmd click, and ctrl click should open links in a new tab as normal.
        if (event.which > 1 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
            return;
        }

        // ignore prevented links
        if (event.isDefaultPrevented()) {
            return;
        }

        // ignore cross origin links
        if (location.protocol !== link.protocol || location.hostname !== link.hostname) {
            return;
        }

        // ignore anchors on the same page
        if (link.hash && link.href.replace(link.hash, '') === location.href.replace(location.hash, '')) {
            return;
        }

        // ignore empty anchor 'foo.html#'
        if (link.href === location.href + '#') {
            return;
        }

        var defaults = {
            url: $.isFunction(link.href) ? link.href() : link.href,
            type: 'GET',  // always GET since we currently not support other methods
            dataType: 'html'
        };

        var opts = fnPjaxR.options = $.extend(true, {}, $.ajaxSettings, defaults, $.fn.pjaxr.defaults, options);

        if (!fire('pjaxr:click', [opts])) {
            event.preventDefault();
            return;
        }

        var timeoutTimer;

        opts.beforeSend = function(xhr, settings) {
            if (!fire('pjaxr:beforeSend', [xhr, settings])) {
                return false;
            }

            xhr.setRequestHeader('X-PJAX', 'true');

            if (!namespace) {
                namespace = $('body').data('pjaxr-namespace') || '';
            }
            xhr.setRequestHeader('X-PJAX-NAMESPACE', namespace);

            if (settings.timeout > 0) {
                timeoutTimer = setTimeout(function () {
                    if (fire('pjaxr:timeout', [xhr, opts])) {
                        xhr.abort('timeout');
                    }
                }, settings.timeout);

                // clear timeout setting so jQuery's internal timeout isn't invoked
                settings.timeout = 0;
            }

            return true;
        };

        // create pjax state for initial page load
        if (!fnPjaxR.state) {
            fnPjaxR.state = {
                id: uniqueId(),
                url: window.location.href,
                title: document.title
            };
            window.history.replaceState(fnPjaxR.state, fnPjaxR.state.title, fnPjaxR.state.url);
        }

        var xhr = fnPjaxR.xhr;

        // cancel the current running pjax request if there is one
        if (xhr && xhr.readyState < 4) {
            xhr.onreadystatechange = $.noop;
            xhr.abort();
        }

        // go-go-pjax
        xhr = fnPjaxR.xhr = $.ajax(opts);

        if (xhr.readyState > 0) {
            fire('pjaxr:start', [opts]);
        }

        xhr.done(function(data, textStatus, jqXHR) {
            fire('pjaxr:success', [opts]);

            var currentVersion = (typeof opts.version === 'function') ? opts.version() : opts.version;
            var latestVersion = jqXHR.getResponseHeader('X-PJAX-Version');

            // If there is a layout version mismatch, hard load the new url
            if (currentVersion && latestVersion && currentVersion !== latestVersion) {
                locationReplace(opts.url);
                return;
            }

            var head_match = data.match(/<pjaxr-head>([\s\S.]*)<\/pjaxr-head>/i);
            var body_match = data.match(/<pjaxr-body>([\s\S.]*)<\/pjaxr-body>/i);

            // if response data doesn't fit, hard load the new url
            if (!head_match && !body_match) {
                locationReplace(opts.url);
                return;
            }
            fire('pjaxr:success', [data, textStatus, jqXHR, opts]);

            // Clear out any focused controls before inserting new page contents.
            document.activeElement.blur();

            var stateId = uniqueId();

            if (head_match) {
                var $head = $(parseHTML(head_match[0]));
                var head_parts = processPjaxHead('forward', $head.children(), null, null);
                var apply_head_parts = head_parts[0];
                var revert_head_parts = head_parts[1];
                var remove_head_parts = head_parts[2];
            }

            if (body_match) {
                var $body = $(parseHTML(body_match[0]));
                var body_parts = processPjaxBody($body.children());
                var apply_body_parts = body_parts[0];
                var revert_body_parts = body_parts[1];
            }

            var namespace_match = data.match(/<pjaxr-namespace>([\s\S.]*)<\/pjaxr-namespace>/i);
            if (namespace_match) {
                namespace = $(parseHTML(namespace_match[0])).html();
            }

            // FF bug: Won't autofocus fields that are inserted via JS.
            // This behavior is incorrect. So if there's no current focus, autofocus
            // the last field.
            //
            // http://www.w3.org/html/wg/drafts/html/master/forms.html
            $(document).find('input[autofocus], textarea[autofocus]').last().focus();

            if (typeof opts.scrollTo === 'number') {
                $(window).scrollTop(opts.scrollTo);
            }

            // enrich current state information with removal instructions
            $.extend(fnPjaxR.state, {
                head_revert: head_match ? revert_head_parts : null,
                head_remove: head_match ? remove_head_parts : null,
                body_revert: body_match ? revert_body_parts : null
            });
            if (opts.push || opts.replace) {
                window.history.replaceState(fnPjaxR.state, fnPjaxR.state.title, fnPjaxR.state.url);
            }

            fnPjaxR.state = {
                id: stateId,
                url: opts.url,
                title: document.title,
                head_apply: head_match ? apply_head_parts : null,
                body_apply: body_match ? apply_body_parts : null
            };

            if (opts.push) {
                window.history.pushState(fnPjaxR.state, fnPjaxR.state.title, fnPjaxR.state.url);
            }
            else if (opts.replace) {
                window.history.replaceState(fnPjaxR.state, fnPjaxR.state.title, fnPjaxR.state.url);
            }

            fire('pjaxr:done', [data, textStatus, jqXHR, opts]);
        });

        xhr.fail(function(jqXHR, textStatus, errorThrown) {
            if (textStatus !== 'abort' && fire('pjaxr:fail', [jqXHR, textStatus, errorThrown, opts])) {
                locationReplace(opts.url);
            }
        });

        xhr.always(function() {
            if (timeoutTimer) {
                clearTimeout(timeoutTimer);
            }

            fire('pjaxr:always', [opts]);
            fire('pjaxr:end', [opts]);
        });

        event.preventDefault();
    }

    function processPjaxHeadElements(elements, append) {
        var apply_head_parts = [];
        var revert_head_parts = [];
        var remove_head_parts = [];

        if (elements && elements.length > 0) {
            $.each(elements, function(index, value) {
                var $value = $(value);

                // only applied on push
                if ($value.is('title')) {
                    document.title = $value.text();
                }
                else if ($value.is('meta')) {
                    var $meta;
                    var name = $value.attr('name');
                    var property = $value.attr('property');

                    if (name) {
                        $meta = $('head > meta[name="'+name+'"]');
                    }
                    else if (property) {
                        $meta = $('head > meta[property="'+property+'"]');
                    }

                    if ($meta.length > 0) {
                        remove_head_parts.push(outerHTML($meta));
                        $meta.remove();
                    }
                    else {
                        revert_head_parts.push(outerHTML($value));
                    }

                    if (append === true) {
                        $('head').append($value);
                        apply_head_parts.push(outerHTML($value));
                    }
                }
                else if ($value.is('link')) {
                    var link_href = $value.attr('href');
                    if (link_href) {
                        var $link = $('head > link[href="'+link_href+'"]');

                        if ($link.length > 0) {
                            remove_head_parts.push(outerHTML($link));
                            $link.remove();
                        }
                        else {
                            revert_head_parts.push(outerHTML($value));
                        }

                        if (append === true) {
                            $('head').append($value);
                            apply_head_parts.push(outerHTML($value));
                        }
                    }
                }
                else if ($value.is('script')) {
                    var script_src = $value.attr('src');
                    if (script_src) {
                        var $script = $('head > script[src="'+script_src+'"]');

                        if ($script.length > 0) {
                            remove_head_parts.push(outerHTML($script));
                            $script.remove();
                        }
                        else {
                            revert_head_parts.push(outerHTML($value));
                        }

                        if (append === true) {
                            $('head').append($value);
                            apply_head_parts.push(outerHTML($value));
                        }
                    }
                }
                else if ($value.is('style')) {
                    if (append === true) {
                        $('head').append($value);
                        apply_head_parts.push(outerHTML($value));
                        revert_head_parts.push(outerHTML($value));
                    }
                }
            });
        }

        return [apply_head_parts, revert_head_parts, remove_head_parts];
    }

    function processPjaxHead(direction, apply_elements, revert_elements, remove_elements) {
        var apply_head_parts = [];
        var revert_head_parts = [];
        var remove_head_parts = [];

        // cleanup head elements
        if (direction === 'forward') {
            $('head > [data-remove-on-pjaxr]').each(function() {
                var $this = $(this);
                remove_head_parts.push(outerHTML($this));
                $this.remove();
            });
        }
        else if (direction === 'back') {
            var revert_result = processPjaxHeadElements(revert_elements, false);
            var remove_result = processPjaxHeadElements(remove_elements, true);

            // there are no apply elements on back processing
            $.extend(revert_head_parts, revert_result[1]);
            $.extend(remove_head_parts, remove_result[2]);
        }

        var apply_result = processPjaxHeadElements(apply_elements, true);
        $.extend(apply_head_parts, apply_result[0]);
        $.extend(revert_head_parts, apply_result[1]);
        $.extend(remove_head_parts, apply_result[2]);

        return [apply_head_parts, revert_head_parts, remove_head_parts];
    }

    function processPjaxBody(elements) {
        var apply_body_parts = [];
        var revert_body_parts = [];

        if (elements && elements.length > 0) {
            $.each(elements, function(index, value) {
                var $value = $(value);
                var id = $value.attr('id');
                if (id) {
                    var $target = $('#'+id);
                    if ($target.length > 0) {
                        revert_body_parts.push(outerHTML($target));
                        $target.html($value.html());
                        apply_body_parts.push(outerHTML($target));
                    }
                }
            });
        }

        return [apply_body_parts, revert_body_parts];
    }

    // helper to trigger jQuery events
    function fire(type, args) {
        var event = $.Event(type);
        $(document).trigger(event, args);
        return !event.isDefaultPrevented();
    }

    // wrapper to save some arguments
    function parseHTML(html) {
        return $.parseHTML(html, document, true)
    }

    // helper to get the outer html
    function outerHTML(element) {
        return element.clone().wrap('<p>').parent().html();
    }

    // generate a unique id for state object based on the current timestamp
    function uniqueId() {
        return (new Date()).getTime();
    }

    // hard replace current state with url
    // workaround for WebKit bug: https://bugs.webkit.org/show_bug.cgi?id=80697
    function locationReplace(url) {
        window.history.replaceState(null, '', '#');
        window.location.replace(url);
    }

    // takes care of the back and forward functionality
    function onPjaxRPopstate(event) {
        var state = event.state;

        if (state) {
            // when coming forward from a separate history session, will get an
            // initial pop with a state we are already at. Skip reloading the current page.
            if (initialPop && initialURL == state.url) {
                return;
            }

            fire('pjaxr:start', [fnPjaxR.options]);

            // title is always set, no check
            document.title = state.title;

            // determine whether to go back or forth
            var direction = fnPjaxR.state.id < state.id ? 'forward' : 'back';

            // null check inside
            processPjaxHead(direction, state.head_apply, state.head_revert, state.head_remove);

            var body = direction === 'forward' ? state.body_apply : state.body_revert;
            if (body && body.length > 0) {
                processPjaxBody(body);
            }

            fnPjaxR.state = state;

            // force reflow / relayout before the browser tries to restore the scroll position.
            document.body.offsetHeight;

            fire('pjaxr:end', [fnPjaxR.options]);
        }
        initialPop = false;
    }

    // helper to extract pjax version from head meta tag
    function findVersion() {
        return $('meta').filter(function() {
            return String($(this).attr('http-equiv')).toUpperCase() === 'X-PJAX-VERSION';
        }).attr('content');
    }

    var initialPop = true;
    var initialURL = window.location.href;
    var initialState = window.history.state;
    var namespace;

    // initialize $.fnPjaxR.state if possible
    // happens when reloading a page and coming forward from a different session history.
    if (initialState) {
        fnPjaxR.state = initialState;
    }

    // non-webkit browsers don't fire an initial popstate event
    if ('state' in window.history) {
        initialPop = false;
    }

    // add the state property to jQuery's event object so we can use it in $(window).on('popstate', ...)
    if ($.inArray('state', $.event.props) < 0) {
        $.event.props.push('state');
    }

    // enables pushState behavior
    function enable() {
        $.fn.pjaxr = fnPjaxR;
        $.fn.pjaxr.click = handleClick;
        $.fn.pjaxr.enable = $.noop;
        $.fn.pjaxr.disable = disable;
        $.fn.pjaxr.defaults = {
            timeout: 650,
            push: true,
            replace: false,
            scrollTo: 0,
            version: findVersion
        };
        $(window).on('popstate.pjaxr', onPjaxRPopstate);
    }

    // disable pushState behavior
    function disable() {
        $.fn.pjaxr = function() { return this; };
        $.fn.pjaxr.enable = enable;
        $.fn.pjaxr.disable = $.noop;
        $(window).off('popstate.pjaxr', onPjaxRPopstate);
    }

    // is pjax supported by this browser?
    $.support.pjaxr = window.history && window.history.pushState && window.history.replaceState &&
        // pushState isn't reliable on iOS until 5
        !navigator.userAgent.match(/((iPod|iPhone|iPad).+\bOS\s+[1-4]|WebApps\/.+CFNetwork)/);
    // initial executes enable / disable pjax when the script gets loaded
    $.support.pjaxr ? enable() : disable();
})(jQuery);
