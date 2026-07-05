/* ============================================================
   PIGMENT — app engine
   hash router · page renderers · search · generative covers
   ============================================================ */
(function(){
"use strict";

/* ---------------- data lookups ---------------- */
const A = window.ARTISTS, M = window.MOVEMENTS, T = window.TECHNIQUES,
      E = window.ERAS, N = window.NATIONS;
const byId = list => Object.fromEntries(list.map(x => [x.id, x]));
const Mx = byId(M), Tx = byId(T), Ex = byId(E), Nx = byId(N), Ax = byId(A);

const movChildren = id => M.filter(m => m.parent === id);
const tecChildren = id => T.filter(t => t.parent === id);
function descendants(id, list){ // id + all sub-branch ids
  const out = [id];
  list.filter(x => x.parent === id).forEach(c => out.push(...descendants(c.id, list)));
  return out;
}
const artistsOfMovement  = id => { const ids = descendants(id, M); return A.filter(a => a.movements.some(m => ids.includes(m))); };
const artistsOfTechnique = id => { const ids = descendants(id, T); return A.filter(a => a.techniques.some(t => ids.includes(t))); };
const artistsOfEra    = id => A.filter(a => a.eras.includes(id));
const artistsOfNation = id => A.filter(a => a.nation === id);

/* ---------------- tiny utils ---------------- */
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function hashStr(s){ let h = 2166136261; for(let i=0;i<s.length;i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
function mulberry(seed){ let a = seed; return function(){ a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function hex2rgb(hx){ const v = hx.replace("#",""); return [parseInt(v.slice(0,2),16), parseInt(v.slice(2,4),16), parseInt(v.slice(4,6),16)]; }
function rgba(hx, a){ const [r,g,b] = hex2rgb(hx); return `rgba(${r},${g},${b},${a})`; }
function shade(hx, f){ const [r,g,b] = hex2rgb(hx); const m = v => Math.max(0, Math.min(255, Math.round(v*f))); return `rgb(${m(r)},${m(g)},${m(b)})`; }
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ============================================================
   GENERATIVE COVER PAINTERS — one per style family
   each: (ctx, w, h, P[5 colours], R rng)
   ============================================================ */
const PAINTERS = {

renaissance(ctx,w,h,P,R){
  const g = ctx.createLinearGradient(0,0,0,h);
  g.addColorStop(0, shade(P[4],0.7)); g.addColorStop(1, shade(P[4],0.35));
  ctx.fillStyle = g; ctx.fillRect(0,0,w,h);
  const cx = w*(0.26+R()*0.48), cy = h*(0.28+R()*0.24);               /* divine light, seeded */
  const glow = ctx.createRadialGradient(cx,cy,10, cx,cy, w*(0.36+R()*0.3));
  glow.addColorStop(0, rgba(P[2],0.95)); glow.addColorStop(0.55, rgba(P[1],0.45)); glow.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = glow; ctx.fillRect(0,0,w,h);
  const figs = 1 + Math.floor(R()*2);                                 /* haloed, robed figures */
  for(let i=0;i<figs;i++){
    const fx = cx + (i ? (R()-0.5)*w*0.34 : (R()-0.5)*w*0.08);
    const fw = w*(0.06+R()*0.045), top = cy + h*(0.06+R()*0.1), base = h*(0.86+R()*0.1);
    ctx.fillStyle = rgba(P[i%2 ? 3 : 0], 0.78);
    ctx.beginPath(); ctx.moveTo(fx, top);
    ctx.bezierCurveTo(fx+fw, top+(base-top)*0.35, fx+fw*1.5, base-(base-top)*0.2, fx+fw*1.25, base);
    ctx.lineTo(fx-fw*1.25, base);
    ctx.bezierCurveTo(fx-fw*1.5, base-(base-top)*0.2, fx-fw, top+(base-top)*0.35, fx, top);
    ctx.closePath(); ctx.fill();
    ctx.fillStyle = rgba(P[3],0.95); dot(ctx, fx, top, fw*0.55);
    ctx.strokeStyle = rgba(P[1],0.85); ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.arc(fx, top, fw*(0.9+R()*0.3), 0, Math.PI*2); ctx.stroke();
  }
  if(R()<0.55){                                                       /* arched panel frame */
    ctx.strokeStyle = rgba(P[1],0.5); ctx.lineWidth = Math.max(6, w*0.018);
    ctx.beginPath();
    ctx.moveTo(w*0.08, h); ctx.lineTo(w*0.08, h*0.36);
    ctx.arc(w*0.5, h*0.36, w*0.42, Math.PI, 0);
    ctx.lineTo(w*0.92, h); ctx.stroke();
  }
  ctx.strokeStyle = "rgba(0,0,0,0.12)"; ctx.lineWidth = 0.6;          /* craquelure */
  for(let i=0;i<26;i++){ ctx.beginPath(); let x=R()*w, y=R()*h; ctx.moveTo(x,y);
    for(let j=0;j<4;j++){ x+=(R()-0.5)*46; y+=(R()-0.5)*46; ctx.lineTo(x,y); } ctx.stroke(); }
  vignette(ctx,w,h,0.55);
},

baroque(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[0],0.5); ctx.fillRect(0,0,w,h);
  ctx.save(); ctx.translate(w*(0.02+R()*0.35),0); ctx.rotate(0.3+R()*0.6); /* light shaft */
  const beam = ctx.createLinearGradient(0,0,w*(0.4+R()*0.3),0);
  beam.addColorStop(0,"rgba(0,0,0,0)"); beam.addColorStop(0.5, rgba(P[3],0.26+R()*0.14)); beam.addColorStop(1,"rgba(0,0,0,0)");
  ctx.fillStyle = beam; ctx.fillRect(-w*0.2,-h*0.4, w*0.9, h*2.2); ctx.restore();
  const pools = 1 + Math.floor(R()*2);                                /* candle pools */
  for(let i=0;i<pools;i++){
    const gx = w*(0.22+R()*0.56), gy = h*(0.28+R()*0.44);
    const glow = ctx.createRadialGradient(gx,gy,5, gx,gy, w*(0.18+R()*0.2));
    glow.addColorStop(0, rgba(P[3],0.88)); glow.addColorStop(0.45, rgba(P[2],0.48)); glow.addColorStop(1,"rgba(0,0,0,0)");
    ctx.fillStyle = glow; ctx.fillRect(0,0,w,h);
  }
  const nb = 2 + Math.floor(R()*3);                                   /* figures in shadow */
  for(let i=0;i<nb;i++){ ctx.fillStyle = rgba(P[1], 0.4+R()*0.3);
    blob(ctx, R()*w, h*(0.58+R()*0.36), w*(0.09+R()*0.13), R); }
  if(R()<0.5){                                                        /* drapery sweep */
    ctx.strokeStyle = rgba(P[2],0.45); ctx.lineWidth = 14+R()*18; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(R()*w*0.3, h*(0.1+R()*0.3));
    ctx.bezierCurveTo(w*0.4, h*(0.2+R()*0.5), w*0.6, h*(0.3+R()*0.5), w*(0.7+R()*0.28), h*(0.7+R()*0.25));
    ctx.stroke();
  }
  vignette(ctx,w,h,0.8);
},

rococo(ctx,w,h,P,R){
  ctx.fillStyle = P[4]; ctx.fillRect(0,0,w,h);
  for(let i=0;i<16;i++){
    const c = P[i%4]; ctx.strokeStyle = rgba(c, 0.30 + R()*0.3); ctx.lineWidth = 7 + R()*16;
    ctx.lineCap = "round"; ctx.beginPath();
    const x = R()*w, y = R()*h;
    ctx.moveTo(x,y);
    ctx.bezierCurveTo(x+(R()-0.5)*220, y-(R())*130, x+(R()-0.5)*220, y+(R())*130, x+(R()-0.5)*260, y+(R()-0.5)*80);
    ctx.stroke();
  }
  for(let i=0;i<40;i++){ ctx.fillStyle = rgba(P[i%4], 0.5+R()*0.4);
    dot(ctx, R()*w, R()*h, 1.5+R()*3.5); }
},

neoclassical(ctx,w,h,P,R){
  const g = ctx.createLinearGradient(0,0,0,h);
  g.addColorStop(0, shade(P[2],1.06)); g.addColorStop(1, shade(P[2],0.72));
  ctx.fillStyle = g; ctx.fillRect(0,0,w,h);
  const n = 3 + Math.floor(R()*4);                                    /* 3–6 columns */
  const span = 0.6 + R()*0.3, x0 = (1-span)/2;
  const cw = w*span/(n*1.9);
  const capY = h*(0.12+R()*0.07), baseY = h*(0.82+R()*0.07);
  for(let i=0;i<n;i++){
    const x = w*x0 + i*(w*span/(n-1)) - cw/2;
    const col = ctx.createLinearGradient(x,0,x+cw,0);
    col.addColorStop(0, rgba(P[3],0.95)); col.addColorStop(0.5, rgba(P[3],0.55)); col.addColorStop(1, shade(P[3],0.6));
    ctx.fillStyle = col; ctx.fillRect(x, capY+h*0.045, cw, baseY-capY-h*0.045);
    ctx.fillStyle = rgba(P[1],0.9);
    ctx.fillRect(x-4, capY, cw+8, h*0.045);
    ctx.fillRect(x-4, baseY, cw+8, h*0.045);
  }
  ctx.fillStyle = rgba(P[0],0.85);
  if(R()<0.6){                                                        /* pediment */
    ctx.beginPath(); ctx.moveTo(w*(x0-0.06), capY-1);
    ctx.lineTo(w*0.5, Math.max(2, capY-h*(0.12+R()*0.1)));
    ctx.lineTo(w*(1-x0+0.06), capY-1); ctx.closePath(); ctx.fill();
  } else {                                                            /* dome */
    ctx.strokeStyle = rgba(P[0],0.85); ctx.lineWidth = Math.max(5, h*0.04);
    ctx.beginPath(); ctx.arc(w*0.5, capY, w*span*(0.5+R()*0.08), Math.PI, 0); ctx.stroke();
  }
  for(let s=0;s<2+Math.floor(R()*2);s++){                             /* steps */
    ctx.fillStyle = rgba(P[1], 0.55 - s*0.14);
    ctx.fillRect(w*(x0-0.03*(s+1)), baseY + h*0.045*(s+1), w*(span+0.06*(s+1)), h*0.035);
  }
  vignette(ctx,w,h,0.3);
},

romantic(ctx,w,h,P,R){
  const g = ctx.createLinearGradient(0,0,0,h);
  g.addColorStop(0, shade(P[3],0.85)); g.addColorStop(0.55, P[0]); g.addColorStop(1, shade(P[1],1.02));
  ctx.fillStyle = g; ctx.fillRect(0,0,w,h);
  const clouds = 8 + Math.floor(R()*8);
  for(let i=0;i<clouds;i++){ ctx.fillStyle = rgba(i%2 ? P[2] : P[4], 0.16+R()*0.16);
    blob(ctx, R()*w, h*(0.1+R()*0.52), 40+R()*110, R); }
  const sx = w*(0.18+R()*0.62), sy = h*(0.26+R()*0.3);                /* sun through storm */
  const sun = ctx.createRadialGradient(sx,sy,2, sx,sy, w*(0.2+R()*0.18));
  sun.addColorStop(0, rgba(P[4],0.9)); sun.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = sun; ctx.fillRect(0,0,w,h);
  const ridge = h*(0.8+R()*0.12), amp = h*(0.03+R()*0.06), ph = R()*7;
  ctx.fillStyle = rgba(shade(P[1],0.4),0.9);                          /* dark foreground */
  ctx.beginPath(); ctx.moveTo(0,h);
  for(let x=0;x<=w;x+=w/14) ctx.lineTo(x, ridge - Math.sin(x*0.013+ph)*amp - R()*h*0.03);
  ctx.lineTo(w,h); ctx.closePath(); ctx.fill();
  if(R()<0.4){                                                        /* lone wanderer */
    const px = w*(0.25+R()*0.5);
    ctx.fillStyle = "rgba(10,8,6,0.9)";
    ctx.fillRect(px-w*0.006, ridge-h*0.09, w*0.012, h*0.09);
    dot(ctx, px, ridge-h*0.1, w*0.009);
  }
},

tonal(ctx,w,h,P,R){
  const g = ctx.createLinearGradient(0,0,0,h);
  g.addColorStop(0, shade(P[3],0.95)); g.addColorStop(0.45+R()*0.2, P[1]); g.addColorStop(1, shade(P[0],0.8));
  ctx.fillStyle = g; ctx.fillRect(0,0,w,h);
  const hz = h*(0.48+R()*0.26);                                       /* horizon */
  ctx.fillStyle = rgba(P[2],0.5); ctx.fillRect(0, hz, w, h*0.025);
  for(let i=0;i<160;i++){ ctx.fillStyle = rgba(P[i%5], 0.10+R()*0.16);
    ctx.fillRect(R()*w, hz - h*0.06 + R()*(h-hz+h*0.06), 6+R()*22, 2+R()*4); }
  if(R()<0.5){                                                        /* haystack / cottage mass */
    const mx = w*(0.15+R()*0.7), mw2 = w*(0.08+R()*0.08);
    ctx.fillStyle = rgba(shade(P[0],0.6),0.92);
    ctx.beginPath(); ctx.moveTo(mx-mw2, hz+2); ctx.quadraticCurveTo(mx, hz-h*(0.12+R()*0.1), mx+mw2, hz+2);
    ctx.closePath(); ctx.fill();
  }
  const gl = ctx.createRadialGradient(w*(0.3+R()*0.4), hz*(0.6+R()*0.3), 4, w*0.5, hz*0.8, w*(0.3+R()*0.2));
  gl.addColorStop(0, rgba(P[3],0.35)); gl.addColorStop(1,"rgba(0,0,0,0)");
  ctx.fillStyle = gl; ctx.fillRect(0,0,w,h);
  vignette(ctx,w,h,0.5);
},

impressionist(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[3],1.04); ctx.fillRect(0,0,w,h);
  for(let i=0;i<420;i++){
    const c = P[Math.floor(R()*5)];
    ctx.save(); ctx.translate(R()*w, R()*h); ctx.rotate((R()-0.5)*1.4);
    ctx.fillStyle = rgba(c, 0.45+R()*0.45);
    ctx.fillRect(0,0, 7+R()*13, 3+R()*5); ctx.restore();
  }
},

pointillist(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[2],1.05); ctx.fillRect(0,0,w,h);
  const step = Math.max(7, w/64);
  for(let y=step/2; y<h; y+=step) for(let x=step/2; x<w; x+=step){
    const f = Math.sin(x*0.012 + Math.sin(y*0.016)*2) + Math.cos(y*0.011 + x*0.004);
    const idx = Math.abs(Math.floor(f*2.5 + R()*1.6)) % 5;
    ctx.fillStyle = rgba(P[idx], 0.75+R()*0.25);
    dot(ctx, x+(R()-0.5)*4, y+(R()-0.5)*4, step*0.33+R()*step*0.16);
  }
},

postimpressionist(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[0],0.85); ctx.fillRect(0,0,w,h);
  for(let i=0;i<330;i++){
    const x = R()*w, y = R()*h;
    const ang = Math.sin(x*0.008)*1.8 + Math.cos(y*0.011)*1.8;
    const c = P[Math.floor(R()*5)];
    ctx.strokeStyle = rgba(c, 0.55+R()*0.4); ctx.lineWidth = 3+R()*4; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(x,y);
    ctx.quadraticCurveTo(x+Math.cos(ang)*16, y+Math.sin(ang)*16, x+Math.cos(ang+0.7)*30, y+Math.sin(ang+0.7)*30);
    ctx.stroke();
  }
  for(let i=0;i<6;i++){                                              /* spiral stars */
    const cx=R()*w, cy=R()*h*0.6;
    ctx.strokeStyle = rgba(P[1],0.8); ctx.lineWidth=2.5;
    ctx.beginPath();
    for(let a=0;a<Math.PI*4;a+=0.25){ const r=2+a*3.2;
      const px=cx+Math.cos(a)*r, py=cy+Math.sin(a)*r*0.8;
      a===0?ctx.moveTo(px,py):ctx.lineTo(px,py); }
    ctx.stroke();
  }
},

expressionist(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[4],0.85); ctx.fillRect(0,0,w,h);
  for(let i=0;i<26;i++){
    const c = P[i%4]; ctx.strokeStyle = rgba(c, 0.6+R()*0.4);
    ctx.lineWidth = 6+R()*16; ctx.lineCap = "square";
    ctx.beginPath();
    let x = R()*w, y = R()*h; ctx.moveTo(x,y);
    for(let j=0;j<3+Math.floor(R()*3);j++){ x += (R()-0.5)*w*0.4; y += (R()-0.5)*h*0.55; ctx.lineTo(x,y); }
    ctx.stroke();
  }
  ctx.fillStyle = rgba(P[0],0.55); blob(ctx, w*0.5+(R()-0.5)*80, h*0.45, 46+R()*30, R);
},

fauvist(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[4]||P[3],1.0); ctx.fillRect(0,0,w,h);
  for(let i=0;i<30;i++){
    const c = P[i%4]; ctx.fillStyle = rgba(c, 0.78+R()*0.22);
    const cx = R()*w, cy = R()*h, r = 26+R()*64;
    ctx.beginPath();
    for(let a=0;a<=Math.PI*2+0.01;a+=Math.PI/4){
      const rr = r*(0.62+R()*0.66);
      const px = cx+Math.cos(a)*rr, py = cy+Math.sin(a)*rr*0.8;
      a===0?ctx.moveTo(px,py):ctx.lineTo(px,py);
    }
    ctx.closePath(); ctx.fill();
  }
},

cubist(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[4],0.95); ctx.fillRect(0,0,w,h);
  const gx = 6, gy = 4, pts = [];
  for(let j=0;j<=gy;j++) for(let i=0;i<=gx;i++)
    pts.push([ i*w/gx + (i&&i<gx ? (R()-0.5)*w/gx*0.9 : 0), j*h/gy + (j&&j<gy ? (R()-0.5)*h/gy*0.9 : 0) ]);
  const at = (i,j) => pts[j*(gx+1)+i];
  for(let j=0;j<gy;j++) for(let i=0;i<gx;i++){
    const c = P[Math.floor(R()*4)];
    const quad = [at(i,j), at(i+1,j), at(i+1,j+1), at(i,j+1)];
    const tris = R()<0.55 ? [[quad[0],quad[1],quad[2]],[quad[0],quad[2],quad[3]]] : [quad];
    tris.forEach(t => {
      ctx.fillStyle = rgba(R()<0.5?c:P[Math.floor(R()*5)], 0.55+R()*0.45);
      ctx.beginPath(); ctx.moveTo(t[0][0],t[0][1]);
      t.slice(1).forEach(p=>ctx.lineTo(p[0],p[1])); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = rgba(shade(P[3],0.4),0.5); ctx.lineWidth = 1; ctx.stroke();
    });
  }
},

