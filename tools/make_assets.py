# Generates pwa/data.js from content-backup/content.json (single source of truth) and the app icons.
import json,sys,os
from PIL import Image,ImageDraw,ImageFont
root=sys.argv[1]
C=json.load(open(os.path.join(root,'content-backup/content.json'),encoding='utf-8'))
WEEK_START=['2026-11-08','2026-11-15','2026-11-22','2026-11-29','2026-12-06']  # from week titles [8-14 NOV] … [6-12 DEC]
DAYS=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
weeks=[]
for wi,w in enumerate(C['weeks']):
    cols=[]
    for c in w['columns']:
        items=[]
        for it in c['items']:
            if it['kind']=='day':
                name=next(d for d in DAYS if d in it['label'])
                items.append({'kind':'day','id':it['block_id'],'label':it['label'],'color':it['color'],'dayIndex':DAYS.index(name),
                  'button':it['button']['name'],
                  'todos':[{'id':t['block_id'],'segments':[[s[0],[a[1] for a in (s[1] if len(s)>1 else []) if a[0]=='h']] for s in t['title_raw']]} for t in it['todos']]})
            elif it['kind']=='callout':
                items.append({'kind':'callout','id':it['block_id'],'icon':it['icon'],'text':it['text']})
        cols.append(items)
    weeks.append({'id':w['block_id'],'title':w['title'],'start':WEEK_START[wi],'columns':cols})
data={'title':C['page']['title'],'quote':C['header_quote']['text'],'weeks':weeks}
open(os.path.join(root,'pwa/data.js'),'w',encoding='utf-8').write('// Generated from content-backup/content.json — do not edit by hand.\nwindow.PLANNER = '+json.dumps(data,ensure_ascii=False,indent=1)+';\n')
# icons
F='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
def icon(size,pad=0.0,name=''):
    im=Image.new('RGB',(size,size),'#37352f');d=ImageDraw.Draw(im)
    s=int(size*(1-2*pad))
    f=ImageFont.truetype(F,int(s*0.34))
    t='SP.';bb=d.textbbox((0,0),t,font=f);w=bb[2]-bb[0];h=bb[3]-bb[1]
    d.text(((size-w)/2-bb[0],(size-h)/2-bb[1]-s*0.04),t,font=f,fill='#f7f6f3')
    lw=int(s*0.36);y=int(size/2+h/2+s*0.06)
    d.rounded_rectangle([(size-lw)//2,y,(size+lw)//2,y+max(2,int(s*0.035))],radius=4,fill='#4dab9a')
    im.save(os.path.join(root,'pwa/icons',name))
icon(192,0,'icon-192.png');icon(512,0,'icon-512.png');icon(512,0.1,'icon-maskable-512.png');icon(180,0,'apple-touch-icon.png');icon(32,0,'favicon-32.png')
print('weeks',len(weeks),'todos',sum(len(i['todos']) for w in weeks for c in w['columns'] for i in c if i['kind']=='day'))
