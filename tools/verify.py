import json,subprocess,time,sys,os
from playwright.sync_api import sync_playwright
ROOT='/home/claude/study-planner'
C=json.load(open(ROOT+'/content-backup/content.json',encoding='utf-8'))
exp_todos=[];exp_days=[];exp_callouts=[];exp_weeks=[]
DN=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
for w in C['weeks']:
    exp_weeks.append(w['title'])
    wd=[]
    for c in w['columns']:
        for i in c['items']:
            if i['kind']=='day': wd.append(i)
            if i['kind']=='callout': exp_callouts.append(i['text'])
    wd.sort(key=lambda i: next(k for k,n in enumerate(DN) if n in i['label']))  # date order
    for i in wd:
        exp_days.append((i['block_id'],i['label']))
        exp_todos+= [(t['block_id'],t['text']) for t in i['todos']]
srv=subprocess.Popen([sys.executable,'-m','http.server','8765','--bind','127.0.0.1'],cwd='/home/claude/study-planner-kaust',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(1)
R=[]
def ok(name,cond,info=''): R.append((name,bool(cond),info)); print(('PASS ' if cond else 'FAIL ')+name,info)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True,
      user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1')
    pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8765/'); pg.wait_for_selector('.task')
    # content
    ids=pg.eval_on_selector_all('span.t[data-id]','els=>els.map(e=>[e.dataset.id,e.textContent])')
    ok('57 original tasks rendered',len(ids)==57,str(len(ids)))
    ok('57 checkboxes',pg.locator('input[data-act=toggle]').count()==57)
    ok('task text exact + order matches content.json',[tuple(x) for x in ids]==exp_todos)
    bad=[(a,b2) for (a,b2),(c,d) in zip(ids,exp_todos) if b2!=d]; 
    if bad: print(bad[:3])
    days=pg.eval_on_selector_all('.day','els=>els.map(e=>[e.dataset.day,e.querySelector(".label").textContent])')
    ok('35 day labels exact + in date order',[tuple(x) for x in days]==exp_days,str(len(days)))
    ok('week titles exact + order',pg.eval_on_selector_all('.week h2','e=>e.map(x=>x.textContent)')==exp_weeks)
    ok('callout texts exact',pg.eval_on_selector_all('.callout b','e=>e.map(x=>x.textContent)')==exp_callouts,str(len(exp_callouts)))
    ok('title + date range',pg.text_content('h1')=='STUDY PLANNER.' and pg.text_content('.range span')==C['header_quote']['text'])
    ok('red highlights',pg.eval_on_selector_all('.hl-red','e=>e.map(x=>x.textContent)')==['this day is the deadline','The date of the EXAM'])
    ok('Arabic is default (lang=ar, dir=rtl)',pg.evaluate('document.documentElement.lang+document.documentElement.dir')=='arrtl')
    ok('Arabic UI text shown',pg.text_content('.olabel')=='الإنجاز الكلي' and pg.text_content('button.add')=='+ إضافة مهمة')
    ok('Arabic font loaded',pg.evaluate("document.fonts.ready.then(()=>document.fonts.check('16px \"Plex Arabic\"','عربي'))") and pg.evaluate("[...document.fonts].some(f=>f.family.includes('Plex Arabic')&&f.status==='loaded')"))
    ok('original tasks stay LTR in Arabic mode',pg.eval_on_selector('.task.orig','e=>getComputedStyle(e).direction')=='ltr' and pg.eval_on_selector('.label','e=>getComputedStyle(e).direction')=='ltr')
    dates=pg.eval_on_selector_all('.day','els=>els.map(e=>e.dataset.day)')
    ok('days strictly chronological across all weeks',[d for d,_ in exp_days]==dates)
    ok('Arabic day names next to dates',pg.text_content('.day .date').split(' ')[0] in ['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت','اليوم'])
    pg.click('button.lang')
    ok('switch to English',pg.evaluate('document.documentElement.lang')=='en' and pg.text_content('.olabel')=='Overall progress')
    ok('button labels "Add Task " (English)',set(pg.eval_on_selector_all('button.add','e=>e.map(x=>x.textContent)'))=={'+ Add Task '})
    ids2=pg.eval_on_selector_all('span.t[data-id]','els=>els.map(e=>[e.dataset.id,e.textContent])')
    ok('content identical in both languages',[tuple(x) for x in ids2]==exp_todos)
    pg.click('button.lang'); pg.reload(); pg.wait_for_selector('.task')
    ok('language choice saved after refresh',pg.evaluate('document.documentElement.lang')=='ar')
    ok('label whitespace preserved visually',pg.eval_on_selector('.label','e=>getComputedStyle(e).whiteSpace')=='pre')
    ok('task text whitespace preserved visually',pg.eval_on_selector('span.t','e=>getComputedStyle(e).whiteSpace')=='pre-wrap')
    ok('progress starts 0 / 57',pg.text_content('.overall .num').startswith('0 / 57'))
    # interactions
    pg.locator('span.t[data-id="'+exp_todos[0][0]+'"]').click()
    pg.locator('span.t[data-id="'+exp_todos[10][0]+'"]').click()
    pg.locator('span.t[data-id="'+exp_todos[56][0]+'"]').click()
    pg.locator('span.t[data-id="'+exp_todos[10][0]+'"]').click()  # uncheck
    ok('check/uncheck updates progress',pg.text_content('.overall .num').startswith('2 / 57'),pg.text_content('.overall .num'))
    ok('done style applied',pg.locator('.task.done').count()==2)
    pg.click('button.add >> nth=2'); pg.fill('#add-input','  my own  task '); pg.keyboard.press('Enter')
    ok('personal task added',pg.locator('.task.mine').count()==1)
    pg.reload(); pg.wait_for_selector('.task')
    ok('progress saved after refresh',pg.text_content('.overall .num').startswith('2 / 57') and pg.locator('input[data-act=toggle]:checked').count()==2)
    ok('personal task saved after refresh, text kept as typed',pg.locator('.task.mine .t').evaluate('e=>e.firstChild.textContent')=='  my own  task ')
    ok('originals untouched by personal task',pg.locator('span.t[data-id]').count()==57)
    ok('weekly progress W1 1/12, W5 1/7',pg.text_content('#w1 .wprog')=='1 / 12' and pg.text_content('#w5 .wprog')=='1 / 7')
    pg.locator('.task.mine .del').click(); ok('personal task delete',pg.locator('.task.mine').count()==0)
    # mobile layout
    ok('no horizontal overflow at 390px',pg.evaluate('document.documentElement.scrollWidth')<=390,str(pg.evaluate('document.documentElement.scrollWidth')))
    ok('tap targets >= 44px',pg.eval_on_selector('.task','e=>e.getBoundingClientRect().height')>=44)
    pg.evaluate('window.scrollTo(0,0)'); pg.screenshot(path='/tmp/m1.png'); pg.click('button.add >> nth=0'); pg.fill('#add-input','مراجعة الملخص'); pg.keyboard.press('Enter'); pg.locator('#w1').scroll_into_view_if_needed(); pg.screenshot(path='/tmp/m5.png'); pg.locator('.task.mine .del').click()
    pg.locator('#w2').scroll_into_view_if_needed(); pg.screenshot(path='/tmp/m2.png')
    # PWA
    m=pg.evaluate('fetch("manifest.webmanifest").then(r=>r.json())')
    ok('manifest standalone + icons 192/512 + maskable',m['display']=='standalone' and {i['sizes'] for i in m['icons']}>={'192x192','512x512'} and any(i.get('purpose')=='maskable' for i in m['icons']))
    icons_ok=all(pg.evaluate(f'fetch("{u}").then(r=>r.ok)') for u in ['icons/icon-192.png','icons/icon-512.png','icons/icon-maskable-512.png','icons/apple-touch-icon.png'])
    ok('all icons load',icons_ok)
    ok('iOS meta tags',pg.locator('meta[name=apple-mobile-web-app-capable][content=yes]').count()==1 and pg.locator('link[rel=apple-touch-icon]').count()==1)
    pg.wait_for_function('navigator.serviceWorker && navigator.serviceWorker.controller !== null || (location.reload(), false)',timeout=8000) if False else None
    pg.evaluate('navigator.serviceWorker.ready.then(()=>true)'); pg.reload(); pg.wait_for_selector('.task')
    ok('service worker controlling page',pg.evaluate('!!navigator.serviceWorker.controller'))
    cdp=ctx.new_cdp_session(pg); ie=cdp.send('Page.getInstallabilityErrors')
    ok('Chrome installability: no errors',ie.get('installabilityErrors')==[],str(ie))
    ctx.set_offline(True); pg.reload(); pg.wait_for_selector('.task',timeout=5000)
    ok('works offline after first visit',pg.locator('span.t[data-id]').count()==57 and pg.text_content('.overall .num').startswith('2 / 57'))
    ctx.set_offline(False)
    ok('no JS errors',not errs,str(errs))
    # dark mode screenshot
    d=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,color_scheme='dark'); dp=d.new_page(); dp.goto('http://127.0.0.1:8765/#w4'); dp.wait_for_selector('.task'); dp.screenshot(path='/tmp/m3.png')
    # desktop/tablet layout
    t=b.new_page(viewport={'width':1100,'height':900}); t.goto('http://127.0.0.1:8765/#w1'); t.wait_for_selector('.task'); t.screenshot(path='/tmp/m4.png')
    b.close()
finally:
  srv.terminate()
print('\nRESULT: %d/%d passed'%(sum(r[1] for r in R),len(R)))
