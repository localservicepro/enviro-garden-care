/* =========================================================================
   Enviro Garden Care & Odd Jobs — site behaviour
   ========================================================================= */
(function () {
  'use strict';

  /* -----------------------------------------------------------------------
     LEAD CAPTURE

     The quote form POSTs JSON to /api/quote (Vercel function, api/quote.js),
     which upserts the contact in GoHighLevel and uploads the photos into the
     Job Photos custom field. Photos are resized here first: canvas, 1600px
     longest side, JPEG 0.82, max 6, ~3.2 MB total — Vercel caps bodies at
     4.5 MB, and the re-encode turns an iPhone HEIC into a JPEG GHL accepts.

     The GHL tracking script also listens for the submit event (attribution +
     a second capture of the text fields). Two things keep that working:
       1. never stopPropagation() on submit;
       2. the redirect waits for the API call and a short grace period, so
          nothing is cancelled by the unload.
     ----------------------------------------------------------------------- */
  var QUOTE_ENDPOINT = '/api/quote';
  var THANK_YOU = '/thank-you/';
  var CAPTURE_GRACE_MS = 900;
  var API_TIMEOUT_MS = 25000;
  var PHOTO = { maxFiles: 6, maxSide: 1600, quality: 0.82, totalBytes: 3.0 * 1024 * 1024, fileBytes: 1.4 * 1024 * 1024 };

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
    var target = THANK_YOU; // never the form action — that is the API
    window.setTimeout(function () { window.location.assign(target); }, delay || 0);
  }

  /* ---------- Photos: resize in the browser ------------------------------ */
  function setupPhotos(form) {
    var wrap = $('.field--file', form);
    if (!wrap) return null;
    var input = wrap.querySelector('input[type="file"]');
    var thumbs = wrap.querySelector('.field__thumbs');
    input._resized = [];

    input.addEventListener('change', function () {
      thumbs.innerHTML = '';
      input._resized = [];
      var files = Array.prototype.slice.call(input.files || []);
      if (files.length > PHOTO.maxFiles) {
        setError(wrap, 'Please attach up to ' + PHOTO.maxFiles + ' photos.');
        input.value = '';
        return;
      }
      var bad = files.filter(function (f) { return f.type && f.type.indexOf('image/') !== 0; });
      if (bad.length) {
        setError(wrap, 'Photos only, please (JPG, PNG or HEIC).');
        input.value = '';
        return;
      }
      setError(wrap, '');
      wrap.classList.add('is-busy');
      Promise.all(files.map(resizeImage)).then(function (results) {
        var total = 0;
        results.forEach(function (r) {
          if (!r) return;
          total += r.bytes;
          input._resized.push(r);
          var img = document.createElement('img');
          img.alt = '';
          img.src = r.dataUrl;
          thumbs.appendChild(img);
        });
        var skipped = results.filter(function (r) { return !r; }).length;
        if (skipped) setError(wrap, skipped + ' photo' + (skipped > 1 ? 's' : '') + ' could not be read and will not be sent.');
        if (total > PHOTO.totalBytes) {
          setError(wrap, 'Those photos are too large together — try fewer, or smaller ones.');
          input._resized = [];
          thumbs.innerHTML = '';
          input.value = '';
        }
      }).then(function () { wrap.classList.remove('is-busy'); });
    });
    return input;
  }

  // Draws the image onto a canvas at <= maxSide and re-encodes as JPEG. This
  // is what makes iPhone HEIC uploads work: the browser decodes HEIC, we send
  // JPEG. Steps quality down if a single photo is still over the per-file cap.
  function resizeImage(file) {
    return decodeImage(file).then(function (img) {
      var w = img.width, h = img.height;
      var scale = Math.min(1, PHOTO.maxSide / Math.max(w, h));
      var canvas = document.createElement('canvas');
      canvas.width = Math.max(1, Math.round(w * scale));
      canvas.height = Math.max(1, Math.round(h * scale));
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = '#fff';                 // PNG/GIF transparency -> white, not black
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      if (img.close) img.close();
      var q = PHOTO.quality;
      var dataUrl = canvas.toDataURL('image/jpeg', q);
      while (b64Bytes(dataUrl) > PHOTO.fileBytes && q > 0.5) {
        q -= 0.1;
        dataUrl = canvas.toDataURL('image/jpeg', q);
      }
      return { name: file.name, type: 'image/jpeg', dataUrl: dataUrl, bytes: b64Bytes(dataUrl) };
    }).catch(function () { return null; });
  }

  function decodeImage(file) {
    if (window.createImageBitmap) {
      // imageOrientation honours EXIF rotation so phone photos come out upright.
      return createImageBitmap(file, { imageOrientation: 'from-image' })
        .catch(function () { return createImageBitmap(file); })
        .catch(function () { return decodeViaImg(file); });
    }
    return decodeViaImg(file);
  }

  function decodeViaImg(file) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () { URL.revokeObjectURL(url); resolve(img); };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error('decode')); };
      img.src = url;
    });
  }

  function b64Bytes(dataUrl) {
    var i = dataUrl.indexOf(',');
    var len = dataUrl.length - i - 1;
    var pad = dataUrl.slice(-2) === '==' ? 2 : dataUrl.slice(-1) === '=' ? 1 : 0;
    return Math.floor(len * 3 / 4) - pad;
  }

  /* ---------- Submit ------------------------------------------------------ */
  function payloadOf(form, photoInput) {
    var data = {};
    $$('[name]', form).forEach(function (c) {
      if (c.type === 'file' || c.name === 'company_website') return; // honeypot handled before we get here
      data[c.name] = (c.value || '').trim();
    });
    data._t = Number(data._t) || 0;
    data.photos = (photoInput && photoInput._resized || []).map(function (r) {
      return { name: r.name, type: r.type, data: r.dataUrl };
    });
    data.page_url = window.location.href;
    return data;
  }

  function postQuote(data) {
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = ctrl && window.setTimeout(function () { ctrl.abort(); }, API_TIMEOUT_MS);
    return fetch(QUOTE_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      signal: ctrl ? ctrl.signal : undefined
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        return { status: r.status, body: j };
      });
    }).finally(function () { if (timer) window.clearTimeout(timer); });
  }

  $$('.quote__form').forEach(function (form) {
    var photoInput = setupPhotos(form);

    // Honeypot — visually hidden (not display:none), bots fill it, humans never see it.
    var pot = document.createElement('div');
    pot.setAttribute('aria-hidden', 'true');
    pot.style.cssText = 'position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden';
    pot.innerHTML = '<label>Do not fill this in<input type="text" name="company_website" tabindex="-1" autocomplete="off"></label>';
    form.appendChild(pot);

    // Minimum fill time — stamped when the page renders, checked server-side.
    var stamp = document.createElement('input');
    stamp.type = 'hidden';
    stamp.name = '_t';
    stamp.value = String(Date.now());
    form.appendChild(stamp);

    var errorBox = $('.quote__error', form);
    var button = form.querySelector('button[type="submit"]');

    function fail(message) {
      form.classList.remove('is-sending');
      if (button) button.classList.remove('is-sending');
      if (errorBox) { errorBox.textContent = message; errorBox.hidden = false; }
    }

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

      // Bots that fill the honeypot get the thank-you page and nothing else —
      // and the tracking script does not see the event either.
      var honey = form.querySelector('[name="company_website"]');
      if (honey && honey.value) {
        e.stopImmediatePropagation();
        goToThankYou(form);
        return;
      }

      if (button) button.classList.add('is-sending');
      form.classList.add('is-sending');

      // Tracker still receives this submit event (no stopPropagation). Wait
      // for the API and a grace period before navigating.
      var grace = new Promise(function (r) { window.setTimeout(r, CAPTURE_GRACE_MS); });
      var api = postQuote(payloadOf(form, photoInput));

      Promise.all([grace, api]).then(function (results) {
        var r = results[1];
        if (r.status >= 200 && r.status < 300 && r.body && r.body.ok) {
          goToThankYou(form);
        } else if (r.status === 400) {
          fail('Something in the form did not look right — please check your phone number and try again.');
        } else {
          fail('We could not send that just now. Please try again, or call ' + (form.querySelector('.quote__alt a') || {}).textContent + '.');
        }
      }).catch(function () {
        fail('We could not send that just now. Please try again, or call us.');
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