abstract(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[4],1.55); ctx.fillRect(0,0,w,h);
  ctx.fillStyle = rgba(P[4],0.12); ctx.fillRect(0,0,w,h);
  for(let i=0;i<7;i++){
    const c = P[i%4], x = R()*w, y = R()*h, r = 14+R()*52;
    ctx.fillStyle = rgba(c, 0.8); dot(ctx,x,y,r);
    if(R()<0.7){ ctx.strokeStyle = rgba(P[(i+2)%5],0.9); ctx.lineWidth = 2.5+R()*3; ctx.beginPath(); ctx.arc(x,y,r+6+R()*12,0,Math.PI*2); ctx.stroke(); }
  }
  for(let i=0;i<6;i++){
    ctx.strokeStyle = rgba(P[(i+1)%5],0.85); ctx.lineWidth = 2+R()*4;
    ctx.beginPath(); ctx.moveTo(R()*w,R()*h); ctx.lineTo(R()*w,R()*h); ctx.stroke();
  }
  for(let i=0;i<4;i++){
    ctx.fillStyle = rgba(P[i%5],0.85);
    const x=R()*w,y=R()*h,s=10+R()*26;
    ctx.beginPath(); ctx.moveTo(x,y-s); ctx.lineTo(x+s,y+s); ctx.lineTo(x-s,y+s); ctx.closePath(); ctx.fill();
  }
},

geometric(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[2],1.02); ctx.fillRect(0,0,w,h);
  const shapes = 6+Math.floor(R()*4);
  for(let i=0;i<shapes;i++){
    const c = i===0 ? P[0] : P[Math.floor(R()*5)];
    ctx.save(); ctx.translate(R()*w*0.8+w*0.1, R()*h*0.8+h*0.1); ctx.rotate((R()-0.5)*0.9);
    ctx.fillStyle = rgba(c, 0.92);
    if(R()<0.3) ctx.fillRect(-w*0.02, -h*0.3, w*0.04, h*0.6);
    else ctx.fillRect(-w*(0.04+R()*0.1), -h*(0.05+R()*0.12), w*(0.08+R()*0.2), h*(0.1+R()*0.24));
    ctx.restore();
  }
},

mondrian(ctx,w,h,P,R){
  ctx.fillStyle = P[3]; ctx.fillRect(0,0,w,h);
  const xs = [0, w*(0.18+R()*0.1), w*(0.42+R()*0.12), w*(0.72+R()*0.1), w];
  const ys = [0, h*(0.3+R()*0.15), h*(0.62+R()*0.15), h];
  const prim = [P[0],P[1],P[2]];
  for(let j=0;j<ys.length-1;j++) for(let i=0;i<xs.length-1;i++){
    if(R()<0.3){ ctx.fillStyle = prim[Math.floor(R()*3)];
      ctx.fillRect(xs[i],ys[j], xs[i+1]-xs[i], ys[j+1]-ys[j]); }
  }
  ctx.strokeStyle = P[4]; ctx.lineWidth = Math.max(5, w*0.014);
  xs.slice(1,-1).forEach(x => { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); });
  ys.slice(1,-1).forEach(y => { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); });
},

