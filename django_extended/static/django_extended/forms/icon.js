$(document).ready(function() {

    $(document).on('click', '.django_extended-icon-widget-tabs-control', function() {
        var target = $($(this).attr('href'));
        var visible = target.is(':visible');
        $(this).parents('.django_extended-icon-widget-tabs').eq(0).find('.django_extended-icon-widget-tabs-content').hide();

        if(!visible) {
            $($(this).attr('href')).show();
        }
        return false;
    })

    $(document).on('click', '.django_extended-icon-widget', function() {
         $('.django_extended-icon-widget.active').removeClass('active')
         $(this).addClass('active');
         $($(this).data('input')).val($(this).data('value'))
    });
});