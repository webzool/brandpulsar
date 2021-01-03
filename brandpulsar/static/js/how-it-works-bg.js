var lFollowX = 0,
  lFollowY = 0,
  x = 0,
  y = 0,
  friction = 1 / 30;

function moveBackground() {
  x += (lFollowX - x) * friction;
  y += (lFollowY - y) * friction;

  translate = 'translate(' + x + 'px, ' + y + 'px) scale(1.1)';

  $('.left').css({
    '-webit-transform': translate,
    '-moz-transform': translate,
    'transform': translate
  });

  $('.right').css({
    '-webit-transform': translate,
    '-moz-transform': translate,
    'transform': translate
  });

  window.requestAnimationFrame(moveBackground);
}

$(window).on('mousemove click', function (e) {

  var lMouseX = Math.max(-200, Math.min(50, $(window).width() / 2 - e.clientX));
  var lMouseY = Math.max(-200, Math.min(50, $(window).height() / 2 - e.clientY));
  lFollowX = (20 * lMouseX) / 50; // 100 : 12 = lMouxeX : lFollow
  lFollowY = (10 * lMouseY) / 50;

});

moveBackground();