surreal(ctx,w,h,P,R){
  const horizon = h*(0.56+R()*0.18);
  const g = ctx.createLinearGradient(0,0,0,h);
  g.addColorStop(0, shade(P[1],1.0)); g.addColorStop(0.62, shade(P[3],1.0)); g.addColorStop(1, shade(P[2],0.85));
  ctx.fillStyle = g; ctx.fillRect(0,0,w,h);
  ctx.fillStyle = rgba(shade(P[4],0.8),0.95); ctx.fillRect(0, horizon, w, h-horizon); /* plain */
  const orbs = 1 + Math.floor(R()*2);                                 /* floating orbs */
  for(let i=0;i<orbs;i++){
    const ox = w*(0.1+R()*0.55), oy = h*(0.14+R()*0.28), orr = h*(0.07+R()*0.09);
    ctx.fillStyle = rgba(P[0],0.95); dot(ctx, ox, oy, orr);
    ctx.fillStyle = rgba(shade(P[0],1.4),0.5); dot(ctx, ox-orr*0.3, oy-orr*0.3, orr*0.4);
    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.beginPath(); ctx.ellipse(ox+w*(0.04+R()*0.1), horizon+h*(0.04+R()*0.08), orr*(2+R()*1.2), orr*0.32, 0.06, 0, Math.PI*2); ctx.fill();
  }
  const mx = w*(0.46+R()*0.3), mw2 = w*(0.16+R()*0.14);               /* melting form */
  ctx.fillStyle = rgba(P[2],0.9);
  ctx.beginPath(); ctx.moveTo(mx, horizon);
  ctx.bezierCurveTo(mx+mw2*0.1, horizon-h*(0.18+R()*0.16), mx+mw2, horizon-h*(0.16+R()*0.14), mx+mw2, horizon-h*0.04);
  ctx.bezierCurveTo(mx+mw2, horizon+h*(0.07+R()*0.09), mx+mw2*0.4, horizon+h*0.04, mx+mw2*0.35, horizon+h*(0.16+R()*0.12));
  ctx.lineTo(mx, horizon+h*0.2); ctx.closePath(); ctx.fill();
  ctx.fillStyle = "rgba(0,0,0,0.2)";
  ctx.beginPath(); ctx.ellipse(mx+mw2*0.5, horizon+h*(0.22+R()*0.08), mw2*(0.7+R()*0.5), h*0.02, 0, 0, Math.PI*2); ctx.fill();
  if(R()<0.5){                                                        /* lone door on the plain */
    const dx = w*(0.08+R()*0.78), dh = h*(0.1+R()*0.07);
    ctx.fillStyle = rgba(P[1],0.9); ctx.fillRect(dx, horizon-dh, w*0.024, dh);
  }
},

metaphysical(ctx,w,h,P,R){
  const left = R() < 0.5, horizon = h*(0.56+R()*0.12);
  const g = ctx.createLinearGradient(0,0,0,horizon);
  g.addColorStop(0, shade(P[0],0.9)); g.addColorStop(1, shade(P[1],1.05));
  ctx.fillStyle = g; ctx.fillRect(0,0,w,horizon);
  ctx.fillStyle = shade(P[1],0.92); ctx.fillRect(0,horizon-2,w,h-horizon+2); /* ochre ground */
  const sx = left ? w*(0.6+R()*0.3) : w*(0.1+R()*0.3);                /* low sun */
  ctx.fillStyle = rgba(P[4],0.85); dot(ctx, sx, h*(0.12+R()*0.14), h*(0.06+R()*0.05));
  const bw = w*(0.36+R()*0.28), bh = h*(0.24+R()*0.16);               /* arcade */
  const bx = left ? 0 : w-bw, by = horizon-bh;
  ctx.fillStyle = shade(P[2],0.85); ctx.fillRect(bx,by,bw,bh);
  ctx.fillStyle = shade(P[2],0.5);
  const arches = 3 + Math.floor(R()*3);
  for(let i=0;i<arches;i++){
    const ax = bx + bw*0.08 + i*(bw*0.88/arches), aw = bw*0.6/arches;
    ctx.beginPath(); ctx.moveTo(ax, by+bh);
    ctx.lineTo(ax, by+bh*0.45); ctx.arc(ax+aw/2, by+bh*0.45, aw/2, Math.PI, 0);
    ctx.lineTo(ax+aw, by+bh); ctx.closePath(); ctx.fill();
  }
  if(R()<0.5){                                                        /* distant tower */
    const tx = left ? w*(0.62+R()*0.25) : w*(0.08+R()*0.25);
    const tw = w*(0.045+R()*0.03), th = h*(0.26+R()*0.14);
    ctx.fillStyle = shade(P[3],0.8); ctx.fillRect(tx, horizon-th, tw, th);
    ctx.beginPath(); ctx.moveTo(tx-tw*0.25, horizon-th);
    ctx.lineTo(tx+tw/2, horizon-th-h*0.07); ctx.lineTo(tx+tw*1.25, horizon-th); ctx.closePath(); ctx.fill();
  }
  ctx.fillStyle = "rgba(20,16,10,0.4)";                               /* raking shadow */
  ctx.beginPath(); ctx.moveTo(bx, horizon); ctx.lineTo(bx+bw, horizon);
  ctx.lineTo(bx+bw+(left?1:-1)*w*(0.16+R()*0.22), h); ctx.lineTo(bx-(left?0:w*0.1), h); ctx.closePath(); ctx.fill();
  ctx.fillStyle = "rgba(20,16,10,0.55)";                              /* lone figure's shadow */
  ctx.beginPath(); ctx.ellipse(w*(0.28+R()*0.5), h*(0.76+R()*0.14), w*0.02, h*(0.06+R()*0.06), (left?-1:1)*0.5, 0, Math.PI*2); ctx.fill();
},

ornament(ctx,w,h,P,R){
  const g = ctx.createLinearGradient(0,0,w,h);
  g.addColorStop(0, shade(P[0],1.05)); g.addColorStop(1, shade(P[2],0.9));
  ctx.fillStyle = g; ctx.fillRect(0,0,w,h);
  for(let i=0;i<200;i++){                                             /* gold mosaic */
    ctx.fillStyle = rgba(R()<0.7 ? P[1] : P[Math.floor(R()*5)], 0.25+R()*0.5);
    ctx.save(); ctx.translate(R()*w,R()*h); ctx.rotate((R()-0.5)*0.6);
    ctx.fillRect(0,0, 4+R()*10, 8+R()*18); ctx.restore();
  }
  for(let i=0;i<9;i++){                                               /* concentric circles */
    const x = R()*w, y = R()*h, base = 5+R()*16;
    for(let k=3;k>0;k--){ ctx.fillStyle = rgba(P[(i+k)%5], 0.85); dot(ctx,x,y, base*k/2.2); }
  }
  for(let i=0;i<5;i++){                                               /* spirals */
    ctx.strokeStyle = rgba(P[3],0.7); ctx.lineWidth = 2;
    const cx=R()*w, cy=R()*h; ctx.beginPath();
    for(let a=0;a<Math.PI*3.2;a+=0.3){ const r=a*2.6;
      const px=cx+Math.cos(a)*r, py=cy+Math.sin(a)*r;
      a===0?ctx.moveTo(px,py):ctx.lineTo(px,py); }
    ctx.stroke();
  }
},

colorfield(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[4],0.8); ctx.fillRect(0,0,w,h);
  const nb = 2 + Math.floor(R()*3), rot = Math.floor(R()*5);          /* 2–4 hovering fields */
  const weights = []; let sum = 0;
  for(let i=0;i<nb;i++){ const v = 0.5+R(); weights.push(v); sum += v; }
  let y = 0.05 + R()*0.05;
  const avail = 0.92 - y - nb*0.04;
  weights.forEach((v,i) => {
    const bh = avail*v/sum, c = P[(i+rot)%4];
    for(let k=8;k>=0;k--){
      ctx.fillStyle = rgba(c, 0.16);
      const inset = k*3;
      ctx.fillRect(w*0.06+inset, h*y+inset, w*0.88-inset*2, h*bh-inset*2);
    }
    for(let j=0;j<50;j++){ ctx.fillStyle = rgba(shade(c,1.25), 0.07);
      ctx.fillRect(w*0.06+R()*w*0.88, h*y+R()*h*bh, 8+R()*30, 2+R()*3); }
    y += bh + 0.04;
  });
},

drip(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[1],1.0); ctx.fillRect(0,0,w,h);
  const layers = [P[4],P[3],P[2],P[0]];
  layers.forEach((c, li) => {
    const n = 5 + Math.floor(R()*3);
    for(let i=0;i<n;i++){
      ctx.strokeStyle = rgba(c, 0.75+R()*0.25);
      ctx.lineWidth = (li===layers.length-1 ? 2.6 : 1.4) + R()*3; ctx.lineCap = "round";
      ctx.beginPath();
      let x = R()*w, y = R()*h; ctx.moveTo(x,y);
      const segs = 14+Math.floor(R()*14);
      for(let s=0;s<segs;s++){
        x += (R()-0.5)*w*0.22; y += (R()-0.5)*h*0.3;
        ctx.quadraticCurveTo(x+(R()-0.5)*40, y+(R()-0.5)*40, x, y);
      }
      ctx.stroke();
      for(let d=0;d<6;d++){ ctx.fillStyle = rgba(c,0.85); dot(ctx, R()*w, R()*h, 1+R()*3.4); }
    }
  });
},

gestural(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[1]||P[4],1.02); ctx.fillRect(0,0,w,h);
  for(let i=0;i<13;i++){
    const c = P[i%5];
    ctx.strokeStyle = rgba(c, 0.62+R()*0.38);
    ctx.lineWidth = 14+R()*26; ctx.lineCap = "round";
    ctx.beginPath();
    const x = R()*w, y = R()*h;
    ctx.moveTo(x,y);
    ctx.bezierCurveTo(x+(R()-0.5)*w*0.7, y+(R()-0.5)*h*0.9, x+(R()-0.5)*w*0.7, y+(R()-0.5)*h*0.9, x+(R()-0.5)*w*0.9, y+(R()-0.5)*h*0.7);
    ctx.stroke();
  }
  for(let i=0;i<4;i++){                                               /* scrape-back */
    ctx.strokeStyle = rgba(shade(P[1]||P[4],1.05), 0.5);
    ctx.lineWidth = 10+R()*16; ctx.beginPath();
    const y = R()*h; ctx.moveTo(0,y); ctx.lineTo(w, y+(R()-0.5)*h*0.3); ctx.stroke();
  }
},

