"""Draw source-grounded landmark diagrams without running biometric models.
Run from any directory with Python 3. Only the standard library is required.
"""
from pathlib import Path
import json, math, re, html, base64
R=Path(__file__).parent
REF=R/'references/systems'
OUT=R/'exports'
DATA=R/'layouts'
C={'contour':'#6a7168','brows':'#8a669c','eyes':'#287f9a','nose':'#b37820','mouth':'#b25260','mesh':'#aab3ae','iris':'#cf5a30'}

def chain(seq,group,closed=False):
    seq=list(seq);return [dict(a=a,b=b,group=group) for a,b in zip(seq,seq[1:]+([seq[0]] if closed else []))]
def group68(i):
    return 'contour' if i<17 else 'brows' if i<27 else 'nose' if i<36 else 'eyes' if i<48 else 'mouth'

# Five-point ArcFace destination template: preserve official float coordinates.
coords5=[[38.2946,51.6963],[73.5318,51.5014],[56.0252,71.7366],
         [41.5493,92.3655],[70.7299,92.2041]]
five=dict(key='alignment-5',title='05 / Alignment anchors',subtitle='ArcFace destination template · exact source coordinates',
    nodes=[dict(id=i,x=x,y=y,group='eyes' if i<2 else 'nose' if i==2 else 'mouth') for i,(x,y) in enumerate(coords5)],edges=[],
    groups=['eyes','nose','mouth'],note='Two eye centres / nose / two mouth corners.',
    detail='Coordinates belong to a 112 × 112 aligned image; no official edge graph.',
    source='https://github.com/deepinsight/insightface/blob/master/python-package/insightface/utils/face_align.py',provenance='Exact arcface_dst coordinates. Dashed measurement guides are diagram annotations only.')
# Original 68-point schematic, with standard iBUG/dlib indexing.
p68=[(80,230),(82,282),(90,334),(105,386),(130,436),(164,484),(208,525),(263,553),(320,564),(377,553),(432,525),(476,484),(510,436),(535,386),(550,334),(558,282),(560,230),
(123,211),(157,190),(198,187),(237,195),(270,213),(370,213),(403,195),(442,187),(483,190),(517,211),
(320,247),(320,294),(320,337),(320,374),(268,391),(292,404),(320,412),(348,404),(372,391),
(145,267),(177,249),(216,250),(250,274),(214,284),(177,284),(390,274),(424,250),(463,249),(495,267),(463,284),(426,284),
(231,465),(269,444),(300,437),(320,443),(340,437),(371,444),(409,465),(374,488),(343,501),(320,503),(297,501),(266,488),
(252,465),(294,457),(320,460),(346,457),(388,465),(346,477),(320,481),(294,477)]
e68=[]
for seq,g,close in [(range(17),'contour',False),(range(17,22),'brows',False),(range(22,27),'brows',False),(range(27,31),'nose',False),(range(30,36),'nose',False),([30,35],'nose',False),(range(36,42),'eyes',True),(range(42,48),'eyes',True),(range(48,60),'mouth',True),(range(60,68),'mouth',True)]:e68+=chain(seq,g,close)
d68=dict(key='landmarks-68',title='68 / Feature contours',subtitle='dlib / iBUG indexing · original schematic geometry',nodes=[dict(id=i,x=x,y=y,group=group68(i)) for i,(x,y) in enumerate(p68)],edges=e68,groups=['contour','brows','eyes','nose','mouth'],note='17 jaw / 10 brow / 12 eye / 9 nose / 20 lip points.',detail='Official index groups and drawing connections; positions are illustrative.',source='https://github.com/davisking/dlib/blob/master/dlib/image_processing/render_face_detections.h',provenance='Original drawn face; not a canonical mean shape or inference output.')
# Approximate pixel centres manually read from the official-linked 106 markup.
p106=[(319,694),(51,165),(128,501),(147,536),(168,570),(187,603),(211,636),(239,665),(274,687),(49,204),(50,243),(53,282),(60,320),(68,358),(80,397),(94,431),(111,468),(581,162),(512,503),(493,538),(474,572),(452,604),(427,636),(399,666),(363,686),(585,201),(585,242),(583,280),(578,317),(571,356),(559,396),(546,432),(531,468),
(181,211),(183,202),(131,196),(154,205),(208,211),(181,194),(235,208),(182,181),(156,185),(211,190),
(91,117),(128,115),(169,114),(252,132),(212,119),(123,82),(169,76),(257,106),(218,86),
(234,529),(319,627),(268,566),(245,575),(272,612),(366,566),(391,573),(365,612),(318,583),(402,527),(318,492),(291,465),(253,486),(241,529),(271,502),(344,465),(382,486),(390,529),(366,502),(318,470),
(317,193),(318,248),(319,303),(270,213),(251,333),(236,378),(260,394),(289,400),(318,410),(363,214),(385,332),(403,378),(378,394),(350,400),(319,359),
(445,211),(445,198),(396,211),(422,212),(474,208),(445,201),(499,196),(446,183),(416,190),(475,185),
(383,137),(425,125),(467,122),(503,121),(543,122),(378,111),(418,93),(467,81),(512,89)]
assert len(p106)==106

