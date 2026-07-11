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
  coords: { F:-85, D:90, E:20, C:-15, M:35 },
  arc: [
    { y:"1577", t:"Plague orphan",
      text:"Michelangelo Merisi is six when plague sweeps Lombardy and takes his father and grandfather on the same day. Apprenticed at thirteen in Milan, he absorbs the Lombard creed — paint what stands in front of you. Around 1592 he bolts for Rome, reportedly one step ahead of trouble over a wounded police officer." },
    { y:"1593–96", t:"Fruit boys on the make",
      text:"Penniless in Rome, he paints street boys, overripe fruit and rigged card games for the open market — con men observed as coolly as still lifes. Cardinal Del Monte buys The Cardsharps, gives the painter rooms in his palace, and starts supplying clients. The apprenticeship is over.",
      works:["boy-with-a-basket-of-fruit","the-cardsharps","bacchus-caravaggio"] },
    { y:"1599–1600", t:"Overnight, in a chapel",
      text:"His first public commission, for the Contarelli Chapel: Saint Matthew called from a tax table by a shaft of light that behaves like an arrest warrant. Rome has never seen sacred history staged in a tavern. Every painter in the city comes to look; half of them start over.",
      works:["the-calling-of-saint-matthew"] },
    { y:"1601–06", t:"Fame with a police file",
      text:"The most in-demand painter in Rome is also its most arrested — libel, illegal weapons, a waiter assaulted with a plate of artichokes. The pictures keep outrunning the scandals until Death of the Virgin, its Madonna reportedly modeled on a drowned courtesan, is refused by the monks who ordered it.",
      works:["judith-beheading-holofernes","the-entombment-of-christ","death-of-the-virgin"] },
    { y:"1606", t:"The murder",
      text:"A quarrel over a wagered tennis match — or a woman, or both — ends with Ranuccio Tomassoni bleeding to death on a Roman court and a capital sentence on Caravaggio's head: anyone may kill him on sight. He flees south to Naples, where nobody asks questions and everybody wants a Caravaggio." },
    { y:"1607", t:"Mercy, painted by a killer",
      text:"For a Naples charity he crams all seven works of mercy into one nocturnal street corner — corpse-bearers, a prisoner nursed through the bars, angels tangled in the dark overhead. The fugitive with blood on his hands paints compassion as street life, caught by torchlight.",
      works:["the-seven-works-of-mercy"] },
    { y:"1608", t:"Malta: knighted, then caged",
      text:"The Knights of St John make him a brother — the murderer reborn as Fra Michelangelo — and he pays with the largest canvas of his life, signed in the Baptist's blood. Within months he wounds a senior knight, is jailed in the rock, escapes by rope, and is expelled 'as a foul and rotten limb.'",
      works:["the-beheading-of-saint-john"] },
    { y:"1609–10", t:"The hunted man's plea",
      text:"Slashed across the face outside a Naples tavern, he paints his own severed head in David's fist and aims it at Rome, where Cardinal Scipione Borghese has the power to trade a pardon. The last pictures go darker still — bare brown grounds, faces surfacing out of nothing.",
      works:["david-with-the-head-of-goliath"] },
    { y:"1610", t:"The beach at Porto Ercole",
      text:"He sails north with paintings for the ransom, is mistakenly arrested at a coastal garrison, and watches the boat leave with them aboard. Days later, at thirty-eight, he is dead of fever on the beach — reportedly just before word of the pardon arrived. Painters have argued with his light ever since." }
  ] },

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
  coords: { F:-80, D:35, E:25, C:0, M:-20 },
  arc: [
    { y:"1606–31", t:"The miller's son",
      text:"Ninth child of a Leiden miller, enrolled at the university at fourteen and gone within months — apprenticed to painters instead. By twenty-five, the statesman-poet Constantijn Huygens is telling anyone who will listen that a miller's boy has out-painted the ancients. Amsterdam sends for him." },
    { y:"1632", t:"Anatomy of a debut",
      text:"His first big Amsterdam commission turns the surgeons' guild's annual dissection into theatre — nobody poses, everybody leans in, and the corpse of a hanged robber gets the best light. He is twenty-six, and the city's merchant class forms a line at his door.",
      works:["the-anatomy-lesson"] },
    { y:"1634–42", t:"Saskia and the spending",
      text:"He marries Saskia van Uylenburgh, his dealer's cousin, and paints her as Flora, as Danaë, as everything. Money pours in and straight back out — a grand house on the Breestraat, weapons, costumes, coral, exotic armor: props for paintings, and a bankruptcy assembling itself in slow motion.",
      works:["the-storm-on-the-sea-of-galilee","danae-rembrandt"] },
    { y:"1642", t:"The Night Watch, the dark year",
      text:"He blows the militia group portrait apart — drums, muskets, motion, a golden girl in the crowd — and delivers the most famous painting in Dutch history the same year Saskia dies at twenty-nine, months after their son Titus is born. The grandest canvas and the worst year arrive together.",
      works:["the-night-watch"] },
    { y:"1649–54", t:"Hendrickje",
      text:"His housekeeper Hendrickje Stoffels becomes his common-law wife; the church council summons her — not him — for 'living in sin with Rembrandt the painter' while pregnant. He answers in paint: Bathsheba with a real body and an unreadable ache, Hendrickje's face on a queen's dilemma.",
      works:["bathsheba-at-her-bath"] },
    { y:"1656", t:"The inventory",
      text:"The debts win. The house, the Roman busts, the Japanese armor, his own collection of his own etchings — all catalogued and auctioned off over three years. The insolvency inventory survives, 363 lots long, one of the great documents of an artist's appetite. He moves to a rented house across town." },
    { y:"1662", t:"The comeback commission",
      text:"The cloth guild's sampling officials want a group portrait; the bankrupt delivers the calmest masterpiece of the century — five men glancing up from their ledger as if you had just opened the door. When he wants the old magic, it is all still there. Increasingly, he wants something rougher instead.",
      works:["syndics-of-the-drapers-guild"] },
    { y:"1663–68", t:"Outliving everyone",
      text:"Hendrickje dies in a plague year; Titus at twenty-seven, months after his wedding. The late self-portraits — paint thick as stucco, lit like verdicts — record all of it without an ounce of self-pity. In one, he stands before two painted circles that no one has ever conclusively explained.",
      works:["self-portrait-with-two-circles"] },
    { y:"1665–69", t:"The tenderest endgame",
      text:"Nearly alone at the end, he paints the gentlest things of his century: a couple's four hands saying belonging, a father's mismatched hands on a returned son's shoulders. He dies in October 1669 and is buried in a rented, unmarked church grave — owning, by the record, his painting tools and little else.",
      works:["the-jewish-bride","the-return-of-the-prodigal-son","self-portrait-at-63"] }
  ] },

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
  coords: { F:-70, D:80, E:50, C:15, M:0 },
  arc: [
    { y:"1746–74", t:"The Aragonese climber",
      text:"A gilder's son from a stone village near Zaragoza, twice rejected by the royal academy, so he takes the other road: Italy on his own money, then marriage to Josefa Bayeu — sister of the court painter. Talent gets you noticed in Madrid; in-laws get you through the door." },
    { y:"1775–92", t:"Picnics for palaces",
      text:"For seventeen years he designs tapestry cartoons for royal walls — parasols, dances, kite days, majas flirting in the sun. It looks like harmless décor, and it is also a complete education in Spanish life, filed away by the sharpest pair of eyes in the country.",
      works:["the-parasol"] },
    { y:"1793", t:"Silence",
      text:"An illness nobody has ever securely diagnosed — lead poisoning and autoimmune disease are the modern guesses — nearly kills him at forty-six and leaves him permanently, totally deaf. The courtier keeps his job and his smile. The painter starts working for himself, and the work turns inward at once." },
    { y:"1799", t:"The sleep of reason",
      text:"Los Caprichos: eighty etchings flaying superstition, vanity, clergy and cruelty, sold out of a perfume shop and withdrawn within days — reportedly before the Inquisition could take a formal interest. Plate 43 is the thesis: a sleeping man mobbed by owls and bats, reason abandoned to monsters.",
      works:["the-sleep-of-reason","witches-sabbath"] },
    { y:"1800–05", t:"First Painter, private nudes",
      text:"The official summit: First Court Painter, unveiling the royal family with almost reckless honesty. The private summit: for the prime minister's hidden cabinet, a maja naked and the same maja clothed — a hinged pair, one made to swing over the other. The Inquisition will eventually ask him about that.",
      works:["charles-iv-of-spain-and-his-family","the-naked-maja","the-clothed-maja"] },
    { y:"1808–14", t:"The war",
      text:"Napoleon's armies occupy Spain; Goya keeps his head down, sketches what he sees, and says nothing for six years. When the French are gone he answers with the Second and Third of May — uprising and reprisal, the firing squad as machine — and invents how war would be pictured from then on.",
      works:["the-second-of-may-1808","the-third-of-may-1808"] },
    { y:"1819–23", t:"The house of the deaf man",
      text:"Deaf, ill and seventy-three, he buys a farmhouse outside Madrid and paints directly onto its plaster walls: Saturn devouring, witches assembling, a dog's head in a void. No commission, no titles, no intention that anyone should see them. The Black Paintings are the most private great pictures ever made.",
      works:["saturn-devouring-his-son","the-dog"] },
    { y:"1820", t:"Gratitude",
      text:"After another near-fatal illness he paints himself limp in the arms of Dr Arrieta, who steadies the medicine glass at his lips, and inscribes it like a votive tablet: in gratitude to the friend whose skill saved his life. The hardest eye in Europe, gone soft exactly once.",
      works:["self-portrait-with-dr-arrieta"] },
    { y:"1824–28", t:"Still learning",
      text:"At seventy-eight he self-exiles to Bordeaux among Spain's liberals, takes up the brand-new craft of lithography, and captions a late drawing of a bearded ancient hobbling on two sticks 'Aún aprendo' — I am still learning. He dies at eighty-two, the hinge between the old masters and everything modern." }
  ] },

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
  coords: { F:-45, D:-30, E:35, C:-70, M:-10 },
  arc: [
    { y:"1840–61", t:"The caricaturist meets the sky",
      text:"A Le Havre teenager earning good money on caricatures until the local marine painter Eugène Boudin drags him outdoors to paint air and water directly. Monet resisted, went once, and described it afterwards as a veil tearing: suddenly he understood what painting could be." },
    { y:"1865–70", t:"Camille and the trench",
      text:"He paints Camille Doncieux — model, lover, then wife over his family's objections — and thinks big: for Women in the Garden he digs a trench so the two-and-a-half-metre canvas can be cranked down to paint the top in the same outdoor light. The Salon shrugs; even his snow-bright Magpie is refused.",
      works:["women-in-the-garden","the-magpie"] },
    { y:"1869", t:"The frog pond",
      text:"Broke, he sets up beside Renoir at La Grenouillère, a bathing spot on the Seine, and between them they work out a shorthand for water in motion — broken touches of unmixed color that only resolve at a distance. Impressionism is invented in a few afternoons; the name comes later.",
      works:["la-grenouillere"] },
    { y:"1874", t:"An insult becomes a movement",
      text:"At the painters' first independent exhibition he hangs a Le Havre harbor at sunrise, titled almost offhandedly Impression. The critic Louis Leroy sneers that wallpaper in its embryonic state is more finished — and the insult sticks as a name. Within a decade, the joke is on the Salon.",
      works:["impression-sunrise"] },
    { y:"1875–79", t:"Steam and grief",
      text:"He paints Camille and their son on a windy rise, then a dozen canvases of the Gare Saint-Lazare — locomotives exhaling weather indoors. In 1879 Camille dies at thirty-two, and Monet, horrified at his own eye, catches himself studying the grays death fixes on her face. Light spares nothing.",
      works:["woman-with-a-parasol","gare-saint-lazare"] },
    { y:"1883", t:"Giverny",
      text:"He rents, and later buys, a pink farmhouse at Giverny and begins the real masterpiece: the garden. Flowerbeds laid out like loaded palettes, then a diverted stream, a pond, water lilies and a Japanese bridge — a motif farm, planted years before he intends to harvest it." },
    { y:"1890–94", t:"Painting time",
      text:"The grainstacks behind his house become a relay — canvases swapped as the light moves, frost-pink dawn to smoldering dusk. Fifteen hang together in 1891 and sell within days. Then thirty-odd façades of Rouen Cathedral, stone as a screen for passing hours. The subject is no longer the thing; it is time moving across the thing.",
      works:["grainstacks","rouen-cathedral-full-sunlight"] },
    { y:"1899–1926", t:"The pond swallows painting",
      text:"From the Japanese bridge to lily pads to pure reflection, the pond grows until the horizon leaves the canvas entirely. Cataracts redden his world for a decade — after surgery in 1923 he destroys canvases painted through the fog — while Clemenceau keeps him at the huge cycle promised to France the day after the armistice.",
      works:["bridge-over-a-pond-of-water-lilies","water-lilies-grandes-decorations"] },
    { y:"1927", t:"The oval rooms",
      text:"He dies in December 1926, at eighty-six, still revising his unfinished walls of water. Five months later the Grandes Décorations open in two oval rooms at the Orangerie — no horizon, no bank, no edge. Painting had followed him to the brink of abstraction; the next generation stepped over." }
  ] },

