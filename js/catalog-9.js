/* PIGMENT — artwork catalog 9 (ARTWORK_SCHEMA v1). Batch 06, docs/CATALOG_BATCH_06.md.

   THE LAST RUN OF INBOUND GRAVITY. The Curator's judgement, and it is right: the
   measure has COMPLETED rather than failed. Three batches drained the painters
   the atlas leans on hard, and the ranking has flattened to where a 9 and an 8
   differ by one prose mention — at that resolution it is measuring paragraph
   length, not significance. A fourth flat band would be an arbitrary cut
   pretending to be a reproducible one. docs/CATALOG_BATCH_06.md names the
   successor rule; this file is the last batch selected the old way.

   THE SIGNAL IS PARTLY ENDOGENOUS, AND SAYING SO IS THE POINT. Four of these
   twelve — fan-kuan, shen-zhou, hasegawa-tohaku, abd-al-samad — are painters the
   E3 roster pass added days ago, and two of them score partly on influence edges
   that same pass drew. Batch 05 called this "nothing was pushed"; that is true
   about intent and false about independence. They are shipped here because
   Travelers Among Mountains and Streams, Pine Trees, Lofty Mount Lu and the
   Akbari workshop stand on the literature — NOT on our own edge count — and
   because a tradition with a painter page and no work page is the worse error by
   a wide margin. Selected on our signal; admitted on external grounds.

   IMAGES: none of these URLs was written by hand. All twelve are read out of
   js/artworks.js, per the standing rule Batch 05 earned the hard way.

   Tier 2 throughout. §8 is deliberately untouched — see the batch doc: with only
   one uncatalogued public-domain painter who is genuinely abstract, relaxing the
   inbound-link rule would admit orphan pages and not one additional abstract
   work. The deck's problem is a list commission, not a schema change.

   `image.status:"pd"` is a rendering token, not a legal finding (§3, OD-5). */
window.CATALOG = (window.CATALOG || []).concat([

{ id:"the-chess-game", tier:2,
  title:"The Chess Game",
  artistId:"sofonisba-anguissola", year:{ display:"c. 1555", sort:1555 },
  movements:["high-renaissance"], techniques:["oil-painting"], nation:"italy",
  museum:{ id:"muzeum-narodowe-poznan", name:"National Museum in Poznań", city:"Poznań" },
  dims:"72 × 97 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/The_Chess_Game_%28Sofonisba_Anguissola%29_1555_%284096x3236px%29.jpg/500px-The_Chess_Game_%28Sofonisba_Anguissola%29_1555_%284096x3236px%29.jpg",
          page:"https://commons.wikimedia.org/wiki/File:The_Chess_Game_(Sofonisba_Anguissola)_1555_(4096x3236px).jpg", status:"pd" },
  coords:{ F:-88, D:-25, E:30, C:-15, M:-10 }, coordsSource:"override",
  description:"Three of the painter's sisters play chess in a landscape, watched by a servant, and every one of the four is a specific person rather than a type. Lucia has just moved and is looking out at you; Minerva raises a hand to concede; Europa, the youngest, is laughing at her. Anguissola was twenty-three, and she signed it on the edge of the board as Amilcare's virgin daughter, painting her three sisters from life.",
  notice:["Europa, the youngest, is laughing at her sister losing",
          "Signed along the edge of the chessboard, in Latin",
          "Group portraits of women, by a woman, in 1555"],
  tags:["portrait", "group-scene", "everyday-life", "playful"] },

{ id:"the-miracle-of-the-slave", tier:2,
  title:"The Miracle of the Slave",
  artistId:"tintoretto", year:{ display:"1548", sort:1548 },
  movements:["venetian-school", "mannerism"], techniques:["oil-painting"], nation:"italy",
  museum:{ id:"accademia-venice", name:"Gallerie dell'Accademia", city:"Venice" },
  dims:"415 × 541 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Tintoretto_-_Miracle_of_the_Slave.jpg/500px-Tintoretto_-_Miracle_of_the_Slave.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Tintoretto_-_Miracle_of_the_Slave.jpg", status:"pd" },
  coords:{ F:-82, D:90, E:45, C:10, M:80 }, coordsSource:"override",
  description:"St Mark drops head-first out of the sky to save a slave whose torturers' instruments have just shattered in their hands. Tintoretto put the saint upside down at the top of a five-metre canvas, foreshortened so hard he reads as a falling object before he reads as a person. It made Tintoretto's name in Venice at twenty-nine, and Titian is said to have been unamused.",
  notice:["The saint enters head-first, upside down, from above",
          "The broken tools are on the ground at the centre",
          "Five metres wide, and painted in a matter of months"],
  tags:["sacred", "group-scene", "theatrical", "monumental-scale"] },

