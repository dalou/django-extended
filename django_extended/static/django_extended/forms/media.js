$(document).ready(function() {




    $(document).on('mouseenter', '.django_extended-media_input', function(self)
    {
        if(this.django_extended_media_input_active === true)
        {
            return;
        }
        this.django_extended_media_input_active = true;
        self = this;

        $(this).mediaDropzone().on('mediaDropzone.deposed', function(e, media, file, embed)
        {
            //console.log('media deposed', media, file, embed)
            if(file)
            {
                $(self).find('.django_extended-media_input-preview').html('<img style="margin-bottom:15px;" class="img-responsive" src="'+file+'"/>').css({
                    backgroundImage: 'url(' + file + ')'
                });
                $(self).find('.django_extended-media_input-media').addClass('active');
                $(self).find('.django_extended-media_input-empty').removeClass('active');
                $(self).find('input[type=checkbox]').eq(0).prop('checked', false);
            }
            else if(embed)
            {
                $(self).find('input[type=checkbox]').eq(0).prop('checked', false);

                $(self).find('.django_extended-media_input-preview').html(embed).css({
                    backgroundImage: ''
                });
                $(self).find('.django_extended-media_input-media').addClass('active');
                $(self).find('.django_extended-media_input-empty').removeClass('active');
            }
        });




    });



});