def group106(i):
    return 'contour' if i<33 else 'eyes' if i<43 else 'brows' if i<52 else 'mouth' if i<72 else 'nose' if i<87 else 'eyes' if i<97 else 'brows'
d106=dict(key='landmarks-106',title='106 / Dense feature sampling',subtitle='InsightFace 2d106 · manual trace of official-linked markup',nodes=[dict(id=i,x=x,y=y,group=group106(i)) for i,(x,y) in enumerate(p106)],edges=[],groups=['contour','brows','eyes','nose','mouth'],note='33 contour / 18 brow / 20 eye / 15 nose / 20 mouth.',detail='Approximate diagram positions. No invented edge topology.',source='https://github.com/deepinsight/insightface/tree/master/alignment/coordinate_reg',provenance='Manual approximate trace of nttstar/insightface-resources/alignment/images/2d106markup.jpg, linked by the official README. Mouth corner labels are crowded in that reference; positions are approximate. Region colors are explanatory annotations.')
# Orthographic front projection of Google's actual 468-vertex canonical model.
verts=[list(map(float,line.split()[1:])) for line in (REF/'canonical_face_model.obj').read_text().splitlines() if line.startswith('v ')]
assert len(verts)==468
connections=(REF/'face_landmarks_connections.ts').read_text()
sets={}
for name,body in re.findall(r'export const FACE_LANDMARKS_(\w+)\s*=\s*convertToConnections\((.*?)\);',connections,re.S):
    sets[name]=[tuple(map(int,p)) for p in re.findall(r'\[(\d+),\s*(\d+)\]',body)]
nodegroups={}; me=[]
for name,g in [('FACE_OVAL','contour'),('LEFT_EYEBROW','brows'),('RIGHT_EYEBROW','brows'),('LEFT_EYE','eyes'),('RIGHT_EYE','eyes'),('LIPS','mouth')]:
    for a,b in sets[name]:me.append(dict(a=a,b=b,group=g));nodegroups[a]=g;nodegroups[b]=g