pop(ctx,w,h,P,R){
  ctx.fillStyle = P[1]; ctx.fillRect(0,0,w,h);
  ctx.fillStyle = P[2];                                               /* split ground */
  if(R()<0.35) ctx.fillRect(0,0,w,h*(0.35+R()*0.3)); else ctx.fillRect(0,0,w*(0.35+R()*0.3),h);
  const step = Math.max(9, w/(32+R()*16));                            /* ben-day patch */
  const dq = Math.floor(R()*4);
  const dx0 = dq%2 ? w*0.48 : 0, dy0 = dq<2 ? 0 : h*0.45;
  for(let y=dy0+step/2; y<Math.min(h,dy0+h*0.55); y+=step)
    for(let x=dx0+step/2; x<Math.min(w,dx0+w*0.52); x+=step){
      ctx.fillStyle = rgba(P[0],0.9); dot(ctx,x,y,step*0.27); }
  const tx = w*(0.18+R()*0.34), ty = h*(0.3+R()*0.4);                 /* target */
  const ts = 0.75+R()*0.5, rot = Math.floor(R()*5);
  [0.3,0.22,0.14,0.07].forEach((r,i)=>{ ctx.fillStyle = [P[0],P[4],P[3],P[0]][(i+rot)%4]; dot(ctx,tx,ty,h*r*ts); });
  ctx.save(); ctx.translate(w*(0.6+R()*0.26), h*(0.5+R()*0.34));      /* star burst */
  ctx.rotate(R()*Math.PI);
  const spikes = 10 + 2*Math.floor(R()*3), outer = h*(0.13+R()*0.07);
  ctx.fillStyle = P[4];
  ctx.beginPath();
  for(let i=0;i<spikes;i++){ const a=i*Math.PI*2/spikes, r = i%2 ? outer*0.42 : outer;
    const px=Math.cos(a)*r, py=Math.sin(a)*r; i===0?ctx.moveTo(px,py):ctx.lineTo(px,py); }
  ctx.closePath(); ctx.fill(); ctx.restore();
  ctx.lineWidth = Math.max(4,w*0.012); ctx.strokeStyle = P[4];
  ctx.strokeRect(w*0.03,h*0.06,w*0.94,h*0.88);
},

ukiyoe(ctx,w,h,P,R){
  ctx.fillStyle = P[2]; ctx.fillRect(0,0,w,h);
  ctx.fillStyle = rgba(P[3],0.5); ctx.fillRect(0,0,w,h*(0.1+R()*0.12));
  const fx = w*(0.52+R()*0.34), fw2 = w*(0.12+R()*0.08), fy = h*(0.18+R()*0.14); /* fuji */
  ctx.fillStyle = rgba(P[4],0.85);
  ctx.beginPath(); ctx.moveTo(fx-fw2,h*0.52); ctx.lineTo(fx,fy); ctx.lineTo(fx+fw2,h*0.52); ctx.closePath(); ctx.fill();
  ctx.fillStyle = P[2];                                               /* snowcap */
  ctx.beginPath(); ctx.moveTo(fx-fw2*0.3, fy+(h*0.52-fy)*0.3); ctx.lineTo(fx,fy);
  ctx.lineTo(fx+fw2*0.3, fy+(h*0.52-fy)*0.3); ctx.closePath(); ctx.fill();
  const wave = (yb, sc, c, alpha, ph) => {
    ctx.fillStyle = rgba(c, alpha);
    ctx.beginPath(); ctx.moveTo(0,h);
    for(let x=0;x<=w;x+=8){
      const y = yb - Math.abs(Math.sin(x*0.012+ph))*h*0.2*sc - Math.sin(x*0.05*sc+ph)*6;
      ctx.lineTo(x,y);
    }
    ctx.lineTo(w,h); ctx.closePath(); ctx.fill();
  };
  wave(h*(0.72+R()*0.1), 0.6+R()*0.3, P[1], 0.9, R()*6);
  wave(h*(0.85+R()*0.08), 1.0+R()*0.3, P[0], 0.95, R()*6);
  wave(h*(0.98+R()*0.08), 1.3+R()*0.4, P[1], 0.9, R()*6);
  ctx.fillStyle = rgba(P[2],0.95);                                    /* foam */
  const foam = 30 + Math.floor(R()*30);
  for(let i=0;i<foam;i++) dot(ctx, R()*w, h*(0.55+R()*0.4), 1.5+R()*3);
  const cx2 = w*(0.16+R()*0.3), cr = h*(0.16+R()*0.12);               /* claw curl */
  ctx.strokeStyle = rgba(P[0],0.85); ctx.lineWidth = 4+R()*3; ctx.lineCap="round";
  const a0 = Math.PI*(0.8+R()*0.2);
  ctx.beginPath(); ctx.arc(cx2, h*(0.5+R()*0.16), cr, a0, a0+Math.PI*(0.75+R()*0.25)); ctx.stroke();
},

naive(ctx,w,h,P,R){
  ctx.fillStyle = P[0]; ctx.fillRect(0,0,w,h);
  const ground = h*(0.45+R()*0.2);
  ctx.fillStyle = rgba(P[1],0.9); ctx.fillRect(0,ground,w,h-ground);
  ctx.fillStyle = P[3]; dot(ctx, w*(0.12+R()*0.76), h*(0.12+R()*0.16), h*(0.07+R()*0.06)); /* sun */
  const trees = 6 + Math.floor(R()*6);
  for(let i=0;i<trees;i++){                                           /* round trees / leaves */
    const x = R()*w, y = ground*(0.6+R()*0.5)+h*0.1, r = 14+R()*30;
    ctx.fillStyle = rgba(P[2], 0.9); dot(ctx,x,y,r);
    ctx.strokeStyle = rgba(shade(P[0],0.65),0.8); ctx.lineWidth = 2;
    for(let k=0;k<5;k++){ const a = -Math.PI/2 + (k-2)*0.5;
      ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+Math.cos(a)*r*0.85, y+Math.sin(a)*r*0.85); ctx.stroke(); }
  }
  for(let i=0;i<14;i++){ ctx.fillStyle = rgba(P[4],0.95); dot(ctx, R()*w, h*(0.6+R()*0.36), 2.5+R()*3.5); }
},

artdeco(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[2],0.85); ctx.fillRect(0,0,w,h);
  const top = R()<0.35;                                               /* fan from below or above */
  const cx = w*(0.32+R()*0.36), cy = top ? -h*0.05 : h*(1.02+R()*0.06);
  const rays = 9 + Math.floor(R()*8);
  for(let i=0;i<rays;i++){                                            /* sunburst */
    const a0 = (top?0:Math.PI) + i*(Math.PI/rays), a1 = a0 + Math.PI/(rays*2);
    ctx.fillStyle = i%2 ? rgba(P[0],0.85) : rgba(P[3],0.7);
    ctx.beginPath(); ctx.moveTo(cx,cy);
    ctx.arc(cx,cy, h*1.2, a0, a1); ctx.closePath(); ctx.fill();
  }
  const arcs = 2 + Math.floor(R()*3);                                 /* chrome arcs */
  for(let i=0;i<arcs;i++){
    ctx.strokeStyle = i%2 ? rgba(P[4],0.9) : rgba(P[1],0.9);
    ctx.lineWidth = 7 - i*1.5;
    ctx.beginPath(); ctx.arc(cx,cy, h*(0.34+i*(0.14+R()*0.06)), top?0:Math.PI, top?Math.PI:Math.PI*2); ctx.stroke();
  }
  const oy = top ? h*(0.58+R()*0.16) : h*(0.26+R()*0.14), orr = h*(0.11+R()*0.06);
  const orb = ctx.createRadialGradient(cx-orr*0.4, oy-orr*0.3, 2, cx, oy, orr*1.1);
  orb.addColorStop(0, shade(P[3],1.3)); orb.addColorStop(1, shade(P[0],0.8));
  ctx.fillStyle = orb; dot(ctx, cx, oy, orr);
},

street(ctx,w,h,P,R){
  ctx.fillStyle = shade(P[3],0.92); ctx.fillRect(0,0,w,h);
  ctx.fillStyle = "rgba(0,0,0,0.07)";
  for(let i=0;i<240;i++) ctx.fillRect(R()*w, R()*h, 1.6, 1.6);        /* concrete grain */
  for(let i=0;i<4;i++){                                               /* spray clusters */
    const c = P[i%3===0 ? 1 : (i%3===1 ? 2 : 0)], cx = R()*w, cy = R()*h*0.7;
    for(let d=0;d<140;d++){
      const a = R()*Math.PI*2, r = Math.pow(R(),0.5)*40;
      ctx.fillStyle = rgba(c, 0.16+R()*0.3);
      dot(ctx, cx+Math.cos(a)*r, cy+Math.sin(a)*r*0.8, 0.8+R()*2);
    }
    ctx.fillStyle = rgba(c,0.75);                                     /* drips */
    for(let d=0;d<3;d++){ const dx = cx+(R()-0.5)*36;
      ctx.fillRect(dx, cy, 2.2, 18+R()*46); dot(ctx, dx+1, cy+20+R()*46, 2.4); }
  }
  ctx.strokeStyle = rgba(P[0],0.92); ctx.lineWidth = 9; ctx.lineCap="round"; /* tag */
  ctx.beginPath(); ctx.moveTo(w*0.14,h*0.74);
  ctx.bezierCurveTo(w*0.3,h*0.5, w*0.42,h*0.95, w*0.56,h*0.66);
  ctx.bezierCurveTo(w*0.66,h*0.46, w*0.78,h*0.8, w*0.88,h*0.6);
  ctx.stroke();
},

contemporary(ctx,w,h,P,R){
  const g = ctx.createLinearGradient(0,0,w,h);
  g.addColorStop(0, shade(P[3],1.0)); g.addColorStop(1, shade(P[3],0.82));
  ctx.fillStyle = g; ctx.fillRect(0,0,w,h);
  for(let i=0;i<8;i++){ ctx.fillStyle = rgba(P[i%3===0?0:(i%3===1?1:4)], 0.2+R()*0.25);
    blob(ctx, R()*w, R()*h, 30+R()*80, R); }
  ctx.lineCap = "round";
  for(let i=0;i<26;i++){                                              /* ink lines */
    ctx.strokeStyle = rgba(P[2+Math.floor(R()*3)] || P[2], 0.5+R()*0.45);
    ctx.lineWidth = 0.8+R()*2.2;
    ctx.beginPath();
    const x=R()*w, y=R()*h;
    ctx.moveTo(x,y);
    ctx.bezierCurveTo(x+(R()-0.5)*200, y+(R()-0.5)*120, x+(R()-0.5)*200, y+(R()-0.5)*120, x+(R()-0.5)*320, y+(R()-0.5)*180);
    ctx.stroke();
  }
  for(let i=0;i<30;i++){ ctx.fillStyle = rgba(P[Math.floor(R()*5)],0.7);
    ctx.fillRect(R()*w, R()*h, 6+R()*14, 2); }
}
};

/* small shared shapes */
function dot(ctx,x,y,r){ ctx.beginPath(); ctx.arc(x,y,Math.max(0.4,r),0,Math.PI*2); ctx.fill(); }
function blob(ctx,cx,cy,r,R){
  ctx.beginPath();
  for(let a=0;a<=Math.PI*2+0.01;a+=Math.PI/7){
    const rr = r*(0.7+R()*0.6);
    const px = cx+Math.cos(a)*rr, py = cy+Math.sin(a)*rr*0.75;
    a===0?ctx.moveTo(px,py):ctx.lineTo(px,py);
  }
  ctx.closePath(); ctx.fill();
}
function vignette(ctx,w,h,strength){
  const v = ctx.createRadialGradient(w/2,h/2, Math.min(w,h)*0.3, w/2,h/2, Math.max(w,h)*0.75);
  v.addColorStop(0,"rgba(0,0,0,0)"); v.addColorStop(1, `rgba(0,0,0,${strength})`);
  ctx.fillStyle = v; ctx.fillRect(0,0,w,h);
}

