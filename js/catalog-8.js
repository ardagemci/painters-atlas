/* PIGMENT — artwork catalog 8 (ARTWORK_SCHEMA v1). Batch 05, docs/CATALOG_BATCH_05.md.

   The same inbound-gravity ranking as Batches 03 and 04, re-run. Two things
   about this run are worth recording.

   THE CUT NEEDED NO TIE-BREAK. Batch 04 had to invent one — seven painters tied
   at 11 points on identical signals. This time the whole 11-band (seven) and the
   whole 10-band (five) come to exactly twelve, so the batch boundary falls on a
   score change rather than inside one. Recorded because it will not happen again
   soon and the tie-break precedent still stands for when it does not.

   THE E3 ROSTER ENTERED THE RANKING ON ITS OWN. Guo Xi comes in at 11 points,
   level with Corot and Daumier — not because a batch pushed him but because the
   E3 records gave him real inbound gravity: three taxonomy mentions and edges
   to Fan Kuan and An Gyeon. Shen Zhou, Hasegawa Tōhaku, Abd al-Samad and Fan
   Kuan all now sit in the ranking too. Widening the roster fed the measure that
   selects what to catalogue, which is the first time these threads have closed
   a loop.

   Vasari remains the standing exclusion (docs/CATALOG_BATCH_04.md).

   All 12 are Tier 2 under §8; none is named in js/tier1-artists.js or
   js/lists-1.js. `image.status:"pd"` is a rendering token, not a legal finding
   (§3, OD-5).

   DIMENSIONS were arbitrated against the holder as usual, and the aggregator was
   wrong again on the-third-class-carriage (Wikidata offers 1862 AND 1868; the
   Met says 1864) and on beata-beatrix (Wikidata 1872; Tate c. 1864–70).
   surname-i-humayun carries NO dims: Wikidata's lone 335 cm height with no width
   is a figure about a manuscript, and a height×width pair for an illustrated
   book would be a claim about one folio. */
window.CATALOG = (window.CATALOG || []).concat([

{ id:"portrait-of-omai", tier:2,
  title:"Portrait of Omai",
  artistId:"joshua-reynolds", year:{ display:"1776", sort:1776 },
  movements:["neoclassicism"], techniques:["oil-painting","glazing"], nation:"britain",
  museum:{ id:"national-portrait-gallery-london", name:"National Portrait Gallery", city:"London" },
  dims:"236 × 145.5 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Joshua_Reynolds_-_Portrait_of_Omai.jpg/500px-Joshua_Reynolds_-_Portrait_of_Omai.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Joshua_Reynolds_-_Portrait_of_Omai.jpg", status:"pd" },
  coords:{ F:-88, D:-10, E:15, C:20, M:60 }, coordsSource:"override",
  description:"Mai of Ra'iatea sailed to London on Cook's second voyage and spent two years being introduced to people. Reynolds painted him full-length, barefoot, in flowing white robes, one hand raised, in the pose reserved for aristocrats and generals — and gave a Polynesian man the grandest visual language Britain had. What that generosity was doing, and to whom, is the argument the picture has been having for two hundred and fifty years.",
  notice:["He is painted in the Grand Manner, kept for dukes and generals",
          "The robes and the tattooed hands are Reynolds's arrangement",
          "Bought jointly in 2023 — it alternates between London and Los Angeles"],
  tags:["portrait","monumental-scale","theatrical","golden"] },

{ id:"the-third-class-carriage", tier:2,
  title:"The Third-Class Carriage",
  artistId:"honore-daumier", year:{ display:"1864", sort:1864 },
  movements:["realism"], techniques:["oil-painting"], nation:"france",
  museum:{ id:"met", name:"The Metropolitan Museum of Art", city:"New York" },
  dims:"65.4 × 90.2 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Honor%C3%A9_Daumier%2C_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg/500px-Honor%C3%A9_Daumier%2C_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Honor%C3%A9_Daumier,_The_Third-Class_Carriage_-_The_Metropolitan_Museum_of_Art.jpg", status:"pd" },
  coords:{ F:-80, D:-15, E:30, C:25, M:-10 }, coordsSource:"override",
  description:"Four people on a bench in a railway carriage: an old woman holding a basket, a mother nursing, a boy asleep. Behind them, packed to the back wall, everybody else. Daumier spent his life as a lithographer aiming at politicians, and here the target is nobody — it is simply what third class looked like, painted with the weight normally spent on saints. The old woman's hands are the whole picture.",
  notice:["Nobody in it is doing anything; that is the subject",
          "The rows behind dissolve into brown — deliberately",
          "He made some four thousand lithographs and few finished paintings"],
  tags:["everyday-life","group-scene","quiet","interior"] },