meshEdges=[dict(a=a,b=b,group='mesh') for a,b in sorted(set(tuple(sorted(p)) for p in sets['TESSELATION']))]
meshNodes=[dict(id=i,x=x,y=-y,z=z,group=nodegroups.get(i,'mesh')) for i,(x,y,z) in enumerate(verts)]
mesh=dict(key='mesh-468',title='468 / Surface mesh',subtitle='MediaPipe canonical model · orthographic front projection',nodes=meshNodes,edges=meshEdges+me,groups=['contour','brows','eyes','mouth'],note='Official vertex coordinates and landmark connections.',detail='A static canonical model; not a detected person or identity signature.',source='https://github.com/google-ai-edge/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model.obj',provenance='Canonical OBJ x/y projected to 2D (y inverted); original z retained in JSON. Edges from official FaceLandmarksConnections. Apache-2.0; © MediaPipe Authors.')
# The canonical OBJ has no iris vertices. Explicit schematic additions, not fabricated source data.
iris=json.loads(json.dumps(mesh));iris.update(key='mesh-478-study',title='478 / Iris extension study',subtitle='468 source vertices + 10 schematic iris landmarks',note='468 + 5 + 5: one centre and four boundary points per iris.',detail='Orange iris positions are constructed; the canonical OBJ contains 468 points.',provenance='Canonical 468 base plus schematic iris positions. Iris IDs and boundary connections follow official definitions; positions are not model predictions or canonical data.')
by={n['id']:n for n in meshNodes}
for center_id,left,right,top,bottom in [(468,33,133,159,145),(473,362,263,386,374)]:
    cx=(by[left]['x']+by[right]['x'])/2;cy=(by[top]['y']+by[bottom]['y'])/2
    r=abs(by[top]['y']-by[bottom]['y'])*.36
    for j,(dx,dy) in enumerate([(0,0),(r,0),(0,-r),(-r,0),(0,r)]):
        iris['nodes'].append(dict(id=center_id+j,x=cx+dx,y=cy+dy,group='iris',synthetic=True))
iris['edges']+= [dict(a=a,b=b,group='iris') for name in ['LEFT_IRIS','RIGHT_IRIS'] for a,b in sets[name]]
iris['groups']=['contour','eyes','mouth','iris']

def text(x,y,content,size=14,color='#62685f',extra=''):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}" {extra}>{html.escape(content)}</text>'

def draw(d,numbered=False):
    dense=len(d['nodes'])>200;ns=d['nodes'];minx=min(n['x'] for n in ns);maxx=max(n['x'] for n in ns);miny=min(n['y'] for n in ns);maxy=max(n['y'] for n in ns)
    scale=min(490/(maxx-minx),520/(maxy-miny));tx=330-(minx+maxx)/2*scale;ty=370-(miny+maxy)/2*scale
    xy={n['id']:(n['x']*scale+tx,n['y']*scale+ty) for n in ns}
    parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 820" width="660" height="820" role="img" aria-labelledby="title desc">',f'<title id="title">{html.escape(d["title"])}</title><desc id="desc">{html.escape(d["provenance"])}</desc>','<rect width="660" height="820" fill="#f6f4ed"/>',text(30,41,d['title'],26,'#202321'),text(30,70,d['subtitle'],13)]
    if d['key']=='alignment-5':
        # Measurement guides are explanatory; point-only templates have no edges.
        for a,b in [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]:
            x,y=xy[a];u,v=xy[b];parts.append(f'<path d="M{x},{y}L{u},{v}" stroke="#c1bcb0" stroke-dasharray="4 7" fill="none"/>')
    for e in d['edges']:
        x,y=xy[e['a']];u,v=xy[e['b']];g=e['group'];width=.75 if g=='mesh' else 1.8
        parts.append(f'<path d="M{x:.3f},{y:.3f}L{u:.3f},{v:.3f}" fill="none" stroke="{C[g]}" stroke-width="{width}"/>')
    for n in ns:
        x,y=xy[n['id']];g=n['group'];rad=1.75 if dense else 3.8 if len(ns)>10 else 8
        parts.append(f'<circle data-node="{n["id"]}" cx="{x:.3f}" cy="{y:.3f}" r="{rad}" fill="{C[g]}" stroke="#f6f4ed" stroke-width="{.4 if dense else 1}"><title>{n["id"]} / {g}</title></circle>')
        if numbered:
            # Alternate offsets where the official 106 eye centre labels are crowded.
            dx,dy=(4,-4)
            if d['key']=='landmarks-106' and n['id'] in [34,88]:dx,dy=(-8,15)
            if d['key']=='landmarks-106' and n['id'] in [65,69]:dx,dy=(0,15)
            parts.append(text(round(x+dx,2),round(y+dy,2),str(n['id']),6 if dense else 10,C[g], 'style="paint-order:stroke;stroke:#f6f4ed;stroke-width:2px;stroke-linejoin:round"'))
    if d['key']=='alignment-5':
        for i,label in enumerate(['Eye centre','Eye centre','Nose','Mouth corner','Mouth corner']):
            x,y=xy[i];parts.append(text(x,y+29,label,14,C[ns[i]['group']],'text-anchor="middle"'))
    if d['key']=='mesh-478-study':
        # Enlarged inset makes the 10 added points legible without distorting the main mesh.
        parts.append('<rect x="490" y="564" width="146" height="102" rx="8" fill="#f6f4ed" stroke="#cecec2"/>')
        parts.append(text(503,580,'IRIS DETAIL × 2',10))
        for i,(dx,dy) in enumerate([(0,0),(24,0),(0,-18),(-24,0),(0,18)]):
            x,y=563+dx,618+dy;parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{C["iris"]}"/>')
        parts.append('<path d="M587 618L563 600L539 618L563 636Z" fill="none" stroke="#cf5a30"/>')
        parts.append(text(503,654,'centre + 4 boundary points',8))
    for i,g in enumerate(d['groups']):
        x=30+i*122;parts.append(f'<circle cx="{x+4}" cy="697" r="4" fill="{C[g]}"/>');parts.append(text(x+15,702,g.title(),12))
    parts.extend([text(30,742,d['note'],13,'#202321'),text(30,768,d['detail'],11),text(30,793,'SOURCE: '+('InsightFace' if d['key'] in ['alignment-5','landmarks-106'] else 'dlib' if d['key']=='landmarks-68' else 'Google MediaPipe')+' / see linked reference and JSON provenance',10)])
    parts.append('</svg>');return ''.join(parts)