/* paint a cover canvas from its data- attributes */
function paintCanvas(cv){
  const style = cv.dataset.style || "contemporary";
  const palette = cv.dataset.colors.split(",");
  const rect = cv.getBoundingClientRect();
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  let cw = Math.max(60, Math.round((rect.width  || 300) * dpr));
  let ch = Math.max(40, Math.round((rect.height || 188) * dpr));
  const maxW = 1000;                       /* keep stroke density rich on big heroes */
  if(cw > maxW){ ch = Math.round(ch * maxW / cw); cw = maxW; }
  cv.width = cw; cv.height = ch;
  const ctx = cv.getContext("2d");
  const R = mulberry(hashStr(cv.dataset.seed || style) ^ (cv.dataset.salt ? hashStr(cv.dataset.salt) : 0));
  (PAINTERS[style] || PAINTERS.contemporary)(ctx, cv.width, cv.height, palette, R);
  cv.dataset.painted = "1";
}

const observer = ("IntersectionObserver" in window) ? new IntersectionObserver(entries => {
  entries.forEach(en => { if(en.isIntersecting){ paintCanvas(en.target); observer.unobserve(en.target); } });
}, { rootMargin: "300px" }) : null;

function paintAll(root){
  root.querySelectorAll("canvas[data-paint]").forEach(cv => {
    if(cv.dataset.painted) return;
    if(cv.dataset.eager || !observer) paintCanvas(cv);
    else observer.observe(cv);
  });
}

/* ============================================================
   HTML BUILDERS
   ============================================================ */
const canvasTag = (style, palette, seed, eager, salt) =>
  `<canvas data-paint data-style="${style}" data-colors="${palette.join(",")}" data-seed="${esc(seed)}"${eager?' data-eager="1"':''}${salt?` data-salt="${esc(salt)}"`:''}></canvas>`;

const chip = (type, href, label) => `<a class="chip ${type}" href="#/${href}">${esc(label)}</a>`;
const chipsFor = a => [
  ...a.movements.map(m => Mx[m] ? chip("m", "movement/"+m, Mx[m].name) : ""),
  ...a.techniques.map(t => Tx[t] ? chip("t", "technique/"+t, Tx[t].name) : ""),
  ...a.eras.map(e => Ex[e] ? chip("e", "era/"+e, Ex[e].name) : ""),
  Nx[a.nation] ? chip("n", "nation/"+a.nation, Nx[a.nation].flag+" "+Nx[a.nation].name) : ""
].join("");

function artistCard(a){
  const movs = a.movements.slice(0,2).map(m => Mx[m] ? chip("m","movement/"+m, Mx[m].name) : "").join("");
  return `<article class="card" data-href="#/artist/${a.id}">
    <div class="card-art">${canvasTag(a.style, a.palette, a.id)}</div>
    <div class="card-body">
      <h3><a href="#/artist/${a.id}">${esc(a.name)}</a></h3>
      <div class="card-meta">${esc(a.years)} · ${Nx[a.nation] ? esc(Nx[a.nation].name) : ""}</div>
      <div class="card-tagline">${esc(a.tagline)}</div>
      <div class="chips">${movs}</div>
    </div>
  </article>`;
}

function taxCard(item, type, count){
  const kids = (type === "movement" ? movChildren(item.id) : tecChildren(item.id));
  return `<article class="card tax-card" data-href="#/${type}/${item.id}">
    <div class="card-art">${canvasTag(item.style, item.palette, item.id)}</div>
    <div class="card-body">
      <h3><a href="#/${type}/${item.id}">${esc(item.name)}</a></h3>
      <div class="card-meta">${item.period ? esc(item.period) + " · " : ""}${count} artist${count===1?"":"s"}</div>
      <div class="card-tagline">${esc(item.blurb)}</div>
      ${kids.length ? `<div class="chips branch-list">${kids.map(k => `<a class="branch-chip" href="#/${type}/${k.id}">${esc(k.name)}</a>`).join("")}</div>` : ""}
    </div>
  </article>`;
}

const crumbs = parts => `<nav class="breadcrumbs">` +
  parts.map((p,i) => i === parts.length-1
    ? `<span>${esc(p[0])}</span>`
    : `<a href="#/${p[1]}">${esc(p[0])}</a><span class="sep">/</span>`).join("") + `</nav>`;

function hero(opts){
  return `<header class="hero">
    ${canvasTag(opts.style, opts.palette, opts.seed, true, opts.salt)}
    <div class="hero-shade"></div>
    <div class="hero-content">
      ${opts.crumbs || ""}
      <h1>${esc(opts.title)}</h1>
      ${opts.sub ? `<div class="hero-sub">${opts.sub}</div>` : ""}
      ${opts.tagline ? `<div class="hero-tagline">“${esc(opts.tagline)}”</div>` : ""}
    </div>
  </header>`;
}

/* ============================================================
   VIEWS
   ============================================================ */
const app = document.getElementById("app");
let artistFilter = { era: "all", sort: "chrono" };
let taxView = { movement: "cards", technique: "cards" };

/* ---------- genealogical tree (movements / techniques) ---------- */
function treeView(list, type){
  const byParent = {};
  list.forEach(x => { (byParent[x.parent || ""] = byParent[x.parent || ""] || []).push(x); });
  const mk = x => ({ item: x, kids: (byParent[x.id] || []).map(mk) });
  const roots = (byParent[""] || []).map(mk);
  const countFn = type === "movement" ? artistsOfMovement : artistsOfTechnique;
  const nodeW = n => Math.min(252, n.item.name.length * 7.4 + 52);

  const ROW = 38, COL = 280;
  let row = 0;
  const nodes = [], links = [];
  (function placeAll(){
    function place(n, depth){
      let y;
      if(!n.kids.length){ y = row * ROW; row += 1; }
      else {
        const ys = n.kids.map(k => place(k, depth + 1));
        y = (Math.min(...ys) + Math.max(...ys)) / 2;
      }
      n.x = depth * COL; n.y = y;
      nodes.push(n);
      n.kids.forEach(k => links.push([n, k]));
      return y;
    }
    roots.forEach(r => { place(r, 0); row += 0.35; });   /* breathing room between families */
  })();

  const H = row * ROW + 16, W = COL * 2 + 300;
  let svg = `<svg class="tree-svg ${type}" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">`;
  links.forEach(([a, b]) => {
    const x1 = a.x + nodeW(a), y1 = a.y + 14, x2 = b.x, y2 = b.y + 14;
    svg += `<path class="tree-link" d="M${x1},${y1} C${x1 + 44},${y1} ${x2 - 44},${y2} ${x2},${y2}"/>`;
  });
  nodes.forEach(n => {
    const w = nodeW(n), cnt = countFn(n.item.id).length;
    svg += `<a href="#/${type}/${n.item.id}"><g class="tree-node">
      <rect x="${n.x}" y="${n.y}" rx="14" width="${w}" height="28"/>
      <text class="tn-name" x="${n.x + 13}" y="${n.y + 19}">${esc(n.item.name)}</text>
      <text class="tn-count" x="${n.x + w - 11}" y="${n.y + 19}" text-anchor="end">${cnt}</text>
    </g><title>${esc(n.item.name)} — ${cnt} painter${cnt === 1 ? "" : "s"}</title></a>`;
  });
  svg += `</svg>`;
  return `<p class="page-lede" style="margin-bottom:14px">Every node is a page — branches read left to right, the number counts its painters (including sub-branches).</p>
    <div class="tree-wrap">${svg}</div>`;
}

/* ---------- the grand timeline ---------- */
let tlZoom = 6;                                            /* pixels per year */
const TL_Y0 = 1240;

function vivid(P){                                         /* pick the punchiest palette colour */
  let best = P[0], bs = -Infinity;
  P.forEach(hx => {
    const [r, g, b] = hex2rgb(hx);
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
    const v = mx / 255, c = (mx - mn) / 255;
    let s = c * 2.4 + v * 0.8;
    if(v > 0.82 && c < 0.2) s -= 1.0;                      /* not near-white */
    if(v < 0.28) s -= 0.8;                                 /* not near-black */
    if(s > bs){ bs = s; best = hx; }
  });
  return best;
}
const luma = hx => { const [r, g, b] = hex2rgb(hx); return (0.299*r + 0.587*g + 0.114*b) / 255; };

function viewTimeline(){
  document.title = "Timeline — Pigment";
  const Y1 = 2030, pxy = tlZoom, W = (Y1 - TL_Y0) * pxy;
  const LANE = 24, BARH = 18, TOP = 34, BOT = 30;

  /* greedy lane packing, chronological */
  const sorted = [...A].sort((a, b) => a.born - b.born || a.name.localeCompare(b.name));
  const laneEnds = [], bars = [];
  sorted.forEach(a => {
    const end = a.died || 2026;
    let li = laneEnds.findIndex(e => e + 3 <= a.born);
    if(li === -1){ li = laneEnds.length; laneEnds.push(0); }
    laneEnds[li] = end;
    bars.push([a, li, end]);
  });
  const H = TOP + laneEnds.length * LANE + BOT;

  let grid = "";
  for(let y = 1300; y <= 2000; y += 50){
    const x = (y - TL_Y0) * pxy, cent = y % 100 === 0;
    grid += `<div class="tl2-grid ${cent ? "c" : ""}" style="left:${x}px"></div>`;
    if(cent) grid += `<div class="tl2-year t" style="left:${x}px">${y}</div><div class="tl2-year b" style="left:${x}px">${y}</div>`;
  }
  grid += `<div class="tl2-grid now" style="left:${(2026 - TL_Y0) * pxy}px"></div>
           <div class="tl2-year t now" style="left:${(2026 - TL_Y0) * pxy}px">today</div>`;

  const barHtml = bars.map(([a, li, end]) => {
    const mov = Mx[a.movements[0]];
    const c = vivid(mov ? mov.palette : a.palette);
    const living = !a.died;
    const x = (a.born - TL_Y0) * pxy, w = Math.max(24, (end - a.born) * pxy);
    const bg = living ? `linear-gradient(90deg, ${c} 70%, ${rgba(c, 0.08)})` : c;
    return `<a class="tl2-bar" data-mov="${a.movements[0]}" href="#/artist/${a.id}"
      title="${esc(a.name)} · ${esc(a.years)} · ${mov ? esc(mov.name) : ""}"
      style="left:${x}px;top:${TOP + li * LANE}px;width:${w}px;height:${BARH}px;background:${bg};color:${luma(c) > 0.62 ? "#1d1a14" : "#f6f1e6"}">
      <span>${esc(a.name)}</span></a>`;
  }).join("");

  /* legend: most-populous primary movements */
  const counts = {};
  A.forEach(a => counts[a.movements[0]] = (counts[a.movements[0]] || 0) + 1);
  const legend = Object.entries(counts).sort((x, y) => y[1] - x[1]).slice(0, 14)
    .map(([mid, c]) => Mx[mid] ? `<button class="tl2-leg" data-tlmov="${mid}"><i style="background:${vivid(Mx[mid].palette)}"></i>${esc(Mx[mid].name)} · ${c}</button>` : "")
    .join("");

  return `
  <div class="page-head">
    <div class="page-kicker">Eight centuries at a glance</div>
    <h1 class="display">The grand timeline</h1>
    <p class="page-lede">Every painter in the atlas as a lifespan, coloured by movement. Picasso overlaps both Monet and Basquiat — see for yourself. Click any bar to visit; click a movement to isolate its painters.</p>
  </div>
  <div class="tl2-toolbar">
    <span class="f-label">Zoom</span>
    ${[["3","Compact"],["6","Standard"],["12","Detail"]].map(([z, l]) =>
      `<button class="f-btn ${tlZoom === +z ? "on" : ""}" data-tlzoom="${z}">${l}</button>`).join("")}
    <span class="f-spacer"></span>
    <span class="f-label">Jump to</span>
    ${E.map(e => `<button class="f-btn" data-tljump="${(e.start - TL_Y0) * pxy}">${esc(e.name.split(" ")[0])}</button>`).join("")}
  </div>
  <div class="tl2-legend"><button class="tl2-leg" data-tlmov=""><i style="background:var(--gold)"></i>All</button>${legend}</div>
  <div class="tl2-wrap" id="tl2"><div class="tl2-inner" style="width:${W}px;height:${H}px">${grid}${barHtml}</div></div>
  <p class="map-hint">${A.length} painters · ${laneEnds.length} lanes · fading bars are still painting</p>`;
}