{ id:"the-forest-seker-ahmed", tier:2,
  title:"The Forest", worksKey:"Forest (Woodland Scene)",
  artistId:"seker-ahmed-pasha", year:{ display:"1894", sort:1894 },
  movements:["realism"], techniques:["oil-painting"], nation:"turkey",
  museum:{ id:"sakip-sabanci", name:"Sakıp Sabancı Museum", city:"Istanbul" },
  dims:"61.5 × 43.5 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Ahmed-Forest.jpg/500px-Ahmed-Forest.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Ahmed-Forest.jpg", status:"pd" },
  coords:{ F:-75, D:-30, E:10, C:-25, M:-30 }, coordsSource:"override",
  description:"An Ottoman general who had trained in Paris under Gérôme came home and painted woods. No sultan, no battle, no ruin — just trees, close to, with the light coming through them and the ground going soft at the bottom of the canvas. He is the first Ottoman painter to treat landscape as a subject sufficient on its own, and he did it at roughly the size you could carry under one arm.",
  notice:["No figures, no story: trees, and the light in them",
          "He was a general, and Gérôme's student in Paris",
          "Ottoman painting's first landscape for its own sake"],
  tags:["landscape", "quiet", "golden", "would-hang"] },

{ id:"the-ray", tier:2,
  title:"The Ray",
  artistId:"jean-simeon-chardin", year:{ display:"1728", sort:1728 },
  movements:["rococo"], techniques:["oil-painting"], nation:"france",
  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },
  dims:"114 × 146 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg/500px-La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg",
          page:"https://commons.wikimedia.org/wiki/File:La_Raie_-_Jean_Baptiste_Sim%C3%A9on_Chardin_-_Mus%C3%A9e_du_Louvre_Peintures_INV_3197.jpg", status:"pd" },
  coords:{ F:-85, D:25, E:35, C:-30, M:10 }, coordsSource:"override",
  description:"A skate hangs split open on a hook, and its face — which is not a face, but reads as one — is grinning at the room. To the left a cat picks its way over oysters with its back up. Chardin submitted this to the Académie in 1728 and was admitted the same day, at twenty-nine, on the strength of a gutted fish. Diderot later said he had never seen paint used like it.",
  notice:["The ray's 'face' is anatomy, and it is smiling",
          "The cat is on the oysters and about to be caught",
          "It got him into the Académie on the day he showed it"],
  tags:["still-life", "unsettling", "interior", "texture"] },

{ id:"death-and-the-maiden", tier:2,
  title:"Death and the Maiden",
  artistId:"egon-schiele", year:{ display:"1915", sort:1915 },
  movements:["expressionism", "vienna-secession"], techniques:["oil-painting"], nation:"austria",
  museum:{ id:"belvedere", name:"Belvedere", city:"Vienna" },
  dims:"150 × 180 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg/500px-Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Egon_Schiele_-_Der_Tod_und_das_M%C3%A4dchen.jpg", status:"pd" },
  coords:{ F:-55, D:70, E:60, C:25, M:15 }, coordsSource:"override",
  description:"Two figures grip each other on a crumpled sheet that behaves like broken ground. The man is Schiele; the woman is Wally Neuzil, who had lived and modelled with him for four years and whom he left in 1915 to marry someone more respectable. He painted this as it ended. Her hands are locked behind his neck and his are not holding her at all.",
  notice:["His hands are not holding her; hers are locked shut",
          "The sheet is painted like torn ground, not cloth",
          "Painted as he left Wally Neuzil to marry someone else"],
  tags:["nude", "mourning", "unsettling", "texture"] },

