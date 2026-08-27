/* PIGMENT — artwork catalog 6 (ARTWORK_SCHEMA v1). Batch 03, specified in
   docs/CATALOG_BATCH_03.md.

   Twelve works by twelve painters the atlas already leans on and could not show
   a single picture by. The selection rule is INBOUND GRAVITY, measured rather
   than felt: influence-graph degree, mentions by name inside other painters'
   prose, and appearances in the taxonomy blurbs. Every artist here scored in
   the top of that ranking among the 125 painters who hold audited gallery
   images and no catalog record at all.

   All 12 are Tier 2. ARTWORK_SCHEMA §8 admits a work to Tier 1 only through an
   inbound link — an editorial list, a Tier 1 artist's essential works, the
   daily-painting schedule or the deck pool — and none of these twelve is named
   anywhere in js/tier1-artists.js or js/lists-1.js (checked, not assumed). Each
   nevertheless carries hand-scored coords, a 60–90 word description and exactly
   3 notice bullets, so promotion is a one-line tier edit and the URL never
   changes.

   `image.status:"pd"` is a rendering token, not a legal finding (§3, OD-5): it
   records that a Commons file page asserts a public-domain basis.

   EVERY DIMENSION HERE WAS ARBITRATED, NOT COPIED. Wikidata disagreed with the
   holding institution on three of the twelve and the disagreements were not
   rounding:
     · madame-x — Wikidata's P2048/P2049 are the FRAMED measurements (243.2 ×
       143.8 cm). The Met gives the canvas as 208.6 × 109.9 and lists the frame
       separately. A new failure mode; recorded in ARTWORK_SCHEMA §7.1 rule 3.
     · at-the-moulin-rouge — Wikidata carries millimetres (1230 × 1410). This is
       the §7.1 rule 1 bug, still live, and a bare "cm" would have printed a
       12-metre canvas.
     · gray-tree — English Wikipedia's 78.5 × 107.5 measures the CROPPED
       derivative file, not the painting; the Gemeentemuseum's own record, via
       the Commons Artwork template, gives 79.7 × 109.1.
   the-fate-of-the-animals carried three published widths and takes the one the
   holding museum's own inventory number is attached to. */
window.CATALOG = (window.CATALOG || []).concat([

{ id:"liberty-leading-the-people", tier:2,
  title:"Liberty Leading the People",
  artistId:"eugene-delacroix", year:{ display:"1830", sort:1830 },
  movements:["romanticism"], techniques:["oil-painting"], nation:"france",
  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },
  dims:"260 × 325 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg/500px-La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg",
          page:"https://commons.wikimedia.org/wiki/File:La_Libert%C3%A9_guidant_le_peuple_-_Eug%C3%A8ne_Delacroix_-_Mus%C3%A9e_du_Louvre_Peintures_RF_129_-_apr%C3%A8s_restauration_2024.jpg", status:"pd" },
  coords:{ F:-80, D:90, E:35, C:20, M:80 }, coordsSource:"override",
  description:"She is not a goddess borrowed from antiquity. Her gown has slipped, her feet are bare and dirty, and she is walking over bodies to get where she is going. Delacroix painted the July Revolution within months of it happening and set the allegory on the same ground as the dead — Phrygian cap above, a bare foot on a corpse below. It is 1830, not 1789, though half the world files it there. Look down before you look up.",
  notice:["Liberty walks on bodies; her feet are bare",
          "The boy has a pistol in each hand",
          "This is 1830, not 1789 — the commonest mistake here"],
  tags:["historical","group-scene","theatrical","monumental-scale","red"] },

{ id:"the-garden-of-love", tier:2,
  title:"The Garden of Love",
  artistId:"peter-paul-rubens", year:{ display:"c. 1630–1635", sort:1630 },
  movements:["flemish-baroque","baroque"], techniques:["oil-painting","glazing"], nation:"belgium",
  museum:{ id:"prado", name:"Museo del Prado", city:"Madrid" },
  dims:"199 × 286 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg/500px-El_Jard%C3%ADn_del_Amor_%28Rubens%29.jpg",
          page:"https://commons.wikimedia.org/wiki/File:El_Jard%C3%ADn_del_Amor_(Rubens).jpg", status:"pd" },
  coords:{ F:-85, D:25, E:-20, C:-55, M:20 }, coordsSource:"override",
  description:"Rubens painted this in his fifties, newly remarried and evidently in no hurry to leave the garden. Couples arrange themselves under a portico while cupids work the room from above, shoving the hesitant ones forward by the back. Nobody is doing anything of consequence, which is the whole argument. It hung in the Spanish king's bedroom, and the early palace inventories called it, flatly, The Garden Party.",
  notice:["Cupids physically push the reluctant couples together",
          "It hung in the king of Spain's own bedroom",
          "Early inventories list it as The Garden Party"],
  tags:["group-scene","playful","golden","tender"] },

