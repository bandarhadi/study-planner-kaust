(function () {
  'use strict';
  var P = window.PLANNER;
  var KEY = 'study-planner:v1';
  var ICONS = {
    '/icons/bell-notification_yellow.svg': '🔔',
    '/icons/arrows-swap-vertically_green.svg': '↕️',
    '/icons/aquarius_blue.svg': '♒',
    '/icons/bookmark_brown.svg': '🔖'
  };
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  /* ---------- state (localStorage) ---------- */
  // done: { originalTaskBlockId: true }   personal: { dayBlockId: [{id, text, done}] }
  var state = load();
  function load() {
    try {
      var s = JSON.parse(localStorage.getItem(KEY) || '{}');
      return { done: s.done || {}, personal: s.personal || {} };
    } catch (e) { return { done: {}, personal: {} }; }
  }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* storage full or blocked */ }
  }

  /* ---------- helpers ---------- */
  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === 'class') n.className = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else n.setAttribute(k, attrs[k]);
    }
    (kids || []).forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }
  function dateOf(week, day) {
    var p = week.start.split('-').map(Number);
    return new Date(p[0], p[1] - 1, p[2] + day.dayIndex);
  }
  function sameDay(a, b) { return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate(); }
  function days(week) {
    var out = [];
    week.columns.forEach(function (col) { col.forEach(function (it) { if (it.kind === 'day') out.push(it); }); });
    return out;
  }
  function originals(week) {
    var out = [];
    days(week).forEach(function (d) { out = out.concat(d.todos); });
    return out;
  }
  var ALL = [];
  P.weeks.forEach(function (w) { ALL = ALL.concat(originals(w)); });
  function countDone(list) { return list.filter(function (t) { return state.done[t.id]; }).length; }
  function personalCounts() {
    var a = 0, b = 0;
    Object.keys(state.personal).forEach(function (k) {
      state.personal[k].forEach(function (t) { a++; if (t.done) b++; });
    });
    return [b, a];
  }
  function currentWeekId() {
    var now = new Date(); now.setHours(0, 0, 0, 0);
    var id = null;
    P.weeks.forEach(function (w) {
      var s = dateOf(w, { dayIndex: 0 }), e = dateOf(w, { dayIndex: 6 });
      if (now >= s && now <= e) id = w.id;
    });
    return id;
  }

  /* ---------- render ---------- */
  var app = document.getElementById('app');
  var adding = null; // dayId currently showing the add field

  function render() {
    var y = window.scrollY;
    app.textContent = '';
    var today = new Date();
    var done = countDone(ALL), total = ALL.length, pct = total ? Math.round(done / total * 100) : 0;
    var pc = personalCounts();
    var cw = currentWeekId();

    app.appendChild(el('h1', { text: P.title }));
    app.appendChild(el('div', { class: 'range' }, [el('span', { text: P.quote })]));

    var bar = el('div', { class: 'bar' }, [el('i', { style: 'width:' + pct + '%' })]);
    var num = el('div', { class: 'num' });
    num.appendChild(document.createTextNode(done + ' / ' + total + ' '));
    num.appendChild(el('small', { text: '(' + pct + '%)' }));
    app.appendChild(el('section', { class: 'overall', 'aria-label': 'Overall progress' }, [
      el('div', { class: 'row' }, [el('span', { class: 'olabel', text: 'Overall progress' }), num]),
      bar,
      pc[1] ? el('div', { class: 'extra', text: 'Personal tasks: ' + pc[0] + ' / ' + pc[1] + ' done' }) : null
    ]));

    var jump = el('nav', { class: 'jump', 'aria-label': 'Weeks' });
    P.weeks.forEach(function (w, i) {
      var p = originals(w);
      jump.appendChild(el('a', { href: '#w' + (i + 1), class: w.id === cw ? 'now' : '', text: 'Week 0' + (i + 1) + ' · ' + countDone(p) + '/' + p.length }));
    });
    app.appendChild(jump);

    P.weeks.forEach(function (w, i) {
      var list = originals(w), wd = countDone(list);
      var sec = el('section', { class: 'week', id: 'w' + (i + 1), 'data-week': w.id });
      sec.appendChild(el('div', { class: 'week-head' }, [
        el('h2', { text: w.title }),
        el('span', { class: 'wprog', text: wd + ' / ' + list.length })
      ]));
      sec.appendChild(el('hr'));
      sec.appendChild(el('div', { class: 'bar' }, [el('i', { style: 'width:' + Math.round(wd / list.length * 100) + '%' })]));
      var cols = el('div', { class: 'cols' });
      w.columns.forEach(function (col) {
        var c = el('div', { class: 'col' });
        col.forEach(function (it) {
          if (it.kind === 'day') c.appendChild(renderDay(w, it, today));
          else if (it.kind === 'callout') c.appendChild(el('div', { class: 'callout' }, [
            el('span', { class: 'ic', 'aria-hidden': 'true', text: ICONS[it.icon] || '•' }),
            el('b', { text: it.text })
          ]));
        });
        if (c.childNodes.length) cols.appendChild(c);
      });
      sec.appendChild(cols);
      app.appendChild(sec);
    });
    app.appendChild(el('p', { class: 'foot', text: 'Progress is saved on this device.' }));
    window.scrollTo(0, y);
    if (adding) { var inp = document.getElementById('add-input'); if (inp) inp.focus(); }
  }

  function renderDay(w, d, today) {
    var dt = dateOf(w, d), isToday = sameDay(dt, today);
    var box = el('div', { class: 'day' + (isToday ? ' today' : ''), 'data-day': d.id });
    box.appendChild(el('span', { class: 'label', style: 'background:var(--' + d.color + ')', text: d.label }));
    var meta = el('div', { class: 'daymeta' }, [
      el('span', { class: 'date', text: (isToday ? 'Today · ' : '') + dt.getDate() + ' ' + MON[dt.getMonth()] }),
      el('button', { class: 'add', type: 'button', 'data-act': 'add', 'data-day': d.id, text: '+ ' + d.button })
    ]);
    box.appendChild(meta);

    d.todos.forEach(function (t) {
      var txt = el('span', { class: 't', 'data-id': t.id });
      t.segments.forEach(function (s) {
        if (s[1] && s[1].length) txt.appendChild(el('span', { class: 'hl-' + s[1][0], text: s[0] }));
        else txt.appendChild(document.createTextNode(s[0]));
      });
      var cb = el('input', { type: 'checkbox', 'data-act': 'toggle', 'data-id': t.id, 'aria-label': 'Mark as done' });
      cb.checked = !!state.done[t.id];
      box.appendChild(el('label', { class: 'task' + (cb.checked ? ' done' : '') }, [cb, txt]));
    });

    (state.personal[d.id] || []).forEach(function (t) {
      var cb = el('input', { type: 'checkbox', 'data-act': 'ptoggle', 'data-day': d.id, 'data-id': t.id, 'aria-label': 'Mark as done' });
      cb.checked = !!t.done;
      var txt = el('span', { class: 't' }, [document.createTextNode(t.text), el('span', { class: 'tag', text: 'personal' })]);
      box.appendChild(el('div', { class: 'task mine' + (t.done ? ' done' : '') }, [
        el('label', { style: 'display:flex;gap:12px;flex:1;min-width:0;align-items:flex-start;cursor:pointer' }, [cb, txt]),
        el('button', { class: 'del', type: 'button', 'data-act': 'pdel', 'data-day': d.id, 'data-id': t.id, 'aria-label': 'Delete personal task', text: '×' })
      ]));
    });

    if (adding === d.id) {
      box.appendChild(el('form', { class: 'addrow', 'data-day': d.id }, [
        el('input', { id: 'add-input', type: 'text', placeholder: 'New personal task', autocomplete: 'off', enterkeyhint: 'done', maxlength: '200' }),
        el('button', { type: 'submit', text: 'Add' }),
        el('button', { type: 'button', class: 'cancel', 'data-act': 'cancel', text: 'Cancel' })
      ]));
    }
    return box;
  }

  /* ---------- events ---------- */
  app.addEventListener('change', function (e) {
    var t = e.target, act = t.getAttribute('data-act');
    if (act === 'toggle') {
      if (t.checked) state.done[t.getAttribute('data-id')] = true;
      else delete state.done[t.getAttribute('data-id')];
      save(); render();
    } else if (act === 'ptoggle') {
      (state.personal[t.getAttribute('data-day')] || []).forEach(function (p) {
        if (p.id === t.getAttribute('data-id')) p.done = t.checked;
      });
      save(); render();
    }
  });
  app.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-act]');
    if (!b) return;
    var act = b.getAttribute('data-act');
    if (act === 'add') { adding = b.getAttribute('data-day'); render(); }
    else if (act === 'cancel') { adding = null; render(); }
    else if (act === 'pdel') {
      var day = b.getAttribute('data-day'), id = b.getAttribute('data-id');
      state.personal[day] = (state.personal[day] || []).filter(function (p) { return p.id !== id; });
      if (!state.personal[day].length) delete state.personal[day];
      save(); render();
    }
  });
  app.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = e.target, day = f.getAttribute('data-day');
    var v = f.querySelector('input').value;
    if (v.trim()) {
      (state.personal[day] = state.personal[day] || []).push({ id: 'p' + Date.now().toString(36), text: v, done: false });
      save();
    }
    adding = null; render();
  });
  app.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && adding) { adding = null; render(); }
  });
  // other open tabs / app instances stay in sync
  window.addEventListener('storage', function (e) { if (e.key === KEY) { state = load(); render(); } });

  render();
  // on first open, jump to the current week
  var cw = currentWeekId();
  if (cw && !location.hash) {
    var s = document.querySelector('[data-week="' + cw + '"]');
    if (s && window.scrollY === 0) s.scrollIntoView();
  }

  /* ---------- offline ---------- */
  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
  }
})();
