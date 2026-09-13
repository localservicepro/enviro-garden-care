/* =========================================================================
   A1 Lawn Care Pty Ltd — site behaviour
   No dependencies. Everything degrades to a working page without JS.
   ========================================================================= */
(function () {
  'use strict';

  /* -----------------------------------------------------------------------
     LEAD CAPTURE

     Quote submissions are captured by the GoHighLevel external-tracking
     script, which listens for submit events on the page and reads the field
     values. Input names are the GHL contact fields exactly:

       full_name, email, phone, property_address,
       property_size, service_needed, job_notes

     Two things below exist to keep that capture working — do not "tidy" them
     away:

     1. We never call stopPropagation() on a real submit, so the tracking
        script's own listener still receives the event.
     2. We hold the redirect for CAPTURE_GRACE_MS so the tracking request has
        left the browser before the page unloads. Redirecting synchronously
        can cancel it in flight and silently lose the lead.

     The tracking script is a plain (non-deferred) tag at the end of <body>
     and this file is deferred, so its listeners are always registered first.
     ----------------------------------------------------------------------- */
  var CAPTURE_GRACE_MS = 900;
  var THANK_YOU = '/thank-you/';

  var root = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var desktop = function () { return window.matchMedia('(min-width: 981px)').matches; };

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) {
    return Array.prototype.slice.call((ctx || document).querySelectorAll(sel));
  }

  /* ---------- Footer year ------------------------------------------------ */
  var year = $('#year');
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---------- Sticky header, scroll progress, back to top ---------------- */
  var header = $('#site-header');
  var bar = $('#scrollbar');
  var toTop = $('#totop');

  var onScroll = function () {
    var y = window.scrollY;
    if (header) header.classList.toggle('is-stuck', y > 12);
    if (toTop) toTop.classList.toggle('is-on', y > 700);
    if (bar) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
    }
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });

  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }

  /* ---------- Mobile navigation ------------------------------------------ */
  var burger = $('#burger');
  var nav = $('#nav');
  if (burger && nav) {
    var setNav = function (open) {
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('nav-open', open);
    };
    burger.addEventListener('click', function () {
      setNav(burger.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setNav(false);
    });
    document.addEventListener('click', function (e) {
      if (!document.body.classList.contains('nav-open')) return;
      if (e.target.closest('#nav') || e.target.closest('#burger')) return;
      setNav(false);
    });
  }

  /* ---------- Services megamenu (desktop) -------------------------------- */
  // Bound via the data-nav hook, not a URL — changing the nav href must not be
  // able to silently unbind the dropdown.
  var mega = $('#megamenu');
  var servicesItem = $('[data-nav="services"]');
  var servicesLink = servicesItem && servicesItem.querySelector('a');
  if (mega && servicesItem && servicesLink && header) {
    var megaTimer = null;
    var showMega = function (show) {
      window.clearTimeout(megaTimer);
      if (show) {
        mega.hidden = false;
      } else {
        megaTimer = window.setTimeout(function () { mega.hidden = true; }, 180);
      }
    };
    servicesItem.addEventListener('mouseenter', function () {
      if (desktop()) showMega(true);
    });
    header.addEventListener('mouseleave', function () { showMega(false); });
    mega.addEventListener('mouseenter', function () { showMega(true); });
    mega.addEventListener('mouseleave', function () { showMega(false); });
    servicesLink.addEventListener('focus', function () { if (desktop()) showMega(true); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') mega.hidden = true;
    });
  }

  /* ---------- Scroll reveal ---------------------------------------------- */
  var revealables = $$('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Counting stats --------------------------------------------- */
  var counters = $$('.count');
  if (counters.length) {
    var run = function (el) {
      // The final number is already in the HTML, so a visitor without JS (and
      // any crawler) sees the real figure. JS only animates up to it.
      var target = parseInt(el.getAttribute('data-count'), 10);
      if (isNaN(target)) return;
      if (reduceMotion) { el.textContent = String(target); return; }
      el.textContent = '0';
      var start = null;
      var DURATION = 1200;
      var tick = function (now) {
        if (start === null) start = now;
        var p = Math.min((now - start) / DURATION, 1);
        // ease-out so the number settles rather than stopping dead
        el.textContent = String(Math.round(target * (1 - Math.pow(1 - p, 3))));
        if (p < 1) window.requestAnimationFrame(tick);
      };
      window.requestAnimationFrame(tick);
    };
    if (!('IntersectionObserver' in window)) {
      counters.forEach(run);
    } else {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          run(entry.target);
          cio.unobserve(entry.target);
        });
      }, { threshold: 0.6 });
      counters.forEach(function (el) { cio.observe(el); });
    }
  }

  /* ---------- Hero parallax ---------------------------------------------- */
  var heroBg = $('.hero__bg');
  if (heroBg && !reduceMotion && desktop()) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        var y = Math.min(window.scrollY, 700);
        heroBg.style.transform = 'translate3d(0,' + (y * 0.16) + 'px,0)';
        ticking = false;
      });
    }, { passive: true });
  }

  /* ---------- Broken image guard ----------------------------------------- */
  // Photography is served from the client's Google Drive folder. If a file is
  // moved or unshared, show the brand gradient rather than a broken icon.
  $$('img').forEach(function (img) {
    img.addEventListener('error', function () {
      img.style.background = 'linear-gradient(135deg,#14472a,#63b32a)';
      img.style.minHeight = '160px';
      img.removeAttribute('src');
    }, { once: true });
  });

  /* ---------- Quote forms ------------------------------------------------ */
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var PHONE_RE = /^[0-9+()\s-]{8,}$/;

  function setError(field, message) {
    var control = field.querySelector('input,select,textarea');
    var msg = field.querySelector('.field__msg');
    if (message) {
      control.setAttribute('aria-invalid', 'true');
      if (!msg) {
        msg = document.createElement('span');
        msg.className = 'field__msg';
        field.appendChild(msg);
      }
      msg.textContent = message;
    } else {
      control.removeAttribute('aria-invalid');
      if (msg) msg.remove();
    }
  }

  function validate(form) {
    var firstBad = null;
    $$('.field', form).forEach(function (field) {
      var control = field.querySelector('input,select,textarea');
      if (!control) return;
      var value = (control.value || '').trim();
      var label = (field.querySelector('label') || {}).textContent || 'This field';
      label = label.replace('*', '').trim();
      var error = '';

      if (control.hasAttribute('required') && !value) {
        error = label + ' is required.';
      } else if (value && control.type === 'email' && !EMAIL_RE.test(value)) {
        error = 'Please enter a valid email address.';
      } else if (value && control.type === 'tel' && !PHONE_RE.test(value)) {
        error = 'Please enter a valid phone number.';
      }

      setError(field, error);
      if (error && !firstBad) firstBad = control;
    });
    return firstBad;
  }

  function goToThankYou(form, delay) {
    var target = form.getAttribute('action') || THANK_YOU;
    window.setTimeout(function () { window.location.assign(target); }, delay || 0);
  }

  $$('.quote__form').forEach(function (form) {
    // Honeypot — bots fill it, humans never see it.
    var pot = document.createElement('div');
    pot.setAttribute('aria-hidden', 'true');
    pot.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden';
    pot.innerHTML = '<label>Do not fill this in' +
      '<input type="text" name="company_website" tabindex="-1" autocomplete="off"></label>';
    form.appendChild(pot);

    var errorBox = $('.quote__error', form);

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      if (form.classList.contains('is-sending')) return;
      if (errorBox) { errorBox.hidden = true; errorBox.textContent = ''; }

      var firstBad = validate(form);
      if (firstBad) {
        firstBad.focus();
        firstBad.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
        return;
      }

      // Bots that fill the honeypot get the thank-you page and nothing else:
      // bail out before the tracking script can log a junk contact.
      var honey = form.querySelector('[name="company_website"]');
      if (honey && honey.value) {
        e.stopImmediatePropagation();
        goToThankYou(form);
        return;
      }

      var button = form.querySelector('button[type="submit"]');
      if (button) button.classList.add('is-sending');
      form.classList.add('is-sending');

      // The GHL tracking script reads the submit event after this handler.
      // Hold the redirect so its request is not cancelled by the unload.
      goToThankYou(form, CAPTURE_GRACE_MS);
    });

    // Clear a field's error as soon as the visitor starts fixing it.
    form.addEventListener('input', function (e) {
      var field = e.target.closest('.field');
      if (field && field.querySelector('.field__msg')) setError(field, '');
    });
  });

  /* ---------- Smooth in-page links --------------------------------------- */
  $$('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      var id = link.getAttribute('href');
      if (!id || id === '#') return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
      window.history.replaceState(null, '', id);
    });
  });

  root.classList.add('js-ready');
}());
