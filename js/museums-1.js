/* Pigment museum notes — v1 (the "album text" overlay)
   Keyed by venue id from js/venues.js. Venues without notes still get a
   museum page (collection grid, artists, kindred) — the essay block is simply absent.
   Schema: { hook (≤64 chars, the tagline under the name),
             photo ({ src, page } — Commons-hosted building photograph; card cover + page hero),
             founded ("YYYY" display string),
             essay (100–180 words, house voice — history, fame, character;
                    paragraphs split on \n\n) }
   Enforced by tools/validate.jxa.js. */
window.MUSEUM_NOTES = {

"prado": {
  hook: "Goya's workplace, Spain's fever dream",
  founded: "1819",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Museo_del_Prado_2016_%2825185969599%29.jpg/960px-Museo_del_Prado_2016_%2825185969599%29.jpg",
           page:"https://en.wikipedia.org/wiki/Museo_del_Prado" },
  essay: "The Prado isn't a survey of art history; it's the inheritance of three centuries of royal obsession. The Habsburg and Bourbon kings collected the way other dynasties waged war — Philip II hoarding Bosch's nightmares, Philip IV keeping Velázquez down the corridor like a court secret — and in 1819 the crown finally opened the vault. The result is a museum with the deepest bench on earth rather than the widest: more Velázquez, more Goya, more Bosch and Titian than anywhere else, hung dense in a building that still feels like a palace corridor. Its gravitational centre is Las Meninas; its dark heart is the room of Goya's Black Paintings, lifted off the walls of his farmhouse. Madrid treats it less like a museum than a national organ — something between a library and a cathedral." },

"moma": {
  hook: "Where 'modern' became the canon",
  founded: "1929",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/MoMa_NY_USA_1.jpg/960px-MoMa_NY_USA_1.jpg",
           page:"https://en.wikipedia.org/wiki/Museum_of_Modern_Art" },
  essay: "Nine days after the 1929 crash, three formidable collectors — Abby Aldrich Rockefeller, Lillie Bliss and Mary Quinn Sullivan — opened a museum for the art nobody respectable wanted. Its first director, Alfred Barr, was twenty-seven, and his famous flowchart of modernism — Cézanne flowing into Cubism flowing into abstraction — quietly became the textbook the whole world teaches from. That's MoMA's real power: it doesn't just own the modern canon, it wrote it. The Demoiselles d'Avignon and The Starry Night hang here the way constitutional documents sit in archives. The galleries perfected the white cube — walls like blank paper, art as argument — and every museum of modern art since is either an imitation or a rebuttal. New Yorkers complain it's crowded. It is. So is the twentieth century." },

"met": {
  hook: "America's five-thousand-year answer",
  founded: "1870",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Metropolitan_Museum_of_Art_%28The_Met%29_-_Central_Park%2C_NYC.jpg/960px-Metropolitan_Museum_of_Art_%28The_Met%29_-_Central_Park%2C_NYC.jpg",
           page:"https://en.wikipedia.org/wiki/Metropolitan_Museum_of_Art" },
  essay: "The Met was founded by businessmen and civic boosters who owned, at the moment of founding, not a single work of art — just the conviction that a young republic deserved everything, from pharaohs to the day before yesterday. Gilded Age fortunes did the rest, and the result sprawls along Central Park like an empire of its own: arms and armor, a Temple of Dendur in a glass hall, and paintings enough to fill a lifetime of visits. It buys with intent — when Velázquez's Juan de Pareja arrived in 1971 for a record price, the museum called it a portrait of human dignity and meant it. The Met is where America goes to feel continuous with everything; the encyclopedic museum in its most confident, most generous form. Wear comfortable shoes and surrender the plan." },

"louvre": {
  hook: "A palace that surrendered to paintings",
  founded: "1793",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Louvre_Museum_Wikimedia_Commons.jpg/960px-Louvre_Museum_Wikimedia_Commons.jpg",
           page:"https://en.wikipedia.org/wiki/Louvre" },
  essay: "Fortress, then royal palace, then — one revolution later — the property of everyone: the Louvre opened in 1793 with the logic that a republic's citizens had inherited the kings' pictures. Napoleon stuffed it with the plunder of Europe (much went back; the habit of grandeur stayed), and two centuries of curators have made it the largest museum on earth — a building you don't visit so much as triage. Its fame has a face: the Mona Lisa, whose 1911 theft turned a quiet Leonardo into the most famous object humans have made. But the Louvre's actual character lives in its long galleries — Leonardo's smoky enigmas, Vermeer's Lacemaker no bigger than a novel, Caravaggio's rejected Virgin — under I. M. Pei's glass pyramid, which Parisians hated for exactly one decade and now cannot imagine gone." },

