
// ═══════════════ 3D IMPERIAL TIMELINE ═══════════════
// Horizontal timeline — emperors spread across time (X axis)
{
const DCOLORS={xia:'#8b7355',shang:'#a0785a','zhou-w':'#b8860b','zhou-e':'#c4a35a',qin:'#c43a31','han-w':'#dc2626',xin:'#654321','han-e':'#b91c1c',sanguo:'#2f4f4f','jin-w':'#556b2f','jin-e':'#6b8e23',nanbei:'#4a4a6a',sui:'#191970',tang:'#1d4ed8',wudai:'#5c4033','song-n':'#3b82f6','song-s':'#60a5fa',liao:'#3e2723',jin:'#4e342e',xixia:'#5d4037',yuan:'#22c55e',ming:'#ef4444',qing:'#a78bfa'};
const EMPERORS=[{name:'大禹',year:-2065,reign:'约前2070-前2060',dynasty:'xia',tagline:'治水定九州，开启家天下',cid:null},{name:'夏桀',year:-1600,reign:'约前1600',dynasty:'xia',tagline:'酒池肉林的原型，第一个亡国之君',cid:null},{name:'商汤',year:-1550,reign:'约前1600',dynasty:'shang',tagline:'顺天应人，革故鼎新',cid:null},{name:'商纣',year:-1046,reign:'约前1075-前1046',dynasty:'shang',tagline:'酒池肉林，炮烙之刑',cid:null},{name:'周武王',year:-1045,reign:'约前1046-前1043',dynasty:'zhou-w',tagline:'牧野之战灭商，八百载周朝',cid:null},{name:'周幽王',year:-771,reign:'前781-前771',dynasty:'zhou-w',tagline:'烽火戏诸侯，西周终结者',cid:null},{name:'齐桓公',year:-650,reign:'前685-前643',dynasty:'zhou-e',tagline:'春秋首霸，尊王攘夷',cid:null},{name:'秦始皇',year:-216,reign:'前221-前210',dynasty:'qin',tagline:'千古一帝。统一六国，功过皆极致',cid:7},{name:'胡亥',year:-209,reign:'前210-前207',dynasty:'qin',tagline:'被赵高操控，三年葬送大秦',cid:9},{name:'刘邦',year:-199,reign:'前202-前195',dynasty:'han-w',tagline:'布衣天子，亭长到皇帝的逆袭',cid:12},{name:'汉文帝',year:-169,reign:'前180-前157',dynasty:'han-w',tagline:'文景之治奠基者，以德化民',cid:14},{name:'汉武帝',year:-114,reign:'前141-前87',dynasty:'han-w',tagline:'雄才大略，开疆拓土',cid:15},{name:'汉宣帝',year:-61,reign:'前74-前48',dynasty:'han-w',tagline:'中兴之主，孝宣之治',cid:null},{name:'汉光武帝',year:41,reign:'25-57',dynasty:'han-e',tagline:'中兴汉室，柔道治国',cid:null},{name:'汉明帝',year:70,reign:'58-75',dynasty:'han-e',tagline:'永平求法，佛教东传之始',cid:null},{name:'汉献帝',year:200,reign:'189-220',dynasty:'han-e',tagline:'末代天子，一生为傀儡',cid:null},{name:'曹操',year:210,reign:'196-220执政',dynasty:'sanguo',tagline:'治世能臣，乱世奸雄',cid:null},{name:'刘备',year:218,reign:'221-223',dynasty:'sanguo',tagline:'弘毅宽厚，知人待士',cid:null},{name:'孙权',year:230,reign:'229-252',dynasty:'sanguo',tagline:'生子当如孙仲谋',cid:null},{name:'司马炎',year:270,reign:'265-290',dynasty:'jin-w',tagline:'三分归一统',cid:null},{name:'司马睿',year:320,reign:'317-323',dynasty:'jin-e',tagline:'衣冠南渡',cid:null},{name:'刘裕',year:420,reign:'420-422',dynasty:'nanbei',tagline:'气吞万里如虎，南朝第一帝',cid:null},{name:'孝文帝',year:485,reign:'471-499',dynasty:'nanbei',tagline:'迁都洛阳，全面汉化',cid:null},{name:'隋文帝',year:590,reign:'581-604',dynasty:'sui',tagline:'开皇之治，结束三百年分裂',cid:null},{name:'隋炀帝',year:609,reign:'604-618',dynasty:'sui',tagline:'大运河，科举制，功在千秋',cid:null},{name:'唐太宗',year:637,reign:'626-649',dynasty:'tang',tagline:'贞观之治，千古明君典范',cid:8},{name:'武则天',year:690,reign:'690-705',dynasty:'tang',tagline:'唯一女帝，上承贞观下启开元',cid:null},{name:'唐玄宗',year:720,reign:'712-756',dynasty:'tang',tagline:'开元盛世→安史之乱，盛极而衰',cid:null},{name:'宋太祖',year:965,reign:'960-976',dynasty:'song-n',tagline:'杯酒释兵权，以文治国',cid:null},{name:'宋仁宗',year:1040,reign:'1022-1063',dynasty:'song-n',tagline:'仁宗盛治，文人黄金时代',cid:null},{name:'岳飞',year:1135,reign:'南宋名将',dynasty:'song-s',tagline:'精忠报国，直捣黄龙未酬',cid:null},{name:'成吉思汗',year:1210,reign:'1206-1227',dynasty:'yuan',tagline:'一代天骄，世界征服者',cid:null},{name:'忽必烈',year:1275,reign:'1260-1294',dynasty:'yuan',tagline:'入主中原，建元大都',cid:null},{name:'朱元璋',year:1375,reign:'1368-1398',dynasty:'ming',tagline:'从乞丐到皇帝，洪武之治',cid:null},{name:'朱棣',year:1415,reign:'1402-1424',dynasty:'ming',tagline:'永乐盛世，五征漠北',cid:null},{name:'康熙',year:1680,reign:'1661-1722',dynasty:'qing',tagline:'千古一帝，奠定清朝版图',cid:null},{name:'雍正',year:1725,reign:'1722-1735',dynasty:'qing',tagline:'铁腕改革，承上启下',cid:null},{name:'乾隆',year:1770,reign:'1735-1796',dynasty:'qing',tagline:'十全武功，盛世巅峰',cid:null},{name:'溥仪',year:1912,reign:'1908-1912',dynasty:'qing',tagline:'末代皇帝，帝制终结',cid:null}];
const DYNASTIES=[{name:'夏',year:-2000,clr:'#8b7355'},{name:'商',year:-1550,clr:'#a0785a'},{name:'周',year:-1000,clr:'#b8860b'},{name:'春秋',year:-550,clr:'#c4a35a'},{name:'秦',year:-215,clr:'#c43a31'},{name:'汉',year:-100,clr:'#dc2626'},{name:'三国',year:230,clr:'#2f4f4f'},{name:'晋',year:300,clr:'#556b2f'},{name:'南北朝',year:480,clr:'#4a4a6a'},{name:'隋',year:590,clr:'#191970'},{name:'唐',year:700,clr:'#1d4ed8'},{name:'五代',year:930,clr:'#5c4033'},{name:'宋',year:1050,clr:'#3b82f6'},{name:'元',year:1270,clr:'#22c55e'},{name:'明',year:1500,clr:'#ef4444'},{name:'清',year:1800,clr:'#a78bfa'}];
const Y_MIN=-2100,Y_MAX=1920,Y_SPAN=Y_MAX-Y_MIN,TL_LEN=32;
function yrX(y){return((y-Y_MIN)/Y_SPAN-0.5)*TL_LEN}

const section=document.getElementById('timeline3d');
if(!section){console.warn('3D timeline section not found')} else {
import('three').then(({default:THREE})=>{
import('three/addons/controls/OrbitControls.js').then(({OrbitControls})=>{

const scene=new THREE.Scene();
scene.background=new THREE.Color('#050510');
scene.fog=new THREE.FogExp2('#050510',0.0001);

const cam=new THREE.PerspectiveCamera(55,section.clientWidth/section.clientHeight,0.5,60);
cam.position.set(0,3,18);cam.lookAt(0,0,0);

const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
renderer.setSize(section.clientWidth,section.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.1;
section.appendChild(renderer.domElement);

// Lights
scene.add(new THREE.AmbientLight('#1a1a3a',0.55));
const gLight=new THREE.PointLight('#e2b64f',70,30,1.5);gLight.position.set(0,2,0);scene.add(gLight);
const lLight=new THREE.PointLight('#c43a31',10,12,2);lLight.position.set(-14,0,0);scene.add(lLight);
const rLight=new THREE.PointLight('#c43a31',10,12,2);rLight.position.set(14,0,0);scene.add(rLight);
const fLight=new THREE.PointLight('#f5d98a',20,18,2);fLight.position.set(0,0,8);scene.add(fLight);

// Controls — optimized for horizontal panning
const ctrl=new OrbitControls(cam,renderer.domElement);
ctrl.enableDamping=true;ctrl.dampingFactor=0.08;
ctrl.minDistance=6;ctrl.maxDistance=28;
ctrl.maxPolarAngle=Math.PI*0.52;ctrl.minPolarAngle=Math.PI*0.28;
ctrl.autoRotate=true;ctrl.autoRotateSpeed=0.15;
ctrl.target.set(0,0,0);ctrl.update();

// Stars
const sGeo=new THREE.BufferGeometry();
const sPos=new Float32Array(2000*3),sSiz=new Float32Array(2000);
for(let i=0;i<2000;i++){sPos[i*3]=(Math.random()-0.5)*40;sPos[i*3+1]=(Math.random()-0.4)*12;sPos[i*3+2]=(Math.random()-0.5)*24;sSiz[i]=Math.random()*2.2}
sGeo.setAttribute('position',new THREE.BufferAttribute(sPos,3));
sGeo.setAttribute('size',new THREE.BufferAttribute(sSiz,1));
const stars=new THREE.Points(sGeo,new THREE.PointsMaterial({color:'#e2b64f',size:0.022,transparent:true,opacity:0.4,blending:THREE.AdditiveBlending,depthWrite:false}));
scene.add(stars);

// Main horizontal track — glowing tube spanning 4000 years
const trackGeo=new THREE.CylinderGeometry(0.06,0.06,TL_LEN,16);
const trackMat=new THREE.MeshStandardMaterial({color:'#b8860b',emissive:'#e2b64f',emissiveIntensity:0.5,metalness:0.9,roughness:0.2});
const track=new THREE.Mesh(trackGeo,trackMat);
track.rotation.z=Math.PI/2; // horizontal
scene.add(track);

// Track ambient glow
const glowGeo=new THREE.CylinderGeometry(0.18,0.18,TL_LEN,16,1,true);
const glowMesh=new THREE.Mesh(glowGeo,new THREE.MeshBasicMaterial({color:'#e2b64f',transparent:true,opacity:0.035,side:THREE.DoubleSide,depthWrite:false}));
glowMesh.rotation.z=Math.PI/2;scene.add(glowMesh);

// Dynasty divider markers — vertical bars along the track
DYNASTIES.forEach(d=>{
  const x=yrX(d.year),c=new THREE.Color(d.clr);
  // Thin vertical marker
  const barGeo=new THREE.BoxGeometry(0.02,0.9,0.02);
  const bar=new THREE.Mesh(barGeo,new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:0.35}));
  bar.position.set(x,0,0);scene.add(bar);
  // Small ring at top
  const ring=new THREE.Mesh(new THREE.TorusGeometry(0.16,0.015,8,20),new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:0.4}));
  ring.position.set(x,0.5,0);scene.add(ring);
});

// Glow texture
function mkGlow(c){
  const cv=document.createElement('canvas');cv.width=64;cv.height=64;
  const ctx=cv.getContext('2d'),g=ctx.createRadialGradient(32,32,0,32,32,32);
  g.addColorStop(0,c.getStyle());g.addColorStop(0.3,c.clone().multiplyScalar(0.5).getStyle());
  g.addColorStop(1,'transparent');ctx.fillStyle=g;ctx.fillRect(0,0,64,64);
  return new THREE.CanvasTexture(cv);
}

// Emperor nodes — spread along X axis with Y/Z offsets for visual rhythm
const empMeshes=[];
EMPERORS.forEach((e,i)=>{
  const x=yrX(e.year);
  const yDir=i%2===0?1:-1;
  const yOff=0.4+Math.sin(i*1.7)*0.3;
  const zOff=Math.cos(i*0.9)*0.5;
  const dc=DCOLORS[e.dynasty]||'#e2b64f',color=new THREE.Color(dc);
  const size=e.cid!==null?0.13:0.08;
  const node=new THREE.Mesh(new THREE.SphereGeometry(size,12,12),new THREE.MeshStandardMaterial({color:color,emissive:color,emissiveIntensity:0.5,metalness:0.7,roughness:0.2}));
  node.position.set(x,yOff*yDir,zOff);node.userData={e:e,i:i};scene.add(node);empMeshes.push(node);
  // Connector to track
  const lg=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(x,yOff*yDir,zOff),new THREE.Vector3(x,0,0)]);
  scene.add(new THREE.Line(lg,new THREE.LineBasicMaterial({color:color,transparent:true,opacity:0.07,depthWrite:false})));
  // Glow sprite
  const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:mkGlow(color),blending:THREE.AdditiveBlending,transparent:true,opacity:0.35,depthWrite:false}));
  sp.position.copy(node.position);sp.scale.set(0.55,0.55,1);scene.add(sp);
});

