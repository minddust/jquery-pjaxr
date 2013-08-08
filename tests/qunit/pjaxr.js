module('$.pjaxr');

asyncTest('push 1rd level url', function() {
    equal(window.location.pathname, '/');
    equal($('head > title').html(), 'qunit');
    equal(document.title, 'qunit');
    equal($('head > meta').length, 1);
    $.each($('head > meta'), function(index, value) {
        var $meta = $(value);
        if ($meta.attr('name') === 'author') { equal($meta.attr('content'), 'minddust'); }
        else { ok(false); }
    });
    equal($('head > link').length, 1);
    equal($('head > script').length, 0);
    equal($('head > style').length, 0);
    equal($('#menu-extra-entry').html().trim(), '');
    equal($('#content').html().trim(), '<h1>qunit tests</h1>');

    $(document).one('pjaxr:end', function() {
        equal(window.location.pathname, '/home/');

        equal($('head > title').html(), 'home');
        equal(document.title, 'home');
        equal($('head > meta').length, 3);
        $.each($('head > meta'), function(index, value) {
            var $meta = $(value);
            if ($meta.attr('name') === 'author') { equal($meta.attr('content'), 'minddust'); }
            else if ($meta.attr('name') === 'title') { equal($meta.attr('content'), 'home'); }
            else if ($meta.attr('name') === 'description') { equal($meta.attr('content'), 'home of everything'); }
            else { ok(false); }
        });
        equal($('head > link').length, 1);
        equal($('head > script').length, 0);
        equal($('head > style').length, 0);
        equal($('#menu-extra-entry').html().trim(), '');
        equal($('#content').html().trim(), '<h1>home - pjax</h1>');

        history.back();

        setTimeout(function() {
            equal(window.location.pathname, '/');
            equal($('head > title').html(), 'qunit');
            equal(document.title, 'qunit');
            equal($('head > meta').length, 1);
            $.each($('head > meta'), function(index, value) {
                var $meta = $(value);
                if ($meta.attr('name') === 'author') { equal($meta.attr('content'), 'minddust'); }
                else { ok(false); }
            });
            equal($('head > link').length, 1);
            equal($('head > script').length, 0);
            equal($('head > style').length, 0);
            equal($('#menu-extra-entry').html().trim(), '');
            equal($('#content').html().trim(), '<h1>qunit tests</h1>');

            history.go(-(history.length - 1));

            start();
        }, 0);
    });

    $(document).pjaxr('a[data-pjaxr]');
    $('a[href="/home/"]').trigger('click');
});

asyncTest('push 2nd level url', function() {
    equal(window.location.pathname, '/');
    equal($('head > title').html(), 'qunit');
    equal($('head > meta').length, 1);

    $(document).one('pjaxr:end', function() {
        equal(window.location.pathname, '/home/');
        equal($('head > title').html(), 'home');
        equal($('head > meta').length, 3);

        $(document).one('pjaxr:end', function() {
            equal(window.location.pathname, '/blog/');
            equal($('head > title').html(), 'blog');

            history.go(-(history.length - 1));

            start();
        });

        $('a[href="/blog/"]').trigger('click');
    });

    $(document).pjaxr('a[data-pjaxr]');
    $('a[href="/home/"]').trigger('click');
});