"national-gallery-london": {
  hook: "Free to everyone since 1824, on purpose",
  founded: "1824",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Galer%C3%ADa_Nacional%2C_Londres%2C_Inglaterra%2C_2014-08-07%2C_DD_036.JPG/960px-Galer%C3%ADa_Nacional%2C_Londres%2C_Inglaterra%2C_2014-08-07%2C_DD_036.JPG",
           page:"https://en.wikipedia.org/wiki/National_Gallery" },
  essay: "Parliament bought a dead banker's thirty-eight pictures in 1824 and made a decision that still defines the place: the collection would sit in the middle of London, on Trafalgar Square, free — positioned deliberately so that the poor of the East End could reach it as easily as the carriages of the West. Two centuries on it remains one of the great democratic bargains: Van Eyck's Arnolfini Portrait, Turner's Temeraire, Velázquez's Venus and Rembrandt's last self-portrait, all for the price of walking in. Its finest hour was its emptiest — during the Blitz the paintings hid in a Welsh slate mine while one masterpiece a month came back to hang alone, and Londoners queued through air raids to see it. A national gallery that behaves like a public utility: that's the style." },

"national-gallery-dc": {
  hook: "Mellon's gift, with his name left off",
  founded: "1937",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/National_Gallery_of_Art_-_2026_%2855255088792%29.jpg/960px-National_Gallery_of_Art_-_2026_%2855255088792%29.jpg",
           page:"https://en.wikipedia.org/wiki/National_Gallery_of_Art" },
  essay: "Andrew Mellon — banker, treasury secretary, and for a while the most quietly effective collector alive — gave America a national gallery the way you'd endow a constitution: the building, the endowment and his old-master collection, with one condition. His name would appear nowhere on it, so that other collectors would feel it was theirs to fill. It worked; the gifts have never stopped. Under the marble rotunda hangs the only Leonardo painting in the Americas — Ginevra de' Benci, bought from Liechtenstein's princes — alongside Vermeer, Monet's parasol wind, and, in I. M. Pei's angular East Building, the moderns. Like the Smithsonian around it, admission is free, which gives the place its particular American flavor: imperial marble, democratic door policy. Washington argues about everything; nobody argues about this." },

"rijksmuseum": {
  hook: "The nation's attic, rebuilt as a cathedral",
  founded: "1800",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/South_facade_of_the_Rijksmuseum_Amsterdam_%28DSCF0528%29.jpg/960px-South_facade_of_the_Rijksmuseum_Amsterdam_%28DSCF0528%29.jpg",
           page:"https://en.wikipedia.org/wiki/Rijksmuseum" },
  essay: "The Dutch built their national museum the way they built their republic — gradually, pragmatically, and then all at once in Pierre Cuypers' 1885 building, a brick cathedral where the choir was replaced by a painting: the Night Watch hangs at the far end of the Gallery of Honour, precisely where another country would put an altar. That's not an accident; it's a thesis. Holland's sacred art is its own seventeenth century — Rembrandt's syndics and lovers, Vermeer's milkmaid pouring the same milk for four hundred years, Hals' laughter. A ten-year renovation finished in 2013 stripped the interior back to Cuypers' colors and confirmed what locals suspected: there is no better-lit room in Europe than the one where the militia marches out. Cyclists ride through a tunnel underneath the museum. The paintings don't mind; they're Dutch." },

"musee-dorsay": {
  hook: "The train station Impressionism pulled into",
  founded: "1986",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/North_side_of_Orsay_Museum_building%2C_4_August_2007.jpg/960px-North_side_of_Orsay_Museum_building%2C_4_August_2007.jpg",
           page:"https://en.wikipedia.org/wiki/Mus%C3%A9e_d%27Orsay" },
  essay: "The Gare d'Orsay opened for the 1900 World's Fair — a Beaux-Arts station so beautiful painters complained it looked like a palais des beaux-arts — and by 1939 its platforms were too short for modern trains. It rotted grandly for decades, dodged demolition, and in 1986 reopened as the missing link of French museums: everything between the Louvre's old masters and the Pompidou's moderns, 1848 to 1914, under one iron-and-glass sky. It is, in effect, the home stadium of Impressionism — Monet's stations and cathedrals, Cézanne's card players, Van Gogh's last months — hung in a building that is itself the century's great subject: industry, light, speed. The giant clock still runs. Stand behind its glass face, look out at the Seine, and you're inside the exact view the movement was invented to catch." },

"tate-modern": {
  hook: "A power station running on art now",
  founded: "2000",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Tate_Modern_-_Bankside_Power_Station.jpg/960px-Tate_Modern_-_Bankside_Power_Station.jpg",
           page:"https://en.wikipedia.org/wiki/Tate_Modern" },
  essay: "For most of a century Bankside power station burned oil across the river from St Paul's; in 2000, Herzog & de Meuron kept the turbine hall's cathedral-scale emptiness and plugged in a different current. The gamble — that London wanted a museum of modern art the size of heavy industry — paid off instantly: Tate Modern became the most visited modern-art museum in the world, and the Turbine Hall commissions turned contemporary art into public spectacle on the scale of weather. Its most sacred room is its dimmest: Rothko's Seagram murals, given by the painter on the condition they hang together, in low light, forever — a chapel inside the machine. The chimney still stands. The smoke is gone; the energy output, measurably, is not." },

