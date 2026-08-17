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

const CAT = window.CATALOG || [];
const CatX = byId(CAT);
const Vx = byId(window.VENUES || []);
const catByArtist = {};
CAT.forEach(w => (catByArtist[w.artistId] = catByArtist[w.artistId] || []).push(w));
const LISTS = window.EDITORIAL_LISTS || [];
/* B2. Actuality — the monthly ritual. See docs/ACTUALITY.md and js/actuality-1.js. */
const ACT = (window.ACTUALITY || []).slice().sort((a,b) => (b.published||"").localeCompare(a.published||""));
const Lsx = byId(LISTS);
const listsByWork = {};
LISTS.forEach(l => l.works.forEach(e => (listsByWork[e.id] = listsByWork[e.id] || []).push(l)));
const VEN = window.VENUES || [];
const MNOTES = window.MUSEUM_NOTES || {};
const VENUE_SENTINELS = { "private-collection":1, "lost":1, "unknown":1 };
const catByVenue = {};
CAT.forEach(w => { if(w.museum && w.museum.id) (catByVenue[w.museum.id] = catByVenue[w.museum.id] || []).push(w); });

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
/* decorative punctuation, hidden from assistive technology (AT-5).
   "or surprise me →" was announced as "or surprise me right arrow". One
   constant per glyph rather than twenty inline spans, so no call site can
   reintroduce a bare arrow, and the visual is byte-identical. */
const ARR = '<span aria-hidden="true">→</span>';
const ARRL = '<span aria-hidden="true">←</span>';

/* ---------------- the results channel (AT-1, AT-3, AT-6, AT-7) ----------------
   The owner's two VoiceOver sessions found one defect wearing four faces: the
   application performs the correct action and never says that it did. The deck
   never named the artwork being judged; dismissing search, cancelling an import
   and completing a merge were all silent. They are fixed as one thing, through
   one channel, because they are one defect.

   `say()` writes the persistent #live-status region in index.html. The clear-
   then-set is required: writing the same string twice in a row is not a
   mutation, and an unchanged region announces nothing.

   `sayNext()` is for the two results that cross a route boundary (import cancel,
   merge outcome). Setting the region before the new page renders races the
   router's focus move; queueing it and flushing at the END of route() makes the
   order deterministic — the heading is announced first, the result second.
   Neither is the whole-page live region unit 25f removed for C-8: route() never
   writes here of its own accord, only when a call site has queued a result. */
const liveStatus = document.getElementById("live-status");
let liveTimer = 0, pendingSay = null;
function say(msg, delay){
  if(!liveStatus || !msg) return;
  clearTimeout(liveTimer);
  liveStatus.textContent = "";
  liveTimer = setTimeout(() => { liveStatus.textContent = msg; }, delay || 60);
}
function sayNext(msg){ pendingSay = msg; }
/* short/family name for an artist — keeps leading particles (van/da/de/el…) with the surname */
const NAME_PARTICLES = new Set(["van","von","der","den","de","del","della","di","da","du","la","le","los","las","dos","ten","ter","of","the","el","al"]);
function artistShortName(a){
  const parts = String(a && a.name || "").trim().split(/\s+/);
  if(parts.length <= 1) return parts[0] || "";
  let i = parts.length - 1;
  while(i > 0 && NAME_PARTICLES.has(parts[i - 1].toLowerCase())) i--;
  return parts.slice(i).join(" ");
}
function hashStr(s){ let h = 2166136261; for(let i=0;i<s.length;i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
function mulberry(seed){ let a = seed; return function(){ a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function hex2rgb(hx){ const v = hx.replace("#",""); return [parseInt(v.slice(0,2),16), parseInt(v.slice(2,4),16), parseInt(v.slice(4,6),16)]; }
function rgba(hx, a){ const [r,g,b] = hex2rgb(hx); return `rgba(${r},${g},${b},${a})`; }
function shade(hx, f){ const [r,g,b] = hex2rgb(hx); const m = v => Math.max(0, Math.min(255, Math.round(v*f))); return `rgb(${m(r)},${m(g)},${m(b)})`; }
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ---------- taste distance (TASTE_MATH §1.3) ---------- */
const AXW = { F: 1.5, D: 1.5, E: 1, C: 1, M: 1 };
function tasteDist(a, b){
  let s = 0;
  for(const k in AXW){ const d = (a[k] || 0) - (b[k] || 0); s += AXW[k] * d * d; }
  return Math.sqrt(s);
}

/* ---------- the Taste Passport (ADMIRE_SPEC §10) ---------- */
const PASSPORT_KEY = "pigment.taste.v1";
/* storage health — reads and writes can fail (quota, private browsing, corrupt JSON).
   We record what actually happened so the interface can say it plainly instead of
   showing an empty state or claiming a save that never landed. */
const ppState = { read: "ok", write: "ok", corrupt: false };
function ppRaw(){
  try{ return localStorage.getItem(PASSPORT_KEY); }catch(e){ return null; }
}
function getPassport(){
  let raw;
  try{ raw = localStorage.getItem(PASSPORT_KEY); }
  catch(e){ ppState.read = "denied"; return null; }
  ppState.read = "ok";
  if(raw === null || raw === ""){ ppState.corrupt = false; return null; }   /* genuinely no passport yet */
  try{
    const p = JSON.parse(raw);
    if(p && typeof p === "object"){ ppState.corrupt = false; return p; }
  }catch(e){}
  ppState.corrupt = true;      /* present but unreadable — the stored bytes stay untouched */
  return null;
}
/* the single write path: it never overwrites a passport we could not read */
function ppWrite(p){
  if(ppState.corrupt || ppState.read === "denied") return false;
  try{
    localStorage.setItem(PASSPORT_KEY, JSON.stringify(p));
    ppState.write = "ok";
    return true;
  }catch(e){ ppState.write = "failed"; return false; }
}
function newPassport(){
  const now = new Date().toISOString();
  return { version: 1, createdAt: now, updatedAt: now,
    admirations: [], notForMe: [], seen: [], wantToSee: [], saved: [], probes: [],
    quiz: null, palette: null,
    persona: { adopted: null, candidates: [], adoptedAt: null, hidden: false },
    tasteVector: null, milestones: { onboarded: false, confidence: "sketch" } };
}
function passportHas(field, id){
  const p = getPassport();
  return !!p && Array.isArray(p[field]) && p[field].some(e => e.id === id);
}
function passportToggle(field, id){
  const p = getPassport() || newPassport();
  const arr = p[field];
  const i = arr.findIndex(e => e.id === id);
  if(i >= 0) arr.splice(i, 1); else arr.push({ id, at: new Date().toISOString() });
  p.updatedAt = new Date().toISOString();
  if(!ppWrite(p)) return null;      /* nothing was stored — the caller must not claim it was */
  return i < 0;
}
const PP_LABELS = {
  admirations: ["Admire", "Admired ✓"],
  seen: ["Seen in person", "Seen in person ✓"],
  saved: ["Save for later", "Saved ✓"]
};
/* a literal notice when storage refuses us — states what did not happen, offers a way out */
const PP_WRITE_MSG = "Not saved. This device would not store your Taste Passport — it may be out of room, or site data may be switched off for this browser. Nothing already saved has changed.";
function ppNotice(msg){
  let el = document.getElementById("pp-notice");
  if(!el){
    el = document.createElement("div");
    el.id = "pp-notice";
    el.className = "pp-notice";
    el.setAttribute("role", "status");
    document.body.appendChild(el);
  }
  el.innerHTML = `<p>${esc(msg)}</p>
    <div class="chips">
      <button class="chip" data-tsx="export">Back up data (.json)</button>
      <a class="chip" href="#/taste">Open the Taste Passport</a>
      <button class="chip" data-tsx="notice-close">Dismiss</button>
    </div>`;
  el.hidden = false;
}
function passportActions(w){
  return ["admirations", "seen", "saved"].map((field, i) => {
    const on = passportHas(field, w.id);
    return `<button class="aw-btn ${i === 0 ? "primary" : ""} ${on ? "on" : ""}" data-pp="${field}" data-ppid="${w.id}" aria-pressed="${on}">${PP_LABELS[field][on ? 1 : 0]}</button>`;
  }).join("");
}

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
/* a cover is never the artwork itself (PIGMENT.md §14) — the accessible name says so */
const coverLabel = subject => `Generative cover for ${subject}, painted in the browser`;
const canvasTag = (style, palette, seed, label, eager, salt) =>
  `<canvas role="img" aria-label="${esc(label || "Generative cover painted in the browser")}" data-paint data-style="${style}" data-colors="${palette.join(",")}" data-seed="${esc(seed)}"${eager?' data-eager="1"':''}${salt?` data-salt="${esc(salt)}"`:''}></canvas>`;

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
    <div class="card-art">${canvasTag(a.style, a.palette, a.id, coverLabel(a.name))}</div>
    <div class="card-body">
      <h3><a href="#/artist/${a.id}">${esc(a.name)}</a></h3>
      <div class="card-meta">${esc(a.years)} · ${Nx[a.nation] ? esc(Nx[a.nation].name) : ""}</div>
      <div class="card-tagline">${esc(a.tagline)}</div>
      <div class="chips">${movs}</div>
    </div>
  </article>`;
}

function artworkCard(w){
  const a = Ax[w.artistId];
  const img = w.image && w.image.src && w.image.status === "pd";
  return `<article class="card aw-card" data-href="#/artwork/${w.id}">
    <div class="card-art">${img
      ? `<img loading="lazy" src="${w.image.src}" alt="${esc(w.title)} by ${esc(a.name)}">`
      : canvasTag(a.style, a.palette, w.id, coverLabel(w.title + " by " + a.name))}</div>
    <div class="card-body">
      <h3><a href="#/artwork/${w.id}">${esc(w.title)}</a></h3>
      <div class="card-meta">${esc(a.name)} · ${esc(w.year.display)}</div>
    </div>
  </article>`;
}

function taxCard(item, type, count){
  const kids = (type === "movement" ? movChildren(item.id) : tecChildren(item.id));
  return `<article class="card tax-card" data-href="#/${type}/${item.id}">
    <div class="card-art">${canvasTag(item.style, item.palette, item.id, coverLabel(item.name))}</div>
    <div class="card-body">
      <h3><a href="#/${type}/${item.id}">${esc(item.name)}</a></h3>
      <div class="card-meta">${item.period ? esc(item.period) + " · " : ""}${count} artist${count===1?"":"s"}</div>
      <div class="card-tagline">${esc(item.blurb)}</div>
      ${kids.length ? `<div class="chips branch-list">${kids.map(k => `<a class="branch-chip" href="#/${type}/${k.id}" aria-label="${esc(k.name)}">${esc(k.name)}</a>`).join("")}</div>` : ""}
    </div>
  </article>`;
}

const crumbs = parts => `<nav class="breadcrumbs">` +
  parts.map((p,i) => i === parts.length-1
    ? `<span>${esc(p[0])}</span>`
    : `<a href="#/${p[1]}">${esc(p[0])}</a><span class="sep">/</span>`).join("") + `</nav>`;

function hero(opts){
  return `<header class="hero">
    ${canvasTag(opts.style, opts.palette, opts.seed, coverLabel(opts.title), true, opts.salt)}
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
let tlLegendAll = false;                                   /* legend collapsed to top 14 by default */
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
/* WCAG 2.2 relative luminance and contrast ratio: the timeline bar labels are
   chosen by measurement, not by a luma threshold (AC19). */
function relLum(hx){
  const lin = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const [r, g, b] = hex2rgb(hx);
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}
function contrast(a, b){
  const l1 = relLum(a), l2 = relLum(b);
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}
function rgb2hsl(hx){
  const [r, g, b] = hex2rgb(hx).map(v => v / 255);
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2;
  if(mx === mn) return [0, 0, l];
  const d = mx - mn, s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn);
  const h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [h / 6, s, l];
}
function hsl2hex(h, s, l){
  const hex2 = v => Math.round(v * 255).toString(16).padStart(2, "0");
  if(s === 0) return "#" + hex2(l).repeat(3);
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q;
  const f = t => {
    t = (t + 1) % 1;
    if(t < 1/6) return p + (q - p) * 6 * t;
    if(t < 1/2) return q;
    if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
    return p;
  };
  return "#" + hex2(f(h + 1/3)) + hex2(f(h)) + hex2(f(h - 1/3));
}
/* A bar label is either the dark ground or the bar paper, whichever clears AA on
   this fill. Five of the movement swatches sit in a dead zone where neither ink
   reaches it; those get a render-time darkening of at most 0.039 in HSL
   lightness, hue and saturation untouched. This is a display transform on the
   painted fill only — the palette records in js/taxonomy.js are never edited. */
const BAR_INK_DARK = "#0d0c0a", BAR_INK_PAPER = "#f6f1e6", BAR_AA = 4.6;
const barInkCache = {};
function barInk(fill){
  if(barInkCache[fill]) return barInkCache[fill];
  let out;
  if(contrast(BAR_INK_DARK, fill) >= BAR_AA) out = { fill: fill, ink: BAR_INK_DARK };
  else if(contrast(BAR_INK_PAPER, fill) >= BAR_AA) out = { fill: fill, ink: BAR_INK_PAPER };
  else {
    const [h, s, l] = rgb2hsl(fill);
    out = { fill: fill, ink: BAR_INK_PAPER };
    for(let d = 1; d <= 80; d++){
      const f = hsl2hex(h, s, Math.max(0, l - d / 1000));
      if(contrast(BAR_INK_PAPER, f) >= BAR_AA){ out.fill = f; break; }
    }
  }
  barInkCache[fill] = out;
  return out;
}

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
    const { fill: c, ink } = barInk(vivid(mov ? mov.palette : a.palette));
    const living = !a.died;
    const x = (a.born - TL_Y0) * pxy, w = Math.max(24, (end - a.born) * pxy);
    const bg = living ? `linear-gradient(90deg, ${c} 70%, ${rgba(c, 0.08)})` : c;
    return `<a class="tl2-bar" data-mov="${a.movements[0]}" href="#/artist/${a.id}"
      title="${esc(a.name)} · ${esc(a.years)} · ${mov ? esc(mov.name) : ""}"
      style="left:${x}px;top:${TOP + li * LANE}px;width:${w}px;height:${BARH}px;background:${bg};color:${ink}">
      <span>${esc(a.name)}</span></a>`;
  }).join("");

  /* legend: every primary movement in use (collapsed to the top 14 by default) */
  const counts = {};
  A.forEach(a => counts[a.movements[0]] = (counts[a.movements[0]] || 0) + 1);
  const legEntries = Object.entries(counts).sort((x, y) => y[1] - x[1]).filter(([mid]) => Mx[mid]);
  const legend = (tlLegendAll ? legEntries : legEntries.slice(0, 14))
    .map(([mid, c]) => `<button class="tl2-leg" data-tlmov="${mid}" aria-pressed="false"><i style="background:${vivid(Mx[mid].palette)}"></i>${esc(Mx[mid].name)} · ${c}</button>`)
    .join("");
  const legMore = legEntries.length > 14
    ? `<button class="tl2-leg tl2-leg-more" data-tlleg aria-expanded="${tlLegendAll}">${tlLegendAll ? "show fewer −" : "+ " + (legEntries.length - 14) + " more movements"}</button>` : "";

  return `
  <div class="page-head">
    <div class="page-kicker">Eight centuries at a glance</div>
    <h1 class="display">The grand timeline</h1>
    <p class="page-lede">Every painter in the atlas as a lifespan, coloured by movement. Picasso overlaps both Monet and Basquiat — see for yourself. Click any bar to visit; click a movement to isolate its painters.</p>
  </div>
  <div class="tl2-toolbar">
    <span class="f-label">Zoom</span>
    ${[["3","Compact"],["6","Standard"],["12","Detail"]].map(([z, l]) =>
      `<button class="f-btn ${tlZoom === +z ? "on" : ""}" data-tlzoom="${z}" aria-pressed="${tlZoom === +z}">${l}</button>`).join("")}
    <span class="f-spacer"></span>
    <span class="f-label">Jump to</span>
    ${E.map(e => `<button class="f-btn" data-tljump="${(e.start - TL_Y0) * pxy}">${esc(e.name.split(" ")[0])}</button>`).join("")}
  </div>
  <div class="tl2-legend"><button class="tl2-leg" data-tlmov="" aria-pressed="false"><i style="background:var(--gold)"></i>All</button>${legend}${legMore}</div>
  <div class="tl2-wrap" id="tl2"><div class="tl2-inner" style="width:${W}px;height:${H}px">${grid}${barHtml}</div></div>
  <p class="map-hint">${A.length} painters · ${laneEnds.length} lanes · fading bars are still painting</p>`;
}

/* ---------- the influence graph ---------- */
const IG_WORDS = {
  taught: ["taught by", "taught"], influenced: ["influenced by", "influenced"],
  befriended: ["friend of", "friend of"], rivaled: ["rival of", "rival of"],
  partners: ["partner of", "partner of"]
};
/* Colour is not carried here any more: a theme-invariant hex cannot satisfy both
   themes at once, and the `<b>` labels below are body text (AC19, 4.5:1). Each
   type gets an `e-<type>` class instead, and `css/styles.css` resolves it to a
   theme token through `--rc` — stroke, arrowhead fill, legend swatch and label
   all read the same custom property. The dash patterns still carry type
   redundantly, so nothing here depends on colour alone. */
const EDGE_STYLE = {
  taught:     { label:"taught",      dash:"",      arrow:true  },
  influenced: { label:"influenced",  dash:"5 4",   arrow:true  },
  befriended: { label:"friends",     dash:"",      arrow:false },
  rivaled:    { label:"rivals",      dash:"2 4",   arrow:false },
  partners:   { label:"partners",    dash:"",      arrow:false }
};

function influenceLayout(W, H){
  const deg = {};
  window.INFLUENCES.forEach(([a, b]) => { deg[a] = (deg[a]||0)+1; deg[b] = (deg[b]||0)+1; });
  const nodes = A.filter(a => deg[a.id]).map(a => ({
    a, d: deg[a.id], x:0, y:0, dx:0, dy:0,
    r: 6 + Math.min(deg[a.id], 9) * 1.4,
    hw: Math.min(110, a.name.length * 3.1) + 8            /* half label width, for margins */
  }));
  const idx = Object.fromEntries(nodes.map((n, i) => [n.a.id, i]));
  const edges = window.INFLUENCES.map(([f, t, ty]) => ({ s: nodes[idx[f]], t: nodes[idx[t]], ty }));

  const R = mulberry(hashStr("pigment-constellation"));
  nodes.forEach(n => {                                    /* seed roughly by birth year → x */
    n.x = W * 0.08 + ((n.a.born - 1240) / 790) * W * 0.84 + (R() - 0.5) * 60;
    n.y = H * 0.12 + R() * H * 0.76;
  });
  const k = Math.sqrt(W * H / nodes.length) * 0.6;
  const clamp = n => {
    n.x = Math.max(n.hw + 8, Math.min(W - n.hw - 8, n.x));
    n.y = Math.max(44, Math.min(H - 48, n.y));            /* room for the label below */
  };
  /* squared distance from point p to segment ab */
  const segDist2 = (p, a, b) => {
    const abx = b.x - a.x, aby = b.y - a.y;
    const t = Math.max(0, Math.min(1, ((p.x - a.x) * abx + (p.y - a.y) * aby) / (abx*abx + aby*aby || 1)));
    const qx = a.x + abx * t - p.x, qy = a.y + aby * t - p.y;
    return { d2: qx*qx + qy*qy, qx, qy };
  };

  const IT = 380;
  for(let it = 0; it < IT; it++){
    const cool = 1 - it / IT, step = 15 * cool + 0.6;
    nodes.forEach(n => { n.dx = 0; n.dy = 0; });
    for(let i = 0; i < nodes.length; i++)
      for(let j = i + 1; j < nodes.length; j++){
        const a = nodes[i], b = nodes[j];
        let dx = a.x - b.x, dy = a.y - b.y;
        let d2 = dx*dx + dy*dy || 0.01;
        if(d2 < k*k*10){ const f = (k*k) / d2; a.dx += dx*f; a.dy += dy*f; b.dx -= dx*f; b.dy -= dy*f; }
        if(it > IT * 0.6){                                /* label boxes repel in the endgame */
          const ox = a.hw + b.hw - Math.abs(dx), oy = 30 - Math.abs(dy);
          if(ox > 0 && oy > 0){
            const push = Math.min(ox, oy) * 0.5, sx = dx < 0 ? -1 : 1, sy = dy < 0 ? -1 : 1;
            if(ox < oy){ a.dx += sx * push; b.dx -= sx * push; }
            else { a.dy += sy * push; b.dy -= sy * push; }
          }
        }
      }
    edges.forEach(e => {                                  /* springs */
      let dx = e.s.x - e.t.x, dy = e.s.y - e.t.y;
      const d = Math.sqrt(dx*dx + dy*dy) || 1, f = (d - k) / d * 0.08;
      e.s.dx -= dx*f*d/k; e.s.dy -= dy*f*d/k; e.t.dx += dx*f*d/k; e.t.dy += dy*f*d/k;
    });
    const ER = 38;                                        /* keep bystanders off other people's edges */
    edges.forEach(e => {
      nodes.forEach(n => {
        if(n === e.s || n === e.t) return;
        const { d2, qx, qy } = segDist2(n, e.s, e.t);
        const lim = ER + n.r;
        if(d2 < lim * lim){
          const d = Math.sqrt(d2) || 0.5, push = (lim - d) * 0.8;
          n.dx -= qx / d * push; n.dy -= qy / d * push;
          e.s.dx += qx / d * push * 0.15; e.s.dy += qy / d * push * 0.15;
          e.t.dx += qx / d * push * 0.15; e.t.dy += qy / d * push * 0.15;
        }
      });
    });
    nodes.forEach(n => {
      n.dx += (W/2 - n.x) * 0.010; n.dy += (H/2 - n.y) * 0.028;  /* gentle gravity */
      const m = Math.sqrt(n.dx*n.dx + n.dy*n.dy) || 1, s = Math.min(m, step) / m;
      n.x += n.dx * s; n.y += n.dy * s;
      clamp(n);
    });
  }
  /* final discrete passes: alternate edge-clearance and label de-overlap */
  for(let pass = 0; pass < 36; pass++){
    let moved = false;
    edges.forEach(e => {                                  /* shove bystanders clear of lines */
      nodes.forEach(n => {
        if(n === e.s || n === e.t) return;
        const { d2, qx, qy } = segDist2(n, e.s, e.t);
        const lim = n.r + 15;
        if(d2 < lim * lim){
          const d = Math.sqrt(d2) || 0.5, push = (lim - d) * 0.9;
          n.x -= qx / d * push; n.y -= qy / d * push;
          clamp(n); moved = true;
        }
      });
    });
    for(let i = 0; i < nodes.length; i++)                 /* labels apart, vertically */
      for(let j = i + 1; j < nodes.length; j++){
        const a = nodes[i], b = nodes[j];
        const dx = a.x - b.x, dy = a.y - b.y;
        const ox = a.hw + b.hw - Math.abs(dx), oy = 26 - Math.abs(dy);
        if(ox > 0 && oy > 0){
          const push = (oy + 1) / 2, sy = dy < 0 ? -1 : 1;
          a.y += sy * push; b.y -= sy * push;
          clamp(a); clamp(b); moved = true;
        }
      }
    if(!moved) break;
  }
  return { nodes, edges };
}