/* ---------- world map (nations) with zoomable Europe inset ---------- */
const MAP_REGIONS = {
  world:  { vb: [0, 0, 1000, 420], mag: 1 },
  europe: { vb: [464, 62, 172, 96], mag: 4.6 }            /* lon ≈ -13…49, lat ≈ 33…68 */
};
let mapZoom = "world";
const mapProj = (lat, lon) => [ (lon + 180) / 360 * 1000, (90 - lat) / 180 * 500 ];

function isEuropean(n){
  const ll = window.NATION_COORDS[n.id];
  return ll && ll[0] > 33 && ll[0] < 67 && ll[1] > -13 && ll[1] < 49;
}

function mapDotsSVG(region){
  const mag = MAP_REGIONS[region].mag;
  let out = "";
  [...N].map(n => [n, artistsOfNation(n.id).length])
    .filter(([n]) => window.NATION_COORDS[n.id] && (region === "world" || isEuropean(n)))
    .sort((a, b) => b[1] - a[1])                          /* big circles behind small */
    .forEach(([n, c]) => {
      const [x, y] = mapProj(...window.NATION_COORDS[n.id]);
      const r  = region === "world" ? 5 + Math.sqrt(c) * 3 : (6 + Math.sqrt(c) * 1.9) / mag;
      const fs = region === "world" ? 13 : 10.5 / mag;
      const name = region === "europe"
        ? `<text class="md-name" style="font-size:${(9.5 / mag).toFixed(2)}px" x="${x.toFixed(1)}" y="${(y + r + 11 / mag).toFixed(2)}">${esc(n.name)} · ${c}</text>`
        : "";
      out += `<a href="#/nation/${n.id}" class="map-dot">
        <circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r.toFixed(2)}" vector-effect="non-scaling-stroke"/>
        <text class="md-flag" style="font-size:${fs.toFixed(2)}px" x="${x.toFixed(1)}" y="${(y + fs * 0.34).toFixed(2)}">${n.flag}</text>
        <title>${esc(n.name)} — ${c} painter${c === 1 ? "" : "s"}</title>${name}</a>`;
    });
  if(region === "world"){
    const [ex, ey, ew, eh] = MAP_REGIONS.europe.vb;       /* clickable Europe frame */
    out += `<rect class="eu-frame" data-zoom="europe" x="${ex}" y="${ey}" width="${ew}" height="${eh}" rx="6" vector-effect="non-scaling-stroke"><title>Zoom into Europe</title></rect>`;
  }
  return out;
}

function setMapZoom(target){
  if(target === mapZoom || !MAP_REGIONS[target]) return;
  const svg = document.getElementById("atlas-map");
  mapZoom = target;
  if(!svg) return;
  document.querySelectorAll(".map-zoom").forEach(b => b.classList.toggle("on", b.dataset.zoom === target));
  const dots = svg.querySelector("#map-dots");
  const from = svg.getAttribute("viewBox").split(/\s+/).map(Number);
  const to = MAP_REGIONS[target].vb;
  const finish = () => { dots.innerHTML = mapDotsSVG(target); dots.style.opacity = 1; };
  if(reducedMotion){ svg.setAttribute("viewBox", to.join(" ")); finish(); return; }
  dots.style.opacity = 0;
  const t0 = performance.now(), dur = 750;
  (function step(t){
    const p = Math.min(1, (t - t0) / dur);
    const e = p < 0.5 ? 4*p*p*p : 1 - Math.pow(-2*p + 2, 3) / 2;     /* easeInOutCubic */
    svg.setAttribute("viewBox", from.map((v, i) => (v + (to[i] - v) * e).toFixed(2)).join(" "));
    if(p < 1) requestAnimationFrame(step); else finish();
  })(t0);
}

function worldMapView(){
  if(!window.WORLD_PATH || !window.NATION_COORDS) return "";
  return `<div class="map-wrap">
    <div class="map-toolbar">
      <span class="f-label">Zoom</span>
      <button class="f-btn map-zoom ${mapZoom === "world" ? "on" : ""}" data-zoom="world">World</button>
      <button class="f-btn map-zoom ${mapZoom === "europe" ? "on" : ""}" data-zoom="europe">Europe</button>
    </div>
    <svg id="atlas-map" viewBox="${MAP_REGIONS[mapZoom].vb.join(" ")}" style="aspect-ratio:1000/420"
         xmlns="http://www.w3.org/2000/svg" role="img" aria-label="World map of painters by nation">
      <path class="map-land" d="${window.WORLD_PATH}" vector-effect="non-scaling-stroke"/>
      <g id="map-dots">${mapDotsSVG(mapZoom)}</g>
    </svg>
    <p class="map-hint">Circle size = painters in the atlas · click a circle to visit the nation · click the dashed frame (or Europe) to zoom in</p></div>`;
}

function viewHome(){
  const muse = A[Math.floor(Math.random()*A.length)];
  const featured = [...A].sort(() => Math.random()-0.5).slice(0,8);
  const topMovs = M.filter(m => !m.parent)
    .map(m => [m, artistsOfMovement(m.id).length]).sort((x,y) => y[1]-x[1]).slice(0,6);
  document.title = "Pigment — An Atlas of Painters";
  return `
  <header class="home-hero">
    ${canvasTag(muse.style, muse.palette, muse.id, true, String(Date.now()%100000))}
    <div class="hero-shade"></div>
    <div class="home-hero-content">
      <div class="kicker">Eight centuries · one atlas</div>
      <h1>Pigment</h1>
      <p class="lede">${A.length} painters from Giotto to right now — cross-linked by movement, technique, era and nation. Click anything; everything connects.</p>
      <div class="btn-row">
        <a class="btn" href="#/artists">Meet the painters</a>
        <a class="btn ghost" href="#/timeline">The grand timeline</a>
        <a class="btn ghost" href="#/movements">Browse movements</a>
      </div>
      <p class="footer-note" style="margin-top:22px">Tonight's cover: mixed after <a href="#/artist/${muse.id}">${esc(muse.name)}</a></p>
    </div>
  </header>

  <div class="stats-row">
    ${[[A.length,"Painters","artists"],[M.length,"Movements","movements"],[T.length,"Techniques","techniques"],[E.length,"Centuries","eras"],[N.length,"Nations","nations"]]
      .map(([n,l,href]) => `<a class="stat" href="#/${href}"><div class="num" data-count="${n}">0</div><div class="lbl">${l}</div></a>`).join("")}
  </div>

  <section>
    <h2 class="sec-title">Begin with an era</h2>
    <div class="era-strip">
      ${E.map(e => `<a class="era-tile" href="#/era/${e.id}">
          ${canvasTag(e.style, e.palette, e.id)}
          <div class="et-shade"></div>
          <div class="et-label"><b>${esc(e.name)}</b><span>${esc(e.range)} · ${artistsOfEra(e.id).length} painters</span></div>
        </a>`).join("")}
    </div>
  </section>

  <section>
    <h2 class="sec-title">Tonight's gallery <span class="count">a fresh hang on every visit</span></h2>
    <div class="cards">${featured.map(artistCard).join("")}</div>
  </section>

  <section>
    <h2 class="sec-title">Major movements</h2>
    <div class="tree-grid">${topMovs.map(([m,c]) => taxCard(m,"movement",c)).join("")}</div>
  </section>`;
}

function viewArtists(){
  document.title = "Artists — Pigment";
  let list = artistFilter.era === "all" ? [...A] : artistsOfEra(artistFilter.era);
  list.sort(artistFilter.sort === "chrono" ? (a,b) => a.born-b.born : (a,b) => a.name.localeCompare(b.name));
  return `
  <div class="page-head">
    <div class="page-kicker">The collection</div>
    <h1 class="display">All ${A.length} painters</h1>
    <p class="page-lede">Sorted ${artistFilter.sort === "chrono" ? "by birth year — a walk through time" : "alphabetically"}. Filter by century, or use the search above.</p>
  </div>
  <div class="filter-bar">
    <span class="f-label">Era</span>
    <button class="f-btn ${artistFilter.era==='all'?'on':''}" data-era="all">All</button>
    ${E.map(e => `<button class="f-btn ${artistFilter.era===e.id?'on':''}" data-era="${e.id}">${esc(e.name)}</button>`).join("")}
    <span class="f-spacer"></span>
    <span class="f-label">Sort</span>
    <button class="f-btn ${artistFilter.sort==='chrono'?'on':''}" data-sort="chrono">Chronological</button>
    <button class="f-btn ${artistFilter.sort==='az'?'on':''}" data-sort="az">A–Z</button>
  </div>
  <div class="cards">${list.map(artistCard).join("")}</div>`;
}

function viewArtist(id){
  const a = Ax[id]; if(!a) return view404();
  document.title = a.name + " — Pigment";
  const kindred = A.filter(o => o.id !== a.id)
    .map(o => [o, o.movements.filter(m => a.movements.includes(m)).length])
    .filter(([,c]) => c > 0).sort((x,y) => y[1]-x[1]).slice(0,6).map(([o]) => o);
  const nation = Nx[a.nation];
  return `
  ${hero({
    style:a.style, palette:a.palette, seed:a.id, salt:"hero",
    crumbs: crumbs([["Atlas",""],["Artists","artists"],[a.name]]),
    title:a.name,
    sub:`<span>${esc(a.years)}</span><a href="#/nation/${a.nation}">${nation ? nation.flag+" "+esc(nation.name) : ""}</a>` +
        a.eras.map(e => Ex[e] ? `<a href="#/era/${e}">${esc(Ex[e].name)}</a>` : "").join(""),
    tagline:a.tagline
  })}
  <div class="chip-label">Movements · Techniques · Era · Nation — click to travel</div>
  <div class="chips" style="margin-bottom:30px">${chipsFor(a)}</div>

  <div class="artist-cols">
    <div class="bio-block">
      <h2>The life</h2><p>${esc(a.life)}</p>
      <h2>The career</h2><p>${esc(a.career)}</p>
      <h2>Beyond the easel</h2><p>${esc(a.outside)}</p>
      <h2>Fun facts</h2>
      <ul class="facts">${a.facts.map(f => `<li>${esc(f)}</li>`).join("")}</ul>
    </div>
    <aside class="side-panel">
      <div class="panel">
        <h3>Major works</h3>
        ${a.works.map(wk => `<div class="work"><span class="w-year">${esc(wk.y)}</span><span class="w-title">${esc(wk.t)}</span></div>`).join("")}
      </div>
      ${kindred.length ? `<div class="panel">
        <h3>Kindred spirits</h3>
        <div class="mini-cards">
          ${kindred.map(o => `<a class="mini-card" href="#/artist/${o.id}">
              ${canvasTag(o.style, o.palette, o.id)}
              <span><span class="mc-name">${esc(o.name)}</span><br><span class="mc-meta">${esc(o.years)}</span></span>
            </a>`).join("")}
        </div>
      </div>` : ""}
      <div class="panel">
        <h3>Keep exploring</h3>
        <div class="chips">
          ${a.movements[0] && Mx[a.movements[0]] ? chip("m","movement/"+a.movements[0], "More "+Mx[a.movements[0]].name) : ""}
          ${nation ? chip("n","nation/"+a.nation, "Painters of "+nation.name) : ""}
          ${Ex[a.eras[0]] ? chip("e","era/"+a.eras[0], "The "+Ex[a.eras[0]].name) : ""}
        </div>
      </div>
    </aside>
  </div>`;
}

