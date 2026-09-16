"""Build reproducible flat and bilateral design studies from manual image traces.
No face detector is run. Source coordinates remain in photograph pixel space.
"""
from pathlib import Path
import json, copy, base64, html
ROOT = Path(__file__).parent
ARCHIVE = 'https://tonyoursler.com/templatevariantfriendstranger-london'
def save(name, data):
    (ROOT / 'layouts' / name).write_text(json.dumps(data, indent=2) + '\n')
def trace(key, title, points, edges, pairs, centers, axis, image, size, crop, color):
    nodes = [dict(id=f'n{i+1:02}', x=x, y=y, color=color, label=label,
                  provenance='manual visible-marker trace') for i,(x,y,label) in enumerate(points)]
    return dict(key=key,title=title,nodes=nodes,
        edges=[dict(a=f'n{a:02}',b=f'n{b:02}',color=color,uncertain=bool(u)) for a,b,u in edges],
        pairs=[[f'n{a:02}',f'n{b:02}'] for a,b in pairs],centers=[f'n{i:02}' for i in centers],axis=axis,
        image=image,imageSize=size,crop=crop,source=ARCHIVE,
        note='Manual visual study; approximate coordinates. Uncaptioned artwork uses a descriptive study label, not an authenticated title. Dashed source edges are uncertain across occlusions.')
vie=json.loads((ROOT/'layouts/vie-preserved.json').read_text())
vie.update(key='vie',title='VIE / preserved layout',image='../../assets/oursler-vie.jpg',imageSize=[749,1000],crop=[150,300,445,420],axis=374,
    pairs=[['n01','n06'],['n02','n05'],['n08','n04'],['n07','n10'],['n11','n13'],['n14','n15'],['n16','n18'],['n19','n20'],['n21','n22']],
    centers=['n03','n09','n17'],source='https://www.lissongallery.com/artists/tony-oursler/artworks/vie?image_id=8831',
    note='Exact copy of the existing 22-node / 39-edge site layout. Earlier reconstruction includes inferred occluded connections; not a fresh measurement.')
# Edges which cross the eye windows are uncertain in the preserved reconstruction.
for e in vie['edges']:
    e['uncertain']=tuple(sorted([e['a'],e['b']])) in {('n07','n08'),('n07','n11'),('n08','n12'),('n04','n10'),('n05','n10'),('n06','n10'),('n10','n15')}
red=trace('red','Red portrait / radial graph',[
(401,305,'Left upper stem'),(484,303,'Right upper stem'),(336,335,'Left outer brow'),(401,335,'Left brow'),(417,341,'Left inner brow'),(444,342,'Centre brow'),(554,336,'Right outer brow'),(445,374,'Upper bridge'),(445,386,'Lower bridge'),(331,384,'Left middle extension'),(571,388,'Right middle extension'),(341,423,'Left lower extension'),(563,428,'Right lower extension'),(445,463,'Chin convergence'),(446,536,'Lower axis')],
[(1,4,0),(1,6,0),(2,6,1),(3,4,0),(4,5,0),(5,6,0),(6,7,1),(6,8,0),(4,8,0),(8,2,1),(8,9,0),(10,9,0),(9,11,0),(12,13,1),(4,14,1),(5,14,1),(2,14,1),(9,14,1),(14,15,0)],
[(1,2),(3,7),(10,11),(12,13)],[6,8,9,14,15],445,'../references/lisson-03.jpg',[960,720],[310,280,280,285],'#b57414')
blue=trace('blue','Blue mask / incised lattice',[
(294,356,'Left upper stem'),(650,358,'Right upper stem'),(300,464,'Left outer brow'),(377,457,'Left inner brow'),(467,472,'Centre brow'),(558,466,'Right inner brow'),(646,473,'Right outer brow'),(212,520,'Left temple'),(723,526,'Right temple'),(390,505,'Left upper eye'),(538,512,'Right upper eye'),(467,535,'Bridge'),(258,570,'Left outer eye'),(684,568,'Right outer eye'),(427,589,'Left nose bridge'),(519,591,'Right nose bridge'),(236,642,'Left outer cheek'),(698,654,'Right outer cheek'),(397,645,'Left inner cheek'),(518,655,'Right inner cheek'),(297,689,'Left lower cheek'),(643,702,'Right lower cheek'),(463,738,'Nose base'),(272,768,'Left outer jaw'),(652,788,'Right outer jaw'),(350,796,'Left middle jaw'),(554,807,'Right middle jaw'),(401,790,'Left inner jaw'),(505,763,'Right inner jaw'),(616,540,'Right inner eye')],
[(1,3,0),(2,7,0),(3,4,0),(4,5,0),(5,6,0),(6,7,0),(3,8,0),(7,9,0),(8,13,0),(8,17,0),(9,14,0),(9,18,0),(3,13,0),(3,10,1),(4,10,0),(5,10,0),(5,11,0),(6,11,0),(6,30,0),(7,30,0),(7,14,0),(10,12,0),(11,12,0),(11,30,0),(12,15,0),(12,16,0),(13,17,0),(14,18,0),(14,30,0),(15,19,0),(16,20,0),(16,30,0),(17,19,0),(17,21,0),(18,20,0),(18,22,0),(19,21,0),(19,23,0),(20,22,0),(20,23,0),(21,24,0),(21,26,0),(21,28,0),(22,25,0),(22,27,0),(22,29,0),(23,28,0),(23,29,0),(24,26,0),(26,28,0),(25,27,0),(27,29,0),(15,17,1)],
[(1,2),(3,7),(4,6),(8,9),(10,11),(13,14),(15,16),(17,18),(19,20),(21,22),(24,25),(26,27),(28,29)],[5,12,23],467,'../references/lisson-04.jpg',[960,1222],[180,320,570,530],'#2755b4')

