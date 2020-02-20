// Chatbot functions

$('#search_entry').keypress(function (e) {
  if (e.which == 13) {
    $('#searchEntry').submit();
    return false;
  }
});

$(document).ready(function() {
  $('#searchEntry').submit(function(e) {
    e.preventDefault();
    var user_entry = $('#search_entry').val();
    user_entry = user_entry.split('<').join('&lt;');
    var resView = $('#dialog');
    resView.append('<p class="user_talk">' + user_entry + '</p>');
    resView.append('<div class="spinner-grow text-dark"></div>');
    resView.animate({
        scrollTop: resView[0].scrollHeight}, 'slow');
    $.post('/search', {user_entry: user_entry,}).done(function(data) {
        $('#search_entry').val('');
        $('.spinner-grow').hide();
        resView.animate({
            scrollTop: resView[0].scrollHeight}, 'slow');
        resView.append('<div class="spinner-grow text-dark"></div>');
        if (data.entity !== '') {
            $('.spinner-grow').hide();
            if (data.brief.length > 0) {
                resView.append('<p class="sys_talk">' + data.brief + '.</p>');
            }
            if (data.address.length > 20) {
                resView.append('<p class="sys_talk">' + data.entity + ' se trouve ' + data.address + '.</p>');
            } else {
                if (data.city.length > 0) {
                resView.append('<p class="sys_talk">Il possède plusieurs établissements dont un à ' + data.city + '.</p>');
                }
            }
            if (data.g_map.length > 0) {
                resView.append('<iframe class="g-map" src=' + data.g_map + '></iframe>');
            }
            if (data.info.length > 0) {
                resView.append('<div class="story"></p>' + data.info + '</p></div>');
            }
            if (data.news[0]['header'].length > 0) {
                resView.append('<p class="sys_talk">Aux dernières nouvelles...</p>');
                for (let i = 0; i < 3; i++) {
                    resView.append('<div class="story"><p><b>' + data.news[i]['header'] + '</b></p><p>' + data.news[i]['subtitle'] + '<a class="wiki" href="' + data.news[i]['source'] + '" target="_blank">Lire +</a></p>');
                    resView.append('<hr>');
                    }
            }
            if (data.extract.length > 0) {
                resView.append('<p class="sys_talk">Je peux vous en dire un peu plus...</p>');
                resView.append('<div class="story">' + data.extract + '<a class="wiki" href="' + data.link + '" target="_blank">Lire +</a></div>');
                resView.append('<hr>');
                for (let i = 0; i < data.ner.length; i++) {
                    resView.append('<span class="ner">' + data.ner[i] + '</span>');
                    }
            }
            resView.append('<p class="sys_talk">' + data.end_reply + '</p>');
            } else {
                $('.spinner-grow').hide();
                resView.append('<p class="sys_talk">' + data.reply + '</p>');
            }
    });
  });
});
