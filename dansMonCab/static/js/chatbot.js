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
        resView.append('<p class="sys_talk">' + data.reply + '</p>');
        resView.animate({
            scrollTop: resView[0].scrollHeight}, 'slow');
        resView.append('<div class="spinner-grow text-dark"></div>');
        if (data.status == 'ok') {
            $('.spinner-grow').hide();
            resView.append('<iframe class="g-map" src=' + data.g_map + '></iframe>');
            resView.append('<p class="sys_talk">A propos, saviez-vous que...</p>');
            resView.append('<div class="story">' + data.extract + ' <a class="wiki" href="' + data.link + '" target="_blank">  lire  </a></div>');
            resView.append('<p class="sys_talk">' + data.end_reply + '</p>');
            } else {
                $('.spinner-grow').hide();
            }
    });
  });
});
