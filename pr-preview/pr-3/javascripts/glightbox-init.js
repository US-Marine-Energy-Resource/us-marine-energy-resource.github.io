// Re-initialize GLightbox and intercept clicks via capture-phase delegation.
// Using capture phase (addEventListener 3rd arg = true) ensures we fire before
// any link navigation handler (Material or browser default) can take over.
(function () {
  var OPTS = {
    touchNavigation: true,
    loop: false,
    openEffect: "zoom",
    closeEffect: "zoom",
    slideEffect: "slide",
    zoomable: true,
    draggable: true,
    descPosition: "bottom",
  };

  var lb = null;

  // Copy figcaption text into data-description on each .glightbox anchor
  // so GLightbox can display it below the image.
  function attachCaptions() {
    document.querySelectorAll("figure").forEach(function (fig, i) {
      var anchor = fig.querySelector("a.glightbox");
      var caption = fig.querySelector("figcaption");
      if (!anchor || !caption) return;
      anchor.setAttribute(
        "data-description",
        "Figure " + (i + 1) + ": " + caption.textContent.trim()
      );
    });
  }

  function init() {
    if (typeof GLightbox !== "undefined") {
      attachCaptions();
      lb = GLightbox(OPTS);
    }
  }

  // Capture-phase delegated click: intercepts before the <a href> navigates
  document.addEventListener(
    "click",
    function (e) {
      var target = e.target.closest("a.glightbox");
      if (!target || !lb) return;
      e.preventDefault();
      e.stopPropagation();
      var els = Array.from(document.querySelectorAll("a.glightbox"));
      var idx = els.indexOf(target);
      if (idx >= 0) lb.openAt(idx);
    },
    true // capture phase
  );

  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