"vincent-van-gogh": {
  why: "Ten years, nine hundred paintings, one sale — then the whole world. Van Gogh turned brushwork into handwriting and color into confession; every stroke is signed by a nervous system. He is proof that painting can carry a life's entire voltage, and modern art's most loved cautionary saint.",
  lookFor: ["Directional strokes following forms like currents","Halos vibrating around lights and stars","Complementary colors set to collide","Paint thick enough to map with a finger"],
  goNext: [
    { t:"artist", id:"paul-gauguin", why:"nine weeks, one ear, lifelong letters" },
    { t:"artist", id:"jean-francois-millet", why:"'father Millet', copied twenty times" },
    { t:"work", id:"the-starry-night", why:"the asylum window, transfigured" },
    { t:"movement", id:"expressionism", why:"everything he made possible" }],
  coords: { F:-55, D:70, E:60, C:-45, M:-25 },
  arc: [
    { y:"1853–80", t:"The failures",
      text:"Art dealer (dismissed), teacher, bookseller, theology student (withdrew), lay missionary in the Borinage coalfields (relieved of duty, reportedly for excessive zeal — he gave away his clothes and slept on straw). At twenty-seven, with nothing left to fail at, he starts to draw. Ten years remain." },
    { y:"1885", t:"Peasants, painted with earth",
      text:"In Nuenen he paints five peasants around one dish by lamplight, in colors he compared to a dusty, unpeeled potato. He means it as his first masterpiece; a friend's critique of its anatomy ends the friendship for good. He never stops defending it.",
      works:["the-potato-eaters"] },
    { y:"1886–87", t:"Paris detonates the palette",
      text:"Two years with Theo in Montmartre: Impressionism, pointillism and Japanese prints hit in quick succession, and the Dutch mud brightens into strokes of pure color. He paints some two dozen self-portraits, partly because models cost money — the face in the mirror is the one sitter who never complains." },
    { y:"1888", t:"The yellow house",
      text:"Fifteen months in Arles, roughly two hundred paintings — sunflowers to decorate Gauguin's promised room, a café terrace glowing gas-orange against blue, his own bedroom painted flat and calm, he said, to rest the brain. He is burning through himself at the rate of a canvas every two days.",
      works:["sunflowers","cafe-terrace-at-night","the-bedroom","the-night-cafe"] },
    { y:"1888–89", t:"The ear",
      text:"Gauguin arrives in October; the shared studio curdles in nine weeks. On 23 December, after a quarrel, Vincent mutilates his left ear — how much of it is still debated — and delivers it to a woman at the local brothel. In January he paints himself bandaged, calm, studying the damage.",
      works:["self-portrait-with-bandaged-ear"] },
    { y:"1889", t:"Saint-Rémy",
      text:"He commits himself to the asylum at Saint-Rémy. Between crises — during one he ate paint — the view through the barred window becomes The Starry Night, the garden becomes irises, and for Theo's newborn son, named Vincent after him, he paints almond branches against a spring sky.",
      works:["the-starry-night","irises","almond-blossom"] },
    { y:"1890", t:"Seventy days in Auvers",
      text:"Released, he settles near Dr Gachet north of Paris and paints at a sprint — close to a canvas a day for seventy days. The wheatfields stretch horizontal and restless; he writes of 'sadness, extreme loneliness' in the same letter that calls the countryside healthy and fortifying.",
      works:["wheatfield-with-crows"] },
    { y:"1890", t:"The end",
      text:"On 27 July he walks out to the fields and is shot in the chest — by his own hand, by every accepted account. He dies two days later with Theo at the bedside. Theo, shattered, follows him within six months; they lie side by side at Auvers under matching ivy." },
    { y:"1891–1905", t:"Johanna builds the legend",
      text:"He had sold almost nothing — one confirmed painting in his lifetime. Theo's widow, Johanna van Gogh-Bonger, inherits some seven hundred works plus the letters, and spends decades exhibiting, translating and publishing until the failure of 1880 has become the most loved painter on earth." }
  ] },

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
  coords: { F:-55, D:85, E:55, C:0, M:-15 },
  arc: [
    { y:"1868", t:"The sickroom",
      text:"His mother dies of tuberculosis when Edvard is five; his sister Sophie follows when he is thirteen. 'Illness, insanity and death were the black angels that kept watch over my cradle' — the inheritance he never escaped, and the one he painted from for sixty years." },
    { y:"1886", t:"The first scandal",
      text:"He abandons engineering for art and falls in with Kristiania's bohemians, whose commandment is 'write your own life.' He obeys in paint: The Sick Child, scraped and reworked for a year, is jeered at the Autumn Exhibition as an unfinished smudge. He later called it the birth of everything he did.",
      works:["the-sick-child"] },
    { y:"1889", t:"The Saint-Cloud vow",
      text:"News of his father's death reaches him in France, where he has gone on a state scholarship. Alone in Saint-Cloud he writes the manifesto that ends naturalism for him: 'No more interiors with men reading and women knitting. I will paint living people who breathe and feel and suffer and love.'" },
    { y:"1892", t:"The Berlin affair",
      text:"The Verein Berliner Künstler invites the young Norwegian to exhibit, sees the paintings, and votes to shut the show within a week. The scandal makes his name across Germany overnight; he stays, drinking with Strindberg at the Black Piglet and painting the dread of a crowd at dusk.",
      works:["evening-on-karl-johan"] },
    { y:"1893–95", t:"The Frieze of Life",
      text:"In three furious years he paints the core of his lifelong cycle on love, jealousy and death — The Scream, Madonna, Anxiety, Puberty — conceived, he said, to be seen together like a symphony. Modern art gets its face; Munch gets a reputation as a dangerous man.",
      works:["the-scream","madonna-munch","anxiety-munch","puberty-munch"] },
    { y:"1902", t:"The revolver",
      text:"The long, corrosive affair with Tulla Larsen ends in his studio with a gunshot that mangles a finger of his left hand. He had already painted them both into The Dance of Life — her in white hope on the left, her in black mourning on the right, himself in the middle, dancing with someone else.",
      works:["the-dance-of-life"] },
    { y:"1908", t:"The collapse",
      text:"Alcohol, brawls and what he called 'my enemies' — years of unraveling end in Dr. Jacobson's Copenhagen clinic, with electrotherapy and eight months of rest. He credited the clinic with saving his life; sobriety brightened his palette and never touched his subjects." },
    { y:"1911", t:"The Sun",
      text:"Home in Norway for good, he throws himself at the competition to decorate the University of Oslo's ceremonial hall — and the painter of screams answers his breakdown with a sunrise, four and a half metres tall, installed after five years of committee wars in 1916.",
      works:["the-sun-munch"] },
    { y:"1937–44", t:"Degenerate, then immortal",
      text:"The Nazis brand his work degenerate and seize 82 pieces from German museums; occupied Norway watches him refuse every overture from the regime. He dies in January 1944, still painting himself honestly — old, thin, standing between the clock and the bed — and wills over a thousand paintings to the city of Oslo.",
      works:["between-the-clock-and-the-bed"] }
  ] },

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
