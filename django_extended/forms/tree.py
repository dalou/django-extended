# encoding: utf-8

from django.conf import settings

from django import forms
from django.utils.html import conditional_escape, format_html, html_safe
from django.utils.encoding import force_text, smart_text
from django.forms.utils import flatatt, to_current_timezone
from django.utils.safestring import mark_safe
from itertools import chain


class TreeInput(forms.SelectMultiple):

    def render_tree(self, name):

        html = '<div id="id_%s_tree_root"><select>' % name
        html += "<option>--- Choississez une option ---</option>"
        for element in self.tree.values():
            html += "<option value="+str(element.pk)+">"+element.title+"</option>"
        html += "</select>"

        for element in self.tree.values():
            html += self.render_tree_element(name, element)

        html +="</div>"
        return html

    def render_tree_element(self, name, element):

        if element._tree_children:

            html = '<div '+('data-independant="1"' if element.is_independant else 'data-choices="1"')+\
                        ' style="display:none; '+('margin-left:50px;' if not element.is_independant else '')+\
                        ('" id="id_%s_tree_%s">' % (name, element.pk))

            if element.is_independant:
                html += """<label>%s</label>""" % element.title

            if element._tree_choices:

                html += "<select>"
                html += "<option>--- Choississez une option ---</option>"
                for choice in element._tree_choices.values():
                    html += "<option value="+str(choice.pk)+">"+choice.title+"</option>"
                html += "</select>"

                for choice in element._tree_choices.values():
                    html += self.render_tree_element(name, choice)

            if element._tree_selects:
                for select in element._tree_selects.values():
                    html += self.render_tree_element(name, select)

            html += "</div>"
            return html
        else:
            return ''



    def render(self, name, value, attrs=None, choices=()):
        original = super(TreeInput, self).render(name, value, attrs=attrs, choices=choices)
        tree = self.render_tree(name)

        html = u"""
        <div style="display:none;" id="id_%(name)s_original">%(original)s</div>

            %(tree)s
            <script>

                function django_extended_tree_has_changed(value)
                {
                    var option = $('#id_%(name)s_tree_root option[value="'+value+'"]');
                    option.prop('selected', true)
                    var select = option.parent()
                    select.val(value)
                    select.parent().find('div[data-choices]').hide();
                    $('#id_%(name)s_tree_'+value).show();
                    $('#id_%(name)s_tree_'+value+' > div[data-independant]').show();

                    values = [];
                    $('#id_%(name)s_tree_root select:visible').each(function()
                    {
                        values.push($(this).val());
                    });
                    $('#id_%(name)s').val(values);
                }

                $('#id_%(name)s_tree_root').on('change', 'select', function(values)
                {
                    django_extended_tree_has_changed($(this).val())
                });
                var values = $('#id_%(name)s').val()
                console.log(values);
                for(var i in values)
                {
                    django_extended_tree_has_changed(values[i]);
                }
            </script>
        """

        return html % { 'tree' : tree, 'name' : name, 'original': original }




class TreeField(forms.ModelMultipleChoiceField):
    widget = TreeInput

    def __init__(self, *args, **kwargs):
        super(TreeField, self).__init__(*args, **kwargs)
        try:
            self.widget.tree = self.get_tree()
        except:
            self.widget.tree = {}

    def get_tree(self):
        if hasattr(self, '_tree'):
            return getattr(self, '_tree')

        tree = {}
        for category in self.queryset:
            category._tree_children = {}
            category._tree_choices = {} #"""<select>%s</select>""" % self.render_options(choices, selected_choices)
            category._tree_selects = {}
            category._tree_parent = None
            tree[category.pk] = category
        for pk, element in tree.items():
            if element.parent_id:
                parent = tree.get(element.parent_id)
                element._tree_parent = parent
                parent._tree_children[pk] = element


        for pk, element in tree.items():

            for child_pk, child in element._tree_children.items():
                if child.is_independant:
                    element._tree_selects[child_pk] = child
                else:
                    element._tree_choices[child_pk] = child

            if element.parent_id:
                del tree[pk]


        print tree

        setattr(self, '_tree', tree)
        return tree