let graphCache = null;
function viewInfluences(){
  document.title = "Influences — Pigment";
  const W = 1900, H = 1500;
  if(!graphCache) graphCache = influenceLayout(W, H);
  const { nodes, edges } = graphCache;

  let defs = `<defs>`;
  Object.entries(EDGE_STYLE).forEach(([ty, st]) => {
    if(st.arrow) defs += `<marker id="arr-${ty}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path class="ig-arr e-${ty}" d="M0,0 L10,5 L0,10 z"/></marker>`;
  });
  defs += `</defs>`;

  const edgeSvg = edges.map((e, i) => {
    const st = EDGE_STYLE[e.ty];
    /* shorten line so arrowheads sit outside the node circle */
    const r2 = e.t.r + 3;
    const dx = e.t.x - e.s.x, dy = e.t.y - e.s.y, d = Math.sqrt(dx*dx + dy*dy) || 1;
    const tx = e.t.x - dx / d * r2, ty2 = e.t.y - dy / d * r2;
    return `<line class="ig-edge e-${e.ty}" data-etype="${e.ty}" data-a="${e.s.a.id}" data-b="${e.t.a.id}"
      x1="${e.s.x.toFixed(1)}" y1="${e.s.y.toFixed(1)}" x2="${tx.toFixed(1)}" y2="${ty2.toFixed(1)}"
      ${st.dash ? `stroke-dasharray="${st.dash}"` : ""} ${st.arrow ? `marker-end="url(#arr-${e.ty})"` : ""}/>`;
  }).join("");

  const nodeSvg = nodes.map(n => {
    const mov = Mx[n.a.movements[0]];
    const c = vivid(mov ? mov.palette : n.a.palette);
    const r = n.r;
    const lab = `${n.a.name}, ${n.a.years}, ${n.d} connection${n.d === 1 ? "" : "s"}`;
    return `<g class="ig-node" data-nid="${n.a.id}" tabindex="0" role="button" aria-label="${esc(lab)}" data-baselabel="${esc(lab)}" transform="translate(${n.x.toFixed(1)},${n.y.toFixed(1)})">
      <circle r="${r.toFixed(1)}" fill="${c}"/>
      <circle class="ig-ring" r="${(r + 5).toFixed(1)}"/>
      <text y="${(r + 12).toFixed(1)}">${esc(n.a.name)}</text>
      <title>${esc(n.a.name)} · ${esc(n.a.years)} — ${n.d} connection${n.d === 1 ? "" : "s"}</title>
    </g>`;
  }).join("");

  const legend = Object.entries(EDGE_STYLE).map(([ty, st]) =>
    `<button class="tl2-leg" data-etype-btn="${ty}"><i class="ig-sw e-${ty}"></i>${st.label} · ${edges.filter(e => e.ty === ty).length}</button>`).join("");

  return `
  <div class="page-head">
    <div class="page-kicker">Who taught whom, who changed whom</div>
    <h1 class="display">The influence graph</h1>
    <p class="page-lede">${nodes.length} painters joined by ${edges.length} documented relationships — teachers, disciples, friends, rivals and partners. Choose a painter — click, or Tab to it and press Enter — to light up their circle; choose it again to visit their page, or press Escape to clear. Chains run from Theophanes teaching Rublev to Warhol sparring with Kusama.</p>
  </div>
  <div class="tl2-legend"><button class="tl2-leg" data-etype-btn=""><i style="background:var(--gold)"></i>all types</button>${legend}</div>
  <button class="skip-inline" data-skipto="ig-end">Skip the graph — ${nodes.length} painters follow</button>
  <div class="ig-wrap" id="ig-wrap">
    <svg id="ig-svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="group" aria-label="Influence graph — ${nodes.length} painters, ${edges.length} relationships" xmlns="http://www.w3.org/2000/svg">${defs}${edgeSvg}${nodeSvg}</svg>
  </div>
  <div class="ig-info" id="ig-info" hidden></div>
  <p class="map-hint" id="ig-end" tabindex="-1">nodes sized by connections, coloured by movement · solitary painters (Hilma af Klint kept her circle a séance) aren't shown</p>`;
}

function igFocus(nid){
  const svg = document.getElementById("ig-svg"), info = document.getElementById("ig-info");
  if(!svg) return;
  const nbs = new Set([nid]);
  const rels = [];
  window.INFLUENCES.forEach(([f, t, ty]) => {
    if(f === nid){ nbs.add(t); rels.push([t, ty, "out"]); }
    if(t === nid){ nbs.add(f); rels.push([f, ty, "in"]); }
  });
  svg.classList.add("focused");
  svg.querySelectorAll(".ig-node").forEach(g => g.classList.toggle("lit", nbs.has(g.dataset.nid)));
  svg.querySelectorAll(".ig-node").forEach(g => {
    const sel = g.dataset.nid === nid;
    g.classList.toggle("sel", sel);
    /* the second activation navigates — say so in the accessible name */
    g.setAttribute("aria-label", g.dataset.baselabel + (sel ? " — circle shown; choose again to open their page" : ""));
  });
  svg.querySelectorAll(".ig-edge").forEach(l => l.classList.toggle("lit", l.dataset.a === nid || l.dataset.b === nid));
  const a = Ax[nid];
  info.hidden = false;
  info.innerHTML = `<strong>${esc(a.name)}</strong> <span class="mc-meta">${esc(a.years)}</span>
    <div class="chips" style="margin-top:8px">${rels.map(([oid, ty, dir]) =>
      Ax[oid] ? `<a class="chip a" href="#/artist/${oid}"><b class="ig-rel e-${ty}">${IG_WORDS[ty][dir === "in" ? 0 : 1]}</b>&nbsp;${esc(Ax[oid].name)}</a>` : "").join("")}</div>
    <a class="btn" style="margin-top:10px;display:inline-block" href="#/artist/${nid}">Open ${esc(artistShortName(a))}'s page ${ARR}</a>`;
}
function igClear(){
  const svg = document.getElementById("ig-svg"), info = document.getElementById("ig-info");
  if(!svg) return;
  svg.classList.remove("focused");
  svg.querySelectorAll(".lit, .sel").forEach(el => el.classList.remove("lit", "sel"));
  svg.querySelectorAll(".ig-node").forEach(g => g.setAttribute("aria-label", g.dataset.baselabel));
  if(info){ info.hidden = true; info.innerHTML = ""; }
}
/* one activation path for pointer and keyboard alike */
function igActivate(g){
  if(g.classList.contains("sel")) location.hash = "#/artist/" + g.dataset.nid;
  else igFocus(g.dataset.nid);
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
  let out = "", names = "";
  /* Label de-collision at the europe zoom — see mapDecollide() below. Each
     label is emitted at its natural place under the dot, and carries the
     alternative place above it in `data-alty`, so the post-render pass can move
     a colliding label without recomputing any geometry. */
  [...N].map(n => [n, artistsOfNation(n.id).length])
    .filter(([n]) => window.NATION_COORDS[n.id] && (region === "world" || isEuropean(n)))
    .sort((a, b) => b[1] - a[1])                          /* big circles behind small */
    .forEach(([n, c]) => {
      const [x, y] = mapProj(...window.NATION_COORDS[n.id]);
      const r  = region === "world" ? 5 + Math.sqrt(c) * 3 : (6 + Math.sqrt(c) * 1.9) / mag;
      const fs = region === "world" ? 13 : 10.5 / mag;
      if(region === "europe"){
        const lfs = 9.5 / mag;
        const below = y + r + 11 / mag, above = y - r - 5 / mag;
        names += `<text class="md-name" style="font-size:${lfs.toFixed(2)}px" x="${x.toFixed(1)}" y="${below.toFixed(2)}" data-alty="${above.toFixed(2)}">${esc(n.name)} · ${c}</text>`;
      }
      out += `<a href="#/nation/${n.id}" class="map-dot">
        <circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r.toFixed(2)}" vector-effect="non-scaling-stroke"/>
        <text class="md-flag" style="font-size:${fs.toFixed(2)}px" x="${x.toFixed(1)}" y="${(y + fs * 0.34).toFixed(2)}">${n.flag}</text>
        <title>${esc(n.name)} — ${c} painter${c === 1 ? "" : "s"}</title></a>`;
    });
  /* Every label after every dot. A halo gives a label its own backdrop over
     what was painted BEFORE it; it is no defence against what is painted after,
     and dots are emitted largest-first, so a later dot's circle landed on an
     earlier dot's label — 2.14-3.24 at 1024-1440 even with the collisions
     resolved. Labels are pointer-events:none and each dot keeps its own <title>
     as its accessible name, so lifting them out of the <a> costs no semantics
     and no hit target. (AC19 / u32 NOT TESTED 7) */
  if(names) out += `<g class="md-labels">${names}</g>`;
  if(region === "world"){
    const [ex, ey, ew, eh] = MAP_REGIONS.europe.vb;       /* clickable Europe frame */
    out += `<rect class="eu-frame" data-zoom="europe" x="${ex}" y="${ey}" width="${ew}" height="${eh}" rx="6" vector-effect="non-scaling-stroke"><title>Zoom into Europe</title></rect>`;
  }
  return out;
}

/* Label de-collision at the europe zoom, on real geometry.
   The `--panel2` halo on .md-name (css/styles.css) gives each label its own
   backdrop over the gold dot circle it sits on — that closed the 1.28 dark
   measurement. A halo cannot help where two LABELS overlap each other, and one
   pair did: "Germany · 19" and "Belgium & Flanders · 8", whose worst glyph
   pixel measured 1.73 against a neighbouring label's ink rather than against
   any surface, at every width in both themes.
   The first attempt at this estimated each label's box from its character count
   and did not fire — a reminder that SVG text has no width until it is laid
   out. So it is done here instead, after render, on getBBox(), which is the
   real thing. A colliding label moves to the alternative place its emitter
   already computed for it; if that also collides it stays where it was, since a
   known collision is better than an unmeasured one. Idempotent, so it is safe
   to call on every render. (AC19 / u32 NOT TESTED 7) */
function mapDecollide(){
  const svg = document.getElementById("atlas-map");
  if(!svg) return;
  const labels = [...svg.querySelectorAll(".md-name[data-alty]")];
  if(!labels.length) return;
  const placed = [];
  const overlap = (b, p) => Math.min(b.x + b.width, p.x + p.width) - Math.max(b.x, p.x);
  const clash = b => placed.filter(p => overlap(b, p) > 0 &&
                                        b.y < p.y + p.height && p.y < b.y + b.height);
  const bbox = t => { try{ return t.getBBox(); }catch(e){ return null; } };
  labels.forEach(t => {
    if(!t.dataset.y0) t.dataset.y0 = t.getAttribute("y");   /* survive a re-run */
    if(!t.dataset.x0) t.dataset.x0 = t.getAttribute("x");
    t.setAttribute("y", t.dataset.y0);
    t.setAttribute("x", t.dataset.x0);
    let box = bbox(t);
    if(!box) return;                                        /* not laid out — leave it */
    let bad = clash(box);
    if(bad.length){
      /* second choice: the other side of the dot */
      t.setAttribute("y", t.dataset.alty);
      const alt = bbox(t);
      if(alt && !clash(alt).length){ box = alt; bad = []; }
      else t.setAttribute("y", t.dataset.y0);
    }
    if(bad.length){
      /* third choice: the smallest sideways nudge that clears every collider.
         Bounded at 60 % of the label's own width — past that the label would no
         longer read as belonging to its dot, and an honest residual is better
         than a label pointing at the wrong country. */
      const left = Math.max(...bad.map(p => box.x + box.width - p.x));
      const right = Math.max(...bad.map(p => p.x + p.width - box.x));
      const d = Math.abs(left) <= Math.abs(right) ? -(left + 0.6) : (right + 0.6);
      if(Math.abs(d) <= box.width * 0.6){
        t.setAttribute("x", (parseFloat(t.dataset.x0) + d).toFixed(2));
        const nudged = bbox(t);
        if(nudged && !clash(nudged).length) box = nudged;
        else t.setAttribute("x", t.dataset.x0);
      }
    }
    placed.push(box);
  });
}

