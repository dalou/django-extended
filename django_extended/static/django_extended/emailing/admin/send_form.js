
$(document).ready(function($textarea, $pre, source_editor, $preview, set_preview) {


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

    $pre = $textarea.prev()

    $preview = $('<iframe noframeborder="on"></iframe>').css({ width:'100%', border:0 }).hide();
    $pre.before($preview);

    $preview.before($('<a class="btn">Aperçu</a>').on('click', function()
    {
        $pre.hide();
        $preview.show();
        set_preview();
    }))
    $preview.before($('<a class="btn">Editer</a>').on('click', function()
    {
        $pre.show();
        $preview.hide();
        $(window).resize();
    }))

    set_preview = function() {
        $preview.contents().find('html').html(source_editor.getValue());
        $preview.css({ height:$preview.contents().find('body').height() });
    }

    if(source_editor.getValue().length > 200)
    {
        set_preview();
    }
});