function taxIndexView(list, type, title, kicker, lede){
  document.title = title + " — Pigment";
  const roots = list.filter(x => !x.parent);
  const countFn = type === "movement" ? artistsOfMovement : artistsOfTechnique;
  const view = taxView[type];
  return `
  <div class="page-head">
    <div class="page-kicker">${kicker}</div>
    <h1 class="display">${title}</h1>
    <p class="page-lede">${lede}</p>
  </div>
  <div class="filter-bar">
    <span class="f-label">View</span>
    <button class="f-btn ${view === "cards" ? "on" : ""}" data-vtype="${type}" data-view="cards">Cards</button>
    <button class="f-btn ${view === "tree" ? "on" : ""}" data-vtype="${type}" data-view="tree">Family tree</button>
  </div>
  ${view === "tree"
    ? treeView(list, type)
    : `<div class="tree-grid">${roots.map(r => taxCard(r, type, countFn(r.id).length)).join("")}</div>`}`;
}

function taxDetailView(item, type){
  const isMov = type === "movement";
  const parent = item.parent ? (isMov ? Mx[item.parent] : Tx[item.parent]) : null;
  const kids = isMov ? movChildren(item.id) : tecChildren(item.id);
  const siblings = parent ? (isMov ? movChildren(parent.id) : tecChildren(parent.id)).filter(s => s.id !== item.id) : [];
  const artists = (isMov ? artistsOfMovement : artistsOfTechnique)(item.id).sort((a,b) => a.born-b.born);
  document.title = item.name + " — Pigment";

  /* cross-link: most common counterpart categories among these artists */
  const counter = {};
  artists.forEach(a => (isMov ? a.techniques : a.movements).forEach(x => counter[x] = (counter[x]||0)+1));
  const related = Object.entries(counter).sort((x,y) => y[1]-x[1]).slice(0,6)
    .map(([cid]) => isMov ? (Tx[cid] && chip("t","technique/"+cid, Tx[cid].name)) : (Mx[cid] && chip("m","movement/"+cid, Mx[cid].name)))
    .filter(Boolean).join("");

  const label = isMov ? "Movements" : "Techniques";
  return `
  ${hero({
    style:item.style, palette:item.palette, seed:item.id, salt:"hero",
    crumbs: crumbs(parent
      ? [["Atlas",""],[label, type+"s"],[parent.name, type+"/"+parent.id],[item.name]]
      : [["Atlas",""],[label, type+"s"],[item.name]]),
    title:item.name,
    sub:`${item.period ? `<span>${esc(item.period)}</span>` : ""}<span>${artists.length} painter${artists.length===1?"":"s"} in the atlas</span>`,
    tagline:item.blurb
  })}
  <section style="margin-top:0">
    <p class="desc-col">${esc(item.desc)}</p>
    <div class="branch-row">
      ${parent ? `<span class="chip-label" style="margin:0 4px 0 0">Branch of</span>${chip(isMov?"m":"t", type+"/"+parent.id, parent.name)}` : ""}
      ${kids.length ? `<span class="chip-label" style="margin:0 4px 0 12px">Branches</span>${kids.map(k => chip(isMov?"m":"t", type+"/"+k.id, k.name)).join("")}` : ""}
      ${siblings.length ? `<span class="chip-label" style="margin:0 4px 0 12px">Sister branches</span>${siblings.map(s => chip(isMov?"m":"t", type+"/"+s.id, s.name)).join("")}` : ""}
    </div>
    ${related ? `<div class="chip-label">${isMov ? "Signature techniques of its painters" : "Movements where it thrives"}</div><div class="chips">${related}</div>` : ""}
  </section>
  <section>
    <h2 class="sec-title">The painters <span class="count">${kids.length ? "including its branches" : ""}</span></h2>
    ${artists.length ? `<div class="cards">${artists.map(artistCard).join("")}</div>` : `<p class="page-lede">No painters filed here yet — follow the branches above.</p>`}
  </section>`;
}

function viewEras(){
  document.title = "Eras — Pigment";
  return `
  <div class="page-head">
    <div class="page-kicker">Time</div>
    <h1 class="display">Eight centuries of painting</h1>
    <p class="page-lede">From Giotto's Padua chapel to the studio livestream — each era gathers its painters, and every painter links onward.</p>
  </div>
  <div class="cards wide">
    ${E.map(e => {
      const n = artistsOfEra(e.id).length;
      return `<article class="card tax-card" data-href="#/era/${e.id}">
        <div class="card-art">${canvasTag(e.style, e.palette, e.id)}</div>
        <div class="card-body">
          <h3><a href="#/era/${e.id}">${esc(e.name)}</a></h3>
          <div class="card-meta">${esc(e.range)} · ${n} painters</div>
          <div class="card-tagline">${esc(e.blurb)}</div>
        </div>
      </article>`;
    }).join("")}
  </div>`;
}

function viewEra(id){
  const e = Ex[id]; if(!e) return view404();
  document.title = e.name + " — Pigment";
  const artists = artistsOfEra(id).sort((a,b) => a.born-b.born);
  const idx = E.findIndex(x => x.id === id);
  const movs = {};
  artists.forEach(a => a.movements.forEach(m => movs[m] = (movs[m]||0)+1));
  const movChips = Object.entries(movs).sort((x,y) => y[1]-x[1]).slice(0,8)
    .map(([mid]) => Mx[mid] && chip("m","movement/"+mid, Mx[mid].name)).filter(Boolean).join("");
  return `
  ${hero({
    style:e.style, palette:e.palette, seed:e.id, salt:"hero",
    crumbs: crumbs([["Atlas",""],["Eras","eras"],[e.name]]),
    title:e.name,
    sub:`<span>${esc(e.range)}</span><span>${artists.length} painters</span>` +
        (idx>0 ? `<a href="#/era/${E[idx-1].id}">← ${esc(E[idx-1].name)}</a>` : "") +
        (idx<E.length-1 ? `<a href="#/era/${E[idx+1].id}">${esc(E[idx+1].name)} →</a>` : ""),
    tagline:e.blurb
  })}
  <p class="desc-col">${esc(e.desc)}</p>
  ${movChips ? `<div class="chip-label">Movements of the era</div><div class="chips">${movChips}</div>` : ""}
  <section>
    <h2 class="sec-title">Born along the century <span class="count">hover the dots</span></h2>
    <div class="timeline">
      <div class="tl-rail"></div>
      ${artists.map(a => {
        const pct = Math.min(97, Math.max(3, ((a.born - e.start) / (e.end - e.start)) * 94 + 3));
        return `<a class="tl-dot" style="left:${pct.toFixed(1)}%" href="#/artist/${a.id}"><span class="tl-tip">${esc(a.name)} · b. ${a.born}</span></a>`;
      }).join("")}
      <span class="tl-year start">${e.start}</span><span class="tl-year end">${e.id==="21st-century" ? "today" : e.end}</span>
    </div>
  </section>
  <section>
    <h2 class="sec-title">The painters</h2>
    <div class="cards">${artists.map(artistCard).join("")}</div>
  </section>`;
}

function viewNations(){
  document.title = "Nations — Pigment";
  const sorted = [...N].map(n => [n, artistsOfNation(n.id).length]).sort((x,y) => y[1]-x[1]);
  return `
  <div class="page-head">
    <div class="page-kicker">Geography</div>
    <h1 class="display">Painting's map</h1>
    <p class="page-lede">Where the painters came from — though most of them, as you'll read, refused to stay put.</p>
  </div>
  ${worldMapView()}
  <div class="cards">
    ${sorted.map(([n,c]) => `<article class="card tax-card" data-href="#/nation/${n.id}">
        <div class="card-art">${canvasTag("fauvist", n.palette, n.id)}</div>
        <div class="card-body">
          <h3><a href="#/nation/${n.id}">${n.flag} ${esc(n.name)}</a></h3>
          <div class="card-meta">${c} painter${c===1?"":"s"}</div>
          <div class="card-tagline">${esc(n.blurb)}</div>
        </div>
      </article>`).join("")}
  </div>`;
}

function viewNation(id){
  const n = Nx[id]; if(!n) return view404();
  document.title = n.name + " — Pigment";
  const artists = artistsOfNation(id).sort((a,b) => a.born-b.born);
  const movs = {};
  artists.forEach(a => a.movements.forEach(m => movs[m] = (movs[m]||0)+1));
  const movChips = Object.entries(movs).sort((x,y) => y[1]-x[1]).slice(0,8)
    .map(([mid]) => Mx[mid] && chip("m","movement/"+mid, Mx[mid].name)).filter(Boolean).join("");
  return `
  ${hero({
    style:"fauvist", palette:n.palette, seed:n.id, salt:"hero",
    crumbs: crumbs([["Atlas",""],["Nations","nations"],[n.name]]),
    title:`${n.flag} ${n.name}`,
    sub:`<span>${artists.length} painter${artists.length===1?"":"s"} in the atlas</span>`,
    tagline:n.blurb
  })}
  ${movChips ? `<div class="chip-label">Movements they shaped</div><div class="chips" style="margin-bottom:26px">${movChips}</div>` : ""}
  <section style="margin-top:8px">
    <h2 class="sec-title">The painters</h2>
    <div class="cards">${artists.map(artistCard).join("")}</div>
  </section>`;
}

function view404(){
  document.title = "Lost — Pigment";
  return `<div class="lost">
    <h1>Blank canvas</h1>
    <p>This page hasn't been painted. Try the <a href="#/">atlas home</a>, or the <a href="#/artists">full collection</a>.</p>
  </div>`;
}

/* ============================================================
   ROUTER
   ============================================================ */