function setMapZoom(target){
  if(target === mapZoom || !MAP_REGIONS[target]) return;
  const svg = document.getElementById("atlas-map");
  mapZoom = target;
  if(!svg) return;
  document.querySelectorAll(".map-zoom").forEach(b => {
    b.classList.toggle("on", b.dataset.zoom === target);
    b.setAttribute("aria-pressed", b.dataset.zoom === target ? "true" : "false");
  });
  const dots = svg.querySelector("#map-dots");
  const from = svg.getAttribute("viewBox").split(/\s+/).map(Number);
  const to = MAP_REGIONS[target].vb;
  const finish = () => { dots.innerHTML = mapDotsSVG(target); mapDecollide(); dots.style.opacity = 1; };
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
      <button class="f-btn map-zoom ${mapZoom === "world" ? "on" : ""}" data-zoom="world" aria-pressed="${mapZoom === "world"}">World</button>
      <button class="f-btn map-zoom ${mapZoom === "europe" ? "on" : ""}" data-zoom="europe" aria-pressed="${mapZoom === "europe"}">Europe</button>
    </div>
    <svg id="atlas-map" viewBox="${MAP_REGIONS[mapZoom].vb.join(" ")}" style="aspect-ratio:1000/420"
         xmlns="http://www.w3.org/2000/svg" role="img" aria-label="World map of painters by nation">
      <path class="map-land" d="${window.WORLD_PATH}" vector-effect="non-scaling-stroke"/>
      <g id="map-dots">${mapDotsSVG(mapZoom)}</g>
    </svg>
    <p class="map-hint">Circle size = painters in the atlas · click a circle to visit the nation · click the dashed frame (or Europe) to zoom in</p></div>`;
}

/* ---------- Painting of the Day ---------- */
const DAILY_POOL = CAT.filter(w => w.tier === 1 && w.description && w.notice && w.notice.length &&
    w.image && w.image.status === "pd" && w.image.src && Ax[w.artistId])
  .slice().sort((a, b) => a.id.localeCompare(b.id));

function gcd(a, b){
  while(b){ const next = a % b; a = b; b = next; }
  return a;
}

function dailyState(date = new Date()){
  if(!DAILY_POOL.length) return null;
  const y = date.getFullYear(), m = date.getMonth(), d = date.getDate();
  const key = `${y}-${String(m + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
  const ordinal = Math.floor(Date.UTC(y, m, d) / 86400000);
  const n = DAILY_POOL.length;
  let step = 31;
  while(gcd(step, n) !== 1) step += 2;                   /* visit the full pool before repeating */
  const index = (hashStr("pigment-daily-v1") + ordinal * step) % n;
  const work = DAILY_POOL[index], artist = Ax[work.artistId];
  const detail = work.notice[hashStr(key + work.id) % work.notice.length];
  const label = new Intl.DateTimeFormat("en", {
    weekday:"long", month:"long", day:"numeric", year:"numeric"
  }).format(date);
  return { work, artist, key, label, detail, index, poolSize:n };
}

function dailyHome(daily){
  const w = daily.work, a = daily.artist;
  const movement = w.movements && w.movements[0] && Mx[w.movements[0]];
  return `<section class="daily-home" aria-labelledby="daily-home-title">
    <div class="daily-copy">
      <div class="daily-kicker">Painting of the day <span>· ${esc(daily.label)}</span></div>
      <h2 id="daily-home-title"><a href="#/daily">${esc(w.title)}</a></h2>
      <div class="daily-meta"><a href="#/artist/${a.id}">${esc(a.name)}</a><span>${esc(w.year.display)}</span>${movement ? `<a href="#/movement/${movement.id}">${esc(movement.name)}</a>` : ""}</div>
      <p class="daily-note">${esc(w.description)}</p>
      <div class="daily-detail"><b>One detail you cannot unsee</b><span>${esc(daily.detail)}</span></div>
      <div class="aw-actions daily-actions">${passportActions(w)}</div>
      <a class="daily-enter" href="#/daily">Enter today's painting <span aria-hidden="true">→</span></a>
    </div>
    <a class="daily-media" href="#/daily" aria-label="Open today's painting: ${esc(w.title)}">
      <img loading="eager" src="${w.image.src}" alt="${esc(w.title)} by ${esc(a.name)}"
           onerror="this.onerror=null;this.src=this.src.replace(/\\d+px-/,'330px-')">
      <span>Today in Pigment</span>
    </a>
  </section>`;
}

/* ---------- photo credit (TASL — title, author, source, licence) ----------
   Attribution is a licence term, not decoration. 87 of the 103 museum building
   photographs and 28 shipped artwork images carry Creative Commons licences
   whose one operative obligation is: name the author, name the licence, link
   both the licence deed and the source file. The registries are generated into
   js/photo-credits.js from the rights evidence (tools/build_photo_credits.py);
   everything below only renders them. Nothing here claims a legal clearance —
   it records what Commons asserts (OD-5). */
const PCREDITS = window.PHOTO_CREDITS || {};
const ICREDITS = window.IMAGE_CREDITS || {};

/* the Commons "File:" title behind an upload.wikimedia.org URL — the mirror of
   commons_file_title() in tools/commons_rights.py, thumbnail form included:
     /wikipedia/commons/thumb/5/59/Name.jpg/500px-Name.jpg  →  File:Name.jpg */
function commonsTitle(src){
  if(!src) return null;
  let path;
  try{ path = new URL(src, location.href).pathname; }catch(e){ return null; }
  const parts = path.split("/").filter(Boolean);
  if(parts.indexOf("commons") < 0) return null;        /* /wikipedia/en/ = a local upload */
  const t = parts.indexOf("thumb");
  const name = t >= 0 ? parts[t + 3] : parts[parts.length - 1];
  if(!name) return null;
  try{ return "File:" + decodeURIComponent(name); }catch(e){ return "File:" + name; }
}
function imageCredit(src){ const t = commonsTitle(src); return t ? ICREDITS[t] || null : null; }

/* One credit line. `label` names what is being credited ("Photograph",
   "Image credit"); every field is escaped, because the author strings come
   from Commons — plain-texted at build time, escaped again here. */
function creditLine(c, label){
  if(!c) return "";
  const bits = [c.author ? esc(label) + ": " + esc(c.author) : esc(label)];
  bits.push(c.licenseUrl
    ? `<a href="${esc(c.licenseUrl)}" target="_blank" rel="noopener license">${esc(c.license)}</a>`
    : esc(c.license));
  if(c.page) bits.push(`<a href="${esc(c.page)}" target="_blank" rel="noopener">file on Commons</a>`);
  return bits.join(" · ");
}

/* ---------- museums ---------- */
function museumCard(v){
  const works = catByVenue[v.id] || [];
  const cw = works.find(w => w.image && w.image.src && w.image.status === "pd");
  const fa = works[0] && Ax[works[0].artistId];
  const note = MNOTES[v.id];
  return `<article class="card list-card mu-card" data-href="#/museum/${v.id}">
    <div class="card-art">${note && note.photo
      ? `<img loading="lazy" src="${note.photo.src}" alt="${esc(v.name)}">`
      : (fa ? canvasTag(fa.style, fa.palette, v.id, coverLabel(v.name)) : "")}</div>
    <div class="card-body">
      <div class="lc-kicker">${esc(v.city)} · ${works.length} work${works.length === 1 ? "" : "s"}</div>
      <h3><a href="#/museum/${v.id}">${esc(v.name)}</a></h3>
      ${note && note.hook ? `<div class="card-tagline">${esc(note.hook)}</div>` : ""}
    </div>
  </article>`;
}

function viewMuseums(){
  document.title = "Museums — Pigment";
  const held = VEN.filter(v => !VENUE_SENTINELS[v.id] && (catByVenue[v.id] || []).length)
    .sort((a, b) => (catByVenue[b.id] || []).length - (catByVenue[a.id] || []).length);
  return `
  <div class="page-head">
    <div class="page-kicker">The buildings</div>
    <h1 class="display">Museums</h1>
    <p class="page-lede">Where the atlas hangs in real life. ${held.length} museums, churches and palaces hold the works catalogued so far — each with its own walls, and the great ones with their own story.</p>
  </div>
  <div class="cards wide">${held.map(museumCard).join("")}</div>
  <p class="img-credit index-credit">Building photographs by Wikimedia Commons contributors. Each museum's page names its photographer and licence; the full list is in <a href="#/credits">Credits</a>.</p>`;
}

function viewMuseum(id){
  const v = Vx[id]; if(!v || VENUE_SENTINELS[id]) return view404();
  document.title = v.name + " — Pigment";
  const works = (catByVenue[id] || []).slice().sort((x, y) => x.year.sort - y.year.sort);
  const note = MNOTES[id];
  const artists = [...new Set(works.map(w => w.artistId))].map(aid => Ax[aid]).filter(Boolean);
  const collage = works.filter(w => w.image && w.image.src && w.image.status === "pd").slice(0, 6);
  const kindred = VEN.filter(o => o.id !== id && !VENUE_SENTINELS[o.id] && (catByVenue[o.id] || []).length &&
    (o.city === v.city || o.country === v.country)).slice(0, 6);
  /* the building photograph's credit. It is rendered on every museum page that
     has a photograph, not only the ones whose hero shows it: 82 of the 103 heroes
     are given over to a collage of the works instead, but the same photograph is
     still this venue's cover everywhere else in the atlas. */
  const photoCredit = note && note.photo ? creditLine(PCREDITS[id], "Photograph") : "";
  return `
  <div class="mu-hero">
    ${collage.length
      ? `<div class="mu-collage c${collage.length}">${collage.map(w => `<img loading="lazy" src="${w.image.src}" alt="">`).join("")}</div>`
      : note && note.photo ? `<div class="mu-photo"><img src="${note.photo.src}" alt="${esc(v.name)}"></div>` : ""}
    <div class="mu-shade"></div>
    <div class="mu-hero-body">
      ${crumbs([["Atlas",""],["Museums","museums"],[v.name]])}
      <h1 class="display">${esc(v.name)}</h1>
      <div class="mu-sub">${esc(v.city)}${v.country ? " · " + esc(v.country) : ""}${note && note.founded ? " · founded " + esc(note.founded) : ""}${v.type && v.type !== "museum" ? " · a " + esc(v.type) : ""}${note && note.photo && !photoCredit ? ` · <a href="${note.photo.page}" target="_blank" rel="noopener">photo via Wikimedia Commons</a>` : ""}</div>
      ${note ? `<div class="mu-hook">${esc(note.hook)}</div>` : ""}
      <div class="chips" style="margin-top:10px">${shareChip("p/museum/" + v.id + ".html")}</div>
    </div>
  </div>
  ${photoCredit ? `<p class="img-credit mu-credit">${photoCredit}</p>` : ""}
  ${note && note.essay ? `<div class="mu-essay">${note.essay.split("\n\n").map(p => `<p>${esc(p)}</p>`).join("")}</div>` : ""}
  <div class="stats-row">
    <div class="stat"><div class="num">${works.length}</div><div class="lbl">Works in the atlas</div></div>
    <div class="stat"><div class="num">${artists.length}</div><div class="lbl">Artists on these walls</div></div>
    ${note && note.founded ? `<div class="stat"><div class="num">${esc(note.founded)}</div><div class="lbl">Founded</div></div>` : ""}
  </div>
  <section>
    <h2 class="sec-title">In the collection <span class="count">every work opens its own page</span></h2>
    <div class="cards">${works.map(artworkCard).join("")}</div>
  </section>
  ${artists.length ? `<section>
    <h2 class="sec-title">Artists on these walls</h2>
    <div class="mini-cards mu-artists">${artists.map(p => {
      const n = works.filter(w => w.artistId === p.id).length;
      return `<a class="mini-card" href="#/artist/${p.id}">${canvasTag(p.style, p.palette, p.id, coverLabel(p.name))}<span><span class="mc-name">${esc(p.name)}</span><br><span class="mc-meta">${n} ${n === 1 ? "work" : "works"} here</span></span></a>`;
    }).join("")}</div>
  </section>` : ""}
  ${kindred.length ? `<section>
    <h2 class="sec-title">Kindred walls <span class="count">same city or country</span></h2>
    <div class="chips">${kindred.map(o => `<a class="chip m" href="#/museum/${o.id}">${esc(o.name)} · ${esc(o.city)}</a>`).join("")}</div>
  </section>` : ""}`;
}

/* ---------- explore hub (timeline + influences under one roof) ---------- */
function viewExplore(){
  document.title = "Explore — Pigment";
  return `
  <div class="page-head">
    <div class="page-kicker">The big pictures</div>
    <h1 class="display">Explore</h1>
    <p class="page-lede">Four instruments for seeing the whole atlas at once — eight centuries laid out on a single scroll, the living web of who taught, rivaled, befriended and influenced whom, the family trees of movements, and a world map of where painters came from.</p>
  </div>
  <div class="entry-cards">
    <a class="entry-card" href="#/timeline" style="--ec:var(--gold2)">
      <div class="ec-kicker">Time</div>
      <h3>The grand timeline</h3>
      <p>Every painter in the atlas as a lifespan bar, coloured by movement — zoom from Giotto to Banksy and watch the centuries hand each other the brush.</p>
      <span class="ec-arrow" aria-hidden="true">→</span>
    </a>
    <a class="entry-card" href="#/influences" style="--ec:var(--teal)">
      <div class="ec-kicker">Connection</div>
      <h3>The influence constellation</h3>
      <p>${(window.INFLUENCES || []).length} relationships — taught, influenced, befriended, rivaled, partnered — drawn as one force-directed web. Find the hidden hubs.</p>
      <span class="ec-arrow" aria-hidden="true">→</span>
    </a>
    <a class="entry-card" href="#/movements" style="--ec:var(--wine)">
      <div class="ec-kicker">Lineage</div>
      <h3>Family trees of movements</h3>
      <p>Switch any movement index to its Family tree view and watch the schools branch from their parents — Post-Impressionism out of Impressionism, and on down the line.</p>
      <span class="ec-arrow" aria-hidden="true">→</span>
    </a>
    <a class="entry-card" href="#/nations" style="--ec:var(--blue)">
      <div class="ec-kicker">Geography</div>
      <h3>A world map of painters</h3>
      <p>Where the painters came from, plotted across the globe with a zoomable Europe inset — though most of them, as you'll read, refused to stay put.</p>
      <span class="ec-arrow" aria-hidden="true">→</span>
    </a>
  </div>`;
}

/* ---------- actuality (B2) ---------- */
/* An entry never carries its own picture: nothing here illustrates the news,
   because Pigment cannot licence a news photograph. The card borrows the cover
   of whatever the entry points at, which is always already in the atlas. */
function actualityTarget(e){
  if(e.kind === "list"){ const l = LISTS.find(x => x.id === e.listId); return l ? { href:"#/list/"+l.id, title:l.title, cover:CatX[l.cover] } : null; }
  const w = CatX[e.workId]; return w ? { href:"#/artwork/"+w.id, title:w.title, cover:w } : null;
}
/* `coverStyle` names a painter whose style and palette drive one of the atlas's
   own generative covers, instead of borrowing an artwork's photograph.

   This is the honest version of "make the news photo into a painting". Pigment
   will not do that: a close restyling of a specific press photograph is a
   derivative of that photograph, the person in it holds publicity rights, and
   PIGMENT.md forbids presenting generated imagery as a real artwork. A
   generative cover copies no photograph and depicts nobody — it is an abstract
   field in a painter's palette, which the atlas already uses wherever a real
   image is unavailable, and it is labelled as being in that painter's manner. */
function actualityCard(e){
  const t = actualityTarget(e); if(!t) return "";
  const styleArtist = e.coverStyle ? Ax[e.coverStyle] : null;
  const cw = t.cover, ca = cw && Ax[cw.artistId];
  const img = !styleArtist && cw && cw.image && cw.image.src && cw.image.status === "pd";
  return `<article class="card list-card" data-href="${t.href}">
    <div class="card-art">${img
      ? `<img loading="lazy" src="${cw.image.src}" alt="${esc(t.title)}">`
      : (styleArtist
        ? canvasTag(styleArtist.style, styleArtist.palette, e.id, coverLabel(t.title))
        : (ca ? canvasTag(ca.style, ca.palette, e.id, coverLabel(t.title)) : ""))}</div>
    <div class="card-body">
      <div class="lc-kicker">${esc(e.kind === "list" ? "List" : "Article")} · ${esc(monthLabel(e.published))}${styleArtist ? " · cover in the manner of " + esc(styleArtist.name.split(" ").pop()) : ""}</div>
      <h3><a href="${t.href}">${esc(e.headline)}</a></h3>
      <div class="card-tagline">${esc(e.hook)}</div>
    </div>
  </article>`;
}
function monthLabel(iso){
  const m = /^(\d{4})-(\d{2})/.exec(iso || ""); if(!m) return "";
  return ["January","February","March","April","May","June","July","August",
          "September","October","November","December"][+m[2]-1] + " " + m[1];
}
/* Echoes — the photo-to-painting comparison (ACTUALITY.md type 1). Named for
   the mechanic the spec already describes: the news photograph and the painting
   are the same picture. Empty until the first one ships, and the empty state
   says why rather than pretending the section is merely new. */
function viewEchoes(){
  document.title = "Echoes — Pigment";
  const echoes = ACT.filter(e => e.kind === "article");
  return `
  <div class="page-head">
    <div class="page-kicker">Once a month</div>
    <h1 class="display">Echoes</h1>
    <p class="page-lede">A photograph from the news and a painting that turns out to be the same picture — the same composition, or the same human situation four centuries earlier. The writing is about the painting; the photograph just opens the door.</p>
  </div>
  ${echoes.length ? `<div class="cards wide">${echoes.map(actualityCard).join("")}</div>`
   : `<div class="page-head" style="padding-top:0">
        <p class="page-lede">Nothing here yet, and the reason is worth saying: Pigment cannot show you the photograph. Press images are licensed, and a repainting of one is still a derivative of it. A rhyme has to be <em>described</em> well enough that you see it — which is a writing problem, and it is being worked on.</p>
        <p class="page-lede"><a href="#/actuality">The Actuality lists</a> are the part of this that already works.</p>
      </div>`}`;
}

function viewActuality(){
  document.title = "Actuality — Pigment";
  return `
  <div class="page-head">
    <div class="page-kicker">Once a month</div>
    <h1 class="display">Actuality</h1>
    <p class="page-lede">The news is the door; the atlas is the room. Each month we take one story the world is already having an opinion about, and answer it with paintings that were here long before it. Nothing on this page illustrates the news — it answers it.</p>
  </div>
  ${ACT.length ? `<div class="cards wide">${ACT.map(actualityCard).join("")}</div>
  <p class="img-credit index-credit">Every entry links a dated, cited report to works already in the atlas. Pigment has no live feed and makes no claim to know what happened today.</p>`
   : `<p class="page-lede">Nothing published yet.</p>`}`;
}

/* ---------- editorial lists ---------- */
function listCard(l){
  const cw = CatX[l.cover], ca = cw && Ax[cw.artistId];
  const img = cw && cw.image && cw.image.src && cw.image.status === "pd";
  return `<article class="card list-card" data-href="#/list/${l.id}">
    <div class="card-art">${img
      ? `<img loading="lazy" src="${cw.image.src}" alt="${esc(l.title)}">`
      : (ca ? canvasTag(ca.style, ca.palette, l.id, coverLabel(l.title)) : "")}</div>
    <div class="card-body">
      <div class="lc-kicker">List · ${l.works.length} works</div>
      <h3><a href="#/list/${l.id}">${esc(l.title)}</a></h3>
      <div class="card-tagline">${esc(l.lede)}</div>
    </div>
  </article>`;
}

function viewLists(){
  document.title = "Lists — Pigment";
  return `
  <div class="page-head">
    <div class="page-kicker">Editorial</div>
    <h1 class="display">Lists</h1>
    <p class="page-lede">Guided walks through the atlas — each one a handful of works that talk to each other across the centuries. Follow a thread, admire what stops you, and let one list hand you to the next.</p>
    <p class="page-lede" style="margin-top:-6px"><a href="#/actuality">Actuality</a> — the monthly list that answers a story in the news out of the atlas.</p>
  </div>
  <div class="cards wide">${LISTS.map(listCard).join("")}</div>`;
}

function viewList(id){
  const l = Lsx[id]; if(!l) return view404();
  document.title = l.title + " — Pigment";
  const cw = CatX[l.cover], ca = cw && Ax[cw.artistId];
  /* An Actuality list carries its own generated cover in a named painter's
     manner (ACTUALITY.md §8a). The SAME image has to open the list page, or the
     card and the page it opens show two different pictures. */
  const act = ACT.find(e => e.listId === l.id);
  const styleArtist = act && act.coverStyle ? Ax[act.coverStyle] : null;
  const cimg = !styleArtist && cw && cw.image && cw.image.src && cw.image.status === "pd";
  const others = LISTS.filter(o => o.id !== l.id).sort(() => Math.random() - 0.5).slice(0, 3);
  return `
  <div class="list-hero">
    <div class="list-hero-art">${cimg
      ? `<img src="${cw.image.src}" alt="${esc(cw.title)}">`
      : (styleArtist
        ? canvasTag(styleArtist.style, styleArtist.palette, act.id, coverLabel(l.title), true)
        : (ca ? canvasTag(ca.style, ca.palette, l.id, coverLabel(l.title), true) : ""))}</div>
    <div class="list-hero-body">
      ${crumbs([["Atlas",""],["Lists","lists"],[l.title]])}
      <h1 class="display">${esc(l.title)}</h1>
      <p class="page-lede">${esc(l.lede)}</p>
      <div class="chip-label">${l.works.length} works — every one opens its own page</div>
      ${act ? `<p class="list-newsline">${esc(act.newsline)} <a href="${esc(act.source.url)}" target="_blank" rel="noopener nofollow">${esc(act.source.name)}</a>${styleArtist ? ` · Cover generated in the manner of ${esc(styleArtist.name)}; it is not a painting and reproduces no photograph.` : ""}</p>` : ""}
      <div class="chips" style="margin-top:8px">${shareChip("p/list/" + l.id + ".html")}</div>
    </div>
  </div>
  <ol class="list-entries">
    ${l.works.map((e, i) => {
      const w = CatX[e.id]; if(!w) return "";
      const a = Ax[w.artistId];
      const img = w.image && w.image.src && w.image.status === "pd";
      const on = passportHas("admirations", w.id);
      return `<li class="list-entry">
        <span class="le-num">${i + 1}</span>
        <a class="le-art" href="#/artwork/${w.id}">${img
          ? `<img loading="lazy" src="${w.image.src}" alt="${esc(w.title)}" onerror="this.onerror=null;this.src=this.src.replace(/\\d+px-/,'330px-')">`
          : canvasTag(a.style, a.palette, w.id + "-le", coverLabel(w.title + " by " + a.name))}</a>
        <div class="le-body">
          <h3><a href="#/artwork/${w.id}">${esc(w.title)}</a></h3>
          <div class="le-meta"><a href="#/artist/${a.id}">${esc(a.name)}</a> · ${esc(w.year.display)}</div>
          <p class="le-note">${esc(e.note)}</p>
          ${e.essay ? `<p class="le-essay">${esc(e.essay)}</p>` : ""}
        </div>
        <button class="aw-btn le-adm ${on ? "on" : ""}" data-pp="admirations" data-ppid="${w.id}" aria-pressed="${on}">${on ? "Admired ✓" : "Admire"}</button>
      </li>`;
    }).join("")}
  </ol>
  ${others.length ? `<section style="margin-top:40px"><h2 class="sec-title">More lists</h2><div class="cards wide">${others.map(listCard).join("")}</div></section>` : ""}`;
}

function viewHome(){
  const muse = A[Math.floor(Math.random()*A.length)];
  const daily = dailyState();
  const featured = [...A].sort(() => Math.random()-0.5).slice(0,8);
  const topMovs = M.filter(m => !m.parent)
    .map(m => [m, artistsOfMovement(m.id).length]).sort((x,y) => y[1]-x[1]).slice(0,6);
  const stripWorks = [...CAT].filter(w => w.image && w.image.src)
    .sort(() => Math.random()-0.5);
  const stripAnchor = (w, dup) =>
    `<a ${dup ? 'tabindex="-1" aria-hidden="true" ' : ""}href="#/artwork/${w.id}" title="${esc(w.title)} — ${Ax[w.artistId] ? esc(Ax[w.artistId].name) : ""}"><img loading="lazy" src="${w.image.src}" alt="${dup ? "" : esc(w.title)}"></a>`;
  const stripItems = stripWorks.map(w => stripAnchor(w, false)).join("");
  const stripItemsDup = stripWorks.map(w => stripAnchor(w, true)).join("");
  document.title = "Pigment — Find your place in the history of art";
  return `
  <header class="home-hero">
    ${canvasTag(muse.style, muse.palette, muse.id, `Tonight's generative cover, mixed after ${muse.name} and painted in the browser`, true, String(Date.now()%100000))}
    <div class="hero-shade"></div>
    <div class="home-hero-content">
      <div class="kicker">Pigment · a taste atlas of painting</div>
      <h1 class="home-title">Find your place in the history of art.</h1>
      <p class="lede">Eight centuries of painters, the masterpieces between them, and every connection that made them. Explore the atlas, admire what speaks to you — and begin your map of taste.</p>
      <p class="footer-note" style="margin-top:18px">Tonight's cover: mixed after <a href="#/artist/${muse.id}">${esc(muse.name)}</a></p>
    </div>
  </header>

  <div class="entry-cards">
    <div class="entry-card" style="--ec:var(--gold2)">
      <a class="ec-cover" href="#/artists" aria-label="Start with an artist"></a>
      <div class="ec-kicker">Begin</div>
      <h3>Start with an artist</h3>
      <p>Pick a painter and follow the threads — teachers, rivals, movements, and the works that made them matter.</p>
      <button class="ec-surprise" data-random-artist>or surprise me ${ARR}</button>
      <span class="ec-arrow" aria-hidden="true">→</span>
    </div>
    <a class="entry-card" href="#/${(() => { const p = getPassport(); return p && p.milestones && p.milestones.onboarded ? "taste" : "palette"; })()}" style="--ec:var(--teal)">
      <div class="ec-kicker">Become</div>
      <h3>Find your palette</h3>
      <p>Four tones, sixteen artworks, five questions — and Pigment sketches the first map of your taste, with a Persona to argue about. Under four minutes.</p>
      <span class="ec-arrow" aria-hidden="true">→</span>
    </a>
    <a class="entry-card" href="#/explore" style="--ec:var(--wine)">
      <div class="ec-kicker">Wander</div>
      <h3>Explore the atlas</h3>
      <p>Eight centuries on one timeline, an influence constellation, family trees of movements, and a world map of painters.</p>
      <span class="ec-arrow" aria-hidden="true">→</span>
    </a>
  </div>

  ${daily ? dailyHome(daily) : ""}

  ${(() => {
    /* B2. Actuality on the front door. It was reachable only through the Lists
       submenu — the most shareable surface in the product, two clicks deep. The
       newest entry gets the homepage; the rest live in the archive. */
    const e = ACT[0];
    if(!e) return "";
    const t = actualityTarget(e); if(!t) return "";
    return `<section>
      <h2 class="sec-title">Actuality <span class="count">the news, answered out of the atlas</span></h2>
      <div class="cards wide">${actualityCard(e)}</div>
      <a class="chip-label" style="display:block;margin-top:14px" href="#/actuality">every month so far ${ARR}</a>
    </section>`;
  })()}

  ${(() => {
    const feat = LISTS.filter(l => l.featured).slice(0, 4);
    return feat.length ? `<section>
      <h2 class="sec-title">Lists <span class="count">guided walks through the atlas</span></h2>
      <div class="cards wide">${feat.map(listCard).join("")}</div>
      <a class="chip-label" style="display:block;margin-top:14px" href="#/lists">all ${LISTS.length} lists ${ARR}</a>
    </section>` : "";
  })()}

  <div class="strip" aria-label="Masterpieces in the atlas">
    <div class="strip-track">${stripItems}${stripItemsDup}</div>
  </div>

  <section>
    <h2 class="sec-title">How Pigment works</h2>
    <div class="hpw">
      <div class="hpw-step"><span class="n">1</span><b>Discover</b><p>Wander artists, artworks, movements, eras and nations — everything links onward.</p></div>
      <div class="hpw-step"><span class="n">2</span><b>Admire</b><p>One button, on every artwork. Press it on what speaks to you.</p></div>
      <div class="hpw-step"><span class="n">3</span><b>Map</b><p>Pigment finds the centre of gravity of your taste — <a href="#/taste">see your map</a>.</p></div>
      <div class="hpw-step"><span class="n">4</span><b>Become</b><p>Unlock your Pigment Persona and your palette — <a href="#/palette">find yours</a>.</p></div>
      <div class="hpw-step"><span class="n">5</span><b>Share</b> <span class="badge-soon">soon</span><p>Send your Taste Passport into the world.</p></div>
    </div>
  </section>

  <div class="stats-row">
    ${[[A.length,"Painters","artists"],[M.length,"Movements","movements"],[T.length,"Techniques","techniques"],[E.length,"Centuries","eras"],[N.length,"Nations","nations"]]
      .map(([n,l,href]) => `<a class="stat" href="#/${href}"><div class="num" data-count="${n}">0</div><div class="lbl">${l}</div></a>`).join("")}
  </div>

  <section>
    <h2 class="sec-title">Begin with an era</h2>
    <div class="era-strip">
      ${E.map(e => `<a class="era-tile" href="#/era/${e.id}">
          ${canvasTag(e.style, e.palette, e.id, coverLabel(e.name))}
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

function viewDaily(){
  const daily = dailyState();
  if(!daily) return view404();
  const w = daily.work, a = daily.artist;
  const movement = w.movements && w.movements[0] && Mx[w.movements[0]];
  const venue = w.museum || null;
  document.title = `${w.title} — Painting of the Day — Pigment`;
  return `
  ${crumbs([["Atlas",""],["Painting of the Day"]])}
  <div class="daily-page-head">
    <div>
      <div class="daily-kicker">Painting of the day <span>· ${esc(daily.label)}</span></div>
      <h1 class="display">${esc(w.title)}</h1>
      <div class="daily-meta"><a href="#/artist/${a.id}">${esc(a.name)}</a><span>${esc(w.year.display)}</span>${movement ? `<a href="#/movement/${movement.id}">${esc(movement.name)}</a>` : ""}</div>
    </div>
    <div class="daily-sequence"><b>${daily.poolSize}</b><span>works in this<br>daily rotation</span></div>
  </div>
  <article class="daily-stage">
    <div class="daily-stage-media" data-lb-img="${w.image.src}" data-lb-cap="${esc(w.title)} (${esc(w.year.display)}) — ${esc(a.name)}" data-lb-link="${w.image.page}">
      <img src="${w.image.src}" alt="${esc(w.title)} by ${esc(a.name)}"
           onerror="this.onerror=null;this.src=this.src.replace(/\\d+px-/,'330px-')">
      <span>Click to look closer</span>
    </div>
    <div class="daily-stage-copy">
      <p class="daily-note">${esc(w.description)}</p>
      <div class="daily-detail"><b>One detail you cannot unsee</b><span>${esc(daily.detail)}</span></div>
      <div class="aw-actions daily-actions">${passportActions(w)}</div>
      <a class="daily-enter" href="#/artwork/${w.id}">Go deeper into the artwork <span aria-hidden="true">→</span></a>
      <p class="daily-return">A new painting enters the atlas at your next local midnight.</p>
    </div>
  </article>
  <section class="daily-threads">
    <h2 class="sec-title">Follow the threads</h2>
    <div class="chips">
      ${chip("a", "artist/" + a.id, a.name)}
      ${movement ? chip("m", "movement/" + movement.id, movement.name) : ""}
      ${(w.techniques || []).slice(0, 2).map(t => Tx[t] ? chip("t", "technique/" + t, Tx[t].name) : "").join("")}
      ${w.nation && Nx[w.nation] ? chip("n", "nation/" + w.nation, Nx[w.nation].flag + " " + Nx[w.nation].name) : ""}
    </div>
    ${venue ? `<p class="aw-provenance">On view at ${venue.id && Vx[venue.id] && !VENUE_SENTINELS[venue.id]
        ? `<a href="#/museum/${venue.id}">${esc(venue.name)}</a>` : esc(venue.name)}${venue.city ? `, ${esc(venue.city)}` : ""} · <a href="${w.image.page}" target="_blank" rel="noopener">public-domain image source</a></p>` : ""}
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
    <button class="f-btn ${artistFilter.era==='all'?'on':''}" data-era="all" aria-pressed="${artistFilter.era==='all'}">All</button>
    ${E.map(e => `<button class="f-btn ${artistFilter.era===e.id?'on':''}" data-era="${e.id}" aria-pressed="${artistFilter.era===e.id}">${esc(e.name)}</button>`).join("")}
    <span class="f-spacer"></span>
    <span class="f-label">Sort</span>
    <button class="f-btn ${artistFilter.sort==='chrono'?'on':''}" data-sort="chrono" aria-pressed="${artistFilter.sort==='chrono'}">Chronological</button>
    <button class="f-btn ${artistFilter.sort==='az'?'on':''}" data-sort="az" aria-pressed="${artistFilter.sort==='az'}">A–Z</button>
  </div>
  <div class="cards">${list.map(artistCard).join("")}</div>`;
}

/* ——— Tier 1 exhibition template: the career arc ——— */
const ARC_NUMS = ["","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve"];

function arcWorkChips(ids){
  const items = (ids || []).map(x => CatX[x]).filter(Boolean);
  if(!items.length) return "";
  return `<div class="arc-works">${items.map(w => {
    const artist = Ax[w.artistId];
    const img = w.image && w.image.src && w.image.status === "pd";
    return `<a class="arc-work" href="#/artwork/${w.id}">${img
      ? `<img loading="lazy" src="${w.image.src}" alt="${esc(w.title)}" onerror="this.onerror=null;this.src=this.src.replace(/\\d+px-/,'330px-')">`
      : `<span class="arc-work-gen">${canvasTag(artist.style, artist.palette, w.id, coverLabel(w.title + " by " + artist.name))}</span>`}
      <span class="arc-work-t">${esc(w.title)}<em>${esc(w.year.display)}</em></span>
    </a>`;
  }).join("")}</div>`;
}

function arcSection(arc){
  return `<section class="arc">
    <h2>The life, in ${ARC_NUMS[arc.length] || arc.length} acts</h2>
    <div class="arc-rail">
      ${arc.map(act => `<div class="arc-act">
        <div class="arc-when">${esc(act.y)}</div>
        <div class="arc-body">
          <h3>${esc(act.t)}</h3>
          <p>${esc(act.text)}</p>
          ${arcWorkChips(act.works)}
        </div>
      </div>`).join("")}
    </div>
  </section>`;
}

function viewArtist(id){
  const a = Ax[id]; if(!a) return view404();
  document.title = a.name + " — Pigment";
  const kindred = A.filter(o => o.id !== a.id)
    .map(o => [o, o.movements.filter(m => a.movements.includes(m)).length])
    .filter(([,c]) => c > 0).sort((x,y) => y[1]-x[1]).slice(0,6).map(([o]) => o);
  const nation = Nx[a.nation];
  const t1 = window.TIER1 && window.TIER1[a.id];
  const arc = (t1 && t1.arc) || null;
  const galleryWorks = arc ? (catByArtist[a.id] || []).slice().sort((x,y) => x.year.sort - y.year.sort) : [];
  return `
  ${hero({
    style:a.style, palette:a.palette, seed:a.id, salt:"hero",
    crumbs: crumbs([["Atlas",""],["Artists","artists"],[a.name]]),
    title:a.name,
    /* A4. `nation` is single-valued, so the identity line can only ever show one
       flag — and for a dozen painters that flag is wrong on a surface every
       visitor sees: a 🇹🇷 on a man who died in 1564, three and a half centuries
       before the Republic. STYLE_GUIDE §3.3/§7 already require "primary filing
       plus acknowledgment"; the prose honours it and the schema had nowhere to
       put it. `nationNote` is that place — additive, optional, and it does not
       re-type the shipped infrastructure the flag chip and the nation index are
       built on. The note sits beside the flag, not instead of it. */
    sub:`<span>${esc(a.years)}</span><a href="#/nation/${a.nation}">${nation ? nation.flag+" "+esc(nation.name) : ""}</a>` +
        (a.nationNote ? `<span class="nation-note">${esc(a.nationNote)}</span>` : "") +
        a.eras.map(e => Ex[e] ? `<a href="#/era/${e}">${esc(Ex[e].name)}</a>` : "").join(""),
    tagline:a.tagline
  })}
  <div class="chip-label">Movements · Techniques · Era · Nation — click to travel</div>
  <div class="chips" style="margin-bottom:30px">${chipsFor(a)}${shareChip("p/artist/" + a.id + ".html")}</div>

  ${(() => {
    const t1 = window.TIER1 && window.TIER1[a.id];
    if(!t1) return "";
    return `<div class="why-card">
      <div class="why-kicker">Why ${esc(artistShortName(a))} matters</div>
      <p>${esc(t1.why)}</p>
      <div class="traits">${t1.lookFor.map(t => `<span class="trait">${esc(t)}</span>`).join("")}</div>
    </div>`;
  })()}
  <div class="artist-cols">
    <div class="bio-block">
      ${arc ? arcSection(arc) : `<h2>The life</h2><p>${esc(a.life)}</p>
      <h2>The career</h2><p>${esc(a.career)}</p>`}
      ${galleryWorks.length ? `<h2>The gallery</h2>
      <div class="chip-label">${galleryWorks.length} works in the atlas — every one opens its own page</div>
      <div class="cards gallery-cards">${galleryWorks.map(artworkCard).join("")}</div>` : ""}
      <h2>Beyond the easel</h2><p>${esc(a.outside)}</p>
      <h2>Fun facts</h2>
      <ul class="facts">${a.facts.map(f => `<li>${esc(f)}</li>`).join("")}</ul>
    </div>
    <aside class="side-panel">
      ${arc ? "" : `<div class="panel">
        <h3>Major works</h3>
        ${(() => {
          const catFor = {};
          (catByArtist[a.id] || []).forEach(cw => { catFor[cw.worksKey || cw.title] = cw.id; });
          return a.works.map(wk => {
            const art = window.ARTWORKS && window.ARTWORKS[a.id] && window.ARTWORKS[a.id][wk.t];
            const cid = catFor[wk.t];
            const titleHtml = cid ? `<a href="#/artwork/${cid}">${esc(wk.t)}</a>` : esc(wk.t);
            return art
              ? `<div class="work has-img" data-lb-img="${art.img}" data-lb-cap="${esc(wk.t)} (${esc(wk.y)}) — ${esc(a.name)}" data-lb-link="${art.page}">
                   <img class="w-thumb" loading="lazy" src="${art.img}" alt="${esc(wk.t)} by ${esc(a.name)}"
                        onerror="this.onerror=null;this.src=this.src.replace(/\\d+px-/,'330px-')">
                   <div><span class="w-year">${esc(wk.y)}</span><span class="w-title">${titleHtml}</span></div>
                 </div>`
              : `<div class="work"><span class="w-year">${esc(wk.y)}</span><span class="w-title">${titleHtml}</span></div>`;
          }).join("");
        })()}
        ${window.ARTWORKS && window.ARTWORKS[a.id]
          ? `<div class="chip-label" style="margin-top:12px">tap a work to enlarge · images via Wikimedia Commons</div>` : ""}
      </div>`}
      ${kindred.length ? `<div class="panel">
        <h3>Kindred spirits</h3>
        <div class="mini-cards">
          ${kindred.map(o => `<a class="mini-card" href="#/artist/${o.id}">
              ${canvasTag(o.style, o.palette, o.id, coverLabel(o.name))}
              <span><span class="mc-name">${esc(o.name)}</span><br><span class="mc-meta">${esc(o.years)}</span></span>
            </a>`).join("")}
        </div>
      </div>` : ""}
      ${(() => {
        const rels = [];
        (window.INFLUENCES || []).forEach(([f, t, ty]) => {
          if(f === a.id && Ax[t]) rels.push([t, ty, "out"]);
          if(t === a.id && Ax[f]) rels.push([f, ty, "in"]);
        });
        return rels.length ? `<div class="panel">
          <h3>Lineage & circle</h3>
          <div class="chips">${rels.map(([oid, ty, dir]) =>
            `<a class="chip a" href="#/artist/${oid}"><b class="ig-rel e-${ty}">${IG_WORDS[ty][dir === "in" ? 0 : 1]}</b>&nbsp;${esc(Ax[oid].name)}</a>`).join("")}</div>
          <a href="#/influences" class="chip-label" style="display:block;margin-top:12px">see the full influence graph ${ARR}</a>
        </div>` : "";
      })()}
      ${(() => {
        const t1 = window.TIER1 && window.TIER1[a.id];
        if(!t1) return `<div class="panel">
          <h3>Keep exploring</h3>
          <div class="chips">
            ${a.movements[0] && Mx[a.movements[0]] ? chip("m","movement/"+a.movements[0], "More "+Mx[a.movements[0]].name) : ""}
            ${nation ? chip("n","nation/"+a.nation, "Painters of "+nation.name) : ""}
            ${Ex[a.eras[0]] ? chip("e","era/"+a.eras[0], "The "+Ex[a.eras[0]].name) : ""}
          </div>
        </div>`;
        const gnName = g => {
          if(g.t === "artist") return Ax[g.id] && Ax[g.id].name;
          if(g.t === "movement") return Mx[g.id] && Mx[g.id].name;
          if(g.t === "technique") return Tx[g.id] && Tx[g.id].name;
          if(g.t === "work") return CatX[g.id] && CatX[g.id].title;
          return null;
        };
        const gnHref = g => (g.t === "work" ? "artwork" : g.t) + "/" + g.id;
        return `<div class="panel">
          <h3>Go next</h3>
          ${t1.goNext.map(g => {
            const n = gnName(g);
            return n ? `<a class="gonext-item" href="#/${gnHref(g)}"><b>${esc(n)}</b><span> — ${esc(g.why)}</span></a>` : "";
          }).join("")}
        </div>`;
      })()}
    </aside>
  </div>`;
}

function viewArtwork(id){
  const w = CatX[id]; if(!w) return view404();
  const a = Ax[w.artistId]; if(!a) return view404();
  document.title = `${w.title} — ${a.name} — Pigment`;
  const venue = w.museum || null;
  const venueEntry = venue && venue.id ? Vx[venue.id] : null;
  const hasImg = w.image && w.image.src && w.image.status === "pd";
  const held = w.image && w.image.status === "copyright";

  const moreBy = (catByArtist[a.id] || []).filter(o => o.id !== w.id);
  const near = w.coords
    ? CAT.filter(o => o.id !== w.id && o.artistId !== w.artistId && o.coords)
        .sort((x, y) => tasteDist(x.coords, w.coords) - tasteDist(y.coords, w.coords)).slice(0, 4)
    : [];

  return `
  ${crumbs([["Atlas",""],[a.name, "artist/" + a.id],[w.title]])}
  <div class="aw-hero" ${hasImg ? `data-lb-img="${w.image.src}" data-lb-cap="${esc(w.title)} (${esc(w.year.display)}) — ${esc(a.name)}" data-lb-link="${w.image.page}"` : ""}>
    ${hasImg
      ? `<img src="${w.image.src}" alt="${esc(w.title)} by ${esc(a.name)}">`
      : `<div class="aw-hero-gen">${canvasTag(a.style, a.palette, w.id, coverLabel(w.title + " by " + a.name), true)}<span class="map-hint">${held
        ? "a seeded Pigment interpretation — the original artwork remains under copyright"
        : "an interpretation painted in the browser — the original is unphotographed"}</span></div>`}
  </div>
  <div class="page-head" style="margin-top:22px">
    <h1 class="display" style="font-size:clamp(1.7rem,3.6vw,2.6rem)">${esc(w.title)}</h1>
    <div class="hero-sub"><a href="#/artist/${a.id}">${esc(a.name)}</a><span>${esc(w.year.display)}</span></div>
  </div>
  <div class="aw-actions">${passportActions(w)}${shareChip("p/artwork/" + w.id + ".html")}</div>
  <div class="chips" style="margin-bottom:26px">
    ${(w.movements || []).map(m => Mx[m] ? chip("m", "movement/" + m, Mx[m].name) : "").join("")}
    ${(w.techniques || []).map(t => Tx[t] ? chip("t", "technique/" + t, Tx[t].name) : "").join("")}
    ${w.nation && Nx[w.nation] ? chip("n", "nation/" + w.nation, Nx[w.nation].flag + " " + Nx[w.nation].name) : ""}
  </div>
  <div class="artist-cols">
    <div class="bio-block">
      ${w.description
        ? `<h2>The picture</h2><p>${esc(w.description)}</p>
           <h2>What to notice</h2><ul class="facts">${w.notice.map(n => `<li>${esc(n)}</li>`).join("")}</ul>`
        : `<p class="aw-empty">Not written about yet — the atlas is still being painted. The image, meanwhile, speaks for itself.</p>`}
      <p class="aw-provenance">${w.dims ? esc(w.dims) + " · " : ""}${venue ? (venue.id && Vx[venue.id] && !VENUE_SENTINELS[venue.id]
          ? `<a href="#/museum/${venue.id}">${esc(venue.name)}</a>` : esc(venue.name)) + (venue.city ? ", " + esc(venue.city) : "") + " · " : ""}${hasImg
        ? `<a href="${w.image.page}" target="_blank" rel="noopener">image via Wikimedia Commons</a>`
        : held ? "original image omitted under copyright" : "image not yet available"}</p>
      ${hasImg && imageCredit(w.image.src)
        ? `<p class="img-credit">${creditLine(imageCredit(w.image.src), "Image credit")}</p>` : ""}
      ${(listsByWork[w.id] || []).length ? `<div class="aw-lists"><span class="chip-label">In lists:</span> ${listsByWork[w.id].map(l =>
        `<a class="chip" href="#/list/${l.id}">${esc(l.title)}</a>`).join("")}</div>` : ""}
    </div>
    <aside class="side-panel">
      ${venue && venue.id && Vx[venue.id] && !VENUE_SENTINELS[venue.id] ? (() => {
        const mv = Vx[venue.id], mn = MNOTES[venue.id], heldHere = (catByVenue[venue.id] || []).length;
        return `<div class="panel mu-panel">
          <h3>Where it hangs</h3>
          ${mn && mn.photo ? `<a class="mu-panel-photo" href="#/museum/${mv.id}"><img loading="lazy" src="${mn.photo.src}" alt="${esc(mv.name)}"></a>` : ""}
          <a class="mu-panel-name" href="#/museum/${mv.id}">${esc(mv.name)}</a>
          <div class="mu-panel-meta">${esc(mv.city)}${mv.country ? " · " + esc(mv.country) : ""}${mn && mn.founded ? " · founded " + esc(mn.founded) : ""}</div>
          ${mn ? `<div class="mu-panel-hook">${esc(mn.hook)}</div>` : ""}
          <a class="chip-label" style="display:block;margin-top:10px" href="#/museum/${mv.id}">${heldHere} work${heldHere === 1 ? "" : "s"} from these walls in the atlas ${ARR}</a>
        </div>`;
      })() : ""}
      ${moreBy.length ? `<div class="panel"><h3>More by ${esc(artistShortName(a))}</h3><div class="mini-cards">${moreBy.slice(0, 4).map(o =>
        `<a class="mini-card" href="#/artwork/${o.id}">${o.image && o.image.src ? `<img class="mc-img" loading="lazy" src="${o.image.src}" alt="">` : canvasTag(a.style, a.palette, o.id, coverLabel(o.title + " by " + a.name))}<span><span class="mc-name">${esc(o.title)}</span><br><span class="mc-meta">${esc(o.year.display)}</span></span></a>`).join("")}</div></div>` : ""}
      ${near.length ? `<div class="panel"><h3>Near it in the atlas</h3><div class="mini-cards">${near.map(o =>
        `<a class="mini-card" href="#/artwork/${o.id}">${o.image && o.image.src ? `<img class="mc-img" loading="lazy" src="${o.image.src}" alt="">` : canvasTag(Ax[o.artistId].style, Ax[o.artistId].palette, o.id, coverLabel(o.title + " by " + Ax[o.artistId].name))}<span><span class="mc-name">${esc(o.title)}</span><br><span class="mc-meta">${esc(Ax[o.artistId].name)}</span></span></a>`).join("")}</div></div>` : ""}
      <div class="panel"><h3>Go next</h3><div class="chips">
        ${chip("a", "artist/" + a.id, "All of " + artistShortName(a))}
        ${w.movements && w.movements[0] && Mx[w.movements[0]] ? chip("m", "movement/" + w.movements[0], "More " + Mx[w.movements[0]].name) : ""}
      </div></div>
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
    <button class="f-btn ${view === "cards" ? "on" : ""}" data-vtype="${type}" data-view="cards" aria-pressed="${view === "cards"}">Cards</button>
    <button class="f-btn ${view === "tree" ? "on" : ""}" data-vtype="${type}" data-view="tree" aria-pressed="${view === "tree"}">Family tree</button>
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
        <div class="card-art">${canvasTag(e.style, e.palette, e.id, coverLabel(e.name))}</div>
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
        (idx>0 ? `<a href="#/era/${E[idx-1].id}">${ARRL} ${esc(E[idx-1].name)}</a>` : "") +
        (idx<E.length-1 ? `<a href="#/era/${E[idx+1].id}">${esc(E[idx+1].name)} ${ARR}</a>` : ""),
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
        <div class="card-art">${canvasTag("fauvist", n.palette, n.id, coverLabel(n.name))}</div>
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

/* ---------- privacy disclosure (#/privacy, AC25) ----------
   Plain, literal copy by design — this is instruction/state/persistence/privacy
   content, where the house style's clarity rule overrides its usual voice.
   Every figure below is measured against this build, not carried over from an
   earlier report; re-run the greps in build-log-unit-23.md before editing. */
function viewPrivacy(){
  document.title = "Privacy — Pigment";
  return `
  <div class="page-head">
    <div class="page-kicker">How Pigment handles your data</div>
    <h1 class="display">Privacy</h1>
    <p class="page-lede">Plain facts about what Pigment stores, what it sends, and to whom.</p>
  </div>
  <section style="max-width:680px">
    <h2 class="sec-title">No account, no server</h2>
    <p>Pigment has no account system and no backend server. Admiring a work, marking it Seen in person, saving it for later, and taking onboarding all write to your own browser's storage on your own device — nothing is sent to Pigment or to anyone else. Three keys are used: <code>pigment.taste.v1</code> (localStorage, your Taste Passport), <code>pigment.onboarding.v1</code> (sessionStorage, only while onboarding is in progress), and <code>pigment-theme</code> (localStorage, your dark/light choice). This data stays on your device until you clear it yourself or clear your browser's site data for Pigment.</p>

    <h2 class="sec-title">No analytics, no tracking</h2>
    <p>Pigment runs no analytics, no tracking pixels, and no beacons. No visit, click, or Admire is logged, measured, or transmitted anywhere. This was checked directly in the source, not assumed.</p>

    <h2 class="sec-title">One third-party host: Wikimedia Commons images</h2>
    <p>Pigment displays artwork and museum photographs hosted on Wikimedia Commons, at <code>upload.wikimedia.org</code>. When a page shows one of these images, your browser requests it directly from Wikimedia's servers, not from Pigment — that request reaches Wikimedia with your IP address, under Wikimedia's own privacy policy, which Pigment does not control. Measured in this build: <strong>888 upload.wikimedia.org image URLs</strong> across the catalog, gallery and museum data, rendered as images at 18 places in the code, on most pages that show artwork or museum photographs — artist pages, artwork pages, museum pages, lists, and more.</p>
    <p>Separately, the "image via Wikimedia Commons" / "source" / "file on Commons" links placed next to individual images point to Wikimedia Commons and Wikipedia file or article pages (<code>commons.wikimedia.org</code>, <code>en.wikipedia.org</code>, and one <code>pt.wikipedia.org</code> page), and the licence names in photo credits link to the licence deeds at <code>creativecommons.org</code> (plus one <code>flickr.com</code> "no known restrictions" statement). Those are ordinary outbound links — your browser only contacts them if you click through.</p>

    <h2 class="sec-title">Fonts are served locally</h2>
    <p>Pigment's typefaces, Playfair Display and Inter, are self-hosted from this site (<code>assets/fonts/</code>). No font provider is contacted when the site loads.</p>

    <h2 class="sec-title">Image credit</h2>
    <p>Artwork and museum images throughout Pigment are sourced from Wikimedia Commons. Where a licence requires it, the photographer, the licence and the source file are named next to the image itself. <a href="#/credits">Credits</a> collects all of them in one place.</p>

    <p style="margin-top:26px"><a class="chip" href="#/">Back to the atlas</a></p>
  </section>`;
}

/* ---------- the credits page (#/credits) ----------
   The per-image credit next to each picture is the one the licence requires;
   this page is the consolidated view of the same facts — every photographer in
   the atlas in one place, plus the general credit to Wikimedia Commons. Counts
   are computed from the registries rather than written down, so they cannot
   drift away from what actually ships. */
function shippedImageTitles(){
  const seen = {};
  CAT.forEach(w => {
    if(!(w.image && w.image.src && w.image.status === "pd")) return;
    const t = commonsTitle(w.image.src); if(t) seen[t] = 1;
  });
  const G = window.ARTWORKS || {};
  Object.keys(G).forEach(aid => Object.keys(G[aid]).forEach(title => {
    const t = commonsTitle(G[aid][title].img); if(t) seen[t] = 1;
  }));
  return Object.keys(seen);
}
/* file title → the works in the atlas that are that picture */
function creditUsage(){
  const use = {};
  const add = (src, label, href) => {
    const t = commonsTitle(src);
    if(!t || !ICREDITS[t]) return;
    const list = use[t] = use[t] || [];
    if(!list.some(u => u.label === label)) list.push({ label, href });
  };
  CAT.forEach(w => {
    if(!(w.image && w.image.src && w.image.status === "pd")) return;
    const a = Ax[w.artistId];
    add(w.image.src, w.title + (a ? " — " + a.name : ""), "#/artwork/" + w.id);
  });
  const G = window.ARTWORKS || {};
  Object.keys(G).forEach(aid => {
    const a = Ax[aid];
    Object.keys(G[aid]).forEach(title =>
      add(G[aid][title].img, title + (a ? " — " + a.name : ""), "#/artist/" + aid));
  });
  return use;
}
function viewCredits(){
  document.title = "Credits — Pigment";
  const venueIds = Object.keys(PCREDITS).filter(id => Vx[id]).sort((x, y) =>
    (Vx[x].name || "").localeCompare(Vx[y].name || ""));
  const venueRequired = venueIds.filter(id => PCREDITS[id].required).length;
  const imageIds = Object.keys(ICREDITS).sort();
  const usage = creditUsage();
  const shippedTotal = shippedImageTitles().length;
  const freeImages = Math.max(0, shippedTotal - imageIds.length);
  return `
  <div class="page-head">
    <div class="page-kicker">Attribution</div>
    <h1 class="display">Credits</h1>
    <p class="page-lede">Pigment is built on pictures other people took and shared. This page names them — every photographer whose licence asks to be named, and the archive that made the rest reachable at all.</p>
  </div>
  <section style="max-width:760px">
    <h2 class="sec-title">Wikimedia Commons</h2>
    <p>Every image in the atlas — the paintings and the buildings that hold them — comes from <a href="https://commons.wikimedia.org/" target="_blank" rel="noopener">Wikimedia Commons</a>, the free media archive maintained by the Wikimedia Foundation and its volunteers. Pigment is not affiliated with Wikimedia; it is one of the many things Commons exists to make possible. Images load directly from Wikimedia's servers, as the <a href="#/privacy">Privacy</a> page explains.</p>
    <p>Most of the paintings are old enough that Commons files them as public domain, and the photographs of them are offered under public-domain or CC0 terms — no credit is required, and none of that is a legal clearance we claim on your behalf. Where a licence <em>does</em> ask for credit, the credit is rendered next to the picture, and repeated here.</p>
  </section>

  <section style="max-width:760px">
    <h2 class="sec-title">Museum photographs <span class="count">${venueIds.length} buildings · ${venueRequired} under a licence requiring credit</span></h2>
    <p class="page-lede" style="font-size:1rem">The photograph on each museum's page and card was taken by one of these people.</p>
    <ul class="credit-list">
      ${venueIds.map(id => `<li>
        <a class="cr-what" href="#/museum/${id}">${esc(Vx[id].name)}</a>
        <span class="img-credit">${creditLine(PCREDITS[id], "Photograph")}</span>
      </li>`).join("")}
    </ul>
  </section>

  <section style="max-width:760px">
    <h2 class="sec-title">Artwork images under a licence <span class="count">${imageIds.length} of ${shippedTotal} images in the atlas</span></h2>
    <p class="page-lede" style="font-size:1rem">Most reproductions here carry Commons' public-domain assertion, and we checked each file really is the work it names — the source's claim and our own check, not a ruling we are qualified to make. These ${imageIds.length} are photographs somebody licensed for reuse on condition of credit — usually a picture taken in the room, of a fresco, a ceiling or a sculpture, where the photographer's own work is part of what you see. The remaining ${freeImages} carry no attribution condition.</p>
    <ul class="credit-list">
      ${imageIds.map(t => {
        const users = usage[t] || [];
        const what = users.length
          ? users.slice(0, 2).map(u => `<a href="${u.href}">${esc(u.label)}</a>`).join(", ")
          : esc(String(t).replace(/^File:/, "").replace(/_/g, " "));
        return `<li>
          <span class="cr-what">${what}</span>
          <span class="img-credit">${creditLine(ICREDITS[t], "Image credit")}</span>
        </li>`;
      }).join("")}
    </ul>
  </section>

  <section style="max-width:760px">
    <h2 class="sec-title">Fonts</h2>
    <p>Playfair Display and Inter are self-hosted under the SIL Open Font License 1.1 (see <code>assets/fonts/LICENSE.md</code>).</p>
    <p style="margin-top:26px"><a class="chip" href="#/">Back to the atlas</a> <a class="chip" href="#/privacy">Privacy</a></p>
  </section>`;
}

/* ============================================================
   ROUTER
   ============================================================ */
/* ---------- route orientation & focus (AC15, AC17) ----------
   `#app` used to carry aria-live="polite" while every navigation replaced its whole
   innerHTML — assistive tech re-read the entire page on every route change, sixteen
   times over during onboarding. That was replaced by a focus move to the new page's
   heading plus a small `#route-status` live region; both fired on every route
   change, so the page was announced twice, and because the live region carried the
   document title while the heading carries the editorial string, the two often
   disagreed ("The grand timeline" / "Timeline", "Blank canvas" / "Lost").
   There is now exactly one channel: focus moves to the new page's `h1`. It is the
   stronger signal — it announces the page identity AND places the caret at the
   content — and a status region that merely restates the heading added no
   information. Every route renders a non-empty `h1`, so identity is never lost.
   A re-render of the page you are already on (every onboarding tap calls route())
   announces nothing and puts focus back on the control you were using. */
let lastRouteKey = null;
function focusSilently(el){
  if(!el) return false;
  if(!el.hasAttribute("tabindex") && !/^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(el.tagName))
    el.setAttribute("tabindex", "-1");
  try{ el.focus({ preventScroll: true }); }catch(e){ try{ el.focus(); }catch(e2){ return false; } }
  return document.activeElement === el;
}
/* the entry point of a view: its heading, or the main landmark if it has none */
function viewEntry(){ return app.querySelector("h1") || app; }
/* a signature stable across a re-render of the same view */
function fpOf(el){
  if(!el || !el.dataset || !app.contains(el)) return null;
  const k = Object.keys(el.dataset);
  if(!k.length && !el.id) return null;
  return (el.id || "") + "|" + el.tagName + "|" + k.sort().map(n => n + "=" + el.dataset[n]).join("&");
}
function restoreFocus(fp){
  if(!fp) return false;
  const list = app.querySelectorAll("a[href], button, input, select, textarea, [tabindex]");
  for(let i = 0; i < list.length; i++) if(fpOf(list[i]) === fp) return focusSilently(list[i]);
  return false;
}
function route(){
  const hash = decodeURIComponent(location.hash.replace(/^#\/?/, ""));
  const [page, id] = hash.split("/");
  /* a genuine navigation, or a re-render of the page already on screen? */
  const key = page + "/" + (id || "");
  const first = lastRouteKey === null, nav = key !== lastRouteKey;
  const keep = nav ? null : fpOf(document.activeElement);
  lastRouteKey = key;
  let html;
  switch(page){
    case "":            html = viewHome(); break;
    case "artists":     html = viewArtists(); break;
    case "timeline":    html = viewTimeline(); break;
    case "influences":  html = viewInfluences(); break;
    case "daily":       html = viewDaily(); break;
    case "actuality":  html = viewActuality(); break;
    case "echoes":     html = viewEchoes(); break;
    case "lists":       html = viewLists(); break;
    case "list":        html = viewList(id); break;
    case "palette":     html = viewPalette(); break;
    case "taste":       html = viewTaste(); break;
    case "passport":    html = viewPassportImport(id); break;
    case "museums":     html = viewMuseums(); break;
    case "museum":      html = viewMuseum(id); break;
    case "explore":     html = viewExplore(); break;
    case "artist":      html = viewArtist(id); break;
    case "artwork":     html = viewArtwork(id); break;
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
    case "privacy":     html = viewPrivacy(); break;
    case "credits":     html = viewCredits(); break;
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
  mapDecollide();                          /* the world map, if this route carries one */
  animateCounters();
  setNav(page);
  hideSearch();
  if(nav && !first){
    /* one concise announcement of the new page identity, and focus at its start.
       Never on the first load — arriving at a page should not steal focus. */
    focusSilently(viewEntry());
  } else if(!nav){
    if(!restoreFocus(keep) && keep) focusSilently(viewEntry());   /* the control is gone — go to the heading, silently */
  }
  /* a queued result, spoken after the destination exists (AT-6, AT-7). Where the
     destination has a message slot the result is also PUT ON THE PAGE, because
     "which choice won" is not a screen-reader-only question — a sighted user was
     not told either. Routes without a slot get the announcement alone. */
  if(pendingSay){
    const m = pendingSay;
    pendingSay = null;
    const slot = document.getElementById("taste-msg");
    if(slot) slot.textContent = m;
    say(m, 320);
  }
}

/* skip navigation (AC17 "repeated navigation can be bypassed"): the header skip
   link, and the bypass past the influence graph's ~200 focusable nodes. A button,
   not an <a href="#…">, because the fragment belongs to the hash router. */
document.addEventListener("click", e => {
  const el = e.target.closest("[data-skipto]");
  if(!el) return;
  e.preventDefault();
  const to = el.dataset.skipto;
  const target = to === "main" ? viewEntry() : document.getElementById(to);
  if(!target || !focusSilently(target)) return;
  try{ target.scrollIntoView({ block: "start", behavior: reducedMotion ? "auto" : "smooth" }); }
  catch(err){ target.scrollIntoView(); }
});

/* The seven destinations that now live behind the Explore disclosure. Landing on
   any of them lights the Explore trigger as well as the link inside the panel,
   so the nav still tells you where you are even while the panel is shut. */
const EXPLORE_CHILDREN = { movements:1, techniques:1, eras:1, nations:1, explore:1, timeline:1, influences:1 };
/* Landing anywhere under Lists lights the Lists trigger too, so the nav still
   says where you are while the panel is shut. */
const LISTS_CHILDREN = { lists:1, actuality:1, echoes:1 };

function setNav(page){
  const map = { artists:"artists", artist:"artists", artwork:"artists", museums:"museums", museum:"museums", lists:"lists", list:"lists", actuality:"actuality", echoes:"echoes",
    explore:"explore", timeline:"timeline", influences:"influences", movements:"movements", movement:"movements",
    techniques:"techniques", technique:"techniques", eras:"eras", era:"eras",
    nations:"nations", nation:"nations", taste:"taste", passport:"taste" };
  const cur = map[page];
  /* The disclosure panels live at body level (see index.html), so they are NOT
     inside #main-nav. Querying only #main-nav here silently dropped all nine
     panel links from the active state and from aria-current — a regression
     introduced when the panels moved out of the header. */
  document.querySelectorAll("#main-nav a, .nav-panel a").forEach(a => {
    const on = a.dataset.nav === cur;
    a.classList.toggle("active", on);
    if(on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");   /* C1 */
  });
  const eb = document.getElementById("explore-btn");
  if(eb) eb.classList.toggle("active", !!EXPLORE_CHILDREN[cur]);
  const lb = document.getElementById("lists-btn");
  if(lb) lb.classList.toggle("active", !!LISTS_CHILDREN[cur]);
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
/* ---------- lightbox for real artworks ---------- */
function openLightbox(img, caption, link){
  let lb = document.getElementById("lightbox");
  if(!lb){
    lb = document.createElement("div");
    lb.id = "lightbox";
    document.body.appendChild(lb);
    lb.addEventListener("click", e => {
      if(e.target === lb || e.target.classList.contains("lb-close")) lb.classList.remove("open");
    });
    document.addEventListener("keydown", e => { if(e.key === "Escape") lb.classList.remove("open"); });
  }
  const big = img.replace(/\/(\d+)px-/, "/1280px-");
  /* the enlarged view is where a gallery thumbnail becomes the image itself —
     so it is where a licence-required credit has to appear (AC11/AC14) */
  const credit = creditLine(imageCredit(img), "Image credit");
  lb.innerHTML = `<figure>
    <button class="lb-close" aria-label="Close">×</button>
    <img src="${big}" onerror="if(this.src!=='${img}')this.src='${img}'" alt="">
    <figcaption>${caption}${link ? ` · <a href="${link}" target="_blank" rel="noopener">source</a>` : ""}${
      credit ? `<span class="img-credit lb-credit">${credit}</span>` : ""}</figcaption>
  </figure>`;
  lb.classList.add("open");
}

app.addEventListener("click", e => {
  const rnd = e.target.closest("[data-random-artist]");
  if(rnd){
    e.preventDefault();
    location.hash = "#/artist/" + A[Math.floor(Math.random() * A.length)].id;
    return;
  }
  const ppBtn = e.target.closest("[data-pp]");
  if(ppBtn){                                               /* Admire / Seen / Save → Taste Passport */
    const on = passportToggle(ppBtn.dataset.pp, ppBtn.dataset.ppid);
    if(on === null){ ppNotice(PP_WRITE_MSG); return; }      /* the write failed — leave the label alone */
    ppBtn.classList.toggle("on", on);
    ppBtn.setAttribute("aria-pressed", on ? "true" : "false");
    ppBtn.textContent = PP_LABELS[ppBtn.dataset.pp][on ? 1 : 0];
    return;
  }
  const lbEl = e.target.closest("[data-lb-img]");
  if(lbEl && !e.target.closest("a")){ openLightbox(lbEl.dataset.lbImg, lbEl.dataset.lbCap, lbEl.dataset.lbLink); return; }
  const ign = e.target.closest(".ig-node");
  if(ign){ igActivate(ign); return; }                      /* first click: focus; second: visit */
  const etb = e.target.closest("[data-etype-btn]");
  if(etb){                                                 /* edge-type filter */
    const ty = etb.dataset.etypeBtn;
    document.querySelectorAll("[data-etype-btn]").forEach(b => {
      b.classList.toggle("on", b === etb);
      b.setAttribute("aria-pressed", b === etb ? "true" : "false");
    });
    document.querySelectorAll(".ig-edge").forEach(l => l.classList.toggle("hid", !!ty && l.dataset.etype !== ty));
    return;
  }
  if(e.target.closest("#ig-svg")){ igClear(); return; }    /* background click clears focus */
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
  const tl = e.target.closest("[data-tlleg]");
  if(tl){                                                  /* expand/collapse the movement legend */
    tlLegendAll = !tlLegendAll;
    const wrap = document.getElementById("tl2");
    const sl = wrap ? wrap.scrollLeft : 0;
    route();
    const w2 = document.getElementById("tl2");
    if(w2) w2.scrollLeft = sl;
    return;
  }
  const tm = e.target.closest("[data-tlmov]");
  if(tm){                                                  /* movement isolation, no re-render */
    const wasOn = tm.classList.contains("on");
    document.querySelectorAll("[data-tlmov]").forEach(b => { b.classList.remove("on"); b.setAttribute("aria-pressed", "false"); });
    const mid = !wasOn ? tm.dataset.tlmov : "";
    if(!wasOn){ tm.classList.add("on"); tm.setAttribute("aria-pressed", "true"); }
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

/* constellation nodes are <g> elements: give them the key behaviour a button would have */
app.addEventListener("keydown", e => {
  const g = e.target.closest && e.target.closest(".ig-node");
  if(!g) return;
  if(e.key === "Enter" || e.key === " " || e.key === "Spacebar"){
    e.preventDefault();                                    /* Space must not scroll the graph */
    igActivate(g);
  } else if(e.key === "Escape"){
    igClear();                                             /* focus stays where it is */
  }
});
/* keep a keyboard-focused node inside the scrollable graph — never scroll the page itself */
app.addEventListener("focusin", e => {
  const g = e.target.closest && e.target.closest(".ig-node");
  const wrap = document.getElementById("ig-wrap");
  if(!g || !wrap) return;
  const b = g.getBoundingClientRect(), w = wrap.getBoundingClientRect();
  if(b.left < w.left || b.right > w.right)  wrap.scrollLeft += (b.left + b.right) / 2 - (w.left + w.right) / 2;
  if(b.top  < w.top  || b.bottom > w.bottom) wrap.scrollTop += (b.top + b.bottom) / 2 - (w.top + w.bottom) / 2;
});

/* F-2: below 820 px the nav is one scrolling row under an edge-fade mask, and a
   mask paints over the element's own box rather than over its content — so any
   link that comes to rest in the faded last 22 % has its focus ring dimmed out
   from under the keyboard user, whatever the scroll position. CSS alone cannot
   reach this: `scroll-padding`/`scroll-margin` only bite when the browser runs
   scroll-into-view, and it declines to run for a link that is already visible,
   which is exactly the case here — the link is visible, it is just faded. So
   scroll the row ourselves, and only as far as it takes to lift the ring clear
   of where the gradient starts. The mask is left alone; the scroll affordance
   is unchanged. The `.main-nav::after` strip is what makes the room to do it. */
const mainNav = document.getElementById("main-nav");
if(mainNav) mainNav.addEventListener("focusin", e => {
  const a = e.target.closest && e.target.closest("a");
  if(!a || !mainNav.contains(a)) return;
  const ncs = getComputedStyle(mainNav);
  if((ncs.maskImage || ncs.webkitMaskImage || "none") === "none") return;  /* wide layout: no fade */
  const acs = getComputedStyle(a);
  const ring = Math.max(5, (parseFloat(acs.outlineWidth) || 0) + (parseFloat(acs.outlineOffset) || 0));
  const nb = mainNav.getBoundingClientRect();
  const over = a.getBoundingClientRect().right + ring - (nb.left + nb.width * 0.78);
  if(over > 0) mainNav.scrollLeft += Math.ceil(over);       /* ceil: never leave a subpixel of ring in the fade */
});

/* ---- nav disclosures (B1, extended for Actuality) ----
   W3C APG disclosure-navigation behaviour, applied to every .nav-group in the
   header. Deliberately NOT a menu widget: each panel holds ordinary links in
   labelled lists, so a screen reader reads them the way it read the flat nav the
   owner's VoiceOver passes signed off. The button contributes aria-expanded and
   nothing more.

   Panels live at body level — see the note in index.html. .site-header carries
   backdrop-filter, which makes it the containing block for position:fixed
   descendants, and .main-nav is a horizontally scrolling row whose overflow-x
   and mask clip anything inside it. Measured at 390px, a panel inside the header
   rendered as a sliver. The cost of moving them out is DOM adjacency, so Tab is
   managed explicitly below. */
function wireNavDisclosure(group){
  const btn = group.querySelector(".nav-disclosure");
  const panel = document.getElementById(btn && btn.getAttribute("aria-controls"));
  if(!btn || !panel) return;
  const links = () => [...panel.querySelectorAll("a")];
  const isOpen = () => btn.getAttribute("aria-expanded") === "true";
  const inWidget = t => !!t && (group.contains(t) || panel.contains(t));
  const afterTrigger = () => group.nextElementSibling;

  function place(){
    const r = btn.getBoundingClientRect();
    const w = panel.offsetWidth;
    panel.style.left = Math.max(8, Math.min(r.left, window.innerWidth - w - 8)) + "px";
    panel.style.top  = Math.round(r.bottom + 6) + "px";
  }
  function open(){
    if(isOpen()) return;
    closeAllNavPanels(group);          /* only one open at a time */
    panel.hidden = false;
    btn.setAttribute("aria-expanded", "true");
    place();
    window.addEventListener("scroll", place, true);
    window.addEventListener("resize", place);
  }
  function close(refocus){
    if(!isOpen()) return;
    btn.setAttribute("aria-expanded", "false");
    panel.hidden = true;
    window.removeEventListener("scroll", place, true);
    window.removeEventListener("resize", place);
    if(refocus) btn.focus();
  }
  group._closeNavPanel = () => close(false);

  btn.addEventListener("click", () => { isOpen() ? close(false) : open(); });
  btn.addEventListener("keydown", e => {
    if(e.key === "ArrowDown" || e.key === "Down"){
      e.preventDefault(); open();
      const first = links()[0]; if(first) first.focus();
      return;
    }
    /* DOM order puts the panel at the end of the document, so an unmanaged Tab
       would jump straight past it. Send it into the panel instead. */
    if(e.key === "Tab" && !e.shiftKey && isOpen()){
      const first = links()[0];
      if(first){ e.preventDefault(); first.focus(); }
    }
  });
  panel.addEventListener("keydown", e => {
    const l = links(), i = l.indexOf(document.activeElement);
    if(e.key === "ArrowDown" || e.key === "Down"){ e.preventDefault(); l[(i+1) % l.length].focus(); }
    else if(e.key === "ArrowUp" || e.key === "Up"){ e.preventDefault(); l[(i-1+l.length) % l.length].focus(); }
    else if(e.key === "Home"){ e.preventDefault(); l[0].focus(); }
    else if(e.key === "End"){ e.preventDefault(); l[l.length-1].focus(); }
    else if(e.key === "Tab" && e.shiftKey && i === 0){ e.preventDefault(); btn.focus(); }
    else if(e.key === "Tab" && !e.shiftKey && i === l.length-1){
      const next = afterTrigger();
      if(next){ e.preventDefault(); close(false); next.focus(); }
    }
  });
  const onEsc = e => { if(e.key === "Escape" || e.key === "Esc"){ e.preventDefault(); close(true); } };
  group.addEventListener("keydown", onEsc);
  panel.addEventListener("keydown", onEsc);
  document.addEventListener("focusin", e => { if(isOpen() && !inWidget(e.target)) close(false); });
  document.addEventListener("pointerdown", e => { if(isOpen() && !inWidget(e.target)) close(false); });
  panel.addEventListener("click", e => { if(e.target.closest("a")) close(false); });
}
function closeAllNavPanels(except){
  document.querySelectorAll(".nav-group").forEach(g => {
    if(g !== except && g._closeNavPanel) g._closeNavPanel();
  });
}
document.querySelectorAll(".nav-group").forEach(wireNavDisclosure);

window.addEventListener("hashchange", route);

/* ============================================================
   SEARCH
   ============================================================ */
const searchInput = document.getElementById("search");
const searchResults = document.getElementById("search-results");
const INDEX = [
  ...A.map(a => ({ type:"Artists",    href:"artist/"+a.id,    name:a.name, meta:a.years })),
  ...CAT.map(w => ({ type:"Artworks", href:"artwork/"+w.id,  name:w.title, meta:Ax[w.artistId] ? Ax[w.artistId].name : "" })),
  ...LISTS.map(l => ({ type:"Lists",  href:"list/"+l.id,     name:l.title, meta:l.works.length + " works", nometa:1 })),
  ...VEN.filter(v => !VENUE_SENTINELS[v.id] && (catByVenue[v.id] || []).length)
        .map(v => ({ type:"Museums", href:"museum/"+v.id,    name:v.name, meta:v.city })),
  ...M.map(m => ({ type:"Movements",  href:"movement/"+m.id,  name:m.name, meta:m.period || "" })),
  ...T.map(t => ({ type:"Techniques", href:"technique/"+t.id, name:t.name, meta:"" })),
  ...E.map(e => ({ type:"Eras",       href:"era/"+e.id,       name:e.name, meta:e.range })),
  ...N.map(n => ({ type:"Nations",    href:"nation/"+n.id,    name:n.flag+" "+n.name, alt:n.name, meta:"" }))
];
let selIdx = -1;

/* ---------- relevance ranking (AC21) ----------
   Six tiers, best first. Ranking is by RELEVANCE; entity type survives only as the
   deterministic tie-break inside a single tier, never as the ordering itself. */
const SR_MAX = 9;
const SR_EXACT = 0, SR_PREFIX = 1, SR_WORD = 2, SR_META = 3, SR_SUB = 4, SR_METASUB = 5, SR_NONE = 9;
const SR_ARTICLE = /^(?:the|a|an|le|la|les|los|las|el|il|der|die|das)\s+(.+)$/;
const SR_BOUNDARY = /[\s\-–—'’"“”()[\]/.,:;!?]/;
/* every string an entry may be matched against: its display name, any explicit
   alternate name (a nation carries the bare country name behind its flag glyph),
   and either of those without a leading article — display ornament is not identity */
function srKeys(it){
  const keys = [it.name.toLowerCase()];
  const add = s => { if(s && keys.indexOf(s) < 0) keys.push(s); };
  if(it.alt) add(it.alt.toLowerCase());
  keys.slice().forEach(k => { const m = k.match(SR_ARTICLE); if(m) add(m[1]); });
  return keys;
}
/* a list's meta is a count ("12 works"), not identity — it is displayed, never matched */
INDEX.forEach(it => { it.keys = srKeys(it); it.metaKey = it.nometa ? "" : (it.meta || "").toLowerCase(); });

/* does q start a word inside hay (a surname, "du Louvre"), or merely fall inside
   one ("sTATE Hermitage")? */
function srWordStart(hay, q){
  for(let i = hay.indexOf(q); i > 0; i = hay.indexOf(q, i + 1)){
    if(SR_BOUNDARY.test(hay.charAt(i - 1))) return true;
  }
  return false;
}
function srRank(it, q){
  let best = SR_NONE;
  for(const k of it.keys){
    if(k === q) return SR_EXACT;                        /* an exact name always ranks first */
    const at = k.indexOf(q);
    if(at === 0) best = Math.min(best, SR_PREFIX);
    else if(at > 0) best = Math.min(best, srWordStart(k, q) ? SR_WORD : SR_SUB);
  }
  if(best <= SR_WORD) return best;
  /* meta was never searched before, so no artwork could be found by its painter's
     name. A meta match on a word boundary is meaningful and outranks an incidental
     substring buried inside an unrelated title. */
  const m = it.metaKey, mat = m ? m.indexOf(q) : -1;
  if(mat >= 0) best = Math.min(best, (mat === 0 || srWordStart(m, q)) ? SR_META : SR_METASUB);
  return best;
}
/* Type-fair fill. Inside one tier the matching types take turns, so a crowded type
   (247 artists) can never consume the whole cap and starve a matching artwork,
   museum or movement. Tiers are never crossed for fairness — a prefix match always
   outranks a substring match, whichever types they belong to. */
function srSelect(scored, max){
  const out = [];
  for(let tier = SR_EXACT; tier <= SR_METASUB && out.length < max; tier++){
    const lanes = [], byType = {};
    scored.forEach(s => {
      if(s.r !== tier) return;
      if(!byType[s.it.type]) lanes.push(byType[s.it.type] = []);
      byType[s.it.type].push(s.it);
    });
    for(let round = 0, moved = true; moved && out.length < max; round++){
      moved = false;
      for(const lane of lanes){
        if(round >= lane.length) continue;
        out.push(lane[round]); moved = true;
        if(out.length >= max) break;
      }
    }
  }
  return out;
}

function runSearch(q){
  q = q.trim().toLowerCase();
  if(!q){ hideSearch(); return; }
  const scored = [];
  INDEX.forEach(it => { const r = srRank(it, q); if(r < SR_NONE) scored.push({ it, r }); });
  const hits = srSelect(scored, SR_MAX);
  selIdx = -1;
  if(!hits.length){
    searchResults.innerHTML = `<div class="sr-empty">Nothing in the atlas matches “${esc(q)}”.</div>`;
    searchResults.setAttribute("aria-label", "Search results — nothing matches");
  } else {
    /* listbox → group → option, so the type headings stay in the tree as group names (C3).
       Grouping happens AFTER ranking, so each type's heading is emitted exactly once and
       the groups are ordered by their best-ranked member. */
    const groups = [];
    hits.forEach(it => {
      let g = groups.find(x => x.type === it.type);
      if(!g) groups.push(g = { type: it.type, items: [] });
      g.items.push(it);
    });
    let html = "", i = 0;
    groups.forEach(g => {
      html += `<div role="group" aria-label="${esc(g.type)}"><div class="sr-group" role="presentation">${g.type}</div>`;
      g.items.forEach(it => {
        html += `<a href="#/${it.href}" id="sr-opt-${i}" role="option" aria-selected="false" tabindex="-1" data-i="${i}"><span>${esc(it.name)}</span><span class="sr-meta">${esc(it.meta)}</span></a>`;
        i++;
      });
      html += `</div>`;
    });
    /* the cap used to truncate in silence; say so instead */
    const more = scored.length - hits.length;
    if(more > 0) html += `<div class="sr-more" aria-hidden="true">Showing ${hits.length} of ${scored.length} matches — keep typing to narrow it.</div>`;
    searchResults.innerHTML = html;
    searchResults.setAttribute("aria-label", more > 0
      ? `Search results — showing ${hits.length} of ${scored.length} matches`
      : `Search results — ${hits.length} match${hits.length === 1 ? "" : "es"}`);
  }
  searchResults.hidden = false;
  searchInput.setAttribute("aria-expanded", "true");
  searchInput.removeAttribute("aria-activedescendant");
}
function hideSearch(){
  searchResults.hidden = true; selIdx = -1;
  searchResults.setAttribute("aria-label", "Search results");
  searchInput.setAttribute("aria-expanded", "false");
  searchInput.removeAttribute("aria-activedescendant");
}

searchInput.addEventListener("input", () => runSearch(searchInput.value));
searchInput.addEventListener("focus", () => { if(searchInput.value.trim()) runSearch(searchInput.value); });
searchInput.addEventListener("keydown", e => {
  const links = [...searchResults.querySelectorAll("a")];
  if(e.key === "ArrowDown" || e.key === "ArrowUp"){
    e.preventDefault();
    if(!links.length) return;
    selIdx = (selIdx + (e.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
    links.forEach((l,i) => {
      l.classList.toggle("sel", i === selIdx);
      l.setAttribute("aria-selected", i === selIdx ? "true" : "false");
    });
    searchInput.setAttribute("aria-activedescendant", links[selIdx].id);
    links[selIdx].scrollIntoView({ block:"nearest" });
  } else if(e.key === "Enter"){
    const target = links[selIdx >= 0 ? selIdx : 0];
    if(target){ location.hash = target.getAttribute("href"); searchInput.value = ""; hideSearch(); }
  } else if(e.key === "Escape"){
    /* AT-3 — Escape closed the results and said nothing. Focus was already
       returning correctly (unit 7 fixed the blur-to-body defect), but the
       frozen criterion asks for the dismissal to be PERCEIVABLE, and a silent
       correct action is not. Announced only from this path: hideSearch() is
       also called by route() and by every outside click, and announcing there
       would re-create the C-8 defect unit 25f removed. Guarded on the panel
       having actually been open, so Escape on a closed field stays silent. */
    const wasOpen = !searchResults.hidden;
    hideSearch();
    searchInput.focus();
    if(wasOpen) say("Search results closed. You are back in the search field.");
  }
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
  themeBtn.setAttribute("aria-pressed", t === "light" ? "true" : "false");   /* C2: stable label, toggled state */
  if(window.__bgInit) window.__bgInit();
}
themeBtn.addEventListener("click", () => applyTheme(currentTheme() === "light" ? "dark" : "light"));
themeBtn.textContent = currentTheme() === "light" ? "☾" : "☀";
themeBtn.setAttribute("aria-pressed", currentTheme() === "light" ? "true" : "false");

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

/* ============ Phase 1.5: the taste engine (TASTE_MATH.md) ============ */
const TAXES = ["F","D","E","C","M"];
const T_POLE = { F:["figurative","abstract"], D:["calm","dramatic"], E:["classical","experimental"], C:["sensual","conceptual"], M:["intimate","monumental"] };

function ppSave(p){
  p.updatedAt = new Date().toISOString();
  return ppWrite(p);
}
function ppFull(){
  const p = getPassport() || newPassport();
  p.skipped = p.skipped || []; p.deckSeen = p.deckSeen || [];
  return p;
}
function coordsOfWork(w){
  if(!w) return null;
  if(w.coords) return w.coords;
  const t1 = window.TIER1 && window.TIER1[w.artistId];
  return (t1 && t1.coords) || null;
}

/* ---------- the engine (TASTE_MATH §2–5) ---------- */
function tasteState(p){
  p = p || ppFull();
  const items = (p.admirations || []).map(e => CatX[e.id]).filter(Boolean)
    .map(w => ({ w: 1.0, x: coordsOfWork(w), work: w })).filter(it => it.x);
  const n = items.length, sw = n * 1.0;

  /* prior: quiz nudges (capped ±60) + whisper palette nudges, re-capped */
  const q = { F:0, D:0, E:0, C:0, M:0 };
  const hasQuiz = !!(p.quiz && p.quiz.prior);
  if(hasQuiz) TAXES.forEach(a => q[a] = p.quiz.prior[a] || 0);
  if(p.palette && p.palette.tones) p.palette.tones.forEach(tid => {
    const t = (window.TASTE_TONES || []).find(o => o.id === tid);
    if(t) Object.keys(t.nudge).forEach(a => q[a] += t.nudge[a]);
  });
  TAXES.forEach(a => q[a] = Math.max(-60, Math.min(60, Math.round(q[a]))));
  const k = hasQuiz ? 6 : 0;

  const u = {};
  TAXES.forEach(a => u[a] = (sw + k) > 0
    ? Math.round((items.reduce((s, it) => s + it.w * it.x[a], 0) + k * q[a]) / (sw + k)) : 0);

  /* per-axis confidence (§4) */
  const nEff = sw + k, conf = {}, informed = {}, sds = {};
  TAXES.forEach(a => {
    const sd = nEff ? Math.sqrt(items.reduce((s, it) => s + it.w * Math.pow(it.x[a] - u[a], 2), 0) / nEff) : 0;
    sds[a] = sd;
    const sem = nEff ? sd / Math.sqrt(nEff) : 99;
    conf[a] = Math.max(0, 1 - Math.min(1, sem / 25));
    informed[a] = items.filter(it => Math.abs(it.x[a]) >= 40).length >= 3;
  });
  const axSd = TAXES.reduce((s, a) => s + sds[a], 0) / TAXES.length;   /* per-axis spread, −100…100 scale (§4/§5) */

  /* 1-or-2 component mixture (§3.1) */
  let components = [{ center: u, items, weight: 1 }], split = false;
  const meanSd = axSd;                                                  /* §5 eclectic threshold operates on this */
  if(n >= 6){
    const S1 = items.reduce((s, it) => s + it.w * Math.pow(tasteDist(it.x, u), 2), 0);
    let far = [0, 1], fd = -1;
    for(let i = 0; i < n; i++) for(let j = i + 1; j < n; j++){
      const d = tasteDist(items[i].x, items[j].x);
      if(d > fd){ fd = d; far = [i, j]; }
    }
    let c1 = Object.assign({}, items[far[0]].x), c2 = Object.assign({}, items[far[1]].x), g1, g2;
    for(let iter = 0; iter < 5; iter++){
      g1 = []; g2 = [];
      items.forEach(it => (tasteDist(it.x, c1) <= tasteDist(it.x, c2) ? g1 : g2).push(it));
      [ [g1, c1], [g2, c2] ].forEach(([g, c]) => {
        if(!g.length) return;
        TAXES.forEach(a => c[a] = Math.round(g.reduce((s, it) => s + it.x[a], 0) / g.length));
      });
    }
    const S2 = g1.reduce((s, it) => s + Math.pow(tasteDist(it.x, c1), 2), 0)
             + g2.reduce((s, it) => s + Math.pow(tasteDist(it.x, c2), 2), 0);
    const fd2 = Math.sqrt(1.5 * Math.pow(c1.F - c2.F, 2) + 1.5 * Math.pow(c1.D - c2.D, 2));
    if(S2 <= 0.6 * S1 && g1.length >= 3 && g2.length >= 3 && fd2 >= 50){
      split = true;
      const [big, small] = g1.length >= g2.length ? [[g1, c1], [g2, c2]] : [[g2, c2], [g1, c1]];
      /* quiz prior attaches to the larger component */
      const bu = {};
      TAXES.forEach(a => bu[a] = Math.round((big[0].reduce((s, it) => s + it.x[a], 0) + k * q[a]) / (big[0].length + k)));
      components = [
        { center: bu, items: big[0], weight: big[0].length / n },
        { center: small[1], items: small[0], weight: small[0].length / n }
      ];
    }
  }

  /* confidence tier — the copy layer */
  const tier = n < 20 ? "provisional" : n < 50 ? "forming" : n < 100 ? "solid" : n < 250 ? "strong" : "deep";
  /* quiz-vs-evidence disagreement keeps things provisional (§4) */
  let disagree = false;
  if(hasQuiz && n) TAXES.forEach(a => {
    const em = items.reduce((s, it) => s + it.x[a], 0) / n;
    if(informed[a] && Math.abs(q[a] - em) > 50) disagree = true;
  });
  return { p, items, n, q, k, u, conf, informed, components, split, meanSd, tier,
           provisional: n < 20 || disagree };
}

function sigMet(sig, items){
  if(sig.movement) return items.filter(it => (it.work.movements || []).indexOf(sig.movement) >= 0).length >= sig.min;
  if(sig.tag) return items.filter(it => (it.work.tags || []).indexOf(sig.tag) >= 0).length >= sig.min;
  return true;
}
function generalFired(st){
  if(st.split && st.components[1].weight >= 0.35) return PERSONAS.find(ps => ps.rule === "contradiction");
  if(!st.split && st.meanSd >= 45 && st.n >= 8) return PERSONAS.find(ps => ps.rule === "eclectic");
  if(st.n >= 8){
    const ys = st.items.map(it => it.work.year.sort);
    if(Math.max.apply(null, ys) - Math.min.apply(null, ys) >= 400) return PERSONAS.find(ps => ps.rule === "time-traveler");
  }
  return null;
}
function personaCandidates(st){
  const score = (ps, center) => {
    let d = tasteDist(ps.coords, center);
    if(ps.sig && !sigMet(ps.sig, st.items)) d += 25;
    return d;
  };
  const primary = st.components[0].center;
  let cands = PERSONAS.filter(ps => ps.kind === "specific")
    .map(ps => ({ ps, d: score(ps, primary) })).sort((a, b) => a.d - b.d).slice(0, 3).map(o => o.ps);
  const fired = generalFired(st);
  if(fired) cands = [fired].concat(cands.slice(0, 2));
  let secondary = null;
  if(st.split){
    secondary = PERSONAS.filter(ps => ps.kind === "specific")
      .map(ps => ({ ps, d: score(ps, st.components[1].center) })).sort((a, b) => a.d - b.d)[0].ps;
  }
  return { cands, secondary };
}

/* ---------- adaptive deck (§6 + ADMIRE_SPEC §6.2 constraints) ---------- */
function deckPool(){
  return CAT.filter(w => w.tier === 1 && w.coords && w.image && w.image.status === "pd" && w.image.src);
}
const NON_EURO = { japan:1, usa:1, mexico:1 };
function buildDeck(seed){
  const R = mulberry(hashStr("deck:" + seed));
  const pool = deckPool(), used = {}, picked = [];
  const take = w => { if(w && !used[w.id]){ used[w.id] = 1; picked.push(w); } };
  const pickFrom = arr => arr.length ? arr[Math.floor(R() * Math.min(3, arr.length))] : null;
  /* stage 1: one anchor per F×D quadrant, |F|,|D| as extreme as the pool allows */
  [[1,1],[1,-1],[-1,-1],[-1,1]].forEach(([sf, sd]) => {
    for(const lim of [50, 25, 1]){
      const cands = pool.filter(w => !used[w.id] && sf * w.coords.F >= lim && sd * w.coords.D >= lim);
      if(cands.length){ take(pickFrom(cands)); return; }
    }
  });
  /* §6.2 quotas over the whole deck */
  const need = [
    { t: w => w.coords.F >= 30, min: 3 },
    { t: w => NON_EURO[w.nation], min: 2 },
    { t: w => w.year.sort < 1700, min: 3 },
    { t: w => w.year.sort >= 1800 && w.year.sort < 1880, min: 3 },
    { t: w => w.year.sort >= 1880 && w.year.sort <= 1935, min: 3 }
  ];
  /* stages 2–4: probe E, then C, then rotate — quota gaps first, extremes preferred */
  ["E", "C", "*"].forEach((ax, si) => {
    for(let i = 0; i < 4 && picked.length < 16; i++){
      const gap = need.find(nd => picked.filter(nd.t).length < nd.min && pool.some(w => !used[w.id] && nd.t(w)));
      let cands = pool.filter(w => !used[w.id] && (!gap || gap.t(w)));
      if(!cands.length) cands = pool.filter(w => !used[w.id]);
      const axis = ax === "*" ? TAXES[(si + i) % 5] : ax;
      const pole = i % 2 ? -1 : 1;
      cands = cands.slice().sort((a, b) => pole * (b.coords[axis] - a.coords[axis]));
      take(pickFrom(cands));
    }
  });
  while(picked.length < 16){
    const rest = pool.filter(w => !used[w.id]);
    if(!rest.length) break;
    take(rest[Math.floor(R() * rest.length)]);
  }
  return picked.slice(0, 16);
}

/* ---------- discovery rings (§7) ---------- */
function discoveryBatch(st){
  const admired = {};
  (st.p.admirations || []).forEach(e => admired[e.id] = 1);
  const centers = st.components.map(c => c.center);
  const scored = deckPool().filter(w => !admired[w.id]).map(w => ({
    w, d: Math.min.apply(null, centers.map(c => tasteDist(coordsOfWork(w), c)))
  }));
  const ring = o => o.d <= 35 ? 0 : o.d <= 65 ? 1 : o.d <= 95 ? 2 : 3;
  const buckets = [[], [], [], []];
  scored.sort((a, b) => a.d - b.d).forEach(o => buckets[ring(o)].push(o));
  const mix = [3, 2, 1, 1], out = [], perArtist = {};
  const pull = b => {
    while(b.length){
      const o = b.shift();
      if((perArtist[o.w.artistId] || 0) >= 2) continue;
      perArtist[o.w.artistId] = (perArtist[o.w.artistId] || 0) + 1;
      return o;
    }
    return null;
  };
  mix.forEach((count, ri) => {
    for(let i = 0; i < count; i++){
      const o = pull(buckets[ri]) || pull(buckets[Math.min(3, ri + 1)]) || pull(buckets[Math.max(0, ri - 1)]);
      if(o) out.push({ w: o.w, ring: ri });
    }
  });
  return out;
}

/* ---------- shared render bits ---------- */
const RING_LABELS = ["Close to your taste", "A little outside your map", "A stretch admiration", "A wildcard from the atlas"];
function signalWords(u){
  const sec = ["E","C","M"].map(a => Math.abs(u[a]) >= 15 ? T_POLE[a][u[a] > 0 ? 1 : 0] : null).filter(Boolean);
  return { primary: T_POLE.F[u.F > 0 ? 1 : 0] + " + " + T_POLE.D[u.D > 0 ? 1 : 0], secondary: sec.join(", ") || "still forming" };
}
function tasteMapSVG(st, size){
  const S = size || 340, pad = 26;
  const px = v => pad + (v + 100) / 200 * (S - 2 * pad);
  const py = v => S - pad - (v + 100) / 200 * (S - 2 * pad);
  const dots = st.items.map(it =>
    `<circle cx="${px(it.x.F)}" cy="${py(it.x.D)}" r="3.4" class="tm-dot"><title>${esc(it.work.title)}</title></circle>`).join("");
  const centers = st.components.map((c, i) =>
    `<circle cx="${px(c.center.F)}" cy="${py(c.center.D)}" r="${i ? 7 : 9}" class="tm-you ${i ? "tm-second" : ""}"/>`).join("");
  return `<svg viewBox="0 0 ${S} ${S}" class="taste-map" role="img" aria-label="Your position on the taste map">
    <line x1="${px(0)}" y1="${pad}" x2="${px(0)}" y2="${S - pad}" class="tm-axis"/>
    <line x1="${pad}" y1="${py(0)}" x2="${S - pad}" y2="${py(0)}" class="tm-axis"/>
    <text x="${pad}" y="${py(0) - 6}" class="tm-lab">figurative</text>
    <text x="${S - pad}" y="${py(0) - 6}" text-anchor="end" class="tm-lab">abstract</text>
    <text x="${px(0) + 6}" y="${pad + 8}" class="tm-lab">dramatic</text>
    <text x="${px(0) + 6}" y="${S - pad}" class="tm-lab">calm</text>
    ${dots}${centers}</svg>`;
}
function personaCard(ps, opts){
  opts = opts || {};
  const g = `linear-gradient(120deg, ${ps.palette.join(", ")})`;
  return `<div class="persona-card ${opts.adopted ? "adopted" : ""}">
    <div class="pc-band" style="background:${g}"></div>
    <div class="pc-body">
      <div class="pc-kind">${ps.kind === "general" ? "a general persona" : "persona"}${opts.adopted ? " · yours" : ""}</div>
      <h3>${esc(ps.name)}</h3>
      <p>${esc(ps.blurb)}</p>
      ${opts.adoptBtn ? `<button class="aw-btn primary" data-tsx="adopt" data-tsid="${ps.id}">Adopt this Persona</button>` : ""}
    </div>
  </div>`;
}

/* ---------- onboarding state + view (#/palette) ----------
   The in-progress state is materialized to sessionStorage after every step, so a
   reload, a back/forward, or a wandered-off tab resumes at the exact checkpoint with
   the same sixteen works and the same answers. The deck ids are stored rather than a
   seed: buildDeck() is seeded with Math.random(), so no seed can rebuild it. This is
   a separate additive key — `pigment.taste.v1` and its schema are untouched, and a
   browser that refuses the write simply loses resumability, never the run itself. */
const OB_KEY = "pigment.onboarding.v1";
let ob = null;
function obWrite(){
  if(!ob) return;
  try{
    sessionStorage.setItem(OB_KEY, JSON.stringify({
      v: 1, step: ob.step, tones: ob.tones, deck: ob.deck.map(w => w.id), di: ob.di,
      admired: ob.admired, skipped: ob.skipped, answers: ob.answers, adopted: ob.adopted
    }));
  }catch(e){}
}
function obClear(){
  ob = null;
  try{ sessionStorage.removeItem(OB_KEY); }catch(e){}
}
function obRestore(){
  let raw = null;
  try{ raw = sessionStorage.getItem(OB_KEY); }catch(e){ return null; }
  if(!raw) return null;
  let s; try{ s = JSON.parse(raw); }catch(e){ return null; }
  if(!s || s.v !== 1 || !Array.isArray(s.deck) || !s.deck.length) return null;
  const deck = s.deck.map(id => CatX[id]).filter(Boolean);
  if(deck.length !== s.deck.length) return null;      /* catalog moved under a stale tab — don't half-resume */
  const o = { step: [1, 2, 3, 4].indexOf(s.step) >= 0 ? s.step : 1,
              tones: (s.tones || []).slice(0, 4), deck: deck,
              di: Math.max(0, Math.min(deck.length, s.di | 0)),
              admired: (s.admired || []).slice(), skipped: (s.skipped || []).slice(),
              answers: Object.assign({}, s.answers || {}), adopted: !!s.adopted };
  /* never resume into a step whose own precondition no longer holds */
  if(o.step === 2 && o.di >= o.deck.length) o.step = 3;
  if(o.step === 3 && Object.keys(o.answers).length >= TASTE_QUESTIONS.length) o.step = 4;
  return o;
}
function obStart(){
  ob = { step: 1, tones: [], deck: buildDeck(new Date().toISOString().slice(0, 10) + ":" + Math.floor(Math.random() * 1e6)),
         di: 0, admired: [], skipped: [], answers: {}, adopted: false };
  obWrite();
}
ob = obRestore();
/* AT-1's active half. The deck re-renders the same route, so route() restores
   focus to the button that was just pressed and announces nothing — correct
   behaviour for a re-render, and exactly why the new artwork went unspoken.
   This is the one thing that changed, said once. */
function obDeckSay(){
  if(!ob || ob.step !== 2) return;
  const w = ob.deck[ob.di];
  if(!w) return;
  const a = Ax[w.artistId];
  /* AT-1 follow-on, unit 34. The owner listened to sixteen consecutive
     announcements and asked for the count at the quarter points only. Card 1
     keeps it because entering the deck says nothing else: obDeckSay() is the
     single spoken event on `tones-done`, so without it a listener learns the
     deck's length at card 4. Title, artist and year stay on every card. */
  const n = ob.di + 1;
  const pos = (n === 1 || n % 4 === 0) ? `Artwork ${n} of 16. ` : "";
  say(`${w.title} — ${a.name}, ${w.year.display}. ${pos}Admire, or pass.`);
}
function viewPalette(){
  document.title = "Find your palette — Pigment";
  if(!ob || ob.step === 0) return `
    <div class="ob-wrap">
      <div class="page-kicker">Onboarding · under four minutes</div>
      <h1 class="display">Find your palette.</h1>
      <p class="page-lede">Four tones, sixteen artworks, five questions — and Pigment sketches the first map of your taste: your position among eight centuries of painting, and a provisional Persona to argue with. It sharpens forever after; nothing here is a grade.</p>
      <button class="aw-btn primary ob-cta" data-tsx="start">Begin ${ARR}</button>
      ${getPassport() && getPassport().milestones && getPassport().milestones.onboarded
        ? `<a class="chip-label" style="display:block;margin-top:14px" href="#/taste">or return to your taste page ${ARR}</a>` : ""}
    </div>`;

  if(ob.step === 1){
    return `
    <div class="ob-wrap">
      <div class="page-kicker">Step 1 of 3 · the palette</div>
      <h1 class="display">Pick four tones.</h1>
      <p class="page-lede">Don't overthink — choose the four you'd want on your walls. They seed your profile palette and whisper (only whisper) to the map.</p>
      <div class="tone-grid">${TASTE_TONES.map(t => `
        <button class="tone ${ob.tones.indexOf(t.id) >= 0 ? "on" : ""}" data-tsx="tone" data-tsid="${t.id}" aria-pressed="${ob.tones.indexOf(t.id) >= 0}" style="--tone:${t.hex}">
          <i></i><span>${esc(t.name)}</span>
        </button>`).join("")}</div>
      <div class="ob-foot">
        <span class="chip-label">${ob.tones.length} of 4 chosen</span>
        <button class="aw-btn primary" data-tsx="tones-done" ${ob.tones.length === 4 ? "" : "disabled"}>To the deck ${ARR}</button>
      </div>
    </div>`;
  }

  if(ob.step === 2){
    const w = ob.deck[ob.di], a = Ax[w.artistId];
    const subject = `${w.title} — ${a.name}, ${w.year.display}`;
    /* AT-1, the most serious accessibility defect found in PIG-001: the deck
       asked the visitor to Admire or Pass on sixteen artworks and never said
       which artwork. Every prior check confirmed the CONTROLS were reachable and
       named; none checked that the SUBJECT was announced, so the core Taste loop
       was not operable by a blind user.
       Two mechanisms, deliberately, because they answer two different questions.
       The card is a labelled group and each button names its object, so a user
       exploring the page — or landing on the button after a tap, which is where
       restoreFocus() puts them — can always find out what is in front of them.
       That is durable but passive: it is only heard if something is focused or
       explored. The active half is the live announcement in obDeckSay(), which
       fires on every card change, since the artwork changes underneath a button
       whose focus never moves. Neither alone is sufficient. */
    return `
    <div class="ob-wrap ob-deck">
      <div class="page-kicker">Step 2 of 3 · the deck</div>
      <div class="deck-progress"><i style="width:${(ob.di / 16) * 100}%"></i></div>
      <div class="deck-card" role="group" aria-label="Artwork ${ob.di + 1} of 16 — ${esc(subject)}">
        <img src="${w.image.src}" alt="${esc(subject)}">
        <div class="deck-meta"><b>${esc(w.title)}</b><span>${esc(a.name)} · ${esc(w.year.display)}</span></div>
      </div>
      <div class="deck-actions">
        <button class="aw-btn deck-pass" data-tsx="deck-pass" aria-label="Pass on ${esc(w.title)} by ${esc(a.name)}">Pass</button>
        <button class="aw-btn primary deck-admire" data-tsx="deck-admire" aria-label="Admire ${esc(w.title)} by ${esc(a.name)}">Admire</button>
      </div>
      <p class="chip-label">passing is silence, not a dislike · ${ob.di + 1} of 16</p>
    </div>`;
  }

  if(ob.step === 3){
    const qi = Object.keys(ob.answers).length;
    const Q = TASTE_QUESTIONS[qi];
    return `
    <div class="ob-wrap">
      <div class="page-kicker">Step 3 of 3 · five questions</div>
      <div class="deck-progress"><i style="width:${(qi / 5) * 100}%"></i></div>
      <h1 class="ob-q">${esc(Q.text)}</h1>
      <div class="q-options">${Q.options.map(o => `
        <button class="q-opt" data-tsx="answer" data-tsid="${Q.id}:${o.id}">${esc(o.text)}</button>`).join("")}</div>
      <p class="chip-label">question ${qi + 1} of 5 · single tap, no wrong answers</p>
    </div>`;
  }

  /* step 4 — the reveal (result computed & saved by obFinish) */
  const st = tasteState(), pc = personaCandidates(st), sig = signalWords(st.u);
  const adopted = st.p.persona && st.p.persona.adopted;
  return `
  <div class="ob-wrap ob-reveal">
    <div class="page-kicker">Your first map</div>
    <h1 class="display">${esc(sig.primary)}.</h1>
    <p class="page-lede">Secondary signals: ${esc(sig.secondary)}. This map is <b>${st.tier}</b> — it sharpens with every artwork you admire, anywhere in the atlas.</p>
    <div class="reveal-cols">
      <div>${tasteMapSVG(st)}
        <div class="chips" style="margin-top:10px">${(st.p.palette.tones || []).map(tid => {
          const t = TASTE_TONES.find(o => o.id === tid);
          return t ? `<span class="chip"><i class="tone-dot" style="background:${t.hex}"></i>${esc(t.name)}</span>` : "";
        }).join("")}</div>
      </div>
      <div class="persona-stack">
        <div class="chip-label">Three Persona candidates — adopt one, or decide later</div>
        ${adopted ? personaCard(PERSONAS.find(x => x.id === adopted), { adopted: true })
                  : pc.cands.map(ps => personaCard(ps, { adoptBtn: true })).join("")}
        ${pc.secondary && !adopted ? `<p class="chip-label">Your map shows a second island — ${esc(pc.secondary.name)} lives there.</p>` : ""}
      </div>
    </div>
    <div class="ob-foot">
      <a class="aw-btn primary" href="#/taste">To your taste page ${ARR}</a>
      <button class="aw-btn" data-tsx="card">Download your card</button>
      ${adopted ? "" : `<button class="aw-btn" data-tsx="later">Decide later</button>`}
    </div>
    ${obHandoff(st)}
  </div>`;
}
function obHandoff(st){
  const artists = Object.keys(window.TIER1 || {})
    .map(aid => ({ aid, d: tasteDist(TIER1[aid].coords, st.u) }))
    .sort((a, b) => a.d - b.d).slice(0, 3).map(o => Ax[o.aid]).filter(Boolean);
  const list = (LISTS || []).map(l => {
    const cs = l.works.map(e => coordsOfWork(CatX[e.id])).filter(Boolean);
    if(!cs.length) return null;
    const c = {}; TAXES.forEach(a => c[a] = cs.reduce((s, x) => s + x[a], 0) / cs.length);
    return { l, d: tasteDist(c, st.u) };
  }).filter(Boolean).sort((a, b) => a.d - b.d)[0];
  return `<section class="ob-handoff">
    <h2 class="sec-title">Start here <span class="count">matched to your map</span></h2>
    <div class="mini-cards mu-artists">${artists.map(p => `
      <a class="mini-card" href="#/artist/${p.id}">${canvasTag(p.style, p.palette, p.id, coverLabel(p.name))}<span><span class="mc-name">${esc(p.name)}</span><br><span class="mc-meta">${esc(p.tagline)}</span></span></a>`).join("")}</div>
    ${list ? `<div class="chips" style="margin-top:12px"><a class="chip m" href="#/list/${list.l.id}">List for you: ${esc(list.l.title)}</a></div>` : ""}
  </section>`;
}
function obFinish(){
  const p = ppFull(), now = new Date().toISOString();
  const prior = { F:0, D:0, E:0, C:0, M:0 };
  TASTE_QUESTIONS.forEach(Q => {
    const oid = ob.answers[Q.id];
    const o = Q.options.find(x => x.id === oid);
    if(o) Object.keys(o.nudge).forEach(a => prior[a] += o.nudge[a]);
  });
  TAXES.forEach(a => prior[a] = Math.max(-60, Math.min(60, prior[a])));
  p.quiz = { answers: ob.answers, prior, at: now };
  p.palette = { tones: ob.tones.slice(), source: "chosen" };
  ob.deck.forEach(w => { if(p.deckSeen.indexOf(w.id) < 0) p.deckSeen.push(w.id); });
  ob.skipped.forEach(id => { if(p.skipped.indexOf(id) < 0) p.skipped.push(id); });
  ob.admired.forEach(id => {
    if(!p.admirations.some(e => e.id === id)) p.admirations.push({ id, at: now });
  });
  const st = tasteState(p), pc = personaCandidates(st);
  p.persona = p.persona || { adopted: null, candidates: [], adoptedAt: null, hidden: false };
  p.persona.candidates = pc.cands.map(ps => ps.id);
  p.persona.provisional = st.provisional;
  p.tasteVector = Object.assign({ n: st.n, sd: Math.round(st.meanSd) }, st.u);
  p.clusters = st.split ? st.components.map(c => ({ center: c.center, weight: +c.weight.toFixed(2), n: c.items.length })) : null;
  p.milestones = p.milestones || {};
  p.milestones.onboarded = true;
  p.milestones.confidence = st.tier;
  if(!ppSave(p)) ppNotice("Your answers were not saved. This device would not store the Taste Passport, so the map you just made will be gone when you leave this page. Back it up below, or free some space and take the onboarding again.");
}

/* ---------- the passport card (a painted, shareable PNG) ---------- */
const CARD_STYLES = ["colorfield", "abstract", "gestural", "ornament", "tonal"];
function cardPalette(p, adopted){
  const tones = (p.palette && p.palette.tones || [])
    .map(tid => (window.TASTE_TONES || []).find(t => t.id === tid)).filter(Boolean);
  if(tones.length === 4) return tones.map(t => t.hex);
  if(adopted) return adopted.palette.slice(0, 4);
  return ["#c9a45c", "#3e5570", "#8a3a3e", "#e8e0cc"];
}
async function paintPassportCard(){
  const p = getPassport(); if(!p) return null;
  const st = tasteState(p), sig = signalWords(st.u);
  const adopted = p.persona && p.persona.adopted ? PERSONAS.find(x => x.id === p.persona.adopted) : null;
  const pal = cardPalette(p, adopted);
  const tones = (p.palette && p.palette.tones || [])
    .map(tid => (window.TASTE_TONES || []).find(t => t.id === tid)).filter(Boolean);
  try{ await document.fonts.load('600 100px "Playfair Display"');
       await document.fonts.load('400 34px "Inter"');
       await document.fonts.ready; }catch(e){}

  const W = 1080, H = 1350;
  const cv = document.createElement("canvas"); cv.width = W; cv.height = H;
  const ctx = cv.getContext("2d");

  /* 1 — the cover, painted in the browser with the user's own tones */
  ctx.fillStyle = "#0d0c0a"; ctx.fillRect(0, 0, W, H);
  const styleName = CARD_STYLES[hashStr("card:" + pal.join() + (adopted ? adopted.id : "")) % CARD_STYLES.length];
  const painter = PAINTERS[styleName] || PAINTERS.colorfield;
  try{ painter(ctx, W, H, pal.concat(["#16140f"]), mulberry(hashStr("cover:" + pal.join()))); }catch(e){}
  const shade = ctx.createLinearGradient(0, 0, 0, H);
  shade.addColorStop(0, "rgba(13,12,10,.62)"); shade.addColorStop(.42, "rgba(13,12,10,.78)");
  shade.addColorStop(1, "rgba(13,12,10,.94)");
  ctx.fillStyle = shade; ctx.fillRect(0, 0, W, H);

  const M = 84;                                   /* margin */
  const gold = "#c9a45c", gold2 = "#e8c98a", ink = "#ece6d9", muted = "#b0a890";
  const serif = '"Playfair Display", Georgia, serif', sans = '"Inter", system-ui, sans-serif';

  /* 2 — brand row */
  ctx.fillStyle = gold;
  ctx.beginPath(); ctx.arc(M + 14, 120, 14, 0, 7); ctx.fill();
  ctx.fillStyle = ink; ctx.font = '800 46px ' + serif;
  ctx.textBaseline = "middle"; ctx.textAlign = "left";
  ctx.fillText("P I G M E N T", M + 48, 120);
  ctx.font = '500 24px ' + sans; ctx.fillStyle = muted; ctx.textAlign = "right";
  ctx.fillText("T A S T E   P A S S P O R T", W - M, 120);
  ctx.strokeStyle = "rgba(201,164,92,.4)"; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(M, 170); ctx.lineTo(W - M, 170); ctx.stroke();

  /* 3 — persona / position */
  ctx.textAlign = "left";
  ctx.fillStyle = gold; ctx.font = '500 26px ' + sans;
  ctx.fillText((adopted ? "PERSONA" : "POSITION") + "  ·  " + st.tier.toUpperCase() + " MAP", M, 240);
  const title = adopted ? adopted.name : sig.primary;
  ctx.fillStyle = ink;
  let fs = 96; ctx.font = '600 ' + fs + 'px ' + serif;
  while(ctx.measureText(title).width > W - 2 * M && fs > 54){ fs -= 4; ctx.font = '600 ' + fs + 'px ' + serif; }
  ctx.fillText(title, M, 320);
  /* wrapped sub-line */
  const sub = adopted ? adopted.blurb : ("Secondary signals: " + sig.secondary + ".");
  ctx.font = '400 33px ' + sans; ctx.fillStyle = muted;
  const words = sub.split(" "); let line = "", ly = 402;
  for(const w of words){
    if(ctx.measureText(line + w).width > W - 2 * M){ ctx.fillText(line.trim(), M, ly); ly += 46; line = ""; if(ly > 402 + 2 * 46) break; }
    line += w + " ";
  }
  if(line.trim() && ly <= 402 + 2 * 46) ctx.fillText(line.trim(), M, ly);

  /* 4 — palette swatches */
  let sy = 560;
  pal.forEach((hex, i) => {
    const sx = M + i * 118;
    ctx.fillStyle = hex;
    ctx.beginPath(); ctx.roundRect(sx, sy, 92, 92, 18); ctx.fill();
    ctx.strokeStyle = "rgba(236,230,217,.25)"; ctx.stroke();
  });
  ctx.font = '400 24px ' + sans; ctx.fillStyle = muted;
  ctx.fillText(tones.length === 4 ? tones.map(t => t.name).join("  ·  ") : "the palette of your persona", M, sy + 134);

  /* 5 — the map */
  const mp = { x: M, y: 760, s: 470 };
  ctx.fillStyle = "rgba(22,20,15,.72)";
  ctx.beginPath(); ctx.roundRect(mp.x, mp.y, mp.s, mp.s, 22); ctx.fill();
  ctx.strokeStyle = "rgba(201,164,92,.35)"; ctx.stroke();
  const pad = 42;
  const px = v => mp.x + pad + (v + 100) / 200 * (mp.s - 2 * pad);
  const py = v => mp.y + mp.s - pad - (v + 100) / 200 * (mp.s - 2 * pad);
  ctx.strokeStyle = "rgba(201,164,92,.28)";
  ctx.beginPath(); ctx.moveTo(px(0), mp.y + pad); ctx.lineTo(px(0), mp.y + mp.s - pad); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(mp.x + pad, py(0)); ctx.lineTo(mp.x + mp.s - pad, py(0)); ctx.stroke();
  ctx.font = '500 20px ' + sans; ctx.fillStyle = "rgba(176,168,144,.85)";
  ctx.textAlign = "left";  ctx.fillText("FIGURATIVE", mp.x + pad, py(0) - 14);
  ctx.textAlign = "right"; ctx.fillText("ABSTRACT", mp.x + mp.s - pad, py(0) - 14);
  ctx.textAlign = "left";  ctx.fillText("DRAMATIC", px(0) + 12, mp.y + pad + 10);
  ctx.fillText("CALM", px(0) + 12, mp.y + mp.s - pad - 10);
  st.items.forEach(it => {
    ctx.fillStyle = "rgba(111,179,168,.75)";
    ctx.beginPath(); ctx.arc(px(it.x.F), py(it.x.D), 7, 0, 7); ctx.fill();
  });
  st.components.forEach((c, i) => {
    ctx.fillStyle = i ? "#c97b6a" : gold;
    ctx.strokeStyle = "#0d0c0a"; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.arc(px(c.center.F), py(c.center.D), i ? 14 : 18, 0, 7); ctx.fill(); ctx.stroke();
  });

  /* 6 — stats beside the map */
  const rx = mp.x + mp.s + 56;
  ctx.textAlign = "left"; ctx.fillStyle = ink;
  const stats = [
    [String(st.n), "admiration" + (st.n === 1 ? "" : "s")],
    [String((p.seen || []).length), "seen in person"],
    [st.split ? "2" : "1", st.split ? "taste islands" : "taste island"]
  ];
  let ty = mp.y + 40;
  stats.forEach(([num, lab]) => {
    ctx.font = '600 64px ' + serif; ctx.fillStyle = gold2; ctx.fillText(num, rx, ty);
    ctx.font = '400 26px ' + sans; ctx.fillStyle = muted; ctx.fillText(lab, rx, ty + 42);
    ty += 132;
  });
  ctx.font = '400 24px ' + sans; ctx.fillStyle = muted;
  ctx.fillText(new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }), rx, mp.y + mp.s - 18);

  /* 7 — footer */
  ctx.strokeStyle = "rgba(201,164,92,.4)";
  ctx.beginPath(); ctx.moveTo(M, H - 118); ctx.lineTo(W - M, H - 118); ctx.stroke();
  ctx.font = 'italic 30px ' + serif; ctx.fillStyle = ink;
  ctx.fillText("Find your place in the history of art.", M, H - 66);
  ctx.font = '400 24px ' + sans; ctx.fillStyle = muted; ctx.textAlign = "right";
  ctx.fillText("ardagemci.github.io/painters-atlas", W - M, H - 66);
  ctx.textAlign = "left";
  return cv;
}
function drawCardPreview(){
  const holder = document.getElementById("pp-card-prev");
  if(!holder) return;
  paintPassportCard().then(cv => {
    if(!cv || !document.getElementById("pp-card-prev")) return;
    cv.className = "pp-card-canvas";
    holder.innerHTML = ""; holder.appendChild(cv);
  });
}

/* ---------- storage cannot be read: say which case it is, keep the data, offer a way out ---------- */
function ppTroubleView(){
  const denied = ppState.read === "denied";
  return `
  <div class="ob-wrap">
    <div class="page-kicker">The Taste Passport · this device's storage</div>
    <h1 class="display">${denied ? "This browser will not let Pigment read its storage." : "Something is stored here, and it cannot be read."}</h1>
    <p class="page-lede">${denied
      ? "Local storage is blocked for this site — private browsing or a site-data setting will do that. Pigment cannot read or write your Taste Passport on this device until it is available again. Nothing has been deleted. Admire, Seen in person and Saved for later will not stick in the meantime."
      : `The data saved under <code>${PASSPORT_KEY}</code> on this device is not readable as a Taste Passport. Pigment has not changed it and will not write over it. Download it first if you want a copy; replacing it is your choice, not ours.`}</p>
    <div class="chips" style="margin-top:16px">
      <button class="chip" data-tsx="storage-retry">Try reading it again</button>
      ${denied ? "" : `<button class="chip" data-tsx="export">Download the stored data</button>
      <button class="chip" data-tsx="storage-reset">Replace it with a new Passport</button>`}
      <a class="chip" href="#/">Back to the atlas</a>
    </div>
    <p class="chip-label" id="taste-msg"></p>
  </div>`;
}

/* ---------- the taste page (#/taste) ---------- */
function viewTaste(){
  document.title = "Your taste — Pigment";
  requestAnimationFrame(drawCardPreview);
  const p = getPassport();
  if(ppState.corrupt || ppState.read === "denied") return ppTroubleView();
  if(!p || (!p.admirations.length && !(p.milestones && p.milestones.onboarded))) return `
    <div class="ob-wrap">
      <div class="page-kicker">The Taste Passport</div>
      <h1 class="display">No map yet — let's sketch one.</h1>
      <p class="page-lede">Admire artworks anywhere in the atlas and your Taste Passport records them locally, on this device. Or take the four-minute onboarding and get a provisional Persona right now.</p>
      <a class="aw-btn primary ob-cta" href="#/palette">Find your palette ${ARR}</a>
    </div>`;
  const st = tasteState(p), pc = personaCandidates(st), sig = signalWords(st.u);
  const adopted = p.persona && p.persona.adopted ? PERSONAS.find(x => x.id === p.persona.adopted) : null;
  const disc = discoveryBatch(st);
  const admiredWorks = (p.admirations || []).map(e => CatX[e.id]).filter(Boolean);
  return `
  <div class="page-head">
    <div class="page-kicker">The Taste Passport · stored on this device</div>
    <h1 class="display">${adopted ? esc(adopted.name) : esc(sig.primary)}</h1>
    <p class="page-lede">Position: <b>${esc(sig.primary)}</b> · secondary signals: ${esc(sig.secondary)} · map is <b>${st.tier}</b>${st.provisional && st.tier !== "provisional" ? " (provisional)" : ""} · ${st.n} admiration${st.n === 1 ? "" : "s"} inform it.</p>
  </div>
  <div class="reveal-cols">
    <div>
      ${tasteMapSVG(st)}
      ${st.split ? `<p class="chip-label">Two islands on your map — ${Math.round(st.components[0].weight * 100)}% and ${Math.round(st.components[1].weight * 100)}% of you.</p>` : ""}
      ${p.palette && p.palette.tones ? `<div class="chips" style="margin-top:10px">${p.palette.tones.map(tid => {
        const t = TASTE_TONES.find(o => o.id === tid);
        return t ? `<span class="chip"><i class="tone-dot" style="background:${t.hex}"></i>${esc(t.name)}</span>` : "";
      }).join("")}</div>` : ""}
      <div class="chips" style="margin-top:14px">
        <button class="chip" data-tsx="share-url">Copy share link</button>
        <a class="chip" href="#/palette" data-tsx="retake">Retake onboarding</a>
        <button class="chip" data-tsx="export">Back up data (.json)</button>
        <button class="chip" data-tsx="reset">Reset everything</button>
      </div>
      <p class="chip-label" id="taste-msg"></p>
    </div>
    <div class="persona-stack">
      ${adopted ? personaCard(adopted, { adopted: true }) + (pc.secondary ? `<p class="chip-label">Second island persona: ${esc(pc.secondary.name)}</p>` : "")
                : `<div class="chip-label">Persona candidates</div>` + pc.cands.map(ps => personaCard(ps, { adoptBtn: true })).join("")}
    </div>
  </div>
  <section>
    <h2 class="sec-title">Your passport card <span class="count">painted in the browser with your own tones</span></h2>
    <div class="pp-card-row">
      <div id="pp-card-prev" class="pp-card-prev"><div class="pp-card-loading">mixing pigment…</div></div>
      <div class="pp-card-side">
        <p>A card, not a spreadsheet: your Persona, your palette and your position on the map, over a cover painted live from your four tones. Download it, send it, print it — your eye, portable.</p>
        <button class="aw-btn primary" data-tsx="card">Download the card</button>
        <p class="chip-label" style="margin-top:10px">PNG · 1080 × 1350 · repaints as your taste sharpens</p>
      </div>
    </div>
  </section>
  ${disc.length ? `<section>
    <h2 class="sec-title">Discovery rings <span class="count">picked for your map — admire to refine it</span></h2>
    <div class="cards">${disc.map(o => artworkCard(o.w)).join("")}</div>
    <p class="chip-label">${disc.map(o => RING_LABELS[o.ring]).filter((v, i, a) => a.indexOf(v) === i).join(" · ")}</p>
  </section>` : ""}
  ${admiredWorks.length ? `<section>
    <h2 class="sec-title">Your admirations <span class="count">${admiredWorks.length}</span></h2>
    <div class="cards">${admiredWorks.slice().reverse().slice(0, 12).map(artworkCard).join("")}</div>
  </section>` : ""}`;
}

/* ---------- passport export / import ---------- */
function passportPayload(){
  const json = JSON.stringify(getPassport() || newPassport());
  return btoa(unescape(encodeURIComponent(json))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
function decodePayload(s){
  try{
    s = s.replace(/-/g, "+").replace(/_/g, "/");
    while(s.length % 4) s += "=";
    return JSON.parse(decodeURIComponent(escape(atob(s))));
  }catch(e){ return null; }
}
/* The list fields below combine by union. These four do not: each is a single value,
   so an import can only ever REPLACE one — and PIGMENT.md §9 forbids doing that silently.
   Nothing here is written until the user has chosen, field by field. */
const PP_CHOICE_FIELDS = ["quiz", "palette", "persona", "milestones"];
const PP_FIELD_LABELS = {
  quiz: "Onboarding answers", palette: "Chosen tones",
  persona: "Adopted Persona", milestones: "Progress markers"
};
/* the decision each field actually carries — an empty shell from newPassport() is not a decision */
function ppFieldKey(field, v){
  if(!v) return "";
  if(field === "persona")    return String(v.adopted || "");
  if(field === "palette")    return (v.tones || []).join(",");
  if(field === "milestones") return v.onboarded ? JSON.stringify([!!v.onboarded, v.confidence || ""]) : "";
  return Object.keys(v.answers || {}).length ? JSON.stringify(v.answers) : "";   /* quiz */
}

function ppFieldSummary(field, v){
  if(!v) return "nothing saved";
  if(field === "quiz") return `${Object.keys(v.answers || {}).length} answers${v.at ? " · saved " + String(v.at).slice(0, 10) : ""}`;
  if(field === "palette"){
    const names = (v.tones || []).map(tid => { const t = TASTE_TONES.find(o => o.id === tid); return t ? t.name : tid; });
    return names.length ? names.join(", ") : "no tones";
  }
  if(field === "persona"){
    if(!v.adopted) return "none adopted";
    const ps = PERSONAS.find(x => x.id === v.adopted);
    return (ps ? ps.name : v.adopted) + (v.adoptedAt ? " · adopted " + String(v.adoptedAt).slice(0, 10) : "");
  }
  if(field === "milestones") return `onboarding ${v.onboarded ? "finished" : "not finished"} · map ${esc(v.confidence || "unknown")}`;
  return "saved";
}

/* which single-value fields would an import overwrite? */
function passportConflicts(mine, theirs){
  if(!mine || !theirs) return [];
  return PP_CHOICE_FIELDS.filter(f => {
    const a = ppFieldKey(f, mine[f]), b = ppFieldKey(f, theirs[f]);
    return a && b && a !== b;
  });
}

/* pure: `mine` is cloned, never mutated, so an abandoned merge cannot leak into local state */
function mergePassports(mine, theirs, choices){
  choices = choices || {};
  const out = mine ? JSON.parse(JSON.stringify(mine)) : newPassport();
  ["admirations", "seen", "wantToSee", "saved", "probes"].forEach(f => {
    const seen = {};
    (out[f] || []).forEach(e => seen[e.id] = e);
    (theirs[f] || []).forEach(e => {
      if(!seen[e.id] || (e.at && seen[e.id].at && e.at < seen[e.id].at)) seen[e.id] = e;
    });
    out[f] = Object.values(seen);
  });
  ["skipped", "deckSeen", "notForMe"].forEach(f => {
    out[f] = Array.from(new Set((out[f] || []).concat(theirs[f] || [])));
  });
  PP_CHOICE_FIELDS.forEach(f => {
    const a = ppFieldKey(f, out[f]), b = ppFieldKey(f, theirs[f]);
    if(!b) return;                                           /* nothing offered */
    const take = () => { out[f] = JSON.parse(JSON.stringify(theirs[f])); };
    if(!a){ take(); return; }                                /* nothing of ours to lose */
    if(a === b) return;                                      /* same decision — no choice to make */
    if(choices[f] === "theirs") take();                      /* replaced only on an explicit choice */
  });
  return out;
}

let ppImport = null;                                         /* { payload, data, choices, step } */

function viewPassportImport(payload){
  document.title = "Import passport — Pigment";
  const data = decodePayload(payload || "");
  if(!data || data.version !== 1){
    ppImport = null;
    return `
    <div class="ob-wrap"><h1 class="display">That passport didn't scan.</h1>
    <p class="page-lede">The link seems damaged. Nothing on this device has been changed. Ask for a fresh one, or start your own map.</p>
    <a class="aw-btn primary" href="#/palette">Find your palette ${ARR}</a>
    <a class="chip-label" style="display:block;margin-top:14px" href="#/">no thanks — take me home</a></div>`;
  }
  if(!ppImport || ppImport.payload !== payload) ppImport = { payload, data, choices: {}, step: 1 };
  ppImport.data = data;
  const mine = getPassport();
  const conflicts = passportConflicts(mine, data);
  conflicts.forEach(f => { if(!ppImport.choices[f]) ppImport.choices[f] = "mine"; });   /* default keeps yours */

  if(ppImport.step === 2 && conflicts.length) return `
  <div class="ob-wrap">
    <div class="page-kicker">Taste Passport · import · ${conflicts.length} choice${conflicts.length === 1 ? "" : "s"}</div>
    <h1 class="display">Which of these should Pigment keep?</h1>
    <p class="page-lede">These are single values, not lists, so they cannot be combined — one of the two has to win. Yours is selected. Nothing is written until you press Merge below, and nothing at all is written if you cancel.</p>
    <div class="pp-conflicts">${conflicts.map(f => `
      <div class="panel">
        <h3>${esc(PP_FIELD_LABELS[f])}</h3>
        <div class="pp-choice">
          <button class="f-btn ${ppImport.choices[f] === "mine" ? "on" : ""}" data-tsx="ppc" data-tsid="${f}:mine" aria-pressed="${ppImport.choices[f] === "mine"}">Keep mine — ${esc(ppFieldSummary(f, mine[f]))}</button>
          <button class="f-btn ${ppImport.choices[f] === "theirs" ? "on" : ""}" data-tsx="ppc" data-tsid="${f}:theirs" aria-pressed="${ppImport.choices[f] === "theirs"}">Take theirs — ${esc(ppFieldSummary(f, data[f]))}</button>
        </div>
      </div>`).join("")}</div>
    <button class="aw-btn primary ob-cta" data-tsx="import">Merge with these choices</button>
    <button class="chip" style="margin-left:10px" data-tsx="import-cancel">Cancel — change nothing</button>
  </div>`;

  const combined = ["admirations", "seen", "wantToSee", "saved", "probes"]
    .reduce((n, f) => n + (data[f] || []).length, 0);
  return `
  <div class="ob-wrap">
    <div class="page-kicker">Taste Passport · import</div>
    <h1 class="display">A passport arrived.</h1>
    <p class="page-lede">${(data.admirations || []).length} admirations · ${(data.seen || []).length} seen in person ·
      persona: ${data.persona && data.persona.adopted ? esc((PERSONAS.find(x => x.id === data.persona.adopted) || {}).name || data.persona.adopted) : "none adopted"}.</p>
    <p class="page-lede">Admirations, works seen in person, saved works, probes and skipped works are <b>combined</b> — all ${combined} entries in this passport are added to yours and none of yours is removed. ${conflicts.length
      ? `Four settings cannot be combined because each holds a single value, and <b>${conflicts.length} of them differ</b> from yours: ${conflicts.map(f => esc(PP_FIELD_LABELS[f].toLowerCase())).join(", ")}. You choose which to keep on the next screen. Nothing is written until then.`
      : `The four single-value settings — onboarding answers, chosen tones, adopted Persona and progress markers — either match yours or are missing from one side, so nothing of yours will be replaced.`}</p>
    ${conflicts.length
      ? `<button class="aw-btn primary ob-cta" data-tsx="import-review">Choose what to keep ${ARR}</button>`
      : `<button class="aw-btn primary ob-cta" data-tsx="import">Merge into my passport</button>`}
    <a class="chip-label" style="display:block;margin-top:14px" href="#/">no thanks — take me home</a>
  </div>`;
}

/* ---------- interactions ---------- */
document.addEventListener("click", e => {
  const el = e.target.closest("[data-tsx]");
  if(!el) return;
  const act = el.dataset.tsx, id = el.dataset.tsid;
  if(act === "start"){ obStart(); route(); }
  else if(act === "tone"){
    const i = ob.tones.indexOf(id);
    if(i >= 0) ob.tones.splice(i, 1);
    else if(ob.tones.length < 4) ob.tones.push(id);
    obWrite();
    route();
  }
  else if(act === "tones-done"){ if(ob.tones.length === 4){ ob.step = 2; obWrite(); route(); obDeckSay(); } }
  else if(act === "deck-admire" || act === "deck-pass"){
    const w = ob.deck[ob.di];
    (act === "deck-admire" ? ob.admired : ob.skipped).push(w.id);
    ob.di++;
    if(ob.di >= 16) ob.step = 3;
    obWrite();
    route();
    obDeckSay();                                           /* AT-1 — name the next artwork */
  }
  else if(act === "answer"){
    const [qid, oid] = id.split(":");
    ob.answers[qid] = oid;
    if(Object.keys(ob.answers).length >= 5){ ob.step = 4; obFinish(); }
    obWrite();
    route();
  }
  else if(act === "adopt"){
    const p = ppFull();
    p.persona = p.persona || {};
    p.persona.adopted = id;
    p.persona.adoptedAt = new Date().toISOString();
    if(!ppSave(p)) ppNotice("Persona not adopted. This device would not store the change, so your Taste Passport is unchanged.");
    else if(ob){ ob.adopted = true; obWrite(); }
    route();
  }
  else if(act === "later"){ location.hash = "#/taste"; }
  else if(act === "retake"){
    /* a real link, and a real consequence: say so, and let cancel mean cancel */
    if(!confirm("Take the onboarding again? You'll choose four tones, sixteen works and five questions from scratch, and finishing replaces the tones and answers behind your current map. Anything you had part-way through is discarded. Your admirations are kept.")){
      e.preventDefault();
      return;
    }
    obClear();
    if(location.hash.replace(/^#\/?/, "").split("/")[0] === "palette") route();
  }
  else if(act === "card"){
    el.disabled = true;
    paintPassportCard().then(cv => {
      el.disabled = false;
      if(!cv) return;
      cv.toBlob(b => {
        const a = document.createElement("a");
        a.href = URL.createObjectURL(b);
        a.download = "pigment-taste-card.png";
        a.click();
        setTimeout(() => URL.revokeObjectURL(a.href), 5000);
        const m = document.getElementById("taste-msg");
        if(m) m.textContent = "Card downloaded — your eye, portable.";
      }, "image/png");
    });
  }
  else if(act === "export"){
    const p = getPassport();
    /* if it could not be parsed, back up the raw bytes rather than exporting "null" */
    const text = p ? JSON.stringify(p, null, 1) : (ppRaw() || "");
    if(!text){ ppNotice("There is nothing stored on this device to back up yet."); return; }
    const a = document.createElement("a");
    a.href = "data:application/json;charset=utf-8," + encodeURIComponent(text);
    a.download = p ? "pigment-passport.json" : "pigment-passport-unreadable.json";
    a.click();
  }
  else if(act === "notice-close"){
    const el = document.getElementById("pp-notice");
    if(el) el.hidden = true;
  }
  else if(act === "storage-retry"){
    ppState.read = "ok"; ppState.write = "ok"; ppState.corrupt = false;
    route();
  }
  else if(act === "storage-reset"){
    if(confirm("Replace the unreadable data on this device with a new, empty Taste Passport? Download it first if you want a copy — this cannot be undone.")){
      let gone = true;
      try{ localStorage.removeItem(PASSPORT_KEY); }catch(err){ gone = false; }
      if(!gone){ ppNotice("Not replaced. This browser would not let Pigment clear its storage, so the existing data is still there."); return; }
      ppState.read = "ok"; ppState.write = "ok"; ppState.corrupt = false;
      obClear(); route();
    }
  }
  else if(act === "share-url"){
    const url = location.href.split("#")[0] + "#/passport/" + passportPayload();
    (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(
      () => { const m = document.getElementById("taste-msg"); if(m) m.textContent = "Share link copied — your eye, portable."; },
      () => { const m = document.getElementById("taste-msg"); if(m) m.textContent = url; });
  }
  else if(act === "reset"){
    if(confirm("Erase your Taste Passport from this device? Export it first if you want a copy.")){
      let gone = true;
      try{ localStorage.removeItem(PASSPORT_KEY); }catch(err){ gone = false; }
      if(!gone){ ppNotice("Not erased. This browser would not let Pigment clear its storage, so your Taste Passport is still on this device."); return; }
      ppState.read = "ok"; ppState.write = "ok"; ppState.corrupt = false;
      obClear(); route();
    }
  }
  else if(act === "import-review"){
    if(ppImport){ ppImport.step = 2; route(); }             /* no write on this path */
  }
  else if(act === "ppc"){                                    /* per-field choice: keep mine / take theirs */
    const [field, which] = String(id).split(":");
    if(ppImport && PP_CHOICE_FIELDS.indexOf(field) >= 0 && (which === "mine" || which === "theirs")){
      ppImport.choices[field] = which;
      route();                                               /* no write on this path either */
    }
  }
  else if(act === "import-cancel"){
    ppImport = null;                                         /* nothing was ever written */
    /* AT-6 — the cancel is functionally perfect (the stored passport is
       byte-identical afterwards, proven by instrumentation) and said nothing.
       For a sighted user the redirect is a cue; for a screen-reader user,
       backing out of something that threatened to overwrite their identity
       produced silence and a change of place. The one sentence they need is the
       one the damaged-passport screen already says, in the voice this build
       already ships: "Nothing on this device has been changed." */
    sayNext("Import cancelled. Nothing on this device has been changed. You are back on the Pigment home page.");
    location.hash = "#/";
  }
  else if(act === "import"){
    if(!ppImport) return;
    const mine = getPassport();
    if(ppState.corrupt || ppState.read === "denied"){
      ppNotice("Not merged. Pigment cannot read the Taste Passport already on this device, so it will not write over it. Open the Taste Passport to deal with that first.");
      return;
    }
    /* AT-7 — read the outcome BEFORE the merge, while `mine` is still mine, so
       the report is of what was decided rather than of what is now stored. */
    const conflicts = passportConflicts(mine, ppImport.data);
    const choices = ppImport.choices || {};
    const added = ["admirations", "seen", "wantToSee", "saved", "probes"]
      .reduce((n, f) => n + (ppImport.data[f] || []).length, 0);
    const merged = mergePassports(mine, ppImport.data, ppImport.choices);
    if(!ppSave(merged)){ ppNotice(PP_WRITE_MSG); return; }    /* failed write leaves local storage untouched */
    ppImport = null;
    /* the destination names a persona and stops; nothing said which choice won,
       so the user had to infer the result of a decision they were explicitly
       asked to make. Say it, field by field, and put it on the page too. */
    sayNext(conflicts.length
      ? `Passport merged. ${added} entries added. ${conflicts.map(f =>
          `${PP_FIELD_LABELS[f]}: ${choices[f] === "theirs" ? "theirs taken" : "yours kept"}`).join(" · ")}.`
      : `Passport merged. ${added} entries added, and nothing of yours was replaced.`);
    location.hash = "#/taste";
  }
});

/* ---------- share buttons (copy the crawlable stub URLs — tools/build_seo.jxa.js) ---------- */
const STUB_BASE = "https://ardagemci.github.io/painters-atlas/";
function shareChip(path){
  return `<button class="chip" data-share="${path}">Share this page</button>`;
}
document.addEventListener("click", e => {
  const el = e.target.closest("[data-share]");
  if(!el) return;
  const url = STUB_BASE + el.dataset.share;
  (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(
    () => { const t = el.textContent; el.textContent = "Link copied ✓"; setTimeout(() => { el.textContent = t; }, 1600); },
    () => { prompt("Copy this link:", url); });
});

/* go */
route();
})();
