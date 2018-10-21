module.exports = function runGrunt(grunt) {
  grunt.loadNpmTasks('grunt-aws');

  grunt.initConfig({
    aws: grunt.file.readJSON('credentials.json'),
    s3: {
      options: {
        accessKeyId: '<%= aws.accessKeyId %>',
        secretAccessKey: '<%= aws.secretAccessKey %>',
        bucket: 'postcard-api-assets',
        region: 'us-west-1',
      },
      build: {
        cwd: 'public/',
        src: '**',
      },
    },
  });

  grunt.registerTask('default', ['s3']);
};
