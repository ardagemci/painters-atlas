/* Pigment Phase 1.5 — onboarding data + Persona prototypes.
   ALL PERSONA NAMES ARE PLACEHOLDERS pending Arda's pass (ADMIRE_SPEC §8);
   prototype vectors are name-independent. Coords scale −100…+100 (TASTE_MATH §1). */

/* ~20 art-named tones. Nudges are whisper-weight priors (ADMIRE_SPEC §6.1):
   ±8 on the −100…100 scale — a quarter of a quiz nudge, folded into q before capping. */
window.TASTE_TONES = [
  { id:"caravaggio-black", name:"Caravaggio Black", hex:"#16120e", nudge:{ D:8 } },
  { id:"ultramarine",      name:"Ultramarine",      hex:"#274b9f", nudge:{} },
  { id:"icon-gold",        name:"Icon Gold",        hex:"#c9a45c", nudge:{ E:-8 } },
  { id:"monet-fog",        name:"Monet Fog",        hex:"#c3d2d4", nudge:{ D:-8, C:-8 } },
  { id:"venetian-red",     name:"Venetian Red",     hex:"#8a3a3e", nudge:{ D:8 } },
  { id:"prussian-blue",    name:"Prussian Blue",    hex:"#1d3a4e", nudge:{ D:8 } },
  { id:"verdigris",        name:"Verdigris",        hex:"#4a8a7a", nudge:{} },
  { id:"dried-rose",       name:"Dried Rose",       hex:"#c98f96", nudge:{ D:-8, C:-8 } },
  { id:"bone-white",       name:"Bone White",       hex:"#e8e0cc", nudge:{ D:-8 } },
  { id:"lamp-smoke",       name:"Lamp Smoke",       hex:"#4a4540", nudge:{ D:8 } },
  { id:"alizarin",         name:"Alizarin Crimson", hex:"#a12b3a", nudge:{ D:8 } },
  { id:"raw-ochre",        name:"Raw Ochre",        hex:"#c98a3a", nudge:{ E:-8 } },
  { id:"viridian",         name:"Viridian",         hex:"#2e7a5e", nudge:{} },
  { id:"cobalt-turquoise", name:"Cobalt Turquoise", hex:"#3aa8b8", nudge:{ C:-8 } },
  { id:"rose-madder",      name:"Rose Madder",      hex:"#d9899e", nudge:{ D:-8, C:-8 } },
  { id:"malachite",        name:"Malachite",        hex:"#3e8a4a", nudge:{} },
  { id:"midnight-indigo",  name:"Midnight Indigo",  hex:"#2a2a4e", nudge:{ D:8 } },
  { id:"chalk-pastel",     name:"Chalk Pastel",     hex:"#e0cfe0", nudge:{ D:-8, C:-8 } },
  { id:"burnt-sienna",     name:"Burnt Sienna",     hex:"#96482b", nudge:{ E:-8 } },
  { id:"mica-silver",      name:"Mica Silver",      hex:"#b8bcc4", nudge:{ C:8 } }
];

/* The launch five (ADMIRE_SPEC §6.3): nudges ±30, soft ±15, 1–2 axes; prior capped ±60/axis. */
window.TASTE_QUESTIONS = [
  { id:"q1", text:"Should art require visible skill?",
    options:[
      { id:"a", text:"Mastery you can see", nudge:{ E:-30 } },
      { id:"b", text:"The idea can matter more", nudge:{ E:30, C:30 } },
      { id:"c", text:"Emotional force beats both", nudge:{ D:30 } },
      { id:"d", text:"Skill exists to be challenged", nudge:{ E:30 } }] },
  { id:"q2", text:"Does art need meaning?",
    options:[
      { id:"a", text:"Depth and symbols, please", nudge:{ C:30 } },
      { id:"b", text:"Beauty is enough", nudge:{ C:-30 } },
      { id:"c", text:"Meaning shows up later, on its own", nudge:{ C:15 } },
      { id:"d", text:"The best art refuses to explain itself", nudge:{ C:30, E:30 } }] },
  { id:"q3", text:"Should a picture comfort you or disturb you?",
    options:[
      { id:"a", text:"Comfort — the world is loud enough", nudge:{ D:-30 } },
      { id:"b", text:"Disturb me. That's what it's for", nudge:{ D:30 } },
      { id:"c", text:"Both at once, ideally", nudge:{ D:15 } },
      { id:"d", text:"Neither — make me notice things", nudge:{ C:30 } }] },
  { id:"q4", text:"Should art explain the world or escape it?",
    options:[
      { id:"a", text:"Explain it — art is a lens", nudge:{ F:-30, C:30 } },
      { id:"b", text:"Escape it — art is a door", nudge:{ C:-30, D:-30 } },
      { id:"c", text:"Transform it", nudge:{ E:30 } },
      { id:"d", text:"Tear it down and rebuild it", nudge:{ E:30, D:30 } }] },
  { id:"q5", text:"Should art be beautiful?",
    options:[
      { id:"a", text:"Deeply, unapologetically", nudge:{ C:-30 } },
      { id:"b", text:"Not necessarily", nudge:{ C:15 } },
      { id:"c", text:"Strange beauty. Ugly beauty", nudge:{ D:30 } },
      { id:"d", text:"I distrust easy beauty", nudge:{ C:30, E:30 } }] }
];

/* Persona prototypes. kind:"specific" → prototype coords + optional signature
   { movement: id, min: n } or { tag: t, min: n }. kind:"general" → rule fired by
   cloud shape (TASTE_MATH §5): "eclectic" | "time-traveler" | "contradiction". */