"nasjonalmuseet-oslo": {
  hook: "Norway's memory, under one new roof",
  founded: "1837",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Nye_Nasjonalmuseet_%282022%29_%282%29.jpg/960px-Nye_Nasjonalmuseet_%282022%29_%282%29.jpg",
           page:"https://en.wikipedia.org/wiki/National_Museum_of_Norway" },
  essay: "Norway collected for nearly two centuries before deciding, in 2022, to put the whole national memory — art, architecture, design — under one slate-grey roof by the Oslofjord, instantly the largest art museum in the Nordics. The building is deliberately quiet: long grey halls, then a glowing marble light-hall floating on top like a lantern. The reason the world comes is one room deep in the paintings floor, where The Scream hangs beside Madonna and The Sick Child — the sickroom, the bridge and the bedroom of Norway's greatest export in a single sweep of wall. Munch bequeathed his estate to Oslo, and the city split the inheritance: the Munch Museum got the archive; the national collection keeps the icons. Between them, one mid-sized capital holds modern anxiety's complete works." },

"guggenheim-ny": {
  hook: "The spiral built for spiritual abstraction",
  founded: "1939",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Solomon_R._Guggenheim_Museum_%2848059131351%29.jpg/960px-Solomon_R._Guggenheim_Museum_%2848059131351%29.jpg",
           page:"https://en.wikipedia.org/wiki/Solomon_R._Guggenheim_Museum" },
  essay: "It began as the Museum of Non-Objective Painting — a mining heir's collection of Kandinskys hung low on grey velvet walls while Bach played, curated by the mystical Baroness Hilla Rebay, who believed abstraction was literally spiritual training. Then Frank Lloyd Wright built the faith its temple: a white concrete spiral on Fifth Avenue, finished in 1959, six months after his death and two months after Guggenheim artists petitioned that the tilted ramp would ruin their pictures. The building won the argument by becoming the collection's one un-loanable masterpiece. The protocol is famous: elevator to the top, drift down the ramp, the whole museum unspooling as one continuous thought — which is, when the walls are covered in Kandinsky's circles and improvisations, exactly what the Baroness had in mind." },

"uffizi": {
  hook: "The offices where the Renaissance filed itself",
  founded: "1581",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Piazzale_degli_Uffizi_perspective_view%2C_Florence%2C_Italy%2C_August_2025.jpg/960px-Piazzale_degli_Uffizi_perspective_view%2C_Florence%2C_Italy%2C_August_2025.jpg",
           page:"https://en.wikipedia.org/wiki/Uffizi" },
  essay: "Uffizi means 'offices' — Vasari built the U-shaped block in the 1560s for Medici bureaucrats, and the family soon began storing its art in the corridor upstairs, which is how the world's first great museum came to have the floor plan of a civil service. Its true founding document came later and remains unbeaten: in 1743 Anna Maria Luisa, the last Medici, willed everything to Florence on the condition that none of it ever leave the city. One clause, and Florence became permanent. The corridor logic survives — you walk the Renaissance in order, Giotto to Leonardo's Annunciation to Michelangelo's only panel painting — until the rooms detonate: Botticelli's Venus, and Artemisia's Judith mid-stroke, hung in the city that taught her to read. Summer queues are biblical. Go anyway; go early." },

"van-gogh-museum": {
  hook: "The family attic, promoted to shrine",
  founded: "1973",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Van_Gogh_Museum_7206_rt_HDR.jpg/960px-Van_Gogh_Museum_7206_rt_HDR.jpg",
           page:"https://en.wikipedia.org/wiki/Van_Gogh_Museum" },
  essay: "When Vincent died unsold and Theo followed six months later, the paintings — hundreds of them — became the property of a widow with a small child. Johanna van Gogh-Bonger spent her life turning that attic inheritance into a reputation, and her son, an engineer who grew up with the Sunflowers over the sofa, turned the reputation into a museum: the family collection passed to the Dutch state on condition it stay together, and the doors opened in 1973. The result is unlike any other single-artist museum — some two hundred paintings, five hundred drawings and the letters, arranged so you walk the ten-year career like a life: potato-dark Holland upstairs into Arles yellow, then the asylum, then the crows. It is Amsterdam's most visited museum and statistically its youngest crowd. The line moves; the letters wait." },

"art-institute-chicago": {
  hook: "Bronze lions, borrowed light, Bertha's Monets",
  founded: "1879",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Art_Institute_of_Chicago_Building%2C_Chicago%2C_Illinois_%2811004251406%29.jpg/960px-Art_Institute_of_Chicago_Building%2C_Chicago%2C_Illinois_%2811004251406%29.jpg",
           page:"https://en.wikipedia.org/wiki/Art_Institute_of_Chicago" },
  essay: "Chicago rebuilt itself after the Great Fire with a certain velocity, and its museum kept pace: founded in 1879, installed behind two bronze lions on Michigan Avenue by 1893, and stocked by the city's new fortunes with what Paris considered unsellable. Bertha Palmer, hotel royalty, bought Monets by the dozen when respectable taste said otherwise — which is why the Art Institute's grainstacks and the great Impressionist rooms rival France's own. It has a habit of owning the picture everyone can already see with their eyes closed: Seurat's Sunday afternoon, Hopper's night diner, Grant Wood's pitchfork couple. And it shares a name and a building with its art school, whose alumni keep ending up on the walls. A museum with the Midwest's particular confidence: unshowy about being world class, lions notwithstanding." },

