from PIL import Image, ImageDraw, ImageFont
W,H=1080,1350
src=Image.open('/home/claude/flip-mascot.png')
BG=src.getpixel((5,5)); CREAM=(247,238,223); GOLD=(236,196,106); PLUM=(42,22,56); MUTED=(190,170,200)
SER="/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
IB="/usr/share/fonts/opentype/inter/Inter-Bold.otf"; IM="/usr/share/fonts/opentype/inter/Inter-Medium.otf"; IS="/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
f=lambda p,s:ImageFont.truetype(p,s)
D='/home/claude/svrepo/botw/sunshine-tienda/'
flip_on=src.crop((520,560,1040,1170)); flip_sm=src.crop((140,1380,500,1740))
def ctext(d,y,t,font,fill):
    tw=d.textlength(t,font=font); d.text(((W-tw)/2,y),t,font=font,fill=fill)
def spaced(d,y,t,font,fill,sp=7):
    tw=sum(d.textlength(c,font=font)+sp for c in t)-sp; x=(W-tw)/2
    for c in t: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+sp
def photo(im,d,box,path,maxscale=99):
    x0,y0,x1,y1=box; d.rounded_rectangle(box,28,fill=CREAM)
    p=Image.open(path).convert('RGB'); pad=24
    bw,bh=x1-x0-2*pad,y1-y0-2*pad
    s=min(bw/p.width,bh/p.height,maxscale)
    p=p.resize((int(p.width*s),int(p.height*s)),Image.LANCZOS)
    im.paste(p,(x0+pad+(bw-p.width)//2,y0+pad+(bh-p.height)//2))
def footer(d,t="Find her on The Switch · switchme.io"):
    d.rectangle((0,H-110,W,H),fill=PLUM); ctext(d,H-78,t,f(IS,34),GOLD)
# Monday
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
spaced(d,70,"BRAND OF THE WEEK",f(IB,30),GOLD); ctext(d,120,"Sunshine Tienda",f(SER,96),CREAM)
ctext(d,240,"Founded by twin sisters Laura and Amanda Ernst",f(IM,34),MUTED)
photo(im,d,(90,310,990,900),D+'founder.jpg',maxscale=2.2)
d.text((90,940),"In her words:",font=f(IS,32),fill=GOLD)
d.text((90,990),"“Be vacation happy.”",font=f(SER,64),fill=CREAM)
d.text((90,1080),"Women-owned and verified on The Switch.",font=f(IM,32),fill=MUTED)
im.paste(flip_sm.resize((150,150)),(880,1060)); footer(d); im.save('st-mon.png')
# Wednesday
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
spaced(d,70,"BRAND OF THE WEEK",f(IB,30),GOLD); ctext(d,120,"Flip's gift pick",f(SER,96),CREAM)
photo(im,d,(90,260,790,990),D+'pippa-cabernet.jpg')
im.paste(flip_on.resize((250,293)),(805,640)); d.text((830,560),'My pick!',font=f(IS,34),fill=GOLD)
ctext(d,1030,"Cabernet Gingham Pippa Dress",f(SER,52),CREAM)
ctext(d,1100,"Sunshine Tienda · for the friend who's always on vacation",f(IM,30),MUTED)
footer(d); im.save('st-wed.png')
# Friday
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
spaced(d,70,"BRAND OF THE WEEK",f(IB,30),GOLD); ctext(d,120,"Gift guide",f(SER,96),CREAM)
ctext(d,240,"Four gifts from Sunshine Tienda",f(IM,34),MUTED)
items=[("For her","Ivory Eyelet Penny Dress","penny-ivory.jpg"),("For the beach bag","Puerto Stripe Caftan","caftan-puerto.jpg"),("For a little one","Kids Confetti Stripe Juno Dress","juno-kids.jpg"),("For the holidays","Cabernet Gingham Jane Dress","jane-cabernet.jpg")]
for i,(who,name,fn) in enumerate(items):
    cx=90+(i%2)*465; cy=310+(i//2)*450
    photo(im,d,(cx,cy,cx+435,cy+330),D+fn)
    d.text((cx+6,cy+345),who.upper(),font=f(IB,24),fill=GOLD)
    d.text((cx+6,cy+380),name,font=f(IS,27),fill=CREAM)
footer(d,"All four on The Switch · switchme.io"); im.save('st-fri.png')
sh=Image.new('RGB',(W*3+80,H+40),(255,255,255))
for i,n in enumerate(['st-mon','st-wed','st-fri']): sh.paste(Image.open(n+'.png'),(20+i*(W+20),20))
sh.resize((sh.width//2,sh.height//2)).save('st-sheet.png')