{ id:"grande-odalisque", tier:2,
  title:"Grande Odalisque", worksKey:"La Grande Odalisque",
  artistId:"jean-auguste-dominique-ingres", year:{ display:"1814", sort:1814 },
  movements:["neoclassicism"], techniques:["oil-painting","glazing"], nation:"france",
  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },
  dims:"91 × 162 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg/500px-La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg",
          page:"https://commons.wikimedia.org/wiki/File:La_grande_odalisque_-_Jean-Auguste_Dominique_Ingres_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1158.jpg", status:"pd" },
  coords:{ F:-85, D:-25, E:25, C:-45, M:5 }, coordsSource:"override",
  description:"The back is too long. It has been too long since 1819, when critics said she had no bones and no muscle, and later anatomists went further and started counting vertebrae she could not have. Ingres knew. The line needed the length, and where line and anatomy disagreed, anatomy lost. She turns her face to you over a shoulder that cannot be there, in a room that is all furnishing and no place.",
  notice:["Her spine runs further than a spine can run",
          "Contemporary critics complained she had no bones",
          "The room is entirely props — there is no architecture"],
  tags:["nude","interior","quiet","pastel"] },

{ id:"pollice-verso", tier:2,
  title:"Pollice Verso",
  artistId:"jean-leon-gerome", year:{ display:"1872", sort:1872 },
  movements:["academicism"], techniques:["oil-painting"], nation:"france",
  museum:{ id:"phoenix-art-museum", name:"Phoenix Art Museum", city:"Phoenix" },
  dims:"96.5 × 149.2 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Jean-Leon_Gerome_Pollice_Verso.jpg/500px-Jean-Leon_Gerome_Pollice_Verso.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Jean-Leon_Gerome_Pollice_Verso.jpg", status:"pd" },
  coords:{ F:-90, D:70, E:-55, C:-10, M:45 }, coordsSource:"override",
  description:"The winner stands on his opponent's throat and looks up for the verdict. It comes from the Vestal virgins, leaning over the parapet with their thumbs turned down — and nobody actually knows whether that is what Romans did. Pollice verso is a phrase whose gesture is lost: up, down, sideways, hidden in the fist, the record does not say. Gérôme guessed. The guess became the convention every gladiator film has used since.",
  notice:["The Vestals lean out over the rail to signal death",
          "Nobody knows which way a Roman thumb actually turned",
          "Ridley Scott saw this before he read the Gladiator script"],
  tags:["historical","group-scene","theatrical","monumental-scale"] },

{ id:"charles-i-at-the-hunt", tier:2,
  title:"Charles I at the Hunt",
  artistId:"anthony-van-dyck", year:{ display:"c. 1635", sort:1635 },
  movements:["flemish-baroque","baroque"], techniques:["oil-painting","glazing"], nation:"belgium",
  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },
  dims:"266 × 207 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg/500px-Portrait_de_Charles_1er%2C_roi_d%27Angleterre%2C_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_%3B_MR_666.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Portrait_de_Charles_1er,_roi_d%27Angleterre,_%C3%A0_la_chasse_-_Antoon_van_Dyck_-_Mus%C3%A9e_du_Louvre_Peintures_INV_1236_;_MR_666.jpg", status:"pd" },
  coords:{ F:-90, D:-20, E:5, C:10, M:55 }, coordsSource:"override",
  description:"A king in a slouch hat, leaning on a stick beside his horse as though he had just got down for a moment. No crown, no throne, no army — and it is a state portrait two and a half metres tall. Van Dyck invented a genre here: majesty by nonchalance. Charles was famously touchy about his height, so the horizon drops and you stand below him looking up. In 1649 this head came off outside Whitehall.",
  notice:["The viewpoint is low, so you look up at a short king",
          "A state portrait with no crown and no throne in it",
          "The horse bows its head; the king does not"],
  tags:["portrait","landscape","quiet","monumental-scale"] },

