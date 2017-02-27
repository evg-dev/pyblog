$(document).ready(function(event) {

    $('.main').on('submit', '.contact-form', function(event) { // catch the form's submit event
        event.preventDefault();

        var maxid = null; //get id lates comment
        $(".comment").each(function () {
                maxid = Math.max(maxid, parseInt($(this).attr("id")));
        });
        $("#max").val(maxid); // add to hidden input
        $.ajax({ // create an AJAX call...
            type: 'POST', // GET or POST
            async: true,
            data: $(this).serialize(),
            url: $(this).attr('action'), // the file to call
            success: function(response) { // on success
                $('.contact-form')[0].reset(); //Clear form

                locale =  { en : {
                                date : "Date #id",
                                reply : "Reply",
                                cansel_reply : "Cancel reply",
                        },
                            ru : {
                                date : "Время #id",
                                reply : "Ответить",
                                cansel_reply : "Свернуть",                        
                        }
                }
                var curl = $(location).attr('href').split('//')[1].split('/')[1]
                l = locale[curl]

                var markup = '<div class="comment" id="${ c.id }">'
                + '<div class="comment-wrapper"><div class="comment-header">'
                + '<p><i class="fa fa-user" aria-hidden="true"></i> ${ c.user_name }</p>'
                + '<p>${ l.date }: <a class="ankor" href="#comment-${ c.id }" name="comment-${ c.id }">'
                + '${ created } #${ c.id }</a></p></div><p>${ c.content }</p>'
                + '<a href="reply/${ c.id }" class="comment-reply">${ l.reply }</a>'
                + '<a href="#" class="comment-cancel-reply" style="display: none;">${ l.cansel_reply }</a></div></div>';

                $.template("commentTemplate", markup);

                for (key in response) {
                    c = response[key];
                    if (c['parent'] === null) {
                        $.tmpl("commentTemplate", c).appendTo(".comment_list");
                    } else {
                        var id = ("#" + c['parent']+"");
                        $.tmpl("commentTemplate", c).appendTo(id);
                    }
                delete response
                }
            },

            // failure: function(response) { 
            //     alert('Got an error dude');
            // }
        });
    });
});

 //CRSF protect

function getCookie(name)
{
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
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});