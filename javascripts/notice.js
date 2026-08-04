/**
 * Site notice: modal (once per session).
 *
 * Suppressed for the remainder of the browser session once dismissed.
 */

(function () {
  var MODAL_KEY = 'site-notice-modal-dismissed';

  var GITHUB_URL     = 'https://github.com/US-Marine-Energy-Resource/us-marine-energy-resource.github.io';
  var FEEDBACK_EMAIL = 'marineresource@nlr.gov';

  function createModal() {
    if (sessionStorage.getItem(MODAL_KEY)) return;

    var overlay = document.createElement('div');
    overlay.className = 'site-notice-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'site-notice-title');

    overlay.innerHTML =
      '<div class="site-notice-modal">' +
        '<h2 id="site-notice-title" class="site-notice-modal__title">Site Under Active Development</h2>' +
        '<div class="site-notice-modal__body">' +
          '<p>This site is a work in progress. Content, data, and structure may change as resources are added and refined.</p>' +
          '<p>Contributions are welcome via <a href="' + GITHUB_URL + '" target="_blank" rel="noopener">GitHub</a>, whether that\'s data corrections, additional resources, or documentation improvements.</p>' +
          '<p>Questions and feedback can be sent to <a href="mailto:' + FEEDBACK_EMAIL + '">' + FEEDBACK_EMAIL + '</a>.</p>' +
        '</div>' +
        '<div class="site-notice-modal__footer">' +
          '<button class="site-notice-modal__btn" id="site-notice-dismiss">Understood</button>' +
        '</div>' +
      '</div>';

    function dismiss() {
      sessionStorage.setItem(MODAL_KEY, '1');
      overlay.classList.add('site-notice-overlay--hidden');
      document.body.style.overflow = '';
    }

    overlay.querySelector('#site-notice-dismiss').addEventListener('click', dismiss);

    /* Also dismiss on overlay click (outside the card) */
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) dismiss();
    });

    /* Dismiss on Escape */
    document.addEventListener('keydown', function handler(e) {
      if (e.key === 'Escape') {
        dismiss();
        document.removeEventListener('keydown', handler);
      }
    });

    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';

    /* Focus the dismiss button for keyboard users */
    var btn = overlay.querySelector('#site-notice-dismiss');
    btn.focus();
  }

  /* ------------------------------------------------------------------ */
  /* Init                                                                 */
  /* ------------------------------------------------------------------ */

  document.addEventListener('DOMContentLoaded', function () {
    createModal();
  });
})();

