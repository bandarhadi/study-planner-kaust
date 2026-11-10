import subprocess,sys,time,tempfile
from playwright.sync_api import sync_playwright
srv=subprocess.Popen([sys.executable,'-m','http.server','8766','--bind','127.0.0.1'],cwd='/home/claude/study-planner/pwa',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
try:
  with sync_playwright() as p:
    ctx=p.chromium.launch_persistent_context(tempfile.mkdtemp(),executable_path='/usr/bin/google-chrome',headless=True,viewport={'width':390,'height':844})
    pg=ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.goto('http://127.0.0.1:8766/');pg.wait_for_selector('.task');pg.wait_for_timeout(1500);pg.reload();pg.wait_for_timeout(1000)
    cdp=ctx.new_cdp_session(pg)
    print('installability errors:',cdp.send('Page.getInstallabilityErrors'))
    m=cdp.send('Page.getAppManifest');print('manifest errors:',m.get('errors'))
    ctx.close()
finally: srv.terminate()