def symmetrical(src):
    out=copy.deepcopy(src); out['nodes']=[]; c=src['axis']; by={n['id']:n for n in src['nodes']}; mirror={}; paired=set()
    for a,b in src['pairs']:
        left,right=by[a],by[b]; d=(abs(left['x']-c)+abs(right['x']-c))/2; y=(left['y']+right['y'])/2
        for n,x in [(left,c-d),(right,c+d)]:
            out['nodes'].append(dict(n,x=x,y=y,synthetic=False))
        mirror[a]=b;mirror[b]=a;paired.update([a,b])
    for k in src['centers']:
        out['nodes'].append(dict(by[k],x=c,synthetic=False));mirror[k]=k;paired.add(k)
    for k,n in by.items():
        if k not in paired:
            m=k+'m';out['nodes'] += [dict(n,synthetic=False),dict(n,id=m,x=2*c-n['x'],synthetic=True,label='Added mirror of '+k)]
            mirror[k]=m;mirror[m]=k
    es={tuple(sorted([e['a'],e['b']])):dict(e,synthetic=False) for e in src['edges']}
    for e in src['edges']:
        a,b=mirror[e['a']],mirror[e['b']];key=tuple(sorted([a,b]))
        if key not in es: es[key]=dict(e,a=a,b=b,synthetic=True)
    out['edges']=list(es.values());out['mirror']=mirror;out['note']='Bilateral design derivative: paired positions averaged, centre nodes aligned, unpaired nodes mirrored, and missing reflected edges added. This is not a recovered original or a detector template.'
    ns={n['id']:n for n in out['nodes']}
    for n in out['nodes']:
        m=ns[mirror[n['id']]]
        assert abs(n['x']+m['x']-2*c)<1e-9 and abs(n['y']-m['y'])<1e-9
    for e in out['edges']:
        assert tuple(sorted([mirror[e['a']],mirror[e['b']]])) in es
    return out

