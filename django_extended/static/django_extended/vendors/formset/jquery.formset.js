/**
 * jQuery simple Formset 1.0
 * @author Autrusseau Damien
 */
;(function($)
{
    $.fn.formset = function(opts, options)
    {
        options = $.extend({}, $.fn.formset.defaults, opts);
        return $(this).each(function(i, self, group, forms, empty_form, total_forms)
        {
            group = $(self);
            empty_form = group.find(options.empty);
            empty_form.detach()

            var refresh = function()
            {
                forms = group.find(options.forms);
                total_forms = $('#id_' + options.prefix + '-TOTAL_FORMS');
                total_forms.val(forms.length);
                group[ forms.length == 0 ? 'addClass' : 'removeClass']('formset-forms-empty');

            }
            refresh();

            group.on('mousedown', options.add, function(form, DELETE)
            {
                var form_html = $('<div>').append(empty_form.clone()).html();
                var form = $(form_html.replace(/__prefix__/g, parseInt(total_forms.val())));
                form.removeClass(options.empty.replace('.', ''))
                var first = forms.filter(':first');
                if(first.length)
                {
                    forms.filter(':first').before(form);
                }
                else {
                    group.append(form)
                }
                refresh();
            });

            applyRemove = function(button, bool)
            {
                form = $(button).parents(options.forms).eq(0);
                DELETE = null;
                form.find('input').each(function(i, input)
                {
                    var id = $(input).attr('id')
                    if(id && id.indexOf('DELETE') !== -1)
                    {
                        DELETE = $(input)
                    }
                });

                if(DELETE)
                {
                    DELETE.prop('checked', bool);
                    form[bool ? 'addClass': 'removeClass']('formset-removed-form');
                    refresh();
                }
                else if(bool)
                {
                    form.remove();
                    refresh();
                }
            }

            group.on('click', options.remove, function(form, DELETE)
            {
                applyRemove($(this), true);
            });

            group.on('click', options.cancelRemove, function(form, DELETE)
            {
                applyRemove($(this), false);
            });
        });
    };

    $.fn.formset.defaults = {
        prefix: 'form',
        forms: '.formset-form',
        empty: '.formset-empty-form',
        add: '.formset-add-form',
        remove: '.formset-remove-form',
        cancelRemove: '.formset-cancel-remove-form',
    };
})(jQuery);