// Floating particles along the horizontal band
const pCount=500,pGeo=new THREE.BufferGeometry();
const pPos=new Float32Array(pCount*3),pVel=[];
for(let i=0;i<pCount;i++){
  const x=(Math.random()-0.5)*TL_LEN,y=(Math.random()-0.5)*2,z=(Math.random()-0.5)*2;
  pPos[i*3]=x;pPos[i*3+1]=y;pPos[i*3+2]=z;
  pVel.push({sp:0.005+Math.random()*0.02,x:x,y:y,z:z,dir:Math.random()>0.5?1:-1});
}
pGeo.setAttribute('position',new THREE.BufferAttribute(pPos,3));
const particles=new THREE.Points(pGeo,new THREE.PointsMaterial({color:'#f5d98a',size:0.03,blending:THREE.AdditiveBlending,transparent:true,opacity:0.4,depthWrite:false}));
scene.add(particles);

// Raycaster
const raycaster=new THREE.Raycaster();
raycaster.params.Points.threshold=0.25;
const mouse=new THREE.Vector2();
let hovered=null;
const info=document.getElementById('tl3dInfo');
const iDyn=document.getElementById('tl3dDynasty');
const iName=document.getElementById('tl3dName');
const iReign=document.getElementById('tl3dReign');
const iDesc=document.getElementById('tl3dDesc');
const yrEl=document.getElementById('tl3dYear');