{ id:"beata-beatrix", tier:2,
  title:"Beata Beatrix",
  artistId:"dante-gabriel-rossetti", year:{ display:"c. 1864–1870", sort:1864 },
  movements:["pre-raphaelites","symbolism"], techniques:["oil-painting"], nation:"britain",
  museum:{ id:"tate-britain", name:"Tate Britain", city:"London" },
  dims:"66 × 86.4 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Dante_Gabriel_Rossetti_-_Beata_Beatrix%2C_1864-1870.jpg/500px-Dante_Gabriel_Rossetti_-_Beata_Beatrix%2C_1864-1870.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Dante_Gabriel_Rossetti_-_Beata_Beatrix,_1864-1870.jpg", status:"pd" },
  coords:{ F:-75, D:10, E:25, C:45, M:-15 }, coordsSource:"override",
  description:"Nominally this is Dante's Beatrice at the moment of her death, eyes closed, hands open, a red bird dropping a white poppy into them. It is also Elizabeth Siddal, Rossetti's wife, who died of a laudanum overdose in 1862 — and the poppy is where laudanum comes from. He began it after her death and worked at it for years. A sundial behind her reads nine, the hour Dante gives.",
  notice:["The bird drops a poppy — laudanum, which killed her",
          "The sundial reads nine, the hour of Beatrice's death",
          "Painted after his wife died, from drawings made while she lived"],
  tags:["portrait","mourning","red","quiet"] },

{ id:"the-bridge-at-narni", tier:2,
  title:"The Bridge at Narni",
  artistId:"camille-corot", year:{ display:"1826", sort:1826 },
  movements:["realism"], techniques:["oil-painting","alla-prima"], nation:"france",
  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },
  dims:"34 × 48 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg/500px-Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Le_pont_de_Narni_-_Jean-Baptiste_Camille_Corot_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1613_-_photo_2.jpg", status:"pd" },
  coords:{ F:-80, D:-40, E:45, C:-30, M:-35 }, coordsSource:"override",
  description:"A broken Roman bridge over the Nera, painted outdoors in one go on a small panel, in the hard Italian light of a single afternoon. Corot then went back to the studio and produced the large, correct, tree-framed Salon version — and it is this thirty-four-centimetre sketch that history kept. Everything Impressionism would later insist on is already here: the whole thing decided by where the light falls, and finished before it moved.",
  notice:["Painted on the spot, at a size you could carry home",
          "The Salon version he made from it is politer and duller",
          "The bridge is Roman, and had already been broken for centuries"],
  tags:["landscape","quiet","golden","would-hang"] },

{ id:"reclining-nude-modigliani", tier:2,
  title:"Reclining Nude", worksKey:"Reclining Nude",
  artistId:"amedeo-modigliani", year:{ display:"1917", sort:1917 },
  movements:["expressionism"], techniques:["oil-painting"], nation:"italy",
  museum:{ id:"met", name:"The Metropolitan Museum of Art", city:"New York" },
  dims:"60.6 × 92.7 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg/500px-Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Amedeo_Modigliani_Reclining_Nude_The_Metropolitan_Museum_of_Art.jpg", status:"pd" },
  coords:{ F:-70, D:5, E:40, C:-60, M:-5 }, coordsSource:"override",
  description:"She fills the canvas edge to edge with nowhere to retreat to, eyes shut, in the pose Titian and Goya and Manet had already used — except that they gave the woman a bed, a room and a maid, and Modigliani gives her a cushion and a wall. His only solo exhibition opened in Paris in December 1917 and the police ordered the nudes taken out of the window on the first day.",
  notice:["The pose is Titian's; everything around it has been removed",
          "Police closed his only solo show over these on day one",
          "The face is a carved mask; he sculpted for years"],
  tags:["nude","quiet","golden","would-hang"] },

