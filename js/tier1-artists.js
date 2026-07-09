/* PIGMENT — Tier 1 artist overlay (25 artists).
   Per ARTWORK_SCHEMA tiering + STYLE_GUIDE §4.2–4.3:
   why    — 40–60 words: the claim, the visible evidence, the lineage
   lookFor — 3–5 traits, each a thing the eye can find
   goNext  — 3–4 onward doors: {t: artist|movement|technique|work, id, why}
   coords  — hand-scored Tier 1 taste vector (TASTE_MATH scale −100…+100) */
window.TIER1 = {

"leonardo-da-vinci": {
  why: "Leonardo made painting a form of research: light studied like physics, faces like anatomy, landscapes like geology. Sfumato — modelling without lines — gave images an inner weather no one had achieved before. Every painter who ever blurred an edge to suggest a soul is quoting him.",
  lookFor: ["Smoky, lineless transitions between light and shade","Faces caught between two expressions","Blue geological fantasy landscapes behind sitters","Hands that speak as much as faces"],
  goNext: [
    { t:"artist", id:"raphael", why:"his grace, systematized" },
    { t:"artist", id:"michelangelo", why:"the rival, and the opposite answer" },
    { t:"technique", id:"sfumato", why:"the smoke itself" },
    { t:"movement", id:"high-renaissance", why:"the summit he defined" }],
  coords: { F:-85, D:-15, E:5, C:15, M:-15 } },

"michelangelo": {
  why: "Michelangelo put the human body in charge of meaning: theology told through torsos, salvation through musculature. The Sistine ceiling made paint monumental; the Last Judgment made it terrifying. Mannerism, the Baroque, and every heroic nude since are footnotes to his anatomy.",
  lookFor: ["Twisting, spiral poses under strain","Muscle on everyone — angels and women included","Sculptural figures against minimal settings","Bodies drawn grander than their architecture"],
  goNext: [
    { t:"artist", id:"tintoretto", why:"his drawing, Venice's color" },
    { t:"artist", id:"raphael", why:"the courteous rival next door" },
    { t:"movement", id:"mannerism", why:"what his style became unleashed" },
    { t:"technique", id:"fresco", why:"the arena of the ceiling" }],
  coords: { F:-80, D:60, E:-10, C:0, M:90 } },

"hieronymus-bosch": {
  why: "Five centuries before Surrealism had a manifesto, Bosch painted moral philosophy as hallucination — tree-bodied demons, egg-shaped hells, humanity swarming toward its appetites. Nobody knows quite what he meant, which is the engine of his immortality: every age reads its own nightmare into him.",
  lookFor: ["Hybrid creatures assembled from the wrong parts","Dozens of tiny scenes teeming inside one panel","Glassy spheres, eggs and hollow shells","Hell rendered busier than heaven"],
  goNext: [
    { t:"artist", id:"pieter-bruegel", why:"the heir who grounded the visions" },
    { t:"artist", id:"salvador-dali", why:"the 20th-century disciple" },
    { t:"work", id:"the-garden-of-earthly-delights", why:"the whole cosmology in three panels" },
    { t:"movement", id:"northern-renaissance", why:"his strange home" }],
  coords: { F:-70, D:65, E:70, C:45, M:30 } },

"jan-van-eyck": {
  why: "Van Eyck perfected oil glazing so completely that legend credited him with inventing paint itself. Light travels into his panels and comes back changed — brocade you can rustle, mirrors holding whole rooms. Northern painting's entire tradition of total observation starts at his easel.",
  lookFor: ["Mirrors and reflections hiding extra rooms","Jewel-light built from transparent glazes","Inscriptions painted into the scene","Detail that survives any magnification"],
  goNext: [
    { t:"artist", id:"rogier-van-der-weyden", why:"observation, taught to weep" },
    { t:"work", id:"the-arnolfini-portrait", why:"the mirror trick at full power" },
    { t:"technique", id:"glazing", why:"the light machine itself" },
    { t:"movement", id:"early-netherlandish", why:"the school he anchors" }],
  coords: { F:-92, D:-35, E:-15, C:-10, M:-60 } },

"caravaggio": {
  why: "Caravaggio detonated European painting in one decade: street kids as angels, pilgrims with dirty feet, miracles staged in cellar darkness under a single brutal light. Every noir shadow since — Rembrandt's, Ribera's, cinema's — runs on his electricity. He painted saints the way police light suspects.",
  lookFor: ["One raking light source, no visible origin","Models with lived-in faces and unwashed feet","Backgrounds swallowed in black","Action frozen at its most irreversible instant"],
  goNext: [
    { t:"artist", id:"artemisia-gentileschi", why:"his darkness, her fury" },
    { t:"artist", id:"georges-de-la-tour", why:"tenebrism gone silent" },
    { t:"technique", id:"tenebrism", why:"the lighting rig he invented" },
    { t:"work", id:"the-calling-of-saint-matthew", why:"the raid that started it" }],
  coords: { F:-85, D:90, E:20, C:-15, M:35 } },

"artemisia-gentileschi": {
  why: "Artemisia took Caravaggio's darkness and gave it muscle, leverage and a point of view no man in the room possessed. Her Judiths don't flinch from the beheading — they brace into it. The first woman admitted to Florence's academy, she negotiated her fees like the master she was.",
  lookFor: ["Women who act rather than pose","Rolled sleeves and straining forearms","Blood with honest physics","Candlelit stages, three figures deep"],
  goNext: [
    { t:"artist", id:"caravaggio", why:"the source of the darkness" },
    { t:"artist", id:"lavinia-fontana", why:"the woman who opened the door first" },
    { t:"work", id:"judith-slaying-holofernes", why:"the manifesto" },
    { t:"movement", id:"baroque", why:"her arena" }],
  coords: { F:-88, D:88, E:15, C:-10, M:30 } },

"rembrandt": {
  why: "Rembrandt traded the Baroque's theatre for inner weather: light that seems to come from inside people. Eighty self-portraits form painting's greatest autobiography; his late crusted surfaces, called unfinished then, look like the invention of modern paint-handling now. Nobody has made gloom feel warmer.",
  lookFor: ["Golden light with no clear source","Impasto thick enough to cast real shadows","Eyes that seem mid-thought","Etching lines scratched like handwriting"],
  goNext: [
    { t:"artist", id:"johannes-vermeer", why:"the other Dutch answer: silence" },
    { t:"artist", id:"kathe-kollwitz", why:"his etching needle, centuries on" },
    { t:"technique", id:"chiaroscuro", why:"his native language" },
    { t:"movement", id:"dutch-golden-age", why:"the market he outgrew" }],
  coords: { F:-80, D:35, E:25, C:0, M:-20 } },

"johannes-vermeer": {
  why: "Thirty-some paintings, mostly one quiet room — and within that whisper, the most perfect light in Western art. Vermeer made stillness an event: a woman reading a letter carries the tension other painters need battles for. Forgotten for two centuries, he now defines what 'luminous' means.",
  lookFor: ["Daylight entering from a window at left","Tiny pearls of thick paint on highlights","Maps and paintings hung as silent commentary","One gesture, suspended forever"],
  goNext: [
    { t:"artist", id:"vilhelm-hammershoi", why:"the same silence, painted grey" },
    { t:"artist", id:"frans-hals", why:"the loud opposite of the Golden Age" },
    { t:"work", id:"girl-with-a-pearl-earring", why:"five strokes make the pearl" },
    { t:"movement", id:"dutch-golden-age", why:"his small, deep pond" }],
  coords: { F:-90, D:-60, E:-20, C:-35, M:-85 } },

"diego-velazquez": {
  why: "Velázquez painted what was actually there — air included. Popes muttered 'too true'; Impressionists called him the painter of painters. Las Meninas turned looking itself into the subject, and his feathery late strokes, meaningless up close and alive at distance, taught Manet everything.",
  lookFor: ["Strokes that dissolve when you step close","Air and distance rendered between figures","Mirrors and canvases inside the picture","Silver-grey harmonies instead of loud color"],
  goNext: [
    { t:"artist", id:"edouard-manet", why:"the heir who said so" },
    { t:"artist", id:"francis-bacon", why:"the pope, screamed" },
    { t:"work", id:"las-meninas", why:"painting's supreme riddle" },
    { t:"artist", id:"francisco-goya", why:"the court, one century darker" }],
  coords: { F:-85, D:20, E:20, C:15, M:45 } },

"francisco-goya": {
  why: "No artist travelled further in one lifetime: sunny tapestry cartoons to the Black Paintings on his own dining-room wall. Goya invented war art without heroes, satire without safety, and nightmare without mythology. Modern art's conscience — and its insomnia — start with him.",
  lookFor: ["Black used as a color, not an absence","Crowd faces smeared into masks","Violence shown without glory or rescue","Late beasts painted straight onto plaster"],
  goNext: [
    { t:"work", id:"saturn-devouring-his-son", why:"the dining room in question" },
    { t:"artist", id:"otto-dix", why:"Der Krieg answers the Disasters" },
    { t:"artist", id:"edouard-manet", why:"the executions, restaged" },
    { t:"movement", id:"romanticism", why:"his uneasy label" }],
  coords: { F:-70, D:80, E:50, C:15, M:0 } },

"katsushika-hokusai": {
  why: "Hokusai gave the world its most reproduced image and Japan its restless genius — thirty name changes, ninety addresses, 'mad about painting' to the last. The Great Wave taught the West that flatness, cropping and pattern could carry monumental force. Monet and Van Gogh collected him like scripture.",
  lookFor: ["Waves with claws, foam like snowflakes","Mount Fuji hiding somewhere small","Imported Prussian blue everywhere","Motion caught mid-gesture, never posed"],
  goNext: [
    { t:"artist", id:"utagawa-hiroshige", why:"the rival who painted weather" },
    { t:"artist", id:"vincent-van-gogh", why:"the most devoted student" },
    { t:"work", id:"the-great-wave-off-kanagawa", why:"the image itself" },
    { t:"technique", id:"woodblock", why:"the medium of multiplication" }],
  coords: { F:-55, D:40, E:30, C:-25, M:0 } },

"jmw-turner": {
  why: "Turner pushed landscape from scenery to cataclysm and then further — into pure vortices of light that contemporaries called unfinished and abstraction later called prophecy. He painted the industrial revolution as weather. Impressionism, and arguably Rothko, disembark from his boats.",
  lookFor: ["Light dissolving solid objects","Vortex compositions that pull you in","The sun stared at directly","Sea and storm as the main characters"],
  goNext: [
    { t:"artist", id:"claude-lorrain", why:"the idol he demanded to hang beside" },
    { t:"artist", id:"claude-monet", why:"the student of his dissolutions" },
    { t:"artist", id:"mark-rothko", why:"the sublime, abstracted" },
    { t:"movement", id:"romanticism", why:"his storm system" }],
  coords: { F:-40, D:75, E:65, C:-30, M:60 } },

"claude-monet": {
  why: "Monet chased fugitive light for sixty years and invented the modern series along the way — the same haystack, cathedral, pond, repainted as the hour turned. Impressionism carries his painting's name by accident and his stubbornness by design. The water lilies end where abstraction begins.",
  lookFor: ["Broken dabs of unmixed color","Shadows in color, never black","The same motif at different hours","Water doing half the painting's work"],
  goNext: [
    { t:"artist", id:"pierre-auguste-renoir", why:"the friend at La Grenouillère" },
    { t:"artist", id:"joan-mitchell", why:"his pond, her storm, same village" },
    { t:"work", id:"impression-sunrise", why:"the insult that named a movement" },
    { t:"movement", id:"impressionism", why:"the church he built" }],
  coords: { F:-45, D:-30, E:35, C:-70, M:-10 } },

"vincent-van-gogh": {
  why: "Ten years, nine hundred paintings, one sale — then the whole world. Van Gogh turned brushwork into handwriting and color into confession; every stroke is signed by a nervous system. He is proof that painting can carry a life's entire voltage, and modern art's most loved cautionary saint.",
  lookFor: ["Directional strokes following forms like currents","Halos vibrating around lights and stars","Complementary colors set to collide","Paint thick enough to map with a finger"],
  goNext: [
    { t:"artist", id:"paul-gauguin", why:"nine weeks, one ear, lifelong letters" },
    { t:"artist", id:"jean-francois-millet", why:"'father Millet', copied twenty times" },
    { t:"work", id:"the-starry-night", why:"the asylum window, transfigured" },
    { t:"movement", id:"expressionism", why:"everything he made possible" }],
  coords: { F:-55, D:70, E:60, C:-45, M:-25 } },

"paul-cezanne": {
  why: "Cézanne wanted to make Impressionism 'solid and durable like museum art' — and accidentally drafted the twentieth century. Form built from color patches, perspective bent by honesty, one mountain repainted sixty times. Matisse and Picasso split the inheritance and called him father of us all.",
  lookFor: ["Tabletops tilting toward the viewer","Form built from parallel patch-strokes","Outlines restated three or four times","The same mountain, again, differently"],
  goNext: [
    { t:"artist", id:"pablo-picasso", why:"heir number one" },
    { t:"artist", id:"nicolas-poussin", why:"'Poussin, redone from nature'" },
    { t:"artist", id:"camille-pissarro", why:"the humble teacher" },
    { t:"movement", id:"cubism", why:"what the patches became" }],
  coords: { F:-60, D:-10, E:60, C:20, M:-15 } },

"gustav-klimt": {
  why: "Klimt armored desire in ornament: real gold leaf, Byzantine geometry, bodies dissolving into pattern. His Vienna scandalized itself on him and then couldn't live without him. The Kiss made the sacred and the erotic share one halo — Art Nouveau's summit and modern portraiture's glamour blueprint.",
  lookFor: ["Actual gold leaf emitting, not reflecting","Pattern swallowing bodies whole","Rectangles for him, circles for her","Faces in closed-eye ecstasy"],
  goNext: [
    { t:"artist", id:"egon-schiele", why:"the protégé who tore the gold off" },
    { t:"work", id:"the-kiss", why:"the summit" },
    { t:"technique", id:"gold-leaf", why:"the inheritance from Byzantium" },
    { t:"movement", id:"vienna-secession", why:"his gilded rebellion" }],
  coords: { F:-55, D:15, E:35, C:-45, M:0 } },

"edvard-munch": {
  why: "Munch painted states of mind as if they were weather — jealousy, illness and dread given color and a horizon. The Scream became modern anxiety's logo, but the whole Frieze of Life pulses with the same voltage. German Expressionism is his echo chamber.",
  lookFor: ["Aura lines radiating from figures","Faces simplified to masks","Blood-dusk skies and long shadows","The same traumas repainted for decades"],
  goNext: [
    { t:"artist", id:"ernst-ludwig-kirchner", why:"the echo in Berlin" },
    { t:"artist", id:"vincent-van-gogh", why:"the other painter of nerves" },
    { t:"work", id:"the-scream", why:"the logo of dread" },
    { t:"movement", id:"expressionism", why:"the movement he seeded" }],
  coords: { F:-55, D:85, E:55, C:0, M:-15 } },

"henri-matisse": {
  why: "Matisse freed color from description twice — first with the Fauves' wild canvases, then, bedridden at eighty, with scissors and painted paper. His lifelong subject was joy treated with total seriousness. Half of modern art argues with Picasso; the other half convalesces with Matisse.",
  lookFor: ["Color choices that describe feeling, not fact","One arabesque line doing a figure's work","Flat patterned interiors without shadows","Late shapes cut, not drawn"],
  goNext: [
    { t:"artist", id:"pablo-picasso", why:"the North Pole to his South" },
    { t:"artist", id:"gustave-moreau", why:"the teacher who allowed it" },
    { t:"artist", id:"paul-signac", why:"the dots that lit the fuse" },
    { t:"movement", id:"fauvism", why:"the cage of wild beasts" }],
  coords: { F:-50, D:0, E:55, C:-60, M:10 } },

"pablo-picasso": {
  why: "Picasso is the century in one career: blue grief, rose circuses, Cubism's earthquake, Guernica's scream, and fifty thousand works of restless everything. He didn't have a style; he had appetites. Every argument about what art is allowed to do passes through him.",
  lookFor: ["Faces showing profile and front at once","Period shifts you can date by color","African mask geometry in the features","Bulls, minotaurs and self-mythology"],
  goNext: [
    { t:"artist", id:"georges-braque", why:"roped together on the cliff of Cubism" },
    { t:"artist", id:"henri-matisse", why:"the lifelong duel" },
    { t:"artist", id:"el-greco", why:"the flame under Les Demoiselles" },
    { t:"movement", id:"cubism", why:"the earthquake itself" }],
  coords: { F:-40, D:45, E:80, C:30, M:20 } },

"wassily-kandinsky": {
  why: "Kandinsky heard colors and painted the sound — then wrote abstraction's scripture to explain why a picture needs no object at all. His pre-war Compositions are apocalypses of pure color; his Bauhaus geometry is the same faith, cooled. Abstract art's loudest prophet, if not its first.",
  lookFor: ["Titles borrowed from music — improvisations, compositions","Storm chaos early, floating geometry late","Black calligraphic lines riding the color","No up, no down, no object"],
  goNext: [
    { t:"artist", id:"hilma-af-klint", why:"the secret first, years earlier" },
    { t:"artist", id:"paul-klee", why:"the Bauhaus neighbor and friend" },
    { t:"work", id:"composition-vii", why:"the apocalypse in four days" },
    { t:"movement", id:"abstract-art", why:"the faith he preached" }],
  coords: { F:80, D:55, E:80, C:25, M:20 } },

"frida-kahlo": {
  why: "Kahlo painted her own reality — a body broken by a bus, a heart broken by Rivera — in the deadpan style of votive miracles. A third of her work is self-portrait, none of it self-pity. She turned autobiography into iconography, and the world is still wearing it.",
  lookFor: ["The unibrow, stated as fact","Retablo flatness and folk framing","The body opened like an anatomy plate","Monkeys, parrots and thorns as heraldry"],
  goNext: [
    { t:"artist", id:"diego-rivera", why:"the partner, twice" },
    { t:"artist", id:"leonora-carrington", why:"Mexico's other magic realist" },
    { t:"movement", id:"naive-art", why:"the votive tradition she weaponized" },
    { t:"movement", id:"surrealism", why:"the label she refused" }],
  coords: { F:-75, D:55, E:45, C:20, M:-60 } },

"salvador-dali": {
  why: "Dalí rendered dreams with a miniaturist's precision — soft watches, crutch-propped flesh, beaches of guilt — and marketed the unconscious better than anyone alive. Expelled from Surrealism for excess, he correctly replied that he was Surrealism. The mustache was load-bearing.",
  lookFor: ["Hard, glassy technique on impossible things","Double images hiding in plain sight","Vast empty beaches with long shadows","Soft things propped on crutches"],
  goNext: [
    { t:"artist", id:"giorgio-de-chirico", why:"the empty stage he inherited" },
    { t:"artist", id:"rene-magritte", why:"the dream, deadpan instead" },
    { t:"artist", id:"hieronymus-bosch", why:"the 500-year-old colleague" },
    { t:"movement", id:"surrealism", why:"the movement he claimed to be" }],
  coords: { F:-55, D:55, E:60, C:35, M:0 } },

"jackson-pollock": {
  why: "Pollock laid the canvas on the floor, stepped inside it, and let the gesture itself become the picture — energy made visible, no brush touching cloth. The drip paintings made American art the world's center of gravity and turned the act of painting into the subject of painting.",
  lookFor: ["All-over webs with no center or edge","Skeins layered color over color","Flicks, pools and speed differences in the line","Scale that swallows your whole vision"],
  goNext: [
    { t:"artist", id:"lee-krasner", why:"partner, editor, keeper of the flame" },
    { t:"artist", id:"willem-de-kooning", why:"the rival who kept the figure" },
    { t:"technique", id:"dripping", why:"the method, patented in motion" },
    { t:"movement", id:"abstract-expressionism", why:"the arena" }],
  coords: { F:85, D:75, E:85, C:15, M:55 } },

"mark-rothko": {
  why: "Rothko floated rectangles of color until they breathed — not abstractions, he insisted, but 'basic human emotions: tragedy, ecstasy, doom.' He wanted viewers eighteen inches away, engulfed. Stand there and the paintings do something no reproduction survives: they wait for you.",
  lookFor: ["Soft-edged rectangles hovering, never resting","Layered glazes glowing from underneath","Edges where two colors negotiate","Late works darkening toward the chapel"],
  goNext: [
    { t:"artist", id:"barnett-newman", why:"the zip beside the field" },
    { t:"artist", id:"caspar-david-friedrich", why:"the sublime, one century earlier" },
    { t:"artist", id:"jmw-turner", why:"light without objects, first draft" },
    { t:"movement", id:"color-field", why:"his quiet wing of AbEx" }],
  coords: { F:90, D:35, E:60, C:0, M:60 } },

"andy-warhol": {
  why: "Warhol pointed painting's eye at the supermarket and the front page — soup cans, Marilyns, car crashes — and silkscreened them until repetition itself became the message. 'I want to be a machine' was the century's slyest artistic confession. Image culture still runs on his operating system.",
  lookFor: ["Repetition until glamour becomes numbness","Silkscreen slippage and misregistration","Celebrity faces treated as icons","Factory flatness, zero brush ego"],
  goNext: [
    { t:"artist", id:"marcel-duchamp", why:"the question Warhol industrialized" },
    { t:"artist", id:"jean-michel-basquiat", why:"the late, electric friendship" },
    { t:"artist", id:"roy-lichtenstein", why:"the other half of Pop's rivalry" },
    { t:"technique", id:"silkscreen", why:"the assembly line" }],
  coords: { F:-30, D:15, E:70, C:75, M:10 } }
};
