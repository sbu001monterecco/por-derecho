from pathlib import Path
import re,json,base64,io,hashlib
from xml.sax.saxutils import escape
from lxml import html as LH
from PIL import Image as PILImage
import fitz
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Table,TableStyle,Image,KeepTogether,Flowable
from reportlab.platypus.tableofcontents import TableOfContents

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'documents/meeting-point-20260923';OUT=WORK
from reportlab import rl_config
rl_config.invariant=1
INK=colors.HexColor('#142c36');TEAL=colors.HexColor('#075b56');GOLD=colors.HexColor('#dab775');PAPER=colors.HexColor('#f6f3eb');LINE=colors.HexColor('#cedad9')
W,H=A4;M=46;CW=W-2*M
for name,file in [('Sans','DejaVuSans.ttf'),('SansB','DejaVuSans-Bold.ttf'),('SansI','DejaVuSans.ttf'),('Serif','DejaVuSerif.ttf'),('SerifB','DejaVuSerif-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansB',italic='SansI',boldItalic='SansB')
pdfmetrics.registerFontFamily('Serif',normal='Serif',bold='SerifB',italic='Serif',boldItalic='SerifB')
ST={
 'p':ParagraphStyle('body',fontName='Sans',fontSize=9.35,leading=14.4,spaceAfter=8,textColor=INK,allowWidows=0,allowOrphans=0),
 'small':ParagraphStyle('small',fontName='Sans',fontSize=7.8,leading=11.7,spaceAfter=7,textColor=INK),
 'h1':ParagraphStyle('h1',fontName='SerifB',fontSize=17,leading=22,spaceBefore=12,spaceAfter=11,textColor=INK,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='SerifB',fontSize=15,leading=20,spaceBefore=16,spaceAfter=10,textColor=TEAL,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='Serif',fontSize=13,leading=18,spaceBefore=14,spaceAfter=8,textColor=TEAL,keepWithNext=True),
 'cover':ParagraphStyle('cover',fontName='Serif',fontSize=39,leading=44,spaceAfter=22,textColor=INK),
 'label':ParagraphStyle('label',fontName='SansB',fontSize=8,leading=12,spaceAfter=14,textColor=TEAL),
 'lead':ParagraphStyle('lead',fontName='Sans',fontSize=11,leading=17,spaceAfter=14,textColor=INK),
}
def normalize(s):return s.replace('\u2011','-').replace('–','-').replace('—','-').replace('\u00a0',' ').replace('→',' > ').replace('↗','').replace('↔',' / ')
def inline(e):
 s=escape(normalize(e.text or ''))
 for c in e:
  inner=inline(c);tag=c.tag.lower() if isinstance(c.tag,str) else ''
  if tag in ['strong','b']:s+='<b>'+inner+'</b>'
  elif tag in ['em','i']:s+='<i>'+inner+'</i>'
  elif tag=='br':s+='<br/>'
  elif tag=='a':
   href=c.get('href','')
   s+=f'<link href="{escape(href)}" color="#075b56">{inner}</link>' if href.startswith(('https://','http://')) else inner
  else:s+=inner
  s+=escape(normalize(c.tail or ''))
 return s
def P(text,style='p'):return Paragraph(text,ST[style])
class Rule(Flowable):
 def __init__(self):Flowable.__init__(self);self.width=CW;self.height=12
 def draw(self):self.canv.setStrokeColor(TEAL);self.canv.setLineWidth(1.3);self.canv.line(0,7,CW,7)
class DDoc(BaseDocTemplate):
 def __init__(self,p,lang):
  super().__init__(str(p),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=M,bottomMargin=48,title='Meeting Point / Club Sei / Sun Park - '+lang.upper()+' public reading edition',author='Gil Marer - public reading edition',pageCompression=1)
  self.lang=lang;self.addPageTemplates(PageTemplate(id='body',frames=Frame(M,48,CW,H-M-48,id='normal',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=self.pagepaint))
 def pagepaint(self,c,doc):
  c.saveState();c.setFillColor(TEAL);c.rect(0,H-9,W,9,fill=1,stroke=0)
  c.setFont('Sans',7);c.setFillColor(INK);c.drawString(M,28,'Meeting Point / Club Sei / Sun Park  |  '+('Edición pública' if self.lang=='es' else 'Public reading edition')+'  |  23.09.2026')
  c.drawRightString(W-M,28,str(doc.page));c.setStrokeColor(LINE);c.line(M,40,W-M,40);c.restoreState()
 def afterFlowable(self,f):
  if hasattr(f,'_toc_title'):
   key=f._toc_key;self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f._toc_title,key,level=0,closed=False);self.notify('TOCEntry',(0,f._toc_title,self.page,key))

data=json.loads((WORK/'reader-data.json').read_text());figs=data['figures'];copy=data['copy']
def img_bytes(src):
 p=ROOT/src
 if p.suffix=='.svg':
  s=p.read_text();m=re.search(r'data:image/(?:png|jpeg);base64,([^"\s]+)',s)
  if not m:raise ValueError('SVG has no source raster '+src)
  return base64.b64decode(m.group(1))
 return p.read_bytes()

for lang in ['es','en']:
 es=lang=='es';d=copy[lang];story=[]
 story+=[Spacer(1,33),P('PROJECT SUN ROCK   /   '+('23 SEPTIEMBRE 2026' if es else '23 SEPTEMBER 2026'),'label'),P('Meeting Point.<br/>Club Sei.<br/>Sun Park.','cover'),P('Edición pública de lectura' if es else 'Public reading edition','h2'),P('Español · Texto sustantivo completo' if es else 'English · Complete substantive translation','lead'),Rule()]
 story.append(P(inline(LH.fragment_fromstring('<div>'+d['claim']+'</div>')),'lead'))
 story.append(P(inline(LH.fragment_fromstring('<div>'+d['limit']+'</div>')),'small'))
 story.append(Spacer(1,12));story.append(P('36/2012  |  357/2024  |  93/2025','label'))
 story.append(P('Una alegación atribuida. Fuentes identificadas. Peticiones pendientes de decisión.' if es else 'An attributed allegation. Identified sources. Requests awaiting a decision.','small'))
 story.append(PageBreak())
 story.append(P('Guía visual de lectura' if es else 'Visual reading guide','h1'))
 story.append(P(d['proof_intro']))
 for row in d['timeline']:
  tab=Table([[P(normalize(row[0]),'h3'),P('<b>'+row[1]+'</b><br/>'+row[2])]],colWidths=[89,CW-89]);tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PAPER),('BOX',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([tab,Spacer(1,9)])
 story.append(P(d['map_title'],'h2'));story.append(P(d['map_intro']))
 boxes=Table([[P('<b>ES</b><br/>'+d['map_left'],'small'),P('⇄<br/>'+('Documentos<br/>y respuesta' if es else 'Documents<br/>and response'),'small'),P('<b>DE</b><br/>'+d['map_right'],'small')],[P(inline(LH.fragment_fromstring('<div>'+d['map_lbody']+'</div>')),'small'),'⇄',P(inline(LH.fragment_fromstring('<div>'+d['map_rbody']+'</div>')),'small')]],colWidths=[207,CW-414,207]);boxes.setStyle(TableStyle([('BOX',(0,0),(-1,-1),.8,TEAL),('INNERGRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),PAPER),('FONTNAME',(0,0),(-1,-1),'Sans'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),9)]));story.append(boxes)
 story.append(PageBreak());story.append(P('Índice de la lectura completa' if es else 'Complete reading contents','h1'))
 toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc',fontName='Sans',fontSize=9,leading=13,spaceBefore=7,rightIndent=22,textColor=INK)];story.append(toc);story.append(PageBreak())
 slug='lectura-publica' if es else 'public-reading'
 docroot=LH.fromstring((ROOT/lang/'lava-verde-club-sei-meeting-point'/slug/'index.html').read_text()).xpath('//article[@class="mp-prose"]')[0]
 def add_elem(el):
  tag=el.tag.lower() if isinstance(el.tag,str) else ''
  if tag in ['h1','h2','h3']:
   t=P(inline(el),'h1' if el.get('class')=='mp-document-title' else tag);t._toc_title=normalize(el.text_content());t._toc_key=el.get('id');story.append(t)
  elif tag=='p':story.append(P(inline(el)))
  elif tag in ['ul','ol']:
   for n,li in enumerate(el.findall('li'),1):story.append(P((str(n)+'. ' if tag=='ol' else '• ')+inline(li)))
  elif tag=='table':
   rows=[]
   for tr in el.findall('.//tr'):rows.append([P(inline(c),'small') for c in tr])
   if rows:
    t=Table(rows,colWidths=[CW/len(rows[0])]*len(rows[0]),repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),PAPER),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]));story.extend([t,Spacer(1,9)])
  elif tag=='hr':story.append(Rule())
  else:
   if el.text_content().strip():story.append(P(inline(el)))
 for el in docroot:
  if el.get('id')!='public-visual-evidence':add_elem(el)
 story.append(PageBreak());h=P('Selección visual pública' if es else 'Public visual selection','h1');h._toc_title=h.getPlainText();h._toc_key='visual-selection';story.append(h)
 story.append(P('Cuatro reproducciones públicas identificadas. Esta selección no sustituye los anexos privados. Se mantienen el idioma y las atribuciones de las imágenes originales; no se presentan sus rótulos como hechos judicialmente probados.' if es else 'Four identified public reproductions. This selection does not replace the private annexes. The original images retain their language and attributions; their labels are not presented as judicially established facts.'))
 for i,f in enumerate(figs):
  if i:story.append(PageBreak())
  b=img_bytes(f['src']);pi=PILImage.open(io.BytesIO(b));pi.load();iw,ih=pi.size;scale=min(CW/iw,500/ih)
  im=Image(io.BytesIO(b),width=iw*scale,height=ih*scale,hAlign='CENTER')
  story.extend([P(('Imagen ' if es else 'Image ')+str(i+1),'label'),im,Spacer(1,12),P(f[lang],'small'),P('<link href="https://sbu001monterecco.github.io/por-derecho/'+f['src']+'" color="#075b56">'+('Abrir reproducción pública en su contexto' if es else 'Open the public reproduction in context')+'</link>','small')])
 out=OUT/f'MeetingPoint_Public_{lang.upper()}.pdf';DDoc(out,lang).multiBuild(story)
 pdf=fitz.open(out);text='\n'.join(p.get_text() for p in pdf)
 assert len(text)>100000,(lang,len(text));assert out.stat().st_size<10000000
 assert not re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',text)
 print(json.dumps({'lang':lang,'pages':len(pdf),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'extracted_characters':len(text)}))
