$(document).ready(function(event) {

    var url = $(location).attr('href').split('//')[1].split('/');
    var form = $('.form-wrapper').clone();
    var reply = $('.comment-reply');
    var cancel = $('.comment-cancel-reply');
    cancel.hide();

    // reload after ajax
    $('.main').on('DOMNodeInserted', function (event) {
        form = $('.form-wrapper').clone();
        reply = $('.comment-reply');
        cancel = $('.comment-cancel-reply');
    });

    $('.main').on('click', '.comment-reply', function (event) {
        event.preventDefault();
        reply.show(); // show previous comment's reply link
        cancel.hide(); // hide previous comment's cancel link
        comment = $(this).parents('.comment-wrapper');
        id = $(this).parents('.comment').attr('id');
        comment.find(cancel).show();
        $(this).hide();
        $('.form-wrapper').remove();
        form.clone().appendTo(comment);
        new_url =  '/' + url.slice(1,3).join('/') + '/reply/' + id + '/';
        $('.contact-form').attr('action', new_url); //reply url
        $('.js-captcha-refresh').click(); 
    });

    $('.main').on('click', '.comment-cancel-reply', function (event) {
        event.preventDefault();
        comment = $(this).parents('.comment-wrapper');
        comment.find(reply).show();
        $(this).hide();
        $('.form-wrapper').remove();
        form.clone().appendTo('.contact');
        $('.js-captcha-refresh').click(); 
    });

    // captcha refresh
    function captcha_refresh() {
        $form = $(this).parents('form');
        c_url = location.protocol + '//' + url.slice(0,2).join('/') + '/captcha/refresh/';
        $.getJSON(c_url, {}, function(json) {
            $form.find('input[name="captcha_0"]').val(json.key);
            $form.find('img.captcha').attr('src', json.image_url);
        });
        return false;
    }
    
    $('#id_captcha_1').after(
            $('<a href="#void" class="js-captcha-refresh">Refresh</a>')
    );
    $('.main').on('click', '.js-captcha-refresh', captcha_refresh);

    // AJAX POST
    $('.main').on('submit', '.contact-form', function(event) { // catch the form's submit event
        event.preventDefault();

        var maxid = null; //get id lates comment
        $('.comment').each(function () {
                maxid = Math.max(maxid, parseInt($(this).attr('id')));
        });
        $('#max').val(maxid); // add to hidden input
        $.ajax({ // create an AJAX call...
            type: 'POST', // GET or POST
            async: true,
            data: $(this).serialize(),
            url: $(this).attr('action'), // the file to call
            success: function(response) { // on success
                $('#captcha_error').remove();
                if (response['success'] === true) {
                    $('.js-captcha-refresh').click(); 
                    $('.contact-form')[0].reset();
                    var locale =  { en : {
                                    date : 'Date #id',
                                    reply : 'Reply',
                                    cansel_reply : 'Cancel reply',
                            },
                                ru : {
                                    date : 'Время #id',
                                    reply : 'Ответить',
                                    cansel_reply : 'Свернуть',                        
                            }
                    }
                    var l = locale[url[1]]
                    var markup = '<div class="comment" id="${ c.id }"><div class="comment-wrapper">'
                    + '<div class="comment-header">'
                    + '<p><i class="fa fa-user" aria-hidden="true"></i> ${ c.user_name }</p>'
                    + '<p>${ l.date }: <a class="ankor" href="#comment-${ c.id }" name="comment-${ c.id }">'
                    + '${ created } #${ c.id }</a></p></div><p>${ c.content }</p>'
                    + '<a href="reply/${ c.id }" class="comment-reply">${ l.reply }</a>'
                    + '<a href="#" class="comment-cancel-reply" style="display: none;">'
                    + '${ l.cansel_reply }</a></div></div>';

                    $.template('commentTemplate', markup);

                    for (key in response['comments']) {
                        c = response['comments'][key];
                        if (c['parent'] === null) {
                            $.tmpl('commentTemplate', c).appendTo('.comment_list');
                        } else {
                            var id = ('#' + c['parent']+'');
                            $.tmpl('commentTemplate', c).appendTo(id);
                        }
                    delete response;
                    }
                } else if (response['success'] === false) {
                    var errors = response['form'];
                    for (var k in errors) {
                        if (k === 'captcha') {
                            var err = (errors[k]);
                        } else {
                            var err = ('error');
                        }
                        $('.js-captcha-refresh').after('<p id="captcha_error">' + err + '</p>');
                    }
                }
            },
        });
    });
});

//CRSF protect

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
         }
     } 
});