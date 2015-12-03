var NAVIGATOR_IS_MOBILE = (/android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase()));

if (!String.prototype.endsWith) {
  String.prototype.endsWith = function(searchString, position) {
    var subjectString = this.toString();
    if (typeof position !== 'number' || !isFinite(position) || Math.floor(position) !== position || position > subjectString.length) {
      position = subjectString.length;
    }
    position -= searchString.length;
    var lastIndex = subjectString.indexOf(searchString, position);
    return lastIndex !== -1 && lastIndex === position;
  };
}

(function($){
    $.unserialize = function(serializedString)
    {
        serializedString = serializedString.split("?");
        if(serializedString.length > 1)
        {
            serializedString = serializedString[1]
        }
        else {
            serializedString = serializedString[0]
        }
        var str = decodeURI(serializedString);
        var pairs = str.split('&');
        var obj = {}, p, idx, val;
        for (var i=0, n=pairs.length; i < n; i++) {
            p = pairs[i].split('=');
            idx = p[0];

            if (idx.indexOf("[]") == (idx.length - 2)) {
                // Eh um vetor
                var ind = idx.substring(0, idx.length-2)
                if (obj[ind] === undefined) {
                    obj[ind] = [];
                }
                obj[ind].push(p[1]);
            }
            else {
                obj[idx] = p[1];
            }
        }
        return obj;
    };
})(jQuery);


$.fn.addLoading = function(text, b, c)
{
    return this.each(function(i, self)
    {
        if( self.is_loading !== true )
        {
            self.is_loading = true;
            $loading = $("<span class='loading-text'></span>");
            $(self).append($loading.hide()).addClass('loading');
            $loading.fadeIn(300);
        }
        var new_text = text;
        if(!new_text)
        {
            new_text = $(self).data('loading');
        };
        if(new_text)
        {
            $(self).find('.loading-text').text(new_text);
        }
    });
}
$.fn.removeLoading = function()
{
    return this.each(function(i, self)
    {
        $(self).removeClass('loading').find('.loading-text').fadeOut(250, function()
        {
            $(this).remove();
        });
        self.is_loading = null;
    });
}

$(document).ready(function(menuTo, select)
{

    $('[data-images-loading]').each(function(e, $self)
    {
        $self = $(this).addLoading();
        $self.imagesLoaded(function()
        {
            $self.removeLoading();
        })
    });

    $('[data-loading]').addLoading();

    $(document).on('mouseenter', '[data-slick]', function(self) {
        if(this.data_slick === true) return
        this.data_slick = true;
        self = $(this);
        //self.imagesLoaded(function() {
            self.slick(self.data('slick'));
        //});
    })
    $('[data-slick]').trigger('mouseenter');


    $('[data-share]').each(function(i, self)
    {
        self = $(this);
        self.tooltipster({
            trigger: 'click',
            interactive: true,
            content: self.next().find('.share')
        });
    });

    $(document).on('click', '[data-modal]', function(event, trigger, target)
    {
        trigger = $(this);
        target = trigger.data('modal');
        if(target[0] == '#') {
            var type = 'inline';
            var cache = true;
        }
        else if(target.endsWith('.png') || target.endsWith('.jpg') || target.endsWith('.gif')) {

            var type = 'image';
            var cache = true;
        }
        else {
            var type = 'ajax';
            var cache = false;
        }
        $.magnificPopup.open({
            type: type,
            closeMarkup: '<button type="button" class="mfp-close"><span class="appicon appicon-close mfp-close"></span></button>',
            items: {
                src: target,
                cache: cache,
            },
            settings: {cache: cache},
            callbacks: {
                open: function() {
                    if(window.mfp) window.mfp.popupsCache = {};
                },
                ajaxContentAdded: function() {
                    select(this.content.find('select'));
                    this.content.find('input,textarea').eq(0).focus();
                }
            },
            mainClass: 'my-mfp-slide-bottom',
            removalDelay: 300
        });
        return false;
    });

    $('[data-isotopes]').each(function(i, self)
    {
        $(self).imagesLoaded(function() {
            $(self).isotope({
                itemSelector: '[data-isotope]',
                layout: 'packery'
            })
        });
    });

    $(document).on('mouseover', '[data-tooltip]', function(content, options)
    {

        if(!this.tooltiptized_over)
        {
            var data = $(this).data('tooltip');
            options = {
                delay: 0,
                theme : 'tooltipster-default'
            }

            if(typeof data == "object")
            {
                options = $.extend(options, data)
            }
            else if(typeof data == "string")
            {
                if(data[0] != '#')
                {
                    options.content = $('<div>'+data+'</div>');
                }
                else
                {
                    options.content = data;
                }
            }
            if(options.content && options.content[0] == '#' && $(options.content).length)
            {
                options.content = $(options.content);
            }
            $(this).tooltipster(options);
            this.tooltiptized_over = true;
            if(!options.trigger || options.trigger == "hover")
            {
                $(this).tooltipster('show')
            }

        }
    });

});



$(document).ready(function($navs, scrollFct)
{
    $navs = $('[data-navigation]').each(function(i, self, $menu)
    {
        self = $(this);
        $menu = $('<li><a class="item"><span>'+self.data('navigation')+'</span></a></li>');
        $menu.on('click', 'a', function()
        {
            $.smoothScroll({
                scrollTarget: self,
                offset: -50
            });
        });
        $('#main-scroll-nav').append($menu);
        self[0].nav_menu = $menu;
    });

    scrollFct = function(windowHeight, scrollTop, closest, closest_depth)
    {

        windowHeight = $(window).height();
        scrollTop = $(window).scrollTop();
        // var middle = scrollTop + windowHeight/2

        closest_depth = null;
        closest = null;

        // $('#fixed-nav-social').css({ top: middle - $('#fixed-nav-social').height()/2 })
        // $('#fixed-nav').css({ top: middle - $('#fixed-nav').height()/2 })

        $navs.each(function(i, self, top, bottom)
        {
            self = $(this);
            top = self.offset().top;

            var wCenter = ( windowHeight/2 + scrollTop );
            var tCenter = (top + self.height()/2);

            //var depth = Math.abs(wCenter - tCenter)
            var depth = Math.abs((scrollTop - top) + ((scrollTop+windowHeight) - (top + self.height())))

            //console.log(self[0].nav_menu.text(), depth, scrollTop >= top)

            if(!closest_depth || ( depth <= closest_depth )  ) {
                closest = self;
                closest_depth = depth;
            }

        });

        if(closest) {
            closest[0].nav_menu.find('a').addClass('active')
            closest[0].nav_menu.siblings().find('a').removeClass('active');
        }

    }
    $(window).scroll(scrollFct);
    $(window).resize(scrollFct);
    scrollFct();
});