systems=[five,d68,d106,mesh,iris]
for d in systems:
    assert len({n['id'] for n in d['nodes']})==len(d['nodes'])
    ids={n['id'] for n in d['nodes']}
    assert all(e['a'] in ids and e['b'] in ids for e in d['edges'])
    (DATA/(d['key']+'.json')).write_text(json.dumps(d,indent=2)+'\n')
    for numbered in [False,True]:
        (OUT/(d['key']+('-numbered' if numbered else '')+'.svg')).write_text(draw(d,numbered))
    print(d['key'],len(d['nodes']),'nodes',len(d['edges']),'rendered edges')

# Original label-map schematic; category IDs follow the official parsing README.
labels=['Background','Skin','Nose','Eyeglasses','Left eye','Right eye','Left brow','Right brow','Left ear','Right ear','Mouth','Upper lip','Lower lip','Hair','Hat','Earring','Necklace','Neck','Cloth']
colors=['#e9e8df','#dabd94','#d9994f','#3c535e','#4994ac','#70adbe','#8974a2','#aa8fae','#82a48e','#a2b89a','#623f4f','#b66779','#d78a96','#726b82','#607d8b','#d39a39','#bea948','#b8a48b','#8b9d99']
mask=['<svg xmlns="http://www.w3.org/2000/svg" width="660" height="820" viewBox="0 0 660 820" role="img" aria-labelledby="title desc"><title id="title">19 / Semantic labels</title><desc id="desc">Original schematic showing the CelebAMask-HQ class IDs including background, skin, nose, glasses, eyes, brows, ears, mouth, lips, hair, hat, earring, necklace, neck and clothing. It is not a segmentation model output.</desc><rect width="660" height="820" fill="#f6f4ed"/>',text(30,41,'19 / Semantic labels',26,'#202321'),text(30,70,'CelebAMask-HQ label IDs · original region schematic',13)]
def path(d,i):return f'<path d="{d}" fill="{colors[i]}" stroke="#f6f4ed" stroke-width="2"><title>{i}: {labels[i]}</title></path>'
def ellipse(x,y,rx,ry,i):return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{colors[i]}" stroke="#f6f4ed" stroke-width="2"><title>{i}: {labels[i]}</title></ellipse>'
mask+=['<rect x="25" y="115" width="370" height="557" rx="8" fill="#e9e8df"/>',path('M36 671L61 585Q205 532 350 585L384 671Z',18),path('M161 476L155 573Q210 613 263 573L260 476Z',17),path('M168 564Q211 602 257 564L263 577Q213 625 158 579Z',16),path('M75 339Q41 159 212 159Q380 161 349 361L335 524L292 578L281 459L135 459L124 559L78 493Z',13),ellipse(83,374,20,54,9),ellipse(338,374,20,54,8),path('M209 223Q92 215 96 345L103 430Q125 511 209 544Q293 511 317 430L323 345Q327 215 209 223Z',1),path('M192 322L225 322L243 431Q207 449 177 431Z',2),ellipse(154,367,35,15,5),ellipse(264,367,35,15,4),path('M117 327Q153 305 190 329L186 340Q154 326 120 339Z',7),path('M229 329Q266 305 301 327L298 339Q264 326 232 340Z',6),path('M110 346H194V387H110ZM116 353V380H188V353ZM224 346H308V387H224ZM230 353V380H302V353Z',3),path('M194 355Q209 350 224 355L224 362Q209 357 194 362Z',3),path('M165 482Q187 458 209 467Q231 458 254 482Q209 478 165 482Z',11),path('M165 482Q209 523 254 482Q209 490 165 482Z',12),ellipse(209,484,36,7,10),path('M107 229Q99 202 140 189Q212 163 282 195L310 257Q267 242 220 233Q156 246 110 296Z',13),path('M94 196L113 142Q210 110 308 144L327 197L351 214Q212 195 68 222L76 204Z',14),ellipse(83,438,8,15,15)]
for i,name in enumerate(labels):
    yy=135+i*28;mask.append(f'<rect x="421" y="{yy-12}" width="13" height="13" rx="2" fill="{colors[i]}"/>');mask.append(text(445,yy,f'{i:02} / {name}',13,'#202321'))