{ id:"surname-i-humayun", tier:2,
  title:"Surname-i Hümayun", worksKey:"Surname-i Hümayun (Imperial Festival Book)",
  artistId:"nakkas-osman", year:{ display:"1582–1583", sort:1582 },
  movements:["ottoman-miniature"], techniques:["miniature-painting","gouache","gold-leaf"], nation:"turkey",
  museum:{ id:"topkapi-palace-museum", name:"Topkapı Palace Museum", city:"Istanbul" },
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Sueleymaniye_painting_by_Osman.jpg/500px-Sueleymaniye_painting_by_Osman.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Sueleymaniye_painting_by_Osman.jpg", status:"pd" },
  coords:{ F:-70, D:35, E:10, C:15, M:35 }, coordsSource:"override",
  description:"In 1582 Murad III held a circumcision festival for his son that ran for fifty-two days in the Hippodrome, and Nakkaş Osman's workshop painted it — guild by guild, act by act, the whole city processing past the sultan's box. On this page a scale model of the Süleymaniye mosque is being carried past on foot. Nothing recedes and nothing casts a shadow, because the page is a record rather than a window.",
  notice:["Fifty-two days of festival, painted procession by procession",
          "A model of the Süleymaniye mosque, carried past the sultan",
          "No shadows, no vanishing point: a register, not a view"],
  tags:["historical","group-scene","pattern","golden"] },

{ id:"early-spring", tier:2,
  title:"Early Spring",
  artistId:"guo-xi", year:{ display:"1072", sort:1072 },
  movements:["song-landscape"], techniques:["ink-wash","silk-painting"], nation:"china",
  museum:{ id:"national-palace-museum-taipei", name:"National Palace Museum", city:"Taipei" },
  dims:"158.3 × 108.1 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Guo_Xi_-_Early_Spring_%28large%29.jpg/500px-Guo_Xi_-_Early_Spring_%28large%29.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Guo_Xi_-_Early_Spring_(large).jpg", status:"pd" },
  coords:{ F:-55, D:20, E:55, C:20, M:65 }, coordsSource:"override",
  description:"Dated 1072, which for a Chinese painting of this age is itself remarkable. Mist comes off ground that has just thawed, and the rock is built from the curling strokes later painters copied by name; the trees end in the hooked 'crab-claw' branches that are his signature. There is no single place to stand. Guo Xi wrote that a viewer should be able to walk into a landscape, through it and out, and then he painted the demonstration.",
  notice:["Signed and dated 1072, which is rare and load-bearing",
          "The branches end in hooks: his 'crab-claw' trees",
          "Find the temple, the travellers and the fishermen — all tiny"],
  tags:["landscape","monumental-scale","fog","quiet"] },

{ id:"the-ninth-wave", tier:2,
  title:"The Ninth Wave",
  artistId:"ivan-aivazovsky", year:{ display:"1850", sort:1850 },
  movements:["romanticism"], techniques:["oil-painting","glazing"], nation:"armenia",
  museum:{ id:"russian-museum", name:"State Russian Museum", city:"St Petersburg" },
  dims:"221 × 332 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg/500px-Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Hovhannes_Aivazovsky_-_The_Ninth_Wave_-_Google_Art_Project.jpg", status:"pd" },
  coords:{ F:-80, D:85, E:-15, C:-25, M:80 }, coordsSource:"override",
  description:"Survivors of a wreck cling to a mast in the trough before the ninth wave, which sailors held to be the largest of a set. The sun is coming up straight into your eyes through the water, and Aivazovsky painted it in translucent glazes so the light seems to be behind the canvas rather than on it. Three and a third metres wide. He painted the sea some six thousand times and this is the one everyone means.",
  notice:["The sun is glazed, not painted — the light comes from behind",
          "They cling to a mast; the ship has already gone",
          "The ninth wave was sailors' lore: the biggest of any set"],
  tags:["seascape","storm","ecstatic","monumental-scale"] },

{ id:"the-ambassadors", tier:2,
  title:"The Ambassadors",
  artistId:"hans-holbein", year:{ display:"1533", sort:1533 },
  movements:["northern-renaissance"], techniques:["oil-painting","glazing"], nation:"germany",
  museum:{ id:"national-gallery-london", name:"The National Gallery", city:"London" },
  dims:"207 × 209.5 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg/500px-Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Hans_Holbein_the_Younger_-_The_Ambassadors_-_Google_Art_Project.jpg", status:"pd" },
  coords:{ F:-90, D:5, E:35, C:60, M:55 }, coordsSource:"override",
  description:"Two young Frenchmen in London in 1533, with a shelf of instruments between them: globes, a sundial, a lute, a hymn book. Every object is a claim about knowledge, and several of them are wrong on purpose — the lute has a broken string. Then there is the grey smear across the floor. Stand at the right edge and look back along the picture and it resolves into a skull. You cannot see the skull and the men at the same time.",
  notice:["The grey smear is a skull, readable only from the side",
          "A lute string is broken — discord, deliberately placed",
          "The instruments are set to a real date: 11 April 1533"],
  tags:["portrait","interior","monumental-scale","unsettling"] },