"centre-pompidou": {
  hook: "The museum built inside-out",
  founded: "1977",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/L%C3%BCftungsrohre_Place_George_Pompidou_Paris.jpg/960px-L%C3%BCftungsrohre_Place_George_Pompidou_Paris.jpg",
           page:"https://en.wikipedia.org/wiki/Centre_Pompidou" },
  essay: "President Pompidou wanted Paris back at the centre of modern art; the competition jury picked two unknowns, Renzo Piano and Richard Rogers, who turned the building inside-out — structure, ducts and escalators worn on the facade, color-coded like a diagram: blue for air, green for water, red for people. Paris was scandalized on schedule and converted on schedule. Inside sits Europe's largest modern collection, its abstraction wing anchored by Kandinsky's own estate — Nina's bequest — from the first claimed abstract watercolor to the Bauhaus geometries. The piazza out front, sloped like a beach for fire-eaters and philosophy, may be the building's real masterpiece. Currently the pipes are getting their mid-life overhaul: the museum is closed for a years-long renovation while the collection tours — the inside-out building, briefly turned outside-in." },

/* ——— thin entries: hook + building photo for every holding venue ——— */

"tate-britain": {
  hook: "Turner's bequest keeps the home fires burning",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Tate_Britain_%285822081512%29_%282%29.jpg/960px-Tate_Britain_%285822081512%29_%282%29.jpg",
           page:"https://en.wikipedia.org/wiki/Tate_Britain" } },

"mauritshuis": {
  hook: "A jewel box the size of a townhouse",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Mauritshuis_museum_logo.png/960px-Mauritshuis_museum_logo.png",
           page:"https://en.wikipedia.org/wiki/Mauritshuis" } },

"tretyakov": {
  hook: "Moscow's merchant gift — Russia, wall to wall",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Moscow_05-2012_TretyakovGallery.jpg/960px-Moscow_05-2012_TretyakovGallery.jpg",
           page:"https://en.wikipedia.org/wiki/Tretyakov_Gallery" } },

"munch-museum": {
  hook: "One painter's entire estate, thirteen floors",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/The_new_Munch_Museum_%28white_color_sign%29.jpg/960px-The_new_Munch_Museum_%28white_color_sign%29.jpg",
           page:"https://en.wikipedia.org/wiki/Munch_Museum" } },

"hermitage": {
  hook: "An empress's habit that outgrew a palace",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/5174-3._St._Petersburg._Greater_Hermitage.jpg/960px-5174-3._St._Petersburg._Greater_Hermitage.jpg",
           page:"https://en.wikipedia.org/wiki/Hermitage_Museum" } },

"sistine-chapel": {
  hook: "The ceiling that redefined ambition",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Sistina-interno.jpg/960px-Sistina-interno.jpg",
           page:"https://en.wikipedia.org/wiki/Sistine_Chapel" } },

"belvedere": {
  hook: "A prince's summer palace, Vienna's gold vault",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Palacio_Belvedere%2C_Viena%2C_Austria%2C_2020-02-01%2C_DD_93-95_HDR.jpg/960px-Palacio_Belvedere%2C_Viena%2C_Austria%2C_2020-02-01%2C_DD_93-95_HDR.jpg",
           page:"https://en.wikipedia.org/wiki/Belvedere%2C_Vienna" } },

"galleria-borghese": {
  hook: "A cardinal's pleasure villa, still showing off",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Galleria_Borghese_-_logo_%28Italy%2C_2022-%29.svg/960px-Galleria_Borghese_-_logo_%28Italy%2C_2022-%29.svg.png",
           page:"https://en.wikipedia.org/wiki/Galleria_Borghese" } },

"kimbell-art-museum": {
  hook: "Louis Kahn's silver light over old masters",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Kimbell_Art_Museum_Highsmith.jpg/960px-Kimbell_Art_Museum_Highsmith.jpg",
           page:"https://en.wikipedia.org/wiki/Kimbell_Art_Museum" } },

"isabella-stewart-gardner": {
  hook: "A palazzo in Boston; two frames still empty",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/IsabellaStewartGardenerMuseumMainLobby.jpg/960px-IsabellaStewartGardenerMuseumMainLobby.jpg",
           page:"https://en.wikipedia.org/wiki/Isabella_Stewart_Gardner_Museum" } },

"courtauld-gallery": {
  hook: "A bank of Impressionism in Somerset House",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Coultauld_Galleries.jpg/960px-Coultauld_Galleries.jpg",
           page:"https://en.wikipedia.org/wiki/Courtauld_Gallery" } },

"getty": {
  hook: "Oil money on a hilltop, open to all",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Aerial_Getty_Museum.jpg/960px-Aerial_Getty_Museum.jpg",
           page:"https://en.wikipedia.org/wiki/Getty_Center" } },

"philadelphia-museum-of-art": {
  hook: "The temple on the hill with the famous steps",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Philadelphia_Museum_of_Art_2005.jpg/960px-Philadelphia_Museum_of_Art_2005.jpg",
           page:"https://commons.wikimedia.org/wiki/File:Philadelphia_Museum_of_Art_2005.jpg" } },