window.PERSONAS = [
  { id:"dutch-interior-goblin", kind:"specific", name:"Dutch Interior Goblin",
    coords:{ F:-80, D:-50, E:-40, C:-40, M:-80 },
    sig:{ movement:"dutch-golden-age", min:2 },
    palette:["#e8e0cc","#8a6e46","#3e5570","#1d1c22"],
    blurb:"You live for bread crusts, brass pitchers and light through a left-hand window. The quieter the room, the louder you feel it." },
  { id:"candlelight-conspirator", kind:"specific", name:"Candlelight Conspirator",
    coords:{ F:-85, D:80, E:-30, C:-15, M:20 },
    sig:{ movement:"baroque", min:2 },
    palette:["#16120e","#c98a3a","#8a3a3e","#e8d9c0"],
    blurb:"One lantern, deep shadow, somebody about to make a terrible decision. You'd have thrived in seventeenth-century Rome — briefly." },
  { id:"gilded-sentimentalist", kind:"specific", name:"Gilded Sentimentalist",
    coords:{ F:-45, D:5, E:30, C:-35, M:-10 },
    sig:{ tag:"golden", min:2 },
    palette:["#c9a45c","#e8c98a","#8a3a3e","#2a2a4e"],
    blurb:"You believe ornament is honesty and gold leaf is a feeling. Vienna, 1907, would like your address." },
  { id:"storm-chaser", kind:"specific", name:"Storm Chaser",
    coords:{ F:-55, D:80, E:45, C:-10, M:45 },
    palette:["#5e6e8a","#e8944a","#1d3a4e","#dce8f0"],
    blurb:"Shipwrecks, avalanches, skies with opinions. You take the sublime with both hands and no umbrella." },
  { id:"keeper-of-quiet-rooms", kind:"specific", name:"Keeper of Quiet Rooms",
    coords:{ F:-75, D:-55, E:10, C:-45, M:-60 },
    palette:["#c3d2d4","#8a8a7a","#4a4540","#e8e0cc"],
    blurb:"Grey doors, empty chairs, dust in a sunbeam. You know stillness is not the absence of drama but its distillation." },
  { id:"geometry-mystic", kind:"specific", name:"Geometry Mystic",
    coords:{ F:85, D:-10, E:80, C:45, M:10 },
    palette:["#274b9f","#c9a45c","#e8e0cc","#a12b3a"],
    blurb:"Circles that mean something. Grids with a pulse. You suspect the universe has a diagram, and you intend to admire it." },
  { id:"hurricane-of-paint", kind:"specific", name:"Hurricane of Paint",
    coords:{ F:70, D:70, E:75, C:-20, M:35 },
    palette:["#1d1c22","#c23a3a","#e8dcc8","#3e7a8a"],
    blurb:"You want to see the wrist move. Drips, slashes, weather made of pigment — painting as an event, not an object." },
  { id:"boulevard-correspondent", kind:"specific", name:"Boulevard Correspondent",
    coords:{ F:-70, D:15, E:55, C:25, M:-25 },
    sig:{ movement:"impressionism", min:2 },
    palette:["#4a4540","#c3d2d4","#8a3a3e","#c9a45c"],
    blurb:"Cafés, railways, gaslight, glances. You read cities the way other people read novels, and you file your reports from the corner table." },
  { id:"sun-drunk-colorist", kind:"specific", name:"Sun-Drunk Colorist",
    coords:{ F:-45, D:-15, E:50, C:-65, M:-5 },
    palette:["#e8944a","#3aa8b8","#d9899e","#8a9a5e"],
    blurb:"Color is not a description; it's a climate. You'd trade correctness for one violet shadow, every time." },
  { id:"keeper-of-myths", kind:"specific", name:"Keeper of Myths",
    coords:{ F:-70, D:25, E:-15, C:30, M:55 },
    palette:["#c9a45c","#3e5570","#8a3a3e","#e8d9c0"],
    blurb:"Gods, floods, annunciations, allegories with footnotes. You like your walls big and your stories older than the paint." },
  { id:"floating-world-pilgrim", kind:"specific", name:"Floating-World Pilgrim",
    coords:{ F:-35, D:-25, E:20, C:-30, M:-20 },
    sig:{ movement:"ukiyo-e", min:2 },
    palette:["#274b9f","#e8d9c0","#8a3a3e","#4a8a7a"],
    blurb:"A wave, a bridge, rain drawn as lines. You believe the whole world fits on a sheet of mulberry paper, and you're mostly right." },
  { id:"dark-mirror", kind:"specific", name:"Dark Mirror",
    coords:{ F:-50, D:65, E:55, C:30, M:-30 },
    palette:["#2a2a4e","#c23a3a","#4a4540","#c3d2d4"],
    blurb:"Anxiety, masks, the sound behind the door. You go to art for the truths that don't behave in daylight." },
  { id:"border-crosser", kind:"general", name:"The Border-Crosser", rule:"contradiction",
    palette:["#c9a45c","#274b9f","#c23a3a","#e8e0cc"],
    blurb:"Your taste keeps two homes — say, quiet interiors and howling abstraction — and refuses to choose. Both passports are valid here." },
  { id:"time-traveler", kind:"general", name:"The Time Traveler", rule:"time-traveler",
    palette:["#8a6e46","#3e5570","#c9a45c","#1d1c22"],
    blurb:"Five centuries, one appetite. You admire across eras the way other people cross streets, and the atlas was built for exactly you." },
  { id:"open-eye", kind:"general", name:"The Open Eye", rule:"eclectic",
    palette:["#e8dcc8","#3aa8b8","#a12b3a","#8a9a5e"],
    blurb:"Your cloud is wide and it isn't confusion — it's appetite. No single island claims you; the whole archipelago does." }
];
