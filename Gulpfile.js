var gulp = require('gulp');
var clean = require('gulp-clean');
var header = require('gulp-header');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var util = require('gulp-util');

var pkg = require('./package.json');
var currentYear = util.date(new Date(), 'yyyy');

var banner = '/*! <%= pkg.name %> v<%= pkg.version %> | Copyright (c) 2013-<%= currentYear %> <%= pkg.author %> | <%= pkg.license %> license | <%= pkg.homepage %> */\n';

gulp.task('scripts', function() {
    return gulp.src('./jquery.pjaxr.js')
        .pipe(uglify())
        .pipe(header(banner, {pkg: pkg, currentYear: currentYear}))
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('.'));
});

gulp.task('clean', function() {
    return gulp.src('./jquery.pjaxr.min.js', {read: false})
        .pipe(clean());
});

gulp.task('default', ['clean', 'scripts']);