{ id:"lofty-mount-lu", tier:2,
  title:"Lofty Mount Lu",
  artistId:"shen-zhou", year:{ display:"1467", sort:1467 },
  movements:["literati-painting"], techniques:["ink-wash", "silk-painting"], nation:"china",
  museum:{ id:"national-palace-museum-taipei", name:"National Palace Museum", city:"Taipei" },
  dims:"193.8 × 98.1 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Lofty_Mt.Lu_by_Shen_Zhou.jpg/960px-Lofty_Mt.Lu_by_Shen_Zhou.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Lofty_Mt.Lu_by_Shen_Zhou.jpg", status:"pd" },
  coords:{ F:-55, D:25, E:20, C:35, M:70 }, coordsSource:"override",
  description:"Shen Zhou painted a mountain he had never seen, at nearly two metres tall, as a seventieth-birthday present for his teacher — Mount Lu standing in for the size of the debt. The figure at the bottom is the size of a fingernail. It is the Yuan masters' dry brush handled by a Ming man with money and no official post, which is the whole literati position in one picture.",
  notice:["A birthday present for his teacher, two metres tall",
          "He had never been to Mount Lu when he painted it",
          "The single walker is about a fingernail high"],
  tags:["landscape", "monumental-scale", "quiet", "texture"] },

{ id:"pine-trees-tohaku", tier:2,
  title:"Pine Trees", worksKey:"Pine Trees",
  artistId:"hasegawa-tohaku", year:{ display:"c. 1595", sort:1595 },
  movements:["momoyama-painting", "zen-painting"], techniques:["ink-wash"], nation:"japan",
  museum:{ id:"tokyo-national-museum", name:"Tokyo National Museum", city:"Tokyo" },
  dims:"Each screen 156.8 × 356 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Hasegawa_Tohaku_-_Pine_Trees_%28Sh%C5%8Drin-zu_by%C5%8Dbu%29_-_left_hand_screen.jpg/500px-Hasegawa_Tohaku_-_Pine_Trees_%28Sh%C5%8Drin-zu_by%C5%8Dbu%29_-_left_hand_screen.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Hasegawa_Tohaku_-_Pine_Trees_(Sh%C5%8Drin-zu_by%C5%8Dbu)_-_left_hand_screen.jpg", status:"pd" },
  coords:{ F:-20, D:-45, E:75, C:40, M:45 }, coordsSource:"override",
  description:"A pair of six-panel screens with pines standing in fog, and the fog is unpainted paper. Tōhaku left more than half the surface empty and let the trunks fade in and out of it as if you were walking past them. Nothing is described that does not need to be. It was designated a National Treasure in 1952 and is the picture most often named when Japanese painting is asked to explain itself.",
  notice:["The mist is bare paper — most of the screen is empty",
          "A pair of screens; the trees continue across the gap",
          "Ink only. No gold, in the age of gold screens"],
  tags:["landscape", "fog", "quiet", "monochrome"] },

{ id:"seaport-with-the-embarkation-of-the-queen-of-sheba", tier:2,
  title:"Seaport with the Embarkation of the Queen of Sheba",
  artistId:"claude-lorrain", year:{ display:"1648", sort:1648 },
  movements:["baroque"], techniques:["oil-painting", "glazing"], nation:"france",
  museum:{ id:"national-gallery-london", name:"The National Gallery", city:"London" },
  dims:"149.1 × 196.7 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Claude_Lorrain_008.jpg/500px-Claude_Lorrain_008.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Claude_Lorrain_008.jpg", status:"pd" },
  coords:{ F:-78, D:-25, E:35, C:-20, M:35 }, coordsSource:"override",
  description:"The queen is a small figure on the steps at the left, and the subject is the sun. Claude put it low and dead centre, painted the harbour into silhouette around it, and made the whole picture about looking into light — which painting had mostly avoided doing. Turner admired it so much that he left two of his own canvases to the National Gallery on condition they hang beside it. They do.",
  notice:["The sun is centred, low, and painted straight into",
          "The queen herself is a small figure on the left steps",
          "Turner willed two paintings to hang next to it. They do."],
  tags:["seascape", "golden", "quiet", "would-hang"] },

{ id:"princes-of-the-house-of-timur", tier:2,
  title:"Princes of the House of Timur",
  artistId:"abd-al-samad", year:{ display:"c. 1550–1555", sort:1550 },
  movements:["mughal-painting", "persian-miniature"], techniques:["miniature-painting", "gouache"], nation:"iran",
  museum:{ id:"british-museum", name:"The British Museum", city:"London" },
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Princes_of_the_House_of_Timur.jpg/500px-Princes_of_the_House_of_Timur.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Princes_of_the_House_of_Timur.jpg", status:"pd" },
  coords:{ F:-72, D:15, E:25, C:30, M:40 }, coordsSource:"override",
  description:"A garden pavilion with the Timurid dynasty seated in it, painted on cotton rather than paper and at a size no page could hold. Large areas are simply gone — the losses are part of what you see. It was begun around 1550, probably at Kabul, and repainted repeatedly over the following century as the faces of later emperors were added to their ancestors. A dynasty updating its own family photograph.",
  notice:["Painted on cloth, not paper, and much of it is lost",
          "Later emperors were painted in among their ancestors",
          "One of the earliest things the Mughal workshop made"],
  tags:["group-scene", "historical", "pattern", "golden"] },

