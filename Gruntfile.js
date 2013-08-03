module.exports = function (grunt) {
	grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
		qunit: {
			files: ['tests/*.html']
		}
	});

	grunt.loadNpmTasks('grunt-contrib-qunit');

    // test task
	grunt.registerTask('test', ['qunit']);

    // default task
	grunt.registerTask('default', ['test']);
};