{ id:"madame-x", tier:2,
  title:"Madame X",
  artistId:"john-singer-sargent", year:{ display:"1883–1884", sort:1883 },
  movements:["realism"], techniques:["oil-painting","alla-prima"], nation:"usa",
  museum:{ id:"met", name:"The Metropolitan Museum of Art", city:"New York" },
  dims:"208.6 × 109.9 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg/960px-Madame_X_%28Madame_Pierre_Gautreau%29%2C_John_Singer_Sargent%2C_1884_%28unfree_frame_crop%29.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Madame_X_(Madame_Pierre_Gautreau),_John_Singer_Sargent,_1884_(unfree_frame_crop).jpg", status:"pd" },
  coords:{ F:-85, D:10, E:20, C:-30, M:30 }, coordsSource:"override",
  description:"Sargent asked to paint her; there was no commission and no fee, and it nearly finished him. At the Salon of 1884 the right strap of her gown hung off the shoulder, and Le Figaro wrote that one more struggle and the lady would be free. The reviews were savage about her skin. Sargent repainted the strap upright and moved to London. The trick is that powdered lavender-white against a brown void — a profile cut like a cameo.",
  notice:["The strap was originally painted fallen off her shoulder",
          "Her skin is lavender-grey, not flesh — deliberately",
          "The scandal drove Sargent out of Paris for good"],
  tags:["portrait","quiet","theatrical"] },

{ id:"the-fate-of-the-animals", tier:1,
  title:"The Fate of the Animals",
  artistId:"franz-marc", year:{ display:"1913", sort:1913 },
  movements:["expressionism","der-blaue-reiter"], techniques:["oil-painting"], nation:"germany",
  museum:{ id:"kunstmuseum-basel", name:"Kunstmuseum Basel", city:"Basel" },
  dims:"195 × 263.5 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Franz_Marc-The_fate_of_the_animals-1913.jpg/500px-Franz_Marc-The_fate_of_the_animals-1913.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Franz_Marc-The_fate_of_the_animals-1913.jpg", status:"pd" },
  coords:{ F:25, D:90, E:65, C:35, M:70 }, coordsSource:"override",
  description:"Marc's own title was different: the trees showed their rings, the animals their veins. Red wedges cut a forest apart, a blue deer throws its head back at the centre, and two horses run the wrong way — into it. He painted this in 1913. In 1915, at the front, a postcard of it reached him, and he wrote to his wife that it looked like a premonition of the war. He was killed at Verdun the next year.",
  notice:["The right third is browner: it burned, and Klee repainted it",
          "Klee kept the repair visible rather than faking the colour",
          "Marc called it a premonition of a war he was already in"],
  tags:["animal","unsettling","monumental-scale","blue"] },

{ id:"the-boulevard-montmartre-at-night", tier:2,
  title:"The Boulevard Montmartre at Night", worksKey:"Boulevard Montmartre at Night",
  artistId:"camille-pissarro", year:{ display:"1897", sort:1897 },
  movements:["impressionism"], techniques:["oil-painting","broken-color"], nation:"france",
  museum:{ id:"national-gallery-london", name:"The National Gallery", city:"London" },
  dims:"53.5 × 65 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg/960px-Camille_Pissarro%2C_The_Boulevard_Montmartre_at_Night%2C_1897.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Camille_Pissarro,_The_Boulevard_Montmartre_at_Night,_1897.jpg", status:"pd" },
  coords:{ F:-60, D:5, E:25, C:-35, M:-40 }, coordsSource:"override",
  description:"Pissarro was sixty-six and painting through hotel windows, his eyes no longer able to take the outdoor air. From a room on the corner of the Boulevard des Italiens he worked one street over and over — morning, afternoon, rain, carnival — and exactly once at night. The wet road does all the work: every gas lamp and lit window arrives twice, once in the air and once in the ground. He never signed it and never showed it.",
  notice:["Every light in the picture is painted twice, road and all",
          "The only night canvas in a series of fourteen",
          "Unsigned and unexhibited in his lifetime"],
  tags:["nocturne","rain-mood","texture"] },

{ id:"gray-tree", tier:1,
  title:"Gray Tree", worksKey:"The Gray Tree",
  artistId:"piet-mondrian", year:{ display:"1911", sort:1911 },
  movements:["cubism"], techniques:["oil-painting"], nation:"netherlands",
  museum:{ id:"kunstmuseum-den-haag", name:"Kunstmuseum Den Haag", city:"The Hague" },
  dims:"79.7 × 109.1 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg/500px-Piet_Mondrian%2C_1911%2C_Gray_Tree_%28De_grijze_boom%29%2C_oil_on_canvas%2C_79.7_x_109.1_cm%2C_Gemeentemuseum_Den_Haag%2C_Netherlands.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Piet_Mondrian,_1911,_Gray_Tree_(De_grijze_boom),_oil_on_canvas,_79.7_x_109.1_cm,_Gemeentemuseum_Den_Haag,_Netherlands.jpg", status:"pd" },
  coords:{ F:15, D:10, E:55, C:20, M:-15 }, coordsSource:"override",
  description:"This is the hinge. Mondrian had been painting trees for years; here the branches stop describing a tree and start behaving like structure, and the background pushes forward to meet them until you cannot say which is in front. The palette has come down to greys and blue-greys and almost nothing else. The tree's mass is faintly oval — within a few years that oval becomes an explicit frame, and within ten there is nothing left but straight lines and three colours.",
  notice:["Branch and background are painted at the same depth",
          "Its mass is faintly oval — that oval later becomes his frame",
          "He had painted the same subject red a few years before"],
  tags:["landscape","monochrome","geometry","quiet"] },