"sfmoma": {
  hook: "The West Coast's modern engine",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/2017_SFMOMA_from_Yerba_Buena_Gardens.jpg/960px-2017_SFMOMA_from_Yerba_Buena_Gardens.jpg",
           page:"https://en.wikipedia.org/wiki/San_Francisco_Museum_of_Modern_Art" } },

"reina-sofia": {
  hook: "Guernica's fortress",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Museo_Nacional_Centro_de_Arte_Reina_Sof%C3%ADa_logo.svg/960px-Museo_Nacional_Centro_de_Arte_Reina_Sof%C3%ADa_logo.svg.png",
           page:"https://en.wikipedia.org/wiki/Museo_Nacional_Centro_de_Arte_Reina_Sof%C3%ADa" } },

"museo-dolores-olmedo": {
  hook: "Frida and Diego, among the peacocks",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Museo_Dolores_Olmedo%2C_Xochimilco%2C_Ciudad_de_M%C3%A9xico_-_Entrada.jpg/960px-Museo_Dolores_Olmedo%2C_Xochimilco%2C_Ciudad_de_M%C3%A9xico_-_Entrada.jpg",
           page:"https://en.wikipedia.org/wiki/Museo_Dolores_Olmedo" } },

"buffalo-akg": {
  hook: "America's oldest taste for the newest art",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/2024.10.10_AKGCampusExteriorDronePhotos-1001.jpg/960px-2024.10.10_AKGCampusExteriorDronePhotos-1001.jpg",
           page:"https://en.wikipedia.org/wiki/Buffalo_AKG_Art_Museum" } },

"san-luigi-dei-francesi": {
  hook: "Drop a coin in the box; Caravaggio lights up",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/%C3%89glise_San_Luigi_Francesi_-_Rome_%28IT62%29_-_2021-08-28_-_2.jpg/960px-%C3%89glise_San_Luigi_Francesi_-_Rome_%28IT62%29_-_2021-08-28_-_2.jpg",
           page:"https://en.wikipedia.org/wiki/San_Luigi_dei_Francesi" } },

"musee-marmottan": {
  hook: "Where Impression, Sunrise lives up to its name",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Mus%C3%A9e_Marmottan_Monet_logo.svg/960px-Mus%C3%A9e_Marmottan_Monet_logo.svg.png",
           page:"https://en.wikipedia.org/wiki/Mus%C3%A9e_Marmottan_Monet" } },

"orangerie": {
  hook: "Two oval rooms, one endless pond",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Mus%C3%A9e_de_l%E2%80%99Orangerie_exterior.JPG/960px-Mus%C3%A9e_de_l%E2%80%99Orangerie_exterior.JPG",
           page:"https://en.wikipedia.org/wiki/Mus%C3%A9e_de_l'Orangerie" } },

"kode-bergen": {
  hook: "Norway's west-coast salon",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/BERGEN_Norway_Lille_Lungeg%C3%A5rdsvannet_KODE_Art_Museum_Kunsthall_Grieghallen_Foreningsgaten_Nyg%C3%A5rdsg._etc_View_from_Mount_Floyen_2019-08-28_by_Forbes_Johnston_Flickr_Some_rights_reserved.jpg/960px-thumbnail.jpg",
           page:"https://commons.wikimedia.org/wiki/File:BERGEN_Norway_Lille_Lungeg%C3%A5rdsvannet_KODE_Art_Museum_Kunsthall_Grieghallen_Foreningsgaten_Nyg%C3%A5rdsg._etc_View_from_Mount_Floyen_2019-08-28_by_Forbes_Johnston_Flickr_Some_rights_reserved.jpg" } },

"oslo-university-aula": {
  hook: "Munch's sunrise over the lecterns" },

"palazzo-barberini": {
  hook: "Baroque Rome's family palace, now everyone's",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Palazzo_Barberini_-_esterno.jpg/960px-Palazzo_Barberini_-_esterno.jpg",
           page:"https://en.wikipedia.org/wiki/Palazzo_Barberini" } },

"vatican-museums": {
  hook: "The popes' collection, nine miles of it",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Musei_vaticani_Coat_of_Arms.svg/960px-Musei_vaticani_Coat_of_Arms.svg.png",
           page:"https://en.wikipedia.org/wiki/Vatican_Museums" } },

"pio-monte-della-misericordia": {
  hook: "Mercy, on permanent view since 1607",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Logo_Pio_Monte_della_Misericordia_Napoli.svg/960px-Logo_Pio_Monte_della_Misericordia_Napoli.svg.png",
           page:"https://en.wikipedia.org/wiki/Pio_Monte_della_Misericordia" } },

"st-johns-co-cathedral": {
  hook: "Caravaggio's only signature lives here",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/St_John%27s_Co-Cathedral%2C_Valletta_001.jpg/960px-St_John%27s_Co-Cathedral%2C_Valletta_001.jpg",
           page:"https://en.wikipedia.org/wiki/St_John's_Co-Cathedral" } },

"kenwood-house": {
  hook: "A country house casually holding a late Rembrandt",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Kenwood_House_2.jpg/960px-Kenwood_House_2.jpg",
           page:"https://en.wikipedia.org/wiki/Kenwood_House" } },

