module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        qunit: {
            all: {
                options: {
                    urls: [
                        'http://localhost:3000/tests/qunit/index.html'
                    ]
                }
            }
        },
        connect: {
            server: {
                options: {
                    port: 3000,
                    base: '.'
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-connect');
    grunt.loadNpmTasks('grunt-contrib-qunit');

    // test task
    grunt.registerTask('test', ['connect', 'qunit']);

    // default task
    grunt.registerTask('default', ['test']);
};