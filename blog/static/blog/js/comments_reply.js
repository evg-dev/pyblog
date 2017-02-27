$(document).ready(function($) {
    
    url = $(location).attr('href').split('//')[1].split('/');
    form = $('.form-wrapper').clone();
    reply = $('.comment-reply');
    cancel = $('.comment-cancel-reply');
    cancel.hide();

    // reload after ajax
    $('.main').on('DOMNodeInserted', function (event) {
        form = $('.form-wrapper').clone();
        reply = $('.comment-reply');
        cancel = $('.comment-cancel-reply');
    });

    $('.main').on('click', '.comment-reply', function () {
        event.preventDefault();
        reply.show(); // show previous comment's reply link
        cancel.hide(); // hide previous comment's cancel link
        comment = $(this).parents('.comment-wrapper');
        id = $(this).parents(".comment").attr("id");
        comment.find(cancel).show();
        $(this).hide();
        $('.form-wrapper').remove();
        form.clone().appendTo(comment);
        new_url =  '/' + url.slice(1,3).join('/') + '/reply/' + id + '/';
        $('.contact-form').attr('action', new_url); //reply url
    });

    $('.main').on('click', '.comment-cancel-reply', function () {
        event.preventDefault();
        comment = $(this).parents('.comment-wrapper');
        comment.find(reply).show();
        $(this).hide();
        $('.form-wrapper').remove();
        form.clone().appendTo('.contact');
    });

    // captcha refresh
    $('img.captcha').after(
            $('<a href="#void" class="js-captcha-refresh">Refresh</a>')
    );

    $('.main').on('click', '.js-captcha-refresh', function(){
        $form = $(this).parents('form');
        c_url = location.protocol + "//" + url.slice(0,2).join('/') + '/captcha/refresh/'

        $.getJSON(c_url, {}, function(json) {
            $form.find('input[name="captcha_0"]').val(json.key);
            $form.find('img.captcha').attr('src', json.image_url);
        });

        return false;
    });

});
// 'http://localhost:8000/ru/captcha/refresh/'