"lazaro-galdiano": {
  hook: "A collector's mansion, Goya's witches upstairs",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Museo_L%C3%A1zaro_Galdiano_%28Madrid%29_02.jpg/960px-Museo_L%C3%A1zaro_Galdiano_%28Madrid%29_02.jpg",
           page:"https://en.wikipedia.org/wiki/L%C3%A1zaro_Galdiano_Museum" } },

"minneapolis-institute-of-art": {
  hook: "Midwestern marble, free since day one",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Mia_minneapolis_logo.svg/960px-Mia_minneapolis_logo.svg.png",
           page:"https://en.wikipedia.org/wiki/Minneapolis_Institute_of_Art" } },

"kroller-muller": {
  hook: "Van Goghs in a national forest",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Entrance_Kr%C3%B6ller-M%C3%BCller_Museum.JPG/960px-Entrance_Kr%C3%B6ller-M%C3%BCller_Museum.JPG",
           page:"https://en.wikipedia.org/wiki/Kr%C3%B6ller-M%C3%BCller_Museum" } },

"yale-university-art-gallery": {
  hook: "The campus museum that outgrew the campus",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Yale_University_Art_Gallery_exterior.jpg/960px-Yale_University_Art_Gallery_exterior.jpg",
           page:"https://en.wikipedia.org/wiki/Yale_University_Art_Gallery" } },

"secession-vienna": {
  hook: "To every age its art — under the golden cabbage",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Secession_2016%2C_Vienna.jpg/960px-Secession_2016%2C_Vienna.jpg",
           page:"https://en.wikipedia.org/wiki/Secession_Building" } },

"wien-museum": {
  hook: "Vienna, explained by Vienna",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Wien_Museum_Neu.jpg/960px-Wien_Museum_Neu.jpg",
           page:"https://en.wikipedia.org/wiki/Vienna_Museum" } },

"mak-vienna": {
  hook: "Where ornament was never a crime",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Wien_01_Museum_f%C3%BCr_angewandte_Kunst_a.jpg/960px-Wien_01_Museum_f%C3%BCr_angewandte_Kunst_a.jpg",
           page:"https://en.wikipedia.org/wiki/Museum_of_Applied_Arts%2C_Vienna" } },

"neue-galerie": {
  hook: "Vienna 1900, transplanted to Fifth Avenue",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Neue_Galerie_New_York_Logo.jpg/960px-Neue_Galerie_New_York_Logo.jpg",
           page:"https://en.wikipedia.org/wiki/Neue_Galerie_New_York" } },

"leopold-museum": {
  hook: "One doctor's Schiele obsession, institutionalized",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Wien_07_Leopold_Museum_a.jpg/960px-Wien_07_Leopold_Museum_a.jpg",
           page:"https://en.wikipedia.org/wiki/Leopold_Museum" } },

"k20-dusseldorf": {
  hook: "The Rhineland's black box for modern paint",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Bild_K20_aktuell.jpg/960px-Bild_K20_aktuell.jpg",
           page:"https://en.wikipedia.org/wiki/Kunstsammlung_Nordrhein-Westfalen" } },

"kunsthistorisches": {
  hook: "The Habsburgs' trophy hall",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/AT_13763_Exterior_of_the_Kunsthistorisches_Museum%2C_Vienna-4.jpg/960px-AT_13763_Exterior_of_the_Kunsthistorisches_Museum%2C_Vienna-4.jpg",
           page:"https://commons.wikimedia.org/wiki/File:AT_13763_Exterior_of_the_Kunsthistorisches_Museum,_Vienna-4.jpg" } },

"stadel": {
  hook: "A merchant's Frankfurt, from Holbein to now",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/St%C3%A4del-Museum.svg/960px-St%C3%A4del-Museum.svg.png",
           page:"https://en.wikipedia.org/wiki/St%C3%A4del" } },

"scottish-national-gallery": {
  hook: "Edinburgh's neoclassical treasure chest",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Scottish_National_Gallery_-_aerial_-_2025-04-19_01.jpg/960px-Scottish_National_Gallery_-_aerial_-_2025-04-19_01.jpg",
           page:"https://en.wikipedia.org/wiki/Scottish_National_Gallery" } },

"doria-pamphilj": {
  hook: "A pope stares down his family's corridor",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Palazzo_Doria_Pamphilj.jpg/960px-Palazzo_Doria_Pamphilj.jpg",
           page:"https://en.wikipedia.org/wiki/Galleria_Doria_Pamphilj" } },

"mfa-boston": {
  hook: "Boston's universal survey, Turner's storm included",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Museum_of_Fine_Arts%2C_Boston_%2854954248311%29.jpg/960px-Museum_of_Fine_Arts%2C_Boston_%2854954248311%29.jpg",
           page:"https://en.wikipedia.org/wiki/Museum_of_Fine_Arts%2C_Boston" } },

"schloss-weissenstein": {
  hook: "A baroque palace hiding a teenage Artemisia",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Aerial_image_of_the_Schloss_Wei%C3%9Fenstein.jpg/960px-Aerial_image_of_the_Schloss_Wei%C3%9Fenstein.jpg",
           page:"https://en.wikipedia.org/wiki/Schloss_Wei%C3%9Fenstein" } },