{ id:"motherhood-wyspianski", tier:2,
  title:"Motherhood", worksKey:"Motherhood",
  artistId:"stanislaw-wyspianski", year:{ display:"1905", sort:1905 },
  movements:["young-poland", "symbolism"], techniques:["pastel"], nation:"poland",
  museum:{ id:"muzeum-narodowe-krakow", name:"National Museum in Kraków", city:"Kraków" },
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Stanis%C5%82aw_Wyspia%C5%84ski%2C_Macierzy%C5%84stwo.jpg/500px-Stanis%C5%82aw_Wyspia%C5%84ski%2C_Macierzy%C5%84stwo.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Stanis%C5%82aw_Wyspia%C5%84ski,_Macierzy%C5%84stwo.jpg", status:"pd" },
  coords:{ F:-70, D:-20, E:40, C:10, M:-25 }, coordsSource:"override",
  description:"Wyspiański drew his wife nursing, in pastel, without softening anything: she is tired, she is not looking at the child, and the chalk is left visibly on the paper. He made the same subject repeatedly across the 1900s and this is the one people mean. He was a playwright and a stained-glass designer as much as a painter, and the outline here is a glazier's — one continuous line doing all the work.",
  notice:["A glazier's outline: one continuous line holds it",
          "She is exhausted, and he did not tidy that away",
          "Pastel, left visibly chalky rather than blended"],
  tags:["portrait", "tender", "pastel", "quiet"] },

{ id:"the-laughing-cavalier", tier:2,
  title:"The Laughing Cavalier",
  artistId:"frans-hals", year:{ display:"1624", sort:1624 },
  movements:["dutch-golden-age", "baroque"], techniques:["oil-painting", "alla-prima"], nation:"netherlands",
  museum:{ id:"wallace-collection", name:"The Wallace Collection", city:"London" },
  dims:"83 × 67.3 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Cavalier_soldier_Hals-1624x.jpg/500px-Cavalier_soldier_Hals-1624x.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Cavalier_soldier_Hals-1624x.jpg", status:"pd" },
  coords:{ F:-88, D:20, E:45, C:-30, M:-5 }, coordsSource:"override",
  description:"He is not laughing, and nobody knows he was a cavalier. The title was attached in the nineteenth century and stuck. What is actually here is the moustache, the tilt, and the sleeve — an acre of embroidery loaded with bees, arrows and lovers' knots, painted wet into wet at speed while the face was worked slowly. Hals lets you see every stroke, three hundred years before that was a virtue.",
  notice:["He is not laughing. The title is a Victorian invention.",
          "The sleeve carries bees, arrows and lovers' knots",
          "Brushwork left visible on purpose, in 1624"],
  tags:["portrait", "playful", "golden", "texture"] },

{ id:"travelers-among-mountains-and-streams", tier:2,
  title:"Travelers among Mountains and Streams",
  artistId:"fan-kuan", year:{ display:"c. 1000", sort:1000 },
  movements:["song-landscape"], techniques:["ink-wash", "silk-painting"], nation:"china",
  museum:{ id:"national-palace-museum-taipei", name:"National Palace Museum", city:"Taipei" },
  dims:"206.3 × 103.3 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg/500px-Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Fan_Kuan_-_Travelers_Among_Mountains_and_Streams_-_Google_Art_Project.jpg", status:"pd" },
  coords:{ F:-60, D:30, E:40, C:25, M:90 }, coordsSource:"override",
  description:"A cliff occupies the top two-thirds and a waterfall drops down its right side into mist. Underneath, at the very bottom, a mule train four centimetres long comes out of the trees, and a temple roof hides in the wood above it. The scale is the argument: this is what it is like to be a person outdoors, and Chinese painting had settled that question five centuries before Europe raised it.",
  notice:["The travellers are about four centimetres of two metres",
          "His signature hid in the leaves until 1958",
          "Probably the only surviving painting by him"],
  tags:["landscape", "monumental-scale", "fog", "texture"] }
]);
