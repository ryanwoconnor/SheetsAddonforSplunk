require.config({
    paths: {
        text: "../app/GoogleDriveAddonforSplunk/components/lib/text",
        'googledriveConfigTemplate' : '../app/GoogleDriveAddonforSplunk/components/templates/index.html'
    }
});

require([
    "underscore",
    "backbone",
    "splunkjs/mvc",
    "jquery",
    "splunkjs/mvc/simplesplunkview",
    '../app/GoogleDriveAddonforSplunk/components/views/settingsView',
    "text!googledriveConfigTemplate",
], function( _, Backbone, mvc, $, SimpleSplunkView, SettingsView, GoogleDriveConfigTemplate){

    var GoogleDriveConfigView = SimpleSplunkView.extend({

        className: "GoogleDriveConfigView",

        el: '#googledriveConfigWrapper',

        initialize: function() {
            this.options = _.extend({}, this.options);
            this.render();
        },

        _loadSettings: function() {

            var that = this;
            var configComponents = $('#googledriveConfig-template', this.$el).text();
            $("#content", this.$el).html(_.template(configComponents));

            new SettingsView({
                id: "settingsView",
                el: $('#googledriveComponentsWrapper')
            }).render();
        },

        render: function() {

            document.title = "Google Drive Add-On Setup";

            var that = this;
            $(this.$el).html(_.template(GoogleDriveConfigTemplate));

            this._loadSettings();

            return this;
        }

    });

    new GoogleDriveConfigView();

});
