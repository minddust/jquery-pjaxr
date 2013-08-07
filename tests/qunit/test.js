if ($.support.pjaxr) {
    module('$.pjaxr', {
        setup: function() {
            var self = this;
            stop();
            window.iframeLoad = function(frame) {
                self.frame = frame;
                self.iframe = $('iframe').contents();
                window.iframeLoad = $.noop;
                start();
            };
            $('#qunit-fixture').append('<iframe src="/home/">');
        },
        teardown: function() {
            delete window.iframeLoad;
        }
    });

    asyncTest('pushes new url', 1, function() {
        var iframe = this.iframe;

        $(document).on('pjaxr:end', function() {
            equal(window.location.pathname, '/blog/');

            start();
        });

        $('body', iframe).pjaxr('a[data-pjaxr]');
        $('a[href="/blog/"]', iframe).trigger("click");
    });
}