"capodimonte": {
  hook: "A Bourbon hunting lodge stuffed with Caravaggisti",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/ReggiaCapodimonte.JPG/960px-ReggiaCapodimonte.JPG",
           page:"https://en.wikipedia.org/wiki/Museo_di_Capodimonte" } },

"detroit-institute-of-arts": {
  hook: "The museum a city refused to sell",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Detroit_Institute_of_Arts_August_2011_01.jpg/960px-Detroit_Institute_of_Arts_August_2011_01.jpg",
           page:"https://commons.wikimedia.org/wiki/File:Detroit_Institute_of_Arts_August_2011_01.jpg" } },

"czartoryski": {
  hook: "A Polish princess's Leonardo, against all odds",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Czartoryski_Palace%2C_17-19_%C5%9Bwi%C4%99tego_Jana_street%2C_Old_Town%2C_Krak%C3%B3w%2C_Poland.jpg/960px-Czartoryski_Palace%2C_17-19_%C5%9Bwi%C4%99tego_Jana_street%2C_Old_Town%2C_Krak%C3%B3w%2C_Poland.jpg",
           page:"https://en.wikipedia.org/wiki/Czartoryski_Museum" } },

"accademia-venice": {
  hook: "Venice keeps its own receipts",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Accademia_%28Venice%29.jpg/960px-Accademia_%28Venice%29.jpg",
           page:"https://en.wikipedia.org/wiki/Gallerie_dell'Accademia" } },

"santa-maria-delle-grazie": {
  hook: "A refectory wall the world queues for",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Santa_Maria_delle_Grazie_Milan_2013.jpg/960px-Santa_Maria_delle_Grazie_Milan_2013.jpg",
           page:"https://en.wikipedia.org/wiki/Santa_Maria_delle_Grazie%2C_Milan" } },

"st-peters-basilica": {
  hook: "The largest church, the tenderest marble",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Basilica_di_San_Pietro_in_Vaticano_September_2015-1a.jpg/960px-Basilica_di_San_Pietro_in_Vaticano_September_2015-1a.jpg",
           page:"https://en.wikipedia.org/wiki/St._Peter's_Basilica" } },

"accademia-florence": {
  hook: "The hallway where David waits",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/David_at_the_Galleria_dell%27Accademia_%2861351%29.jpg/960px-David_at_the_Galleria_dell%27Accademia_%2861351%29.jpg",
           page:"https://en.wikipedia.org/wiki/Galleria_dell'Accademia" } },

"mnaa-lisbon": {
  hook: "Portugal's green-shuttered treasury",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Museu_Nacional_de_Arte_Antiga_logo.png/960px-Museu_Nacional_de_Arte_Antiga_logo.png",
           page:"https://en.wikipedia.org/wiki/National_Museum_of_Ancient_Art" } },

"st-bavo-cathedral": {
  hook: "Home of the most-stolen altarpiece on earth",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Gent-Sint-Baafskathedraal_vom_Belfried_aus_gesehen.jpg/960px-Gent-Sint-Baafskathedraal_vom_Belfried_aus_gesehen.jpg",
           page:"https://en.wikipedia.org/wiki/Saint_Bavo's_Cathedral%2C_Ghent" } },

"groeningemuseum": {
  hook: "Bruges' painters, still in Bruges",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Brugge_-_Dijver_12_-Voormalig_poortgebouw_van_de_proosdij_van_Onze-Lieve-Vrouw%2C_heden_ingang_van_het_Groeningemuseum_-_82339.jpg/960px-Brugge_-_Dijver_12_-Voormalig_poortgebouw_van_de_proosdij_van_Onze-Lieve-Vrouw%2C_heden_ingang_van_het_Groeningemuseum_-_82339.jpg",
           page:"https://en.wikipedia.org/wiki/Groeningemuseum" } },

"gemaldegalerie-berlin": {
  hook: "Old masters, hung with German rigor",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Berlin_Kulturforum_2002a.jpg/960px-Berlin_Kulturforum_2002a.jpg",
           page:"https://en.wikipedia.org/wiki/Gem%C3%A4ldegalerie%2C_Berlin" } },

"masp": {
  hook: "Paintings on glass easels above São Paulo",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Novo_MASP.jpg/960px-Novo_MASP.jpg",
           page:"https://en.wikipedia.org/wiki/S%C3%A3o_Paulo_Museum_of_Art" } },

"baltimore-museum-of-art": {
  hook: "The Cone sisters' Matisse hoard",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Baltimore_Museum_of_Art_entrance.jpg/960px-Baltimore_Museum_of_Art_entrance.jpg",
           page:"https://commons.wikimedia.org/wiki/File:Baltimore_Museum_of_Art_entrance.jpg" } },

"royal-collection": {
  hook: "The king's pictures, in a working castle",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Windsor_Castle_at_Sunset_-_Nov_2006.jpg/960px-Windsor_Castle_at_Sunset_-_Nov_2006.jpg",
           page:"https://en.wikipedia.org/wiki/Windsor_Castle" } },

"barnes-foundation": {
  hook: "One stubborn doctor's hang, preserved verbatim",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Barnes_Foundation_%2853574516274%29.jpg/960px-Barnes_Foundation_%2853574516274%29.jpg",
           page:"https://en.wikipedia.org/wiki/Barnes_Foundation" } },

