
$(document).ready(function($textarea) {


    $textarea = $('<textarea id="id_template" name="template"></textarea>')
    $textarea.val($('#id_template').val()).hide();

    var $parent = $('#id_template').parent()

    source_editor = ace.edit("id_template");
    source_editor.setTheme("ace/theme/monokai");
    source_editor.getSession().setMode("ace/mode/html");
    source_editor.setOptions({
      maxLines: Infinity
    });
    source_editor.resize();
    source_editor.on("change", function(e) {

        $textarea.val(source_editor.getValue());
    });
    $textarea.val(source_editor.getValue());

    $parent.append($textarea)
});