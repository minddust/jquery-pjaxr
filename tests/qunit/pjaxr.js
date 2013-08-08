module('$.pjaxr');

asyncTest('push 1rd level url', function() {
    equal(window.location.pathname, '/');
    equal($('head > title').html(), 'qunit');
    equal(document.title, 'qunit');
    equal($('head > meta').length, 1);
    $.each($('head > meta'), function(index, value) {
        var $meta = $(value);
        if ($meta.attr('name') === 'author') { equal($meta.attr('content'), 'minddust'); }
    });

    $(document).one('pjaxr:end', function() {
        equal(window.location.pathname, '/home/');

        equal($('head > title').html(), 'home');
        equal(document.title, 'home');

        history.go(-(history.length - 1));

        start();
    });

    $(document).pjaxr('a[data-pjaxr]');
    $('a[href="/home/"]').trigger("click");
});

asyncTest('push 2nd level url', function() {
    equal(window.location.pathname, '/');
    equal($('head > title').html(), 'qunit');

    $(document).one('pjaxr:end', function() {
        equal(window.location.pathname, '/home/');
        equal($('head > title').html(), 'home');

        $(document).one('pjaxr:end', function() {
            equal(window.location.pathname, '/blog/');
            equal($('head > title').html(), 'blog');

            history.go(-(history.length - 1));

            start();
        });

        $('a[href="/blog/"]').trigger("click");
    });

    $(document).pjaxr('a[data-pjaxr]');
    $('a[href="/home/"]').trigger("click");
});
