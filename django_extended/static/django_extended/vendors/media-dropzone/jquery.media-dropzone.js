
(function ( $ ) {

    var EMBED_TYPES =
    {
        "soundcloud": [
            [
                "(http[s]?\\:\\/\\/w\\.soundcloud\\.com\\/player\\/\\?url=([^\"]+))",
                "<iframe class=\"django_extended-media\" src=\"https://w.soundcloud.com/player/?url=\\2\" scrolling=\"no\" frameborder=\"no\" allowfullscreen></iframe>"
            ],
            [
                "(http[s]?\\:\\/\\/soundcloud\\.com\\/[\\d\\w\\-_]+/[\\d\\w\\-_]+)",
                "<iframe class=\"django_extended-media\" src=\"https://w.soundcloud.com/player/?url=\\1\" scrolling=\"no\" frameborder=\"no\" allowfullscreen></iframe>"
            ]
        ],
        "youtube": [
            [
                "(https?://)?(www\\.)?(youtube|youtu|youtube-nocookie)\\.(com|be)/(watch\\?v=|embed/|v/|.+\\?v=)?([^&=%\\?\\s\"]{11})",
                "<iframe class=\"django_extended-media\" src=\"https://www.youtube.com/embed/\\6?controls=0&amp;showinfo=0\"scrolling=\"no\" frameborder=\"no\" allowfullscreen></iframe>"
            ]
        ]
    }

    var default_options =
    {
        uploadMultiple: false,
        maxFilesize : 5,
        paramName: 'media',
        maxMedias : 1,
        clickable: true,
        authorizedTypes : ['image', 'youtube', 'soundcloud'],
        addRemoveLinks : true,
        dictRemoveFile: '',
        dictCancelUpload: '',
    }

    function MediaDropzone($elm, options, self)
    {
        self = this;
        self.$elm = $elm
        self.options = $.extend(default_options, options, self.$elm.data('media-dropzone'));
        self.listeners = {}
        self.progress = 0;
        self.file = null;
        self.embed = null;
        self.data = null;
        self.input = null;
        if(self.options.clickable == true)
        {
            self.$elm.click(function(e) {
                console.log(self.dropzone)
                if(e.target != this)
                {
                    if(self.dropzone)
                    {
                        self.dropzone.hiddenFileInput.click();
                    }
                    return false;
                }
            })
            // self.options.clickable = self.$elm.find('> *')
        }

        self.options.uploadMultiple = false;//self.options.maxMedias > 1;

        if(self.options.uploadUrl)
        {
            var dropzone_options = $.extend(self.options,
            {
                url: self.options.uploadUrl,
                clickable: self.options.clickable,
                previewTemplate: '<div></div>'
                , sending: function(file, xhr, formData)
                {
                    self.file = file;
                    var params = self.options.params
                    for(var i in params) {
                        if(params[i])
                        {
                            formData.append(i, params[i]);
                        }
                    }
                    self.file_type = file.type;
                    formData.append("file_typemime", file.type);
                    self.$elm.trigger('mediaDropzone.sending', [self, file]);
                }
                , removedfile: function(file)
                {
                    self.file = file;
                    self.$elm.trigger('mediaDropzone.removedfile', [self, dataUrl])
                }
                , thumbnail : function(file, dataUrl)
                {
                    self.file = file;
                    self.$elm.trigger('mediaDropzone.thumbnail', [self, dataUrl])
                    //self.$elm.css({ background: 'url(' + dataUrl + ')', opacity:0 }).addClass('media-dropzone-processing')
                }
                , uploadprogress: function(file, progress)
                {
                    self.progress = progress;
                    self.$elm.trigger('mediaDropzone.uploadprogress', [self, progress])
                    //self.$elm.css({ opacity: progress/100.00 })
                    //console.log('uploadprogress', file,e)
                }
                , success: function(file, data)
                {
                    self.progress = 100;
                    self.data = data;
                    self.$elm.trigger('mediaDropzone.success', [self, data]);
                    self.$elm.trigger('mediaDropzone.deposed', [self, data]);
                    return true;
                }

            })
            self.dropzone = new Dropzone(self.$elm[0], dropzone_options);
            console.log(self.dropzone)
        }
        // No file upload
        else
        {
            if(self.options.input)
            {
                self.input = $(self.options.input);
            }
        }
    }

    MediaDropzone.prototype.is_embed = function(self)
    {
        return self.embed !== null;
    }

    MediaDropzone.prototype.is_file = function(self)
    {
        return self.file !== null;
    }

    MediaDropzone.prototype.paste = function(clipboardData, self)
    {
        self = this;

        // console.log('PASTE', clipboardData)

        // console.log('text', clipboardData.getData('Text'))
        // console.log('file', clipboardData.getData('File'))

        var files = clipboardData.files;
        var text = clipboardData.getData('Text');
        // console.log(files)
        // if(!files)
        // {
        //     files = clipboardData.items;
        // }
        // console.log(files)

        if(files.length && self.dropzone)
        {
            for(var i in files)
            {
                self.dropzone.enqueueFiles(files[i]);//.getAsFile());
            }
        }
        else if(text)
        {
            console.log(text)
            if(self.options.uploadUrl)
            {
                $.post(self.options.uploadUrl, [
                    { name: self.options.paramName, value: text }
                ], function(data) {
                    self.$elm.trigger('mediaDropzone.deposed', [self, data]);
                });
            }
        }

    }
    MediaDropzone.prototype.on = function(eventName, fct, self)
    {
        self = this;
        self.listeners[eventName] = fct;
    }


    MediaDropzone.prototype.trigger = function(eventName, a, b, c, d)
    {
        self = this;
        if( self.listeners[eventName] )
        {
            self.listeners[eventName](a, b, c, d);
        }
    }


    MediaDropzone.prototype.apply_embed = function(dataClipboard, self)
    {
        self = this;
    }


    $.fn.mediaDropzone = function(options, a, b, c, d)
    {
        this.each(function(i, self, opt)
        {
            if(!options)
            {
                options = {}
            }

            if(!self.mediaDropzone_attached)
            {
                self.mediaDropzone_attached = new MediaDropzone($(self), options);
            }
            if(typeof options === "string")
            {
                if(options == "paste")
                {
                    self.mediaDropzone_attached.paste(a, b, c ,d)
                }
                if(options == "on")
                {
                    self.mediaDropzone_attached.on(a, b, c ,d)
                }
            }
        });
        return this;
    };

}( jQuery ));

$(document).ready(function(hover_element)
{

    $('[data-media-dropzone]').mediaDropzone();
    $(document).on('mouseenter', "[data-media-dropzone]", function(e)
    {
        $(this).mediaDropzone();
        hover_element = $(this)
    });
    $(document).on('mouseleave', "[data-media-dropzone]", function(e)
    {
        $(this).mediaDropzone();
        hover_element = null;
    });

    $(document).on('paste', function (e)
    {
        if(hover_element)
        {
            hover_element.mediaDropzone('paste', e.originalEvent.clipboardData);
        }
    });

});
