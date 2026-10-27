// Freeday scroll tour: pins the phone, swaps its screen as each step reaches the middle of the view,
// and lets Freeday's sunrise rise with progress. First-party, no tracking, nothing stored.
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  // The pinned phone sits just under the header, whose height changes when the menu wraps on small screens.
  var header = document.querySelector('.site-header');
  function headerHeight() { if (header) root.style.setProperty('--header-h', header.offsetHeight + 'px'); }
  headerHeight();
  window.addEventListener('resize', headerHeight);
  var tour = document.querySelector('.tour');
  if (!tour || !('IntersectionObserver' in window)) return;

  var steps = [].slice.call(tour.querySelectorAll('.tour-step'));
  var screens = [].slice.call(tour.querySelectorAll('.tour-screen'));
  var buttons = [].slice.call(tour.querySelectorAll('.tour-rail button'));
  var body = tour.querySelector('.tour-body');
  var wide = window.matchMedia('(min-width: 900px)');
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');
  var active = 0, observer = null, ticking = false;

  // Captions pinned with the phone on smaller screens: copies of the steps, hidden from screen readers
  // (which read the steps themselves).
  var caps = document.createElement('div');
  caps.className = 'tour-caps';
  caps.setAttribute('aria-hidden', 'true');
  steps.forEach(function (s, k) {
    var cap = document.createElement('div');
    cap.className = 'tour-cap' + (k === 0 ? ' is-active' : '');
    cap.innerHTML = s.innerHTML;
    caps.appendChild(cap);
  });
  tour.querySelector('.tour-stage').appendChild(caps);
  var capItems = [].slice.call(caps.children);

  function setActive(i) {
    if (i === active) return;
    active = i;
    screens.forEach(function (s, k) { s.classList.toggle('is-active', k === i); s.classList.toggle('is-before', k < i); });
    steps.forEach(function (s, k) { s.classList.toggle('is-active', k === i); });
    capItems.forEach(function (c, k) { c.classList.toggle('is-active', k === i); });
    buttons.forEach(function (b, k) { if (k === i) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current'); });
  }

  function observe() {
    if (observer) observer.disconnect();
    // A thin band across the middle of the view: the step crossing it is the one shown.
    observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) setActive(Number(e.target.getAttribute('data-step'))); });
    }, { rootMargin: '-48% 0px -48% 0px' });
    steps.forEach(function (s) { observer.observe(s); });
  }

  function rise() {
    ticking = false;
    var r = body.getBoundingClientRect();
    var travel = Math.max(1, r.height - window.innerHeight);
    var p = Math.min(1, Math.max(0, -r.top / travel));
    tour.style.setProperty('--rise', p.toFixed(3));
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      var step = steps[Number(b.getAttribute('data-goto'))];
      var y = step.getBoundingClientRect().top + window.scrollY - (window.innerHeight - step.offsetHeight) / 2;
      window.scrollTo({ top: y + 2, behavior: calm.matches ? 'auto' : 'smooth' });
    });
  });

  observe();
  (wide.addEventListener ? wide.addEventListener('change', observe) : wide.addListener(observe));
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(rise); } }, { passive: true });
  window.addEventListener('resize', rise);
  rise();
})();
