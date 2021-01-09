// Chatbot

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
    $('#search_entry').val('');
    resView.animate({
        scrollTop: resView[0].scrollHeight}, 'slow');
    $.post('/search', {user_entry: user_entry,}).done(function(data) {
        $('.spinner-grow').hide();
        resView.animate({
            scrollTop: resView[0].scrollHeight}, 'slow');
        if (data.entity !== '') {
            if (data.map.length > 0) {
                resView.append('<iframe class="g-map" src=' + data.map + '></iframe>');
            }
            if (data.intro.length > 0) {
                resView.append('<p class="sys_talk">' + data.intro + '.</p>');
            }
            if (data.extract.length > 0) {
                resView.append('<p class="sys_talk">Je peux vous en dire un peu plus...</p>');
                resView.append('<div class="story">' + data.extract + '<a class="wiki" href="' +
                data.link + '" target="_blank">Lire +</a></div>');
            }
            if (data.news['total'] > 0) {
                resView.append('<p class="sys_talk">Aux dernières nouvelles...</p>');
                for (let i = 0; i < 3; i++) {
                    resView.append('<div class="story"><p><b>' + data.news['news'][i]['header'] + '</b></p>' +
                    '<p><img class="img-fluid" alt="" src="' + data.news['news'][i]['img'] + '"></p>' +
                    '<p>' + data.news['news'][i]['subtitle'] + '<a class="wiki" href="' + data.news['news'][i]['source'] +
                    '" target="_blank">Lire +</a></p><hr>');
                    }
            }
            resView.append('<p class="sys_talk">' + data.ok_reply + '</p>');
            } else {
                resView.append('<p class="sys_talk">' + data.nok_reply + '</p>');
            }
    });
  });
});
