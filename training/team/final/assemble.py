import re, subprocess, json, os, sys
from PIL import Image, ImageDraw, ImageFont
T='/home/claude/svrepo/training/team/'; V=T+'voice/'
B='/tmp/claude-0/-home-claude/6be1530c-5430-5137-8516-ea307a382ea2/scratchpad/train/build/'
CH={'01d':('01-sign-in-desktop','Chapter 1','Signing in'),'01p':('01-sign-in-phone','Chapter 1','Signing in on a phone'),
    '02d':('02-menu-tour-desktop','Chapter 2','Finding your way'),'02p':('02-menu-tour-phone','Chapter 2','Finding your way on a phone'),
    '06':('06-add-a-brand','Chapter 6','Adding a brand'),'07':('07-add-a-provider','Chapter 7','Adding a service provider')}
PLUM=(42,22,56); CREAM=(247,238,223); GOLD=(236,196,106)
SER="/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"; IM="/usr/share/fonts/opentype/inter/Inter-Medium.otf"; IB="/usr/share/fonts/opentype/inter/Inter-Bold.otf"
W,H,BAR=1920,1080,130
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).strip())
def ts(s):
    h,m,r=s.split(':'); return int(h)*3600+int(m)*60+float(r)
def cues(vtt):
    out=[]; txt=open(vtt).read()
    for m in re.finditer(r'(\d\d:\d\d:\d\d\.\d+) --> (\d\d:\d\d:\d\d\.\d+)\n(.+?)(?:\n\n|\Z)',txt,re.S):
        out.append((ts(m.group(1)),m.group(3).strip().replace('\n',' ')))
    return out
def assfmt(t):
    h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
def title(key):
    name,ch,ttl=CH[key]
    im=Image.new('RGB',(W,H+BAR),PLUM); d=ImageDraw.Draw(im)
    def c(y,t,f,fill):
        tw=d.textlength(t,font=f); d.text(((W-tw)/2,y),t,font=f,fill=fill)
    sp="THE SWITCH · TEAM TRAINING"; c(430,sp,ImageFont.truetype(IB,34),GOLD)
    c(500,ch,ImageFont.truetype(IM,48),CREAM); c(570,ttl,ImageFont.truetype(SER,110),CREAM)
    p=B+key+'-title.png'; im.save(p); return p
def build(key):
    name=CH[key][0]; src=T+name+'.mp4'; vd=dur(src)
    cs=cues(T+name+'.vtt')
    lines=[]
    for t,text in cs:
        mm=int(t//60); ss=int(t%60); f=V+f"{key}-{mm:02d}{ss:02d}.mp3"
        if not os.path.exists(f): print('MISSING',f); continue
        lines.append([t,text,f,dur(f)])
    lines.sort()
    # segments with freeze pads
    bounds=[0]+[l[0] for l in lines]+[vd]
    segs=[]; newstart=[]; acc=0.0
    for i in range(len(bounds)-1):
        s,e=bounds[i],bounds[i+1]; length=e-s; pad=0.0
        if i>=1:
            need=lines[i-1][3]+0.35
            if need>length: pad=need-length
            newstart.append(acc)
        segs.append((s,e,pad)); acc+=length+pad
    total=acc
    # filter
    is_phone=key.endswith('p')
    if is_phone:
        base="scale=-2:1040,pad=1920:1080:(ow-iw)/2:20:color=0x2a1638"
    else:
        base="scale=1920:1080"
    seglist=B+key+'-segs.txt'; sl=open(seglist,'w')
    for i,(s0,e0,pad) in enumerate(segs):
        sp=B+f"{key}-seg{i:03d}.mp4"
        subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(s0),'-to',str(e0),'-i',src,'-vf',f"{base},fps=25,tpad=stop_mode=clone:stop_duration={pad:.3f}",'-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',sp],check=True)
        sl.write(f"file '{sp}'\n")
    sl.close()
    joined=B+key+'-joined.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',seglist,'-c','copy',joined],check=True)
    total=dur(joined)
    fc=[f"[0:v]pad=1920:{H+BAR}:0:0:color=0x2a1638[vb]"]
    # ass captions
    ass=B+key+'.ass'
    with open(ass,'w') as f:
        f.write(f"[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: {H+BAR}\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV\nStyle: D,Inter,40,&H00DFEEF7,&H00000000,&H00000000,0,0,1,0,0,2,80,80,42\n\n[Events]\nFormat: Layer, Start, End, Style, Text\n")
        for i,l in enumerate(lines):
            st=newstart[i]; en=(newstart[i+1] if i+1<len(lines) else total)-0.05
            en=max(en,st+l[3]); en=min(en,total)
            f.write(f"Dialogue: 0,{assfmt(st)},{assfmt(en)},D,{l[1]}\n")
    fc.append(f"[vb]subtitles={ass}[vs]")
    # audio
    ins=['-i',joined]; amix=[]
    for i,l in enumerate(lines):
        ins+=['-i',l[2]]; ms=int(newstart[i]*1000)
        fc.append(f"[{i+1}:a]aresample=44100,adelay={ms}|{ms}[a{i}]")
        amix.append(f"[a{i}]")
    fc.append(''.join(amix)+f"amix=inputs={len(amix)}:normalize=0,apad,atrim=0:{total:.3f}[aout]")
    body=B+key+'-body.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',';'.join(fc),'-map','[vs]','-map','[aout]','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-r','25',body],check=True)
    tp=title(key); tv=B+key+'-title.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-t','2.5','-i',tp,'-f','lavfi','-t','2.5','-i','anullsrc=r=44100:cl=stereo','-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p','-r','25','-c:a','aac','-b:a','160k','-shortest',tv],check=True)
    out=B+f"{name}.mp4"
    lst=B+key+'.txt'; open(lst,'w').write(f"file '{tv}'\nfile '{body}'\n")
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',lst,'-c','copy',out],check=True)
    pads=sum(s[2] for s in segs)
    print(key,'video',round(vd,1),'-> final',round(dur(out),1),'freeze added',round(pads,1),'lines',len(lines))
for k in (sys.argv[1:] or CH): build(k)