function showInfo(emp){
  if(!emp){info.classList.remove('on');hovered=null;section.style.cursor='grab';return}
  const e=emp.userData.e,dc=DCOLORS[e.dynasty]||'#e2b64f';
  iDyn.textContent=e.dynasty.toUpperCase();iDyn.style.background=dc+'22';iDyn.style.color=dc;iDyn.style.border='1px solid '+dc+'44';
  iName.textContent=e.name;iReign.textContent=e.reign;iDesc.textContent=e.tagline;
  info.classList.add('on');section.style.cursor='pointer';
}

function onMove(ev){
  mouse.x=(ev.clientX/window.innerWidth)*2-1;mouse.y=-(ev.clientY/window.innerHeight)*2+1;
  raycaster.setFromCamera(mouse,cam);
  const hits=raycaster.intersectObjects(empMeshes);
  if(hits.length>0){
    const obj=hits[0].object;
    if(hovered!==obj){
      if(hovered){hovered.material.emissiveIntensity=0.5;hovered.scale.set(1,1,1)}
      hovered=obj;hovered.material.emissiveIntensity=1.2;hovered.scale.set(1.6,1.6,1.6);
      showInfo(obj);
    }
  }else{if(hovered){hovered.material.emissiveIntensity=0.5;hovered.scale.set(1,1,1);hovered=null}showInfo(null)}
}

