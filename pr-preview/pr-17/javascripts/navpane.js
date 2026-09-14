// Auto-expand the left navigation pane up to level 2 on wide screens.
function load_navpane() {
  if (window.innerWidth <= 1200) return;

  var nav = document.getElementsByClassName("md-nav__toggle");
  for (var i = 0; i < nav.length; i++) {
    if ((nav.item(i).id.match(/_\d/g) || []).length > 2) continue;
    nav.item(i).checked = true;
  }
}

document.addEventListener("DOMContentLoaded", load_navpane);

document.addEventListener("DOMContentLoaded", function () {
  var title = document.querySelector(".md-header__title");
  if (title) {
    title.addEventListener("click", function () {
      window.location.href = "/";
    });
  }
});
