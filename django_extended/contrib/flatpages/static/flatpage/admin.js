$(document).ready(function(urls)
{

    $('#content-main > form').each(function(update) {
        update = function()
        {
            var value = $("#id_link_type").val();
            var $tabs = $('#suit_form_tabs li');
            var $contents = $(this).find('.tab-content fieldset');
            if(value == "PAGE")
            {
                $('.field-link_value').hide();
                $('.field-tags').show();
                $('.field-content').show();
                $tabs.eq(2).show()
            }
            else if(value == "APP")
            {
                $('.field-link_value').show();
                $('.field-tags').hide();
                $('.field-content').hide();
                $tabs.eq(2).hide()

            }
            else if(value == "EXTERNAL")
            {
                $('.field-link_value').show();
                $('.field-tags').hide();
                $('.field-content').hide();
                $tabs.eq(2).hide()

            }
        }
        $("#id_link_type").on('change', update);
        update();


    });


    urls = {}
    $('#result_list .field-url a').each(function()
    {
        var url = $(this).attr('href');
        console.log(url)
        if(urls[url])
        {
            $(this).parents('tr').css({ opacity: 0.5 });
        }
        urls[url] = 1;
    })

})