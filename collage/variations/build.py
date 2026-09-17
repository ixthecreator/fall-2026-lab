"""Six collage compositions. SVG does the layout; the browser only adds dragging."""
from pathlib import Path
import json,base64,html,copy
R=Path(__file__).parent
MODELS=R.parent/'studies/layouts'
PHOTOS={k:(R.parent/'assets'/f'{k}.jpg') for k in ['bernhardt','herschel','thompson']}
DIMS={'bernhardt':(960,1272),'herschel':(960,1375),'thompson':(960,1248)}
# Source-image rectangles: cropping stays in SVG and is reversible.
CROPS={
 'b-eye':('bernhardt',(400,275,94,66)), 'b-mouth':('bernhardt',(379,390,90,57)),
 'h-eye':('herschel',(596,653,151,132)), 'h-nose':('herschel',(532,718,142,212)),
 'h-mouth':('herschel',(478,890,224,133)), 't-eye':('thompson',(441,306,114,77)),
 't-left':('thompson',(316,308,103,80)), 't-nose':('thompson',(369,347,103,116)),
 't-mouth':('thompson',(370,444,151,82)), 'b-hair':('bernhardt',(280,130,520,390)),
 'b-ear':('bernhardt',(531,322,74,111)), 'b-cloth':('bernhardt',(280,710,550,340)),
 't-brow':('thompson',(326,282,216,65)), 'h-skin':('herschel',(724,499,141,188)),
 'h-face':('herschel',(304,311,570,838)), 't-face':('thompson',(282,180,360,417)),
 'b-face':('bernhardt',(328,191,335,340))}
HEAD='M490 121 C330 84 214 175 211 343 L177 465 Q164 522 214 553 L229 725 Q245 855 379 925 L392 996 L649 996 L627 903 Q764 812 778 660 L803 463 Q810 414 774 379 C798 198 670 91 490 121Z'
COLORS={'green':('#a7fc26','#082317'),'blue':('#a4dbff','#09257d'),'red':('#ff7356','#6b071a'),'pink':('#ffc1f0','#6f124b'),'silver':('#f8f2df','#202225'),'amber':('#f8d469','#3e2119')}
def colorfilter(name,light,dark):
    def rgb(h):return [int(h[i:i+2],16)/255 for i in (1,3,5)]
    rows=[]
    for a,b in zip(rgb(light),rgb(dark)): rows += [f'{v*(a-b):.5f}' for v in [.2126,.7152,.0722]]+['0',f'{b:.5f}']
    return f'<filter id="{name}" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="{" ".join(rows)} 0 0 0 1 0"/></filter>'

def definitions():
    s='<defs>'+''.join(colorfilter(k,*v) for k,v in COLORS.items())
    for k,(w,h) in DIMS.items():s+=f'<image id="photo-{k}" href="../assets/{k}.jpg" width="{w}" height="{h}"/>'
    s+='<pattern id="scan" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M0 1H5" stroke="#10100e" stroke-opacity=".18" stroke-width="1"/></pattern>'
    s+=f'<clipPath id="head"><path d="{HEAD}"/></clipPath></defs>'
    return s

def photo(crop,x,y,w,h,tint='silver',opacity=1):
    name,box=CROPS[crop];v=' '.join(map(str,box))
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{v}" preserveAspectRatio="none" overflow="hidden" opacity="{opacity}"><use href="#photo-{name}" filter="url(#{tint})"/></svg>'

def model(name,box):
    d=json.loads((MODELS/f'{name}.json').read_text());nodes=copy.deepcopy(d['nodes'])
    xmin=min(n['x'] for n in nodes);xmax=max(n['x'] for n in nodes);ymin=min(n['y'] for n in nodes);ymax=max(n['y'] for n in nodes)
    x,y,w,h=box
    for n in nodes:n['x']=round(x+(n['x']-xmin)/(xmax-xmin)*w,3);n['y']=round(y+(n['y']-ymin)/(ymax-ymin)*h,3)
    edges={tuple(sorted((e['a'],e['b']))):e for e in d['edges']}
    return nodes,list(edges.values())

def centroid(nodes,ids):
    selected=[n for n in nodes if n['id'] in ids]
    return (sum(n['x'] for n in selected)/len(selected),sum(n['y'] for n in selected)/len(selected))

class Scene:
    def __init__(self,key,title,modelkey,bg,box=None):
        self.key,self.title,self.modelkey,self.bg=key,title,modelkey,bg
        self.nodes,self.edges=model(modelkey,box) if box else ([],[])
        self.base=[];self.features=[];self.attachments={};self.bounds={};self.extra=[];self.node_system=False
    def feature(self,id,crop,box,tint='silver',shape='rect',ids=(),angle=0,stroke=None,opacity=1,pattern=True):
        x,y,w,h=box;cid=self.key+'-'+id
        if shape=='ellipse':clip=f'<ellipse cx="{w/2}" cy="{h/2}" rx="{w/2}" ry="{h/2}"/>'
        elif shape=='shard':clip=f'<path d="M{w*.11} 0 L{w} {h*.09} L{w*.92} {h} L0 {h*.9}Z"/>'
        elif shape.startswith('M'):clip=f'<path d="{shape}"/>'
        else:clip=f'<rect width="{w}" height="{h}"/>'
        src=f'<g data-feature="{id}" tabindex="0" role="button" aria-label="Move {id.replace("-"," ")}. Use arrow keys; Escape resets." transform="translate(0 0)"><title>{html.escape(id.replace("-"," "))}: draggable photograph fragment</title><g transform="translate({x} {y}) rotate({angle} {w/2} {h/2})"><defs><clipPath id="{cid}">{clip}</clipPath></defs><g clip-path="url(#{cid})">'
        src+=photo(crop,0,0,w,h,tint,opacity)
        if self.node_system:
            alternate={'left-eye':'h-eye','right-eye':'b-eye','nose':'h-nose','mouth':'b-mouth'}[id]
            src+='<g class="alternate-image" opacity="0">'+photo(alternate,0,0,w,h,'pink' if id=='mouth' else 'silver')+'</g>'
        if pattern:src+=f'<rect width="{w}" height="{h}" fill="url(#scan)" pointer-events="none"/>'
        src+='</g>'
        if stroke:src+=f'<g fill="none" stroke="{stroke}" stroke-width="2">{clip}</g>'
        src+='</g></g>'
        self.features.append(src);self.attachments[id]=list(ids)
        # Allow 30px around rotated corners, keeping fragments on the canvas.
        self.bounds[id]=dict(x=x,y=y,w=w,h=h)
    def at(self,id,crop,ids,w,h,tint='silver',shape='rect',offset=(0,0),**kwargs):
        x,y=centroid(self.nodes,ids);self.feature(id,crop,(x-w/2+offset[0],y-h/2+offset[1],w,h),tint,shape,ids,**kwargs)
    def network(self,color='#d6d2b8',width=1,radius=2,opacity=1):
        by={n['id']:n for n in self.nodes};s=f'<g class="network" fill="none" stroke="{color}" opacity="{opacity}" aria-hidden="true">'
        for e in self.edges:
            a,b=by[e['a']],by[e['b']]
            s+=f'<line data-a="{e["a"]}" data-b="{e["b"]}" x1="{a["x"]}" y1="{a["y"]}" x2="{b["x"]}" y2="{b["y"]}" stroke-width="{width}"/>'
        for n in self.nodes:
            iris=n.get('group')=='iris';r=5 if iris else radius
            s+=f'<circle data-node="{n["id"]}" cx="{n["x"]}" cy="{n["y"]}" r="{r}" stroke="{"#ff7e2c" if iris else color}" stroke-width="{1.7 if iris else .8}" fill="{self.bg if radius>3 else color}"/>'
        return s+'</g>'
    def render(self,network):
        desc='Original collage layout influenced by Tony Oursler’s projected facial fragments and by '+self.modelkey+'. Found photographs by Julia Margaret Cameron, Nadar and Dorothea Lange. Drag facial fragments; arrow keys move the focused fragment; Escape restores the composition. This artwork does not run face recognition.'
        s=f'<svg xmlns="http://www.w3.org/2000/svg" class="artwork" viewBox="0 0 1000 1100" role="group" aria-labelledby="art-title art-desc"><title id="art-title">{self.title}</title><desc id="art-desc">{html.escape(desc)}</desc>'+definitions()+f'<rect width="1000" height="1100" fill="{self.bg}"/>'
        s+=''.join(self.base)+('<g class="template-network" opacity=".18" aria-hidden="true">'+network+'</g>' if self.node_system else '')+'<g class="features">'+''.join(self.features)+'</g>'+network+''.join(self.extra)+'</svg>'
        config=dict(nodes=self.nodes,attachments=self.attachments,bounds=self.bounds)
        if self.node_system:
            config.update(edges=self.edges,mode='template-resistance')
            handles=''.join(f'<circle class="node-handle" fill="transparent" stroke="none" data-handle="{n["id"]}" cx="{n["x"]}" cy="{n["y"]}" r="12" tabindex="{0 if n["id"] in [1,4,33,133,159,263,362,386,61,291,13,14,152,10] else -1}" role="button" aria-label="Move facial node {n["id"]}. Arrow keys move it. Escape resets."/>' for n in self.nodes)
            s=s[:-6]+'<g class="node-handles">'+handles+'</g><g class="gesture-traces" aria-hidden="true"/></svg>'
        doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{self.title} / Six borrowed faces</title><meta name="description" content="A draggable photographic face collage influenced by Tony Oursler and computational facial structures."/><link rel="stylesheet" href="art.css"/><script src="drag.js" defer></script></head><body style="--canvas:{self.bg}"><main aria-label="{self.title}">{s}</main><p class="sr-only" role="status" aria-live="polite"></p><script type="application/json" id="composition">{json.dumps(config)}</script></body></html>'''
        if self.node_system:
            doc=doc.replace('<script src="drag.js" defer></script>','<script type="module" src="node-system.js"></script>').replace('<body style=', '<body class="node-system" style=')
            doc=doc.replace('Drag facial fragments; arrow keys', 'Drag any facial node or image window. Nearby nodes and images respond. On release the template pulls the face back, leaving a trace. This is an artistic rule, not a recognition prediction. Arrow keys')
        (R/(self.key+'.html')).write_text(doc)
        export=s.replace('class="artwork"','width="1000" height="1100"')
        for name,path in PHOTOS.items():export=export.replace('../assets/'+name+'.jpg','data:image/jpeg;base64,'+base64.b64encode(path.read_bytes()).decode())
        (R/'exports'/(self.key+'.svg')).write_text(export)
        return dict(key=self.key,title=self.title,model=self.modelkey,nodes=len(self.nodes),features=len(self.features))

scenes=[]
# 01 — five anchored islands; alignment geometry holds a face that has no surface.
s=Scene('01-alignment','01 / A face in five places','alignment-5','#e8e6df',(279,345,444,431))
s.base += ['<path d="M351 213L681 170L802 794L574 971L254 842L180 411Z" fill="#dcd9cf"/>','<path d="M266 167L727 178L740 903L258 919Z" stroke="#c8c5ba" stroke-width="1" fill="none"/>']
s.edges=[dict(a=a,b=b) for a,b in [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]]
s.at('left-eye','h-eye',[0],260,167,'silver','shard',angle=-5)
s.at('right-eye','b-eye',[1],218,142,'green',angle=4)
s.at('nose','t-nose',[2],103,181,'silver','shard',angle=-3)
s.at('left-mouth','t-mouth',[3],175,84,'pink',angle=8)
s.at('right-mouth','b-mouth',[4],158,101,'silver',angle=-7)
scenes.append(s.render(s.network('#5c514c',1.4,7)))
# 02 — sparse contours etched into a flat blue mask.
s=Scene('02-contours','02 / Borrowed contours','landmarks-68','#eae9e4',(214,336,575,538))
s.base += [f'<path d="{HEAD}" fill="#162cac"/>','<path d="M227 314Q198 176 382 126L379 948Q224 880 217 635Z" fill="#243fc4" opacity=".58"/>']
s.at('left-eye','b-eye',range(36,42),221,117,'silver','ellipse',angle=-6)
s.at('right-eye','h-eye',range(42,48),189,157,'green','rect',angle=4)
s.at('nose','h-nose',range(27,36),97,206,'blue','shard')
s.at('mouth','t-mouth',range(48,68),237,132,'pink','ellipse',angle=3)
s.at('left-brow','t-brow',range(17,22),177,49,'blue','shard',angle=3)
s.at('right-brow','t-brow',range(22,27),144,35,'silver','shard',angle=-4)
scenes.append(s.render(s.network('#f6b446',1.7,3)))
# 03 — an unconnected point cloud and unstable islands of borrowed skin.
s=Scene('03-scatter','03 / No single person','landmarks-106','#111914',(167,197,667,740))
s.at('left-eye','t-left',range(33,43),233,137,'green','shard',angle=-10)
s.at('right-eye','b-eye',range(87,97),269,95,'silver','rect',angle=8)
s.at('nose','h-nose',range(72,87),98,213,'silver','shard',angle=9)
s.at('upper-mouth','b-mouth',range(62,72),255,85,'pink','rect',angle=-8)
s.at('lower-mouth','t-mouth',range(52,62),199,119,'silver','shard',angle=12)
s.at('left-brow','t-brow',range(43,52),162,42,'silver','shard',angle=-8)
s.at('right-brow','t-brow',range(97,106),115,60,'green','shard',angle=5)
s.feature('left-cheek','h-skin',(174,517,108,143),'blue','shard',ids=[12,13,14],angle=-9)
s.feature('right-cheek','b-face',(701,579,99,153),'silver','shard',ids=[29,30,31],angle=14)
s.feature('chin','h-mouth',(408,902,161,48),'green','shard',ids=[0,7,8,23,24],angle=-3)
scenes.append(s.render(s.network('#b5d483',.8,2.8)))
# 04 — a photographic head beneath an imposed triangulated skin.
s=Scene('04-surface','04 / A measured stranger','mesh-468','#dddcd3',(201,180,588,725))
s.node_system=True
s.base += [f'<g clip-path="url(#head)"><path d="{HEAD}" fill="#a31424"/>'+photo('h-face',189,115,635,873,'red')+'</g>']
left=[n['id'] for n in s.nodes if n['group']=='eyes' and n['x']<500];right=[n['id'] for n in s.nodes if n['group']=='eyes' and n['x']>=500];mouth=[n['id'] for n in s.nodes if n['group']=='mouth']
s.at('left-eye','b-eye',left,178,123,'blue','rect',angle=-3)
s.at('right-eye','t-eye',right,185,156,'green','rect',angle=3)
s.at('nose','t-nose',[1,2,4,5,6,19,94,97,98,326,327],102,183,'red','shard')
s.at('mouth','t-mouth',mouth,236,107,'silver','rect',angle=-5)
scenes.append(s.render(s.network('#e9da72',.8,1.3,.87)))
# 05 — eyes exceed their assigned topology; the iris extension becomes a visible target.
s=Scene('05-gaze','05 / The face looks back','mesh-478-study','#1b1331',(178,205,645,694))
s.base += ['<path d="M345 174Q137 233 195 627Q168 894 466 954L709 868L838 496L717 149Z" fill="#291b69"/>']
left=[n['id'] for n in s.nodes if n['group'] in ['eyes','iris'] and n['x']<500];right=[n['id'] for n in s.nodes if n['group'] in ['eyes','iris'] and n['x']>=500];mouth=[n['id'] for n in s.nodes if n['group']=='mouth']
s.at('left-eye','h-eye',left,326,247,'blue','ellipse',angle=-9)
s.at('right-eye','b-eye',right,309,283,'green','ellipse',angle=11)
s.at('nose','h-nose',[1,2,4,5,6,19,94,97,98,326,327],78,180,'pink','shard')
s.at('mouth','b-mouth',mouth,140,61,'pink','rect')
scenes.append(s.render(s.network('#a0a1c9',.55,1.05,.7)))
# 06 — handmade image masks explore label regions; no model inference is claimed.
s=Scene('06-segments','06 / The face comes apart','parsing-19','#eee9dd')
s.feature('skin','h-face',(241,277,539,542),'silver','M257 0Q36 -18 0 127L37 333Q112 497 267 542Q437 485 510 333L539 127Q483 -18 257 0Z')
s.feature('hair','b-hair',(220,116,545,234),'blue','M0 219Q-17 18 248 0Q512 -11 545 173L463 234L361 127L191 134L45 227Z',angle=-5)
s.feature('left-ear','b-ear',(156,424,69,150),'amber','ellipse',angle=-13)
s.feature('right-ear','b-ear',(792,436,73,143),'pink','ellipse',angle=12)
s.feature('left-brow','t-brow',(300,331,169,42),'pink','shard',angle=-7)
s.feature('right-brow','t-brow',(567,320,158,46),'silver','shard',angle=8)
s.feature('left-eye','h-eye',(288,394,168,125),'blue','ellipse',angle=-5)
s.feature('right-eye','b-eye',(584,389,175,116),'green','ellipse',angle=7)
s.feature('nose','t-nose',(464,451,101,193),'amber','M39 0L71 0L101 168L51 193L0 168Z',angle=5)
s.feature('upper-lip','t-mouth',(394,678,222,66),'pink','M0 54L65 4L108 16L152 0L222 48L165 66L60 64Z',angle=-4)
s.feature('mouth','b-mouth',(420,745,178,60),'silver','ellipse',angle=2)
s.feature('lower-lip','h-mouth',(417,813,204,64),'red','M0 0L100 13L204 0L169 48L102 64L37 45Z',angle=4)
s.feature('neck','h-skin',(415,916,188,105),'silver','shard',angle=-4)
s.feature('cloth','b-cloth',(277,1028,452,60),'blue','M0 60L52 3L387 0L452 60Z')
scenes.append(s.render(''))
(R/'manifest.json').write_text(json.dumps(scenes,indent=2)+'\n')
print(json.dumps(scenes,indent=2))
