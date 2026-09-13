/* =========================================================================
   Enviro Garden Care & Odd Jobs — site behaviour
   ========================================================================= */
(function () {
  'use strict';

  /* -----------------------------------------------------------------------
     CONFIG — set this before launch.

     LEAD_ENDPOINT is where quote form submissions are POSTed. Use the
     GoHighLevel inbound webhook URL for the "Website Quote Request" workflow
     (GHL → Automation → Workflows → Inbound Webhook → copy URL).

     Field names posted match the GHL contact fields exactly:
       full_name, email, phone, property_address,
       property_size, service_needed, job_notes

     While this is an empty string the form still validates and still sends
     the visitor to thank-you.html, but nothing is transmitted — so set it.
     ----------------------------------------------------------------------- */
  var LEAD_ENDPOINT = '';
  var THANK_YOU = 'thank-you.html';

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
  var mega = $('#megamenu');
  var servicesLink = $('.nav__list a[href$="services.html"]');
  if (mega && servicesLink && header) {
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
    servicesLink.parentElement.addEventListener('mouseenter', function () {
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

  function payloadOf(form) {
    var data = {};
    $$('[name]', form).forEach(function (control) {
      data[control.name] = (control.value || '').trim();
    });
    data.page_url = window.location.href;
    data.page_title = document.title;
    data.submitted_at = new Date().toISOString();
    return data;
  }

  function goToThankYou(form) {
    var target = form.getAttribute('action') || THANK_YOU;
    window.location.assign(target);
  }

  $$('.quote__form').forEach(function (form) {
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

      // Silently drop bot submissions.
      var honey = form.querySelector('[name="company_website"]');
      if (honey && honey.value) { goToThankYou(form); return; }

      var button = form.querySelector('button[type="submit"]');
      if (button) button.classList.add('is-sending');
      form.classList.add('is-sending');

      var data = payloadOf(form);
      delete data.company_website;

      if (!LEAD_ENDPOINT) {
        // Not wired up yet — still complete the visitor journey.
        goToThankYou(form);
        return;
      }

      var done = false;
      var finish = function () {
        if (done) return;
        done = true;
        goToThankYou(form);
      };
      // Never strand the visitor if the endpoint is slow or unreachable.
      window.setTimeout(finish, 6000);

      fetch(LEAD_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(finish).catch(finish);
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
