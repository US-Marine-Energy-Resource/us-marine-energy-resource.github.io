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
  var citeObserver = null;

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

  // Re-attach captions and reload GLightbox element data once cite.js has
  // finished rendering inline citations (signalled by the "cite-ready" class
  // being added to document.body).  This ensures the lightbox caption shows
  // the rendered citation number (e.g. "[1]") rather than the raw [@key].
  function watchForCiteReady() {
    if (citeObserver) citeObserver.disconnect();
    if (document.body.classList.contains("cite-ready")) {
      attachCaptions();
      if (lb) lb.reload();
      return;
    }
    citeObserver = new MutationObserver(function (mutations) {
      for (var i = 0; i < mutations.length; i++) {
        if (document.body.classList.contains("cite-ready")) {
          citeObserver.disconnect();
          citeObserver = null;
          attachCaptions();
          if (lb) lb.reload();
          return;
        }
      }
    });
    citeObserver.observe(document.body, { attributes: true, attributeFilter: ["class"] });
  }

  function init() {
    if (typeof GLightbox !== "undefined") {
      attachCaptions();
      lb = GLightbox(OPTS);
      watchForCiteReady();
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