{ id:"the-city-leger", tier:1,
  title:"The City", worksKey:"The City",
  artistId:"fernand-leger", year:{ display:"1919", sort:1919 },
  movements:["cubism"], techniques:["oil-painting","flat-color"], nation:"france",
  museum:{ id:"philadelphia-museum-of-art", name:"Philadelphia Museum of Art", city:"Philadelphia" },
  dims:"231.1 × 298.4 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Fernand_L%C3%A9ger%2C_1919%2C_The_City_%28La_Ville%29%2C_oil_on_canvas%2C_231.1_x_298.4_cm%2C_Philadelphia_Museum_of_Art.jpg/500px-Fernand_L%C3%A9ger%2C_1919%2C_The_City_%28La_Ville%29%2C_oil_on_canvas%2C_231.1_x_298.4_cm%2C_Philadelphia_Museum_of_Art.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Fernand_L%C3%A9ger,_1919,_The_City_(La_Ville),_oil_on_canvas,_231.1_x_298.4_cm,_Philadelphia_Museum_of_Art.jpg", status:"pd" },
  coords:{ F:45, D:35, E:70, C:30, M:70 }, coordsSource:"override",
  description:"Léger came out of the trenches in 1917 having spent the war among machinery and men who were not artists, and painted the city as it actually arrives: signage, scaffolding, a staircase, two stencilled figures, a fragment of a letter. Nothing is behind anything else. It is three metres wide and flat as a poster, which is the point — this is the first painting that looks like graphic design, twenty years before there was any.",
  notice:["Stencilled letters, scaffolding and poles, all on one plane",
          "The two figures are the only curves in it",
          "Painted straight out of the war, in which he served at Verdun"],
  tags:["geometry","flatness","monumental-scale","red"] },

{ id:"the-cradle", tier:2,
  title:"The Cradle",
  artistId:"berthe-morisot", year:{ display:"1872", sort:1872 },
  movements:["impressionism"], techniques:["oil-painting"], nation:"france",
  museum:{ id:"musee-dorsay", name:"Musée d'Orsay", city:"Paris" },
  dims:"56 × 46.5 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Berthe_Morisot_008.jpg/500px-Berthe_Morisot_008.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Berthe_Morisot_008.jpg", status:"pd" },
  coords:{ F:-80, D:-55, E:35, C:-20, M:-55 }, coordsSource:"override",
  description:"Morisot's sister Edma watches her sleeping daughter through a veil of white gauze, and the gauze is the picture: a whole canvas organised around a fabric you can see through. Morisot shows a mother looking at a child and declines to make it tender — Edma's hand props her chin, her eyes are steady, and what she is doing is thinking. It hung in the first Impressionist exhibition of 1874 and did not sell.",
  notice:["The veil is the subject, and everything is arranged behind it",
          "Edma is not doting; she is watching, with her chin propped",
          "Shown in the first Impressionist exhibition, 1874. Unsold."],
  tags:["portrait","interior","tender","quiet"] },

{ id:"the-cheat-with-the-ace-of-diamonds", tier:2,
  title:"The Cheat with the Ace of Diamonds",
  artistId:"georges-de-la-tour", year:{ display:"c. 1635", sort:1635 },
  movements:["baroque"], techniques:["oil-painting","chiaroscuro"], nation:"france",
  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },
  dims:"106 × 146 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg/960px-Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Georges_de_La_Tour_-_Cheater_with_the_Ace_of_Diamonds_-_WGA12334.jpg", status:"pd" },
  coords:{ F:-88, D:40, E:10, C:35, M:20 }, coordsSource:"override",
  description:"Four people at a table, and three of them are in on it. The cheat pulls an ace from his belt behind his back while the courtesan and the servant exchange a look over the wine; the rich boy on the right studies his own hand and sees none of it. Every glance in the picture goes somewhere except his. La Tour was forgotten for two and a half centuries and only rediscovered in 1915.",
  notice:["Three people are looking at each other; the mark is not",
          "The ace comes from his belt, behind his back",
          "La Tour vanished from art history until 1915"],
  tags:["group-scene","theatrical","interior","golden"] }

]);