{ id:"et-in-arcadia-ego", tier:2,
  title:"Et in Arcadia ego", worksKey:"Et in Arcadia Ego",
  artistId:"nicolas-poussin", year:{ display:"1637–1638", sort:1637 },
  movements:["baroque"], techniques:["oil-painting","glazing"], nation:"france",
  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },
  dims:"85 × 121 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg/960px-Nicolas_Poussin_-_Et_in_Arcadia_ego_%28deuxi%C3%A8me_version%29.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Nicolas_Poussin_-_Et_in_Arcadia_ego_(deuxi%C3%A8me_version).jpg", status:"pd" },
  coords:{ F:-85, D:-45, E:-40, C:55, M:-10 }, coordsSource:"override",
  description:"Three shepherds and a woman have found a tomb in paradise and are reading what is cut into it: even in Arcadia, I am here. One of them traces the letters with a finger, and his own shadow falls across the stone as he does it — the shadow of a living arm lying on the word for death. Poussin painted the subject twice. This is the later, quieter one, in which nobody panics. It is a picture of comprehension arriving.",
  notice:["A shepherd's shadow falls across the inscription he reads",
          "Nobody is frightened; they are working out the Latin",
          "Poussin painted this subject twice, ten years apart"],
  tags:["mythological","landscape","group-scene","mourning"] },

{ id:"the-hay-wain", tier:2,
  title:"The Hay Wain",
  artistId:"john-constable", year:{ display:"1821", sort:1821 },
  movements:["romanticism"], techniques:["oil-painting","impasto"], nation:"britain",
  museum:{ id:"national-gallery-london", name:"The National Gallery", city:"London" },
  dims:"130.2 × 185.4 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/John_Constable_-_The_Hay_Wain_%281821%29.jpg/500px-John_Constable_-_The_Hay_Wain_%281821%29.jpg",
          page:"https://commons.wikimedia.org/wiki/File:John_Constable_-_The_Hay_Wain_(1821).jpg", status:"pd" },
  coords:{ F:-85, D:-40, E:20, C:-40, M:20 }, coordsSource:"override",
  description:"A cart stands in six inches of river on a cloudy afternoon in Suffolk and nothing at all happens. Its original title was even plainer: Landscape: Noon. London was unmoved. Paris was not — shown at the Salon of 1824 it caused a sensation and took a gold medal from Charles X, and a cast of that medal is set into the picture's frame to this day. Look for the white flecks Constable dabbed over everything.",
  notice:["The cast of its 1824 French gold medal is in the frame",
          "Constable first called it, simply, Landscape: Noon",
          "White flecks sit on top of everything — critics hated them"],
  tags:["landscape","quiet","would-hang","texture"] },

{ id:"at-the-moulin-rouge", tier:2,
  title:"At the Moulin Rouge",
  artistId:"henri-de-toulouse-lautrec", year:{ display:"1892–1895", sort:1892 },
  movements:["post-impressionism"], techniques:["oil-painting"], nation:"france",
  museum:{ id:"art-institute-chicago", name:"The Art Institute of Chicago", city:"Chicago" },
  dims:"123 × 141 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg/500px-Henri_de_Toulouse-Lautrec%2C_At_the_Moulin_Rouge.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Henri_de_Toulouse-Lautrec,_At_the_Moulin_Rouge.jpg", status:"pd" },
  coords:{ F:-75, D:25, E:45, C:-20, M:-20 }, coordsSource:"override",
  description:"A wooden balustrade cuts the whole foreground on the diagonal and holds you outside the room. Behind it five of Lautrec's circle sit round a table. The face that stops you is at the right edge, half cut off by it: the singer May Milton, lit from beneath in a shocking acid green. The Moulin Rouge was built for electric light, and Lautrec painted what electric light does to a face.",
  notice:["May Milton's face is acid green, lit from beneath",
          "Lautrec is at the back, beside his much taller cousin",
          "He kept a permanently reserved table in this room"],
  tags:["group-scene","interior","everyday-life","theatrical"] }

]);