"pushkin-museum": {
  hook: "Moscow's window on the West",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Gmii.jpg/960px-Gmii.jpg",
           page:"https://en.wikipedia.org/wiki/Pushkin_Museum" } },

"musee-picasso-paris": {
  hook: "Paid in paintings: the estate-tax museum",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/H%C3%B4tel_Sal%C3%A9.JPG/960px-H%C3%B4tel_Sal%C3%A9.JPG",
           page:"https://en.wikipedia.org/wiki/Mus%C3%A9e_Picasso_Paris" } },

"museu-picasso-barcelona": {
  hook: "The teenage Picasso, kept by his city",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Museu_Picasso_Barcelona.jpg/960px-Museu_Picasso_Barcelona.jpg",
           page:"https://en.wikipedia.org/wiki/Museu_Picasso" } },

"thyssen-bornemisza": {
  hook: "Two generations of one family's eye",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Site_of_the_Retiro_and_the_Prado_in_Madrid_49_%2829684554308%29.jpg/960px-Site_of_the_Retiro_and_the_Prado_in_Madrid_49_%2829684554308%29.jpg",
           page:"https://en.wikipedia.org/wiki/Thyssen-Bornemisza_Museum" } },

"kelvingrove": {
  hook: "Glasgow's red sandstone cabinet of everything",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Kelvingrove_Art_Gallery_and_Museum_-_aerial_-_2025-04-17.jpg/960px-Kelvingrove_Art_Gallery_and_Museum_-_aerial_-_2025-04-17.jpg",
           page:"https://en.wikipedia.org/wiki/Kelvingrove_Art_Gallery_and_Museum" } },

"dali-museum-florida": {
  hook: "Dalí under a geodesic glass eye, in Florida",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/St._Pete_Dali_Museum03.jpg/960px-St._Pete_Dali_Museum03.jpg",
           page:"https://en.wikipedia.org/wiki/Salvador_Dal%C3%AD_Museum" } },

"museo-arte-moderno-mexico": {
  hook: "Mexican modernism under Chapultepec trees",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Museo_de_Arte_Moderno_DSC0023_%2835557149325%29.jpg/960px-Museo_de_Arte_Moderno_DSC0023_%2835557149325%29.jpg",
           page:"https://en.wikipedia.org/wiki/Museo_de_Arte_Moderno" } },

"harry-ransom-center": {
  hook: "An archive that happens to own Frida",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Harry_ransom_center_2012.jpg/960px-Harry_ransom_center_2012.jpg",
           page:"https://en.wikipedia.org/wiki/Harry_Ransom_Center" } },

"museo-frida-kahlo": {
  hook: "The blue house she was born and died in",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Museo_Frida_Kahlo.JPG/960px-Museo_Frida_Kahlo.JPG",
           page:"https://en.wikipedia.org/wiki/Frida_Kahlo_Museum" } },

"stanley-museum-iowa": {
  hook: "The university that owns a Pollock mural",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Stanley_Museum_of_Art%2C_Burlington_Street_and_Museum_Drive%2C_Iowa_City%2C_IA.jpg/960px-Stanley_Museum_of_Art%2C_Burlington_Street_and_Museum_Drive%2C_Iowa_City%2C_IA.jpg",
           page:"https://en.wikipedia.org/wiki/University_of_Iowa_Stanley_Museum_of_Art" } },

"dallas-museum-art": {
  hook: "Texas scale, encyclopedic appetite",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Dallas_Museum_of_Art_logo.svg/960px-Dallas_Museum_of_Art_logo.svg.png",
           page:"https://en.wikipedia.org/wiki/Dallas_Museum_of_Art" } },

"national-gallery-australia": {
  hook: "Blue Poles, vindicated",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/National_Gallery_from_SW%2C_Canberra_Australia.jpg/960px-National_Gallery_from_SW%2C_Canberra_Australia.jpg",
           page:"https://en.wikipedia.org/wiki/National_Gallery_of_Australia" } },

"moca-la": {
  hook: "LA's contemporary conscience",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Moca-exterior.jpg/960px-Moca-exterior.jpg",
           page:"https://en.wikipedia.org/wiki/Museum_of_Contemporary_Art%2C_Los_Angeles" } },

"whitney": {
  hook: "American art, argued about since 1930",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Gansevoort_Whitney_April_2013_jeh.jpg/960px-Gansevoort_Whitney_April_2013_jeh.jpg",
           page:"https://commons.wikimedia.org/wiki/File:Gansevoort_Whitney_April_2013_jeh.jpg" } },

"rothko-chapel": {
  hook: "Fourteen dark paintings, one octagon of silence",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Rothko_Chapel_-_1_August_2010.jpg/960px-Rothko_Chapel_-_1_August_2010.jpg",
           page:"https://en.wikipedia.org/wiki/Rothko_Chapel" } },

"museum-ludwig": {
  hook: "Chocolate money, pop art, Cologne",
  photo: { src:"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Museum_Ludwig_002.jpg/960px-Museum_Ludwig_002.jpg",
           page:"https://en.wikipedia.org/wiki/Museum_Ludwig" } }
};
