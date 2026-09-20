/* =========================================================================
   Enviro Garden Care & Odd Jobs — site behaviour
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

     1. We never call stopPropagation() on the submit event, so the tracking
        script's own listener still receives it.
     2. We hold the redirect for CAPTURE_GRACE_MS so the tracking request has
        left the browser before the page unloads. Redirecting synchronously
        can cancel it in-flight and silently lose the lead.

     The tracking script is a plain (non-deferred) tag at the end of <body>
     and this file is deferred, so its listeners are always registered first.
     ----------------------------------------------------------------------- */
  var CAPTURE_GRACE_MS = 900;
  var THANK_YOU = '/thank-you/';

  /* -----------------------------------------------------------------------
     PROPERTY PHOTOS (Change Doc r20)

     The client wants customers to attach photos of the property. The GHL
     tracking script only reads text field values, so files need their own
     transport. Set UPLOAD_ENDPOINT to a URL that accepts multipart/form-data
     (a GHL inbound webhook, or any small upload handler) and the photo field
     appears. While it is empty the field stays hidden and the form shows a
     "text or email your photos" line instead — a visitor is never offered an
     upload that would silently go nowhere.

     Files are POSTed as multipart with the visitor's email and phone so they
     can be matched to the contact GHL creates from the tracked submission.
     ----------------------------------------------------------------------- */
  var UPLOAD_ENDPOINT = '';
  var UPLOAD_TIMEOUT_MS = 15000;

  var root = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ---------- Footer year ------------------------------------------------ */
  var year = $('#year');
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---------- Sticky header shadow --------------------------------------- */
  var header = $('#site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 12);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
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
  // Bound via the data-nav hook, not a URL — an href change must not be able to
  // silently unbind the dropdown (it did once, when .html was dropped from URLs).
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
    var desktop = function () { return window.matchMedia('(min-width: 981px)').matches; };
    servicesItem.addEventListener('mouseenter', function () {
      if (desktop()) showMega(true);
    });
    header.addEventListener('mouseleave', function () { showMega(false); });
    mega.addEventListener('mouseenter', function () { showMega(true); });
    mega.addEventListener('mouseleave', function () { showMega(false); });
    servicesLink.addEventListener('focus', function () { if (desktop()) showMega(true); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { mega.hidden = true; }
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

  /* ---------- Hero parallax ---------------------------------------------- */
  var heroBg = $('.hero__bg');
  if (heroBg && !reduceMotion && window.matchMedia('(min-width: 981px)').matches) {
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
  $$('img').forEach(function (img) {
    img.addEventListener('error', function () {
      img.style.background = 'linear-gradient(135deg,#1f6343,#2a8154)';
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
      if (!control || control.type === 'file') return;
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

  function setupPhotos(form) {
    var wrap = $('.field--file', form);
    var alt = $('.field--photos-alt', form);
    if (!wrap) return null;
    if (!UPLOAD_ENDPOINT) {
      wrap.hidden = true;
      if (alt) alt.hidden = false;
      return null;
    }
    wrap.hidden = false;
    if (alt) alt.hidden = true;

    var input = wrap.querySelector('input[type="file"]');
    var thumbs = wrap.querySelector('.field__thumbs');
    var maxFiles = parseInt(input.getAttribute('data-max-files') || '6', 10);
    var maxBytes = parseFloat(input.getAttribute('data-max-mb') || '8') * 1024 * 1024;

    input.addEventListener('change', function () {
      thumbs.innerHTML = '';
      var files = Array.prototype.slice.call(input.files || []);
      var problem = '';
      if (files.length > maxFiles) problem = 'Please attach up to ' + maxFiles + ' photos.';
      files.forEach(function (f) {
        if (f.size > maxBytes) problem = 'Each photo needs to be under ' + Math.round(maxBytes / 1048576) + ' MB.';
        if (f.type && f.type.indexOf('image/') !== 0) problem = 'Photos only, please (JPG, PNG or HEIC).';
      });
      setError(wrap, problem);
      if (problem) { input.value = ''; return; }
      files.forEach(function (f) {
        if (!window.URL || !URL.createObjectURL) return;
        var img = document.createElement('img');
        img.alt = '';
        img.src = URL.createObjectURL(f);
        img.onload = function () { URL.revokeObjectURL(img.src); };
        thumbs.appendChild(img);
      });
    });
    return input;
  }

  // Sends photos to UPLOAD_ENDPOINT. Resolves either way — a slow or failed
  // upload must never stop the visitor reaching the thank-you page, and the
  // text fields have already been captured by the tracking script.
  function uploadPhotos(form, input) {
    if (!input || !input.files || !input.files.length) return Promise.resolve();
    var fd = new FormData();
    fd.append('email', (form.email && form.email.value || '').trim());
    fd.append('phone', (form.phone && form.phone.value || '').trim());
    fd.append('full_name', (form.full_name && form.full_name.value || '').trim());
    fd.append('page_url', window.location.href);
    Array.prototype.forEach.call(input.files, function (f) { fd.append('property_photos[]', f, f.name); });
    return new Promise(function (resolve) {
      var done = false;
      var finish = function () { if (!done) { done = true; resolve(); } };
      window.setTimeout(finish, UPLOAD_TIMEOUT_MS);
      fetch(UPLOAD_ENDPOINT, { method: 'POST', body: fd, keepalive: true }).then(finish, finish);
    });
  }

  $$('.quote__form').forEach(function (form) {
    var photoInput = setupPhotos(form);

    // Honeypot — bots fill it, humans never see it.
    var pot = document.createElement('div');
    pot.setAttribute('aria-hidden', 'true');
    pot.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden';
    pot.innerHTML = '<label>Do not fill this in<input type="text" name="company_website" tabindex="-1" autocomplete="off"></label>';
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
      // Photos (if any, and if an endpoint is configured) go out in parallel;
      // the redirect waits for whichever finishes last.
      var grace = new Promise(function (r) { window.setTimeout(r, CAPTURE_GRACE_MS); });
      Promise.all([grace, uploadPhotos(form, photoInput)]).then(function () {
        goToThankYou(form);
      });
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
