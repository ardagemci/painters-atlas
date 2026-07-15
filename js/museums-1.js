/* Pigment museum notes — v1 (the "album text" overlay)
   Keyed by venue id from js/venues.js. Venues without notes still get a
   museum page (collection grid, artists, kindred) — the essay block is simply absent.
   Schema: { hook (≤64 chars, the tagline under the name),
             founded ("YYYY" display string),
             essay (100–180 words, house voice — history, fame, character;
                    paragraphs split on \n\n) }
   Enforced by tools/validate.jxa.js. */
window.MUSEUM_NOTES = {

"prado": {
  hook: "Goya's workplace, Spain's fever dream",
  founded: "1819",
  essay: "The Prado isn't a survey of art history; it's the inheritance of three centuries of royal obsession. The Habsburg and Bourbon kings collected the way other dynasties waged war — Philip II hoarding Bosch's nightmares, Philip IV keeping Velázquez down the corridor like a court secret — and in 1819 the crown finally opened the vault. The result is a museum with the deepest bench on earth rather than the widest: more Velázquez, more Goya, more Bosch and Titian than anywhere else, hung dense in a building that still feels like a palace corridor. Its gravitational centre is Las Meninas; its dark heart is the room of Goya's Black Paintings, lifted off the walls of his farmhouse. Madrid treats it less like a museum than a national organ — something between a library and a cathedral." },

"moma": {
  hook: "Where 'modern' became the canon",
  founded: "1929",
  essay: "Nine days after the 1929 crash, three formidable collectors — Abby Aldrich Rockefeller, Lillie Bliss and Mary Quinn Sullivan — opened a museum for the art nobody respectable wanted. Its first director, Alfred Barr, was twenty-seven, and his famous flowchart of modernism — Cézanne flowing into Cubism flowing into abstraction — quietly became the textbook the whole world teaches from. That's MoMA's real power: it doesn't just own the modern canon, it wrote it. The Demoiselles d'Avignon and The Starry Night hang here the way constitutional documents sit in archives. The galleries perfected the white cube — walls like blank paper, art as argument — and every museum of modern art since is either an imitation or a rebuttal. New Yorkers complain it's crowded. It is. So is the twentieth century." },

"met": {
  hook: "America's five-thousand-year answer",
  founded: "1870",
  essay: "The Met was founded by businessmen and civic boosters who owned, at the moment of founding, not a single work of art — just the conviction that a young republic deserved everything, from pharaohs to the day before yesterday. Gilded Age fortunes did the rest, and the result sprawls along Central Park like an empire of its own: arms and armor, a Temple of Dendur in a glass hall, and paintings enough to fill a lifetime of visits. It buys with intent — when Velázquez's Juan de Pareja arrived in 1971 for a record price, the museum called it a portrait of human dignity and meant it. The Met is where America goes to feel continuous with everything; the encyclopedic museum in its most confident, most generous form. Wear comfortable shoes and surrender the plan." },

"louvre": {
  hook: "A palace that surrendered to paintings",
  founded: "1793",
  essay: "Fortress, then royal palace, then — one revolution later — the property of everyone: the Louvre opened in 1793 with the logic that a republic's citizens had inherited the kings' pictures. Napoleon stuffed it with the plunder of Europe (much went back; the habit of grandeur stayed), and two centuries of curators have made it the largest museum on earth — a building you don't visit so much as triage. Its fame has a face: the Mona Lisa, whose 1911 theft turned a quiet Leonardo into the most famous object humans have made. But the Louvre's actual character lives in its long galleries — Leonardo's smoky enigmas, Vermeer's Lacemaker no bigger than a novel, Caravaggio's rejected Virgin — under I. M. Pei's glass pyramid, which Parisians hated for exactly one decade and now cannot imagine gone." },

"national-gallery-london": {
  hook: "Free to everyone since 1824, on purpose",
  founded: "1824",
  essay: "Parliament bought a dead banker's thirty-eight pictures in 1824 and made a decision that still defines the place: the collection would sit in the middle of London, on Trafalgar Square, free — positioned deliberately so that the poor of the East End could reach it as easily as the carriages of the West. Two centuries on it remains one of the great democratic bargains: Van Eyck's Arnolfini Portrait, Turner's Temeraire, Velázquez's Venus and Rembrandt's last self-portrait, all for the price of walking in. Its finest hour was its emptiest — during the Blitz the paintings hid in a Welsh slate mine while one masterpiece a month came back to hang alone, and Londoners queued through air raids to see it. A national gallery that behaves like a public utility: that's the style." },

"national-gallery-dc": {
  hook: "Mellon's gift, with his name left off",
  founded: "1937",
  essay: "Andrew Mellon — banker, treasury secretary, and for a while the most quietly effective collector alive — gave America a national gallery the way you'd endow a constitution: the building, the endowment and his old-master collection, with one condition. His name would appear nowhere on it, so that other collectors would feel it was theirs to fill. It worked; the gifts have never stopped. Under the marble rotunda hangs the only Leonardo painting in the Americas — Ginevra de' Benci, bought from Liechtenstein's princes — alongside Vermeer, Monet's parasol wind, and, in I. M. Pei's angular East Building, the moderns. Like the Smithsonian around it, admission is free, which gives the place its particular American flavor: imperial marble, democratic door policy. Washington argues about everything; nobody argues about this." },

"rijksmuseum": {
  hook: "The nation's attic, rebuilt as a cathedral",
  founded: "1800",
  essay: "The Dutch built their national museum the way they built their republic — gradually, pragmatically, and then all at once in Pierre Cuypers' 1885 building, a brick cathedral where the choir was replaced by a painting: the Night Watch hangs at the far end of the Gallery of Honour, precisely where another country would put an altar. That's not an accident; it's a thesis. Holland's sacred art is its own seventeenth century — Rembrandt's syndics and lovers, Vermeer's milkmaid pouring the same milk for four hundred years, Hals' laughter. A ten-year renovation finished in 2013 stripped the interior back to Cuypers' colors and confirmed what locals suspected: there is no better-lit room in Europe than the one where the militia marches out. Cyclists ride through a tunnel underneath the museum. The paintings don't mind; they're Dutch." },

"musee-dorsay": {
  hook: "The train station Impressionism pulled into",
  founded: "1986",
  essay: "The Gare d'Orsay opened for the 1900 World's Fair — a Beaux-Arts station so beautiful painters complained it looked like a palais des beaux-arts — and by 1939 its platforms were too short for modern trains. It rotted grandly for decades, dodged demolition, and in 1986 reopened as the missing link of French museums: everything between the Louvre's old masters and the Pompidou's moderns, 1848 to 1914, under one iron-and-glass sky. It is, in effect, the home stadium of Impressionism — Monet's stations and cathedrals, Cézanne's card players, Van Gogh's last months — hung in a building that is itself the century's great subject: industry, light, speed. The giant clock still runs. Stand behind its glass face, look out at the Seine, and you're inside the exact view the movement was invented to catch." },

"tate-modern": {
  hook: "A power station running on art now",
  founded: "2000",
  essay: "For most of a century Bankside power station burned oil across the river from St Paul's; in 2000, Herzog & de Meuron kept the turbine hall's cathedral-scale emptiness and plugged in a different current. The gamble — that London wanted a museum of modern art the size of heavy industry — paid off instantly: Tate Modern became the most visited modern-art museum in the world, and the Turbine Hall commissions turned contemporary art into public spectacle on the scale of weather. Its most sacred room is its dimmest: Rothko's Seagram murals, given by the painter on the condition they hang together, in low light, forever — a chapel inside the machine. The chimney still stands. The smoke is gone; the energy output, measurably, is not." },

"nasjonalmuseet-oslo": {
  hook: "Norway's memory, under one new roof",
  founded: "1837",
  essay: "Norway collected for nearly two centuries before deciding, in 2022, to put the whole national memory — art, architecture, design — under one slate-grey roof by the Oslofjord, instantly the largest art museum in the Nordics. The building is deliberately quiet: long grey halls, then a glowing marble light-hall floating on top like a lantern. The reason the world comes is one room deep in the paintings floor, where The Scream hangs beside Madonna and The Sick Child — the sickroom, the bridge and the bedroom of Norway's greatest export in a single sweep of wall. Munch bequeathed his estate to Oslo, and the city split the inheritance: the Munch Museum got the archive; the national collection keeps the icons. Between them, one mid-sized capital holds modern anxiety's complete works." },

"guggenheim-ny": {
  hook: "The spiral built for spiritual abstraction",
  founded: "1939",
  essay: "It began as the Museum of Non-Objective Painting — a mining heir's collection of Kandinskys hung low on grey velvet walls while Bach played, curated by the mystical Baroness Hilla Rebay, who believed abstraction was literally spiritual training. Then Frank Lloyd Wright built the faith its temple: a white concrete spiral on Fifth Avenue, finished in 1959, six months after his death and two months after Guggenheim artists petitioned that the tilted ramp would ruin their pictures. The building won the argument by becoming the collection's one un-loanable masterpiece. The protocol is famous: elevator to the top, drift down the ramp, the whole museum unspooling as one continuous thought — which is, when the walls are covered in Kandinsky's circles and improvisations, exactly what the Baroness had in mind." },

"uffizi": {
  hook: "The offices where the Renaissance filed itself",
  founded: "1581",
  essay: "Uffizi means 'offices' — Vasari built the U-shaped block in the 1560s for Medici bureaucrats, and the family soon began storing its art in the corridor upstairs, which is how the world's first great museum came to have the floor plan of a civil service. Its true founding document came later and remains unbeaten: in 1743 Anna Maria Luisa, the last Medici, willed everything to Florence on the condition that none of it ever leave the city. One clause, and Florence became permanent. The corridor logic survives — you walk the Renaissance in order, Giotto to Leonardo's Annunciation to Michelangelo's only panel painting — until the rooms detonate: Botticelli's Venus, and Artemisia's Judith mid-stroke, hung in the city that taught her to read. Summer queues are biblical. Go anyway; go early." },

"van-gogh-museum": {
  hook: "The family attic, promoted to shrine",
  founded: "1973",
  essay: "When Vincent died unsold and Theo followed six months later, the paintings — hundreds of them — became the property of a widow with a small child. Johanna van Gogh-Bonger spent her life turning that attic inheritance into a reputation, and her son, an engineer who grew up with the Sunflowers over the sofa, turned the reputation into a museum: the family collection passed to the Dutch state on condition it stay together, and the doors opened in 1973. The result is unlike any other single-artist museum — some two hundred paintings, five hundred drawings and the letters, arranged so you walk the ten-year career like a life: potato-dark Holland upstairs into Arles yellow, then the asylum, then the crows. It is Amsterdam's most visited museum and statistically its youngest crowd. The line moves; the letters wait." },

"art-institute-chicago": {
  hook: "Bronze lions, borrowed light, Bertha's Monets",
  founded: "1879",
  essay: "Chicago rebuilt itself after the Great Fire with a certain velocity, and its museum kept pace: founded in 1879, installed behind two bronze lions on Michigan Avenue by 1893, and stocked by the city's new fortunes with what Paris considered unsellable. Bertha Palmer, hotel royalty, bought Monets by the dozen when respectable taste said otherwise — which is why the Art Institute's grainstacks and the great Impressionist rooms rival France's own. It has a habit of owning the picture everyone can already see with their eyes closed: Seurat's Sunday afternoon, Hopper's night diner, Grant Wood's pitchfork couple. And it shares a name and a building with its art school, whose alumni keep ending up on the walls. A museum with the Midwest's particular confidence: unshowy about being world class, lions notwithstanding." },

"centre-pompidou": {
  hook: "The museum built inside-out",
  founded: "1977",
  essay: "President Pompidou wanted Paris back at the centre of modern art; the competition jury picked two unknowns, Renzo Piano and Richard Rogers, who turned the building inside-out — structure, ducts and escalators worn on the facade, color-coded like a diagram: blue for air, green for water, red for people. Paris was scandalized on schedule and converted on schedule. Inside sits Europe's largest modern collection, its abstraction wing anchored by Kandinsky's own estate — Nina's bequest — from the first claimed abstract watercolor to the Bauhaus geometries. The piazza out front, sloped like a beach for fire-eaters and philosophy, may be the building's real masterpiece. Currently the pipes are getting their mid-life overhaul: the museum is closed for a years-long renovation while the collection tours — the inside-out building, briefly turned outside-in." }
};