mask += [text(30,709,'One label per pixel; accessories and background are classes too.',13,'#202321'),text(30,739,'Shapes and colors are illustrative; this is not a model prediction.',12),text(30,766,'Left/right labels follow the subject, not the viewer.',12),text(30,793,'SOURCE: official CelebAMask-HQ / face_parsing label definitions',10),'</svg>']
(OUT/'parsing-19.svg').write_text(''.join(mask))
(DATA/'parsing-19.json').write_text(json.dumps(dict(provenance='Original schematic shapes; official category IDs. Not an inference result.',source='https://github.com/switchablenorms/CelebAMask-HQ/blob/master/face_parsing/README.md',classes=[dict(id=i,label=label,color=colors[i]) for i,label in enumerate(labels)]),indent=2)+'\n')
# Single portable board with all six diagrams.
board=['<svg xmlns="http://www.w3.org/2000/svg" width="1980" height="1860" viewBox="0 0 1980 1860"><rect width="1980" height="1860" fill="#f6f4ed"/>',text(35,50,'FACE / COMPUTATIONAL STRUCTURES',27,'#202321'),text(35,82,'Alignment → feature sampling → surface topology → pixel regions. These drawings do not perform identity verification.',17)]
for i,key in enumerate([d['key'] for d in systems]+['parsing-19']):
    data=base64.b64encode((OUT/(key+'.svg')).read_bytes()).decode();x=(i%3)*650+15;y=(i//3)*840+105
    board.append(f'<image x="{x}" y="{y}" width="650" height="807.6" href="data:image/svg+xml;base64,{data}"/>')
board+=[text(35,1808,'Sources: InsightFace / dlib / Google MediaPipe / CelebAMask-HQ. Exactness and schematic additions are labeled on each panel.',16),text(35,1838,'Course study • Full references and reusable coordinate data: ixthecreator.github.io/fall-2026-lab/collage/studies/#structures',15),'</svg>']
(OUT/'system-structures.svg').write_text(''.join(board))