function onClick(){
  if(hovered&&hovered.userData.e.cid){window.location.href='courses.html?course='+hovered.userData.e.cid}
}
window.addEventListener('mousemove',onMove,{passive:true});
window.addEventListener('click',onClick);
window.addEventListener('touchmove',e=>{if(e.touches.length===1)onMove(e.touches[0])},{passive:true});
window.addEventListener('touchend',onClick);

// Animate
const clock=new THREE.Clock();
function animate(){
  requestAnimationFrame(animate);
  const dt=Math.min(clock.getDelta(),0.1),t=performance.now()*0.001;
  ctrl.update();
  stars.rotation.y+=dt*0.02;stars.rotation.x+=dt*0.005;
  // Float particles
  const pA=pGeo.attributes.position.array;
  for(let i=0;i<pCount;i++){const v=pVel[i];v.y+=v.sp*v.dir;if(Math.abs(v.y)>1)v.dir*=-1;pA[i*3]=v.x+Math.sin(t+v.x*0.5)*0.12;pA[i*3+1]=v.y;pA[i*3+2]=v.z+Math.cos(t+v.x*0.5)*0.1;}
  pGeo.attributes.position.needsUpdate=true;
  gLight.intensity=70*(1+Math.sin(t*0.5)*0.1);
  // Year display from camera X position
  const apY=Math.round(Y_MIN+(cam.position.x/TL_LEN+0.5)*Y_SPAN);
  yrEl.textContent=apY<0?'前'+Math.abs(apY)+'年':'公元'+apY+'年';
  renderer.render(scene,cam);
}
animate();

window.addEventListener('resize',()=>{
  cam.aspect=section.clientWidth/section.clientHeight;cam.updateProjectionMatrix();
  renderer.setSize(section.clientWidth,section.clientHeight);
});

// Keyboard shortcuts — jump to major dynasties
window.addEventListener('keydown',e=>{
  const k=e.key.toLowerCase();
  if(k==='r')ctrl.autoRotate=!ctrl.autoRotate;
  else if(k==='q'||k==='1'){ctrl.target.set(yrX(-216),0,0);ctrl.update()}
  else if(k==='h'||k==='2'){ctrl.target.set(yrX(-100),0,0);ctrl.update()}
  else if(k==='t'||k==='3'){ctrl.target.set(yrX(637),0,0);ctrl.update()}
  else if(k==='m'||k==='4'){ctrl.target.set(yrX(1375),0,0);ctrl.update()}
  else if(k==='0'){ctrl.target.set(0,0,0);cam.position.set(0,3,18);ctrl.update()}
});

}).catch(e=>console.error('OrbitControls load failed:',e));
}).catch(e=>console.error('Three.js load failed:',e));
}
}