function route(){
  const hash = decodeURIComponent(location.hash.replace(/^#\/?/, ""));
  const [page, id] = hash.split("/");
  let html;
  switch(page){
    case "":            html = viewHome(); break;
    case "artists":     html = viewArtists(); break;
    case "timeline":    html = viewTimeline(); break;
    case "artist":      html = viewArtist(id); break;
    case "movements":   html = taxIndexView(M, "movement", "Movements", "Schools & revolutions",
                          "Every -ism with its branches and sub-branches — from the Renaissance workshop to Superflat. Open one to find its painters, techniques and offspring."); break;
    case "movement":    html = Mx[id] ? taxDetailView(Mx[id], "movement") : view404(); break;
    case "techniques":  html = taxIndexView(T, "technique", "Techniques", "The hand & the tool",
                          "How the paint actually got there — glazes, drips, dots, squeegees and stencils, each with its family tree and its practitioners."); break;
    case "technique":   html = Tx[id] ? taxDetailView(Tx[id], "technique") : view404(); break;
    case "eras":        html = viewEras(); break;
    case "era":         html = viewEra(id); break;
    case "nations":     html = viewNations(); break;
    case "nation":      html = viewNation(id); break;
    default:            html = view404();
  }
  app.classList.remove("view-enter");
  void app.offsetWidth;                    /* restart animation */
  app.innerHTML = html;
  app.classList.add("view-enter");
  const de = document.documentElement;
  de.style.scrollBehavior = "auto";        /* jump, don't glide, between pages */
  window.scrollTo(0, 0);
  de.style.scrollBehavior = "";
  paintAll(app);
  animateCounters();
  setNav(page);
  hideSearch();
}

function setNav(page){
  const map = { artists:"artists", artist:"artists", timeline:"timeline", movements:"movements", movement:"movements",
    techniques:"techniques", technique:"techniques", eras:"eras", era:"eras", nations:"nations", nation:"nations" };
  document.querySelectorAll("#main-nav a").forEach(a =>
    a.classList.toggle("active", a.dataset.nav === map[page]));
}

function animateCounters(){
  app.querySelectorAll("[data-count]").forEach(el => {
    const target = +el.dataset.count, t0 = performance.now(), dur = reducedMotion ? 1 : 900;
    (function tick(t){
      const p = Math.min(1, (t - t0) / dur);
      el.textContent = Math.round(target * (1 - Math.pow(1-p, 3)));
      if(p < 1) requestAnimationFrame(tick);
    })(t0);
  });
}

/* clicks: cards navigate; filter buttons re-render */
app.addEventListener("click", e => {
  const zoomEl = e.target.closest("[data-zoom]");
  if(zoomEl){ setMapZoom(zoomEl.dataset.zoom); return; }   /* map zoom: animate, don't re-render */
  const tz = e.target.closest("[data-tlzoom]");
  if(tz){                                                  /* timeline zoom: keep centre in view */
    const wrap = document.getElementById("tl2");
    const fr = wrap ? (wrap.scrollLeft + wrap.clientWidth / 2) / wrap.scrollWidth : 0;
    tlZoom = +tz.dataset.tlzoom;
    route();
    const w2 = document.getElementById("tl2");
    if(w2) w2.scrollLeft = fr * w2.scrollWidth - w2.clientWidth / 2;
    return;
  }
  const tj = e.target.closest("[data-tljump]");
  if(tj){
    const wrap = document.getElementById("tl2");
    if(wrap) wrap.scrollTo({ left: Math.max(0, +tj.dataset.tljump - 30), behavior: reducedMotion ? "auto" : "smooth" });
    return;
  }
  const tm = e.target.closest("[data-tlmov]");
  if(tm){                                                  /* movement isolation, no re-render */
    const wasOn = tm.classList.contains("on");
    document.querySelectorAll("[data-tlmov]").forEach(b => b.classList.remove("on"));
    const mid = !wasOn ? tm.dataset.tlmov : "";
    if(!wasOn) tm.classList.add("on");
    document.querySelectorAll(".tl2-bar").forEach(b => b.classList.toggle("dim", !!mid && b.dataset.mov !== mid));
    return;
  }
  const fbtn = e.target.closest(".f-btn");
  if(fbtn){
    if(fbtn.dataset.era) artistFilter.era = fbtn.dataset.era;
    if(fbtn.dataset.sort) artistFilter.sort = fbtn.dataset.sort;
    if(fbtn.dataset.view) taxView[fbtn.dataset.vtype] = fbtn.dataset.view;
    route(); return;
  }
  if(e.target.closest("a")) return;
  const card = e.target.closest("[data-href]");
  if(card) location.hash = card.dataset.href;
});

window.addEventListener("hashchange", route);

/* ============================================================
   SEARCH
   ============================================================ */
const searchInput = document.getElementById("search");
const searchResults = document.getElementById("search-results");
const INDEX = [
  ...A.map(a => ({ type:"Artists",    href:"artist/"+a.id,    name:a.name, meta:a.years })),
  ...M.map(m => ({ type:"Movements",  href:"movement/"+m.id,  name:m.name, meta:m.period || "" })),
  ...T.map(t => ({ type:"Techniques", href:"technique/"+t.id, name:t.name, meta:"" })),
  ...E.map(e => ({ type:"Eras",       href:"era/"+e.id,       name:e.name, meta:e.range })),
  ...N.map(n => ({ type:"Nations",    href:"nation/"+n.id,    name:n.flag+" "+n.name, meta:"" }))
];
let selIdx = -1;

function runSearch(q){
  q = q.trim().toLowerCase();
  if(!q){ hideSearch(); return; }
  const starts = [], contains = [];
  INDEX.forEach(it => {
    const n = it.name.toLowerCase();
    if(n.startsWith(q)) starts.push(it);
    else if(n.includes(q)) contains.push(it);
  });
  const hits = [...starts, ...contains].slice(0, 9);
  selIdx = -1;
  if(!hits.length){
    searchResults.innerHTML = `<div class="sr-empty">Nothing in the atlas matches “${esc(q)}”.</div>`;
  } else {
    let html = "", lastType = "";
    hits.forEach((it, i) => {
      if(it.type !== lastType){ html += `<div class="sr-group">${it.type}</div>`; lastType = it.type; }
      html += `<a href="#/${it.href}" data-i="${i}"><span>${esc(it.name)}</span><span class="sr-meta">${esc(it.meta)}</span></a>`;
    });
    searchResults.innerHTML = html;
  }
  searchResults.hidden = false;
}
function hideSearch(){ searchResults.hidden = true; selIdx = -1; }

searchInput.addEventListener("input", () => runSearch(searchInput.value));
searchInput.addEventListener("focus", () => { if(searchInput.value.trim()) runSearch(searchInput.value); });
searchInput.addEventListener("keydown", e => {
  const links = [...searchResults.querySelectorAll("a")];
  if(e.key === "ArrowDown" || e.key === "ArrowUp"){
    e.preventDefault();
    if(!links.length) return;
    selIdx = (selIdx + (e.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
    links.forEach((l,i) => l.classList.toggle("sel", i === selIdx));
    links[selIdx].scrollIntoView({ block:"nearest" });
  } else if(e.key === "Enter"){
    const target = links[selIdx >= 0 ? selIdx : 0];
    if(target){ location.hash = target.getAttribute("href"); searchInput.value = ""; hideSearch(); searchInput.blur(); }
  } else if(e.key === "Escape"){ hideSearch(); searchInput.blur(); }
});
searchResults.addEventListener("click", () => { searchInput.value = ""; hideSearch(); });
document.addEventListener("click", e => { if(!e.target.closest(".search-wrap")) hideSearch(); });

/* ============================================================
   THEME — dark gallery / light paper, persisted
   ============================================================ */
const themeBtn = document.getElementById("theme-toggle");
function currentTheme(){ return document.documentElement.dataset.theme === "light" ? "light" : "dark"; }
function applyTheme(t){
  document.documentElement.dataset.theme = t;
  try{ localStorage.setItem("pigment-theme", t); }catch(e){}
  themeBtn.textContent = t === "light" ? "☾" : "☀";
  if(window.__bgInit) window.__bgInit();
}
themeBtn.addEventListener("click", () => applyTheme(currentTheme() === "light" ? "dark" : "light"));
themeBtn.textContent = currentTheme() === "light" ? "☾" : "☀";

/* ============================================================
   AMBIENT BACKGROUND — drifting pigment blobs & flowing ribbons
   ============================================================ */
(function bg(){
  const cv = document.getElementById("bg-canvas");
  const ctx = cv.getContext("2d");
  const SETS = {
    dark:  { blobs:["#c9a45c","#7b3b43","#3e5570","#3e5a46","#6e3a5e"],
             ribbons:["#c9a45c","#6fb3a8","#c97b6a"], blobA:0.16, ribA:0.07, comp:"lighter" },
    light: { blobs:["#a8813c","#a85544","#4a6e9e","#3e7a5e","#6e3a5e"],
             ribbons:["#a8813c","#2e7a6e","#a85544"], blobA:0.10, ribA:0.10, comp:"source-over" }
  };
  let blobs = [], ribbons = [], W, H, set = SETS.dark;
  function init(){
    set = SETS[currentTheme()] || SETS.dark;
    W = cv.width = Math.round(innerWidth * 0.55);
    H = cv.height = Math.round(innerHeight * 0.55);
    blobs = set.blobs.map(c => ({
      c, r: (0.22 + Math.random()*0.16) * Math.max(W,H),
      dx: 0.18 + Math.random()*0.4, dy: 0.14 + Math.random()*0.36,
      px: Math.random()*1000, py: Math.random()*1000
    }));
    ribbons = set.ribbons.map((c, i) => ({
      c, base: 0.18 + i*0.28 + Math.random()*0.08,
      amp: 0.05 + Math.random()*0.07,
      freq: 1.1 + Math.random()*1.6,
      speed: 0.00012 + Math.random()*0.00012,
      ph: Math.random()*Math.PI*2,
      w: Math.max(6, H*0.012) + Math.random()*10
    }));
    if(reducedMotion) frame(0);
  }
  function ribbonPath(rb, t){                     /* a brushstroke that breathes */
    ctx.beginPath();
    for(let i=0;i<=72;i++){
      const u = i/72;
      const x = u*W;
      const y = (rb.base + Math.sin(u*rb.freq*Math.PI*2 + t*rb.speed + rb.ph)*rb.amp
                + Math.sin(u*5.3 + t*rb.speed*0.55 + rb.ph*2)*rb.amp*0.4) * H;
      i ? ctx.lineTo(x,y) : ctx.moveTo(x,y);
    }
  }
  function frame(t){
    ctx.clearRect(0,0,W,H);
    ctx.globalCompositeOperation = set.comp;
    blobs.forEach(b => {
      const x = (Math.sin(t*0.00004*b.dx + b.px) * 0.5 + 0.5) * W;
      const y = (Math.cos(t*0.00005*b.dy + b.py) * 0.5 + 0.5) * H;
      const g = ctx.createRadialGradient(x,y,1, x,y,b.r);
      g.addColorStop(0, rgba(b.c, set.blobA)); g.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = g;
      ctx.fillRect(x-b.r, y-b.r, b.r*2, b.r*2);
    });
    ctx.lineCap = "round";
    ribbons.forEach(rb => {
      ribbonPath(rb, t);
      ctx.strokeStyle = rgba(rb.c, set.ribA);     /* soft halo pass */
      ctx.lineWidth = rb.w * 2.6;
      ctx.stroke();
      ribbonPath(rb, t);
      ctx.strokeStyle = rgba(rb.c, set.ribA * 1.8); /* brighter core */
      ctx.lineWidth = rb.w;
      ctx.stroke();
    });
    ctx.globalCompositeOperation = "source-over";
    if(!reducedMotion) requestAnimationFrame(frame);
  }
  window.__bgInit = init;
  window.addEventListener("resize", init);
  init();
  if(!reducedMotion) requestAnimationFrame(frame);
})();

/* go */
route();
})();