def svg(src, sym=False, photo=False, labels=False):
    x,y,w,h=src['crop']; pad=10
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x-pad} {y-pad} {w+pad*2} {h+pad*2}" role="img" aria-labelledby="title"><title id="title">{html.escape(src["title"])}: {"symmetrical design" if sym else "photo trace" if photo else "flat source layout"}</title>']
    s.append(f'<rect x="{x-pad}" y="{y-pad}" width="{w+pad*2}" height="{h+pad*2}" fill="#f6f4ed"/>')
    if photo:
        p=(ROOT/'exports'/src['image']).resolve();data=base64.b64encode(p.read_bytes()).decode()
        s.append(f'<image width="{src["imageSize"][0]}" height="{src["imageSize"][1]}" href="data:image/jpeg;base64,{data}" opacity=".72"/>')
    if sym:s.append(f'<path d="M {src["axis"]},{y} v {h}" stroke="#bab7b0" stroke-dasharray="3 7"/>')
    by={n['id']:n for n in src['nodes']};r=w/95;sw=w/280
    for e in src['edges']:
        a,b=by[e['a']],by[e['b']];color='#db6331' if e.get('synthetic') else '#938b7f' if e.get('uncertain') else '#202321' if sym else e['color']
        dash=f' stroke-dasharray="{sw*3} {sw*3}"' if e.get('synthetic') or e.get('uncertain') else ''
        s.append(f'<line x1="{a["x"]}" y1="{a["y"]}" x2="{b["x"]}" y2="{b["y"]}" stroke="{color}" stroke-width="{sw}"{dash}/>')
    for n in src['nodes']:
        color='#db6331' if n.get('synthetic') else '#202321' if sym else n['color']
        s.append(f'<circle cx="{n["x"]}" cy="{n["y"]}" r="{r}" fill="#f6f4ed" stroke="{color}" stroke-width="{sw}"><title>{n["id"]}: {html.escape(n["label"])}</title></circle>')
        if labels:s.append(f'<text x="{n["x"]+r*1.6}" y="{n["y"]-r*1.4}" font-family="monospace" font-size="{w/38}" fill="{color}">{n["id"][1:]}</text>')
    s.append('</svg>');return ''.join(s)

rows=[]
for src in [vie,red,blue]:
    sym=symmetrical(src); key=src['key']
    save(key+'-source.json',src);save(key+'-symmetric.json',sym)
    for kind,data,kwargs in [('photo',src,dict(photo=True)),('flat',src,dict()),('symmetric',sym,dict(sym=True)),('numbered',sym,dict(sym=True,labels=True))]:
        (ROOT/'exports'/f'{key}-{kind}.svg').write_text(svg(data,**kwargs))
    rows.append(dict(key=key,title=src['title'],nodes=len(src['nodes']),edges=len(src['edges']),symNodes=len(sym['nodes']),symEdges=len(sym['edges']),added=sum(n.get('synthetic',False) for n in sym['nodes'])))
    print(key,rows[-1])
(ROOT/'layouts/manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
# Standalone, image-embedded comparison board; references and limitations stay with export.
board=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1700" viewBox="0 0 1440 1700"><rect width="1440" height="1700" fill="#f6f4ed"/><style>text{font-family:Arial,sans-serif;fill:#202321}.small{font-size:17px;fill:#65685f}.label{font-size:20px}</style><text x="56" y="68" font-size="16" letter-spacing="3">FACE / STRUCTURE STUDIES — 01</text><text x="56" y="126" font-size="44">From observed nodes to bilateral order.</text><text x="56" y="164" class="small">Three layouts after Tony Oursler. Manual traces and design derivatives; not recognition models.</text>']
for i,title in enumerate(['01  SOURCE + TRACE','02  FLAT LAYOUT','03  SYMMETRICAL STUDY']): board.append(f'<text x="{56+i*450}" y="219" class="label">{title}</text>')
for j,row in enumerate(rows):
    yy=250+j*440;key=row['key']
    board.append(f'<text x="56" y="{yy}" class="label">{row["title"]}</text>')
    board.append(f'<text x="506" y="{yy}" class="small">{row["nodes"]} traced nodes</text><text x="956" y="{yy}" class="small">{row["symNodes"]} nodes / {row["added"]} added mirror(s)</text>')
    for i,kind in enumerate(['photo','flat','symmetric']):
        img=base64.b64encode((ROOT/'exports'/f'{key}-{kind}.svg').read_bytes()).decode()
        board.append(f'<image x="{56+i*450}" y="{yy+18}" width="410" height="372" href="data:image/svg+xml;base64,{img}"/>')
    board.append(f'<path d="M56 {yy+410}H1384" stroke="#cccac1"/>')
board += ['<text x="56" y="1598" class="small">Solid: traced structure. Grey dash: uncertain / occluded. Orange dash: added for bilateral symmetry.</text><text x="56" y="1630" class="small">Reference artworks © Tony Oursler. Artist archive: tonyoursler.com/templatevariantfriendstranger-london</text><text x="56" y="1662" class="small">Red and blue are descriptive labels. Blue mask belongs to the parallel panel series in the same 2015 exhibition.</text></svg>']
(ROOT/'exports/node-comparison.svg').write_text(''.join(board))
assert (ROOT/'layouts/vie-preserved.json').read_bytes() == (ROOT.parent/'network.json').read_bytes(), 'Original layout changed'
