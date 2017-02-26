$(document).ready(function($) {
    
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
        url = $(location).attr('href').split('//')[1].split('/');
        url = url.slice(1,-1)
        new_url = '/' + url.join('/') + '/reply/' + id + '/'
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

});
