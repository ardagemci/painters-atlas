/* PIGMENT — artwork catalog 7 (ARTWORK_SCHEMA v1). Batch 04, specified in
   docs/CATALOG_BATCH_04.md.

   The Batch 03 ranking, re-run over the 113 painters who still hold audited
   gallery images and no catalog record: influence-graph degree x3, mentions by
   name in other painters' prose x2, taxonomy-copy mentions x1.

   THE TIE. Ten painters ranked cleanly. Seven then tied at 11 points with
   IDENTICAL values on all three signals, so the measure could not choose the
   last two and was not asked to guess. The tie is broken by a second-order form
   of the same question — how many of a painter's influence edges land on a
   painter who ALREADY has a catalog record — which asks not just whether the
   atlas argues for them but whether it argues for them from ground it has
   already covered. Signac scored 3 of 3 and Carracci 2 of 3; the other five
   scored 1 or 0. Signac's promotion is caused by Batch 03: one of his three
   edges runs to Delacroix, who was inert until last week.

   Vasari is EXCLUDED AGAIN and this is now a standing exclusion, not a fresh
   decision each batch — his ten prose mentions are all citations of the Lives.
   See docs/CATALOG_BATCH_04.md "STANDING EXCLUSIONS".

   All 12 are Tier 2 under ARTWORK_SCHEMA §8's inbound-link rule; none is named
   in js/tier1-artists.js or js/lists-1.js (checked by search). Each carries
   hand-scored coords, a 60-90 word description and 3 notice bullets, so
   promotion is a one-line tier edit and the URL never changes.

   `image.status:"pd"` is a rendering token, not a legal finding (§3, OD-5).

   DIMENSIONS. Batch 03 predicted that the aggregator would keep being wrong and
   it was, five times in twelve:
     · the-gleaners and bal-du-moulin-de-la-galette — Wikidata and English
       Wikipedia AGREE with each other and BOTH differ from the Musée d'Orsay
       (83.5 x 110 and 131.5 x 176.5). Two sources agreeing is not two checks.
     · the-embarkation-for-cythera — Wikidata carries METRES (1.29 x 1.94), the
       §7.1 rule 1 regression case, live again.
     · the-papal-palace-avignon — Wikidata offers two inceptions, 1900 and 1909,
       neither preferred; the Orsay says 1909, and its dimensions differ too.
     · bal-du-moulin-de-la-galette and the-embarkation-for-cythera both list an
       ENDED collection first (Louvre 1929-86; Académie royale 1717-93).
   Where the holding institution publishes a measurement, the institution wins. */
window.CATALOG = (window.CATALOG || []).concat([

{ id:"bal-du-moulin-de-la-galette", tier:2,
  title:"Bal du moulin de la Galette",
  artistId:"pierre-auguste-renoir", year:{ display:"1876", sort:1876 },
  movements:["impressionism"], techniques:["oil-painting","broken-color"], nation:"france",
  museum:{ id:"musee-dorsay", name:"Musée d'Orsay", city:"Paris" },
  dims:"131.5 × 176.5 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Renoir%2C_Pierre-Auguste_-_Dance_at_Le_Moulin_de_la_Galette%2C_1876.jpg/500px-Renoir%2C_Pierre-Auguste_-_Dance_at_Le_Moulin_de_la_Galette%2C_1876.jpg",
          page:"https://en.wikipedia.org/wiki/Bal_du_moulin_de_la_Galette", status:"pd" },
  coords:{ F:-75, D:30, E:40, C:-55, M:25 }, coordsSource:"override",
  description:"A Sunday afternoon at the Moulin de la Galette in Montmartre, where working Parisians dressed up to dance, drink and eat galettes into the evening. The sun comes through the trees in loose violet patches and is allowed to fall across faces, which is the Impressionist argument in one gesture. Gustave Caillebotte owned it; when he died the French state took it in lieu of death duties. And Renoir painted the scene twice.",
  notice:["A near-identical second version exists, smaller",
          "Which of the two is the original is not known",
          "Caillebotte owned it; France took it as death duties"],
  tags:["group-scene","everyday-life","golden","playful"] },

{ id:"the-bolt", tier:2,
  title:"The Bolt",
  artistId:"jean-honore-fragonard", year:{ display:"1777", sort:1777 },
  movements:["rococo"], techniques:["oil-painting"], nation:"france",
  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },
  dims:"73.5 × 93.5 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Le_Verrou_-_Jean-Honor%C3%A9_Fragonard_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1974_2.jpg/500px-Le_Verrou_-_Jean-Honor%C3%A9_Fragonard_-_Mus%C3%A9e_du_Louvre_Peintures_RF_1974_2.jpg",
          page:"https://en.wikipedia.org/wiki/The_Bolt_(Fragonard)", status:"pd" },
  coords:{ F:-85, D:65, E:5, C:-30, M:-5 }, coordsSource:"override",
  description:"Everything is thrown along one diagonal: a red bed curtain, a wrecked gold bedspread, two bodies, and at the top corner a hand driving the bolt home. What is happening in it is disputed and has been for a long time. One reading is two lovers shutting the door; another is a woman trying to get free while a man locks it. Her arm is straight and her face is turned away. The picture does not settle it.",
  notice:["A single diagonal runs from the bed to the bolt",
          "Her arm is braced against him, not around him",
          "Scholars read this as an embrace or as an assault"],
  tags:["interior","unsettling","theatrical","red"] },

{ id:"mr-and-mrs-andrews", tier:2,
  title:"Mr and Mrs Andrews",
  artistId:"thomas-gainsborough", year:{ display:"c. 1750", sort:1750 },
  movements:["rococo"], techniques:["oil-painting"], nation:"britain",
  museum:{ id:"national-gallery-london", name:"The National Gallery", city:"London" },
  dims:"69.8 × 119.4 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg/500px-Thomas_Gainsborough_-_Mr_and_Mrs_Andrews.jpg",
          page:"https://en.wikipedia.org/wiki/Mr_and_Mrs_Andrews", status:"pd" },
  coords:{ F:-90, D:-45, E:20, C:25, M:-10 }, coordsSource:"override",
  description:"Gainsborough was about twenty-three, painting neighbours in Suffolk, and he gave the land more canvas than the couple. That is the argument the picture has been having ever since: is this a marriage portrait with scenery, or an inventory of an estate that arrived as her dowry? Then look at her lap. There is a shape there that was never painted — the blue stops and bare ground shows through. Nobody knows what was going to go in it.",
  notice:["A patch of her lap was reserved and never filled in",
          "The pheasant theory fails: the corn is cut too early",
          "More landscape than in any other Gainsborough portrait"],
  tags:["portrait","landscape","quiet","storm"] },

{ id:"the-gleaners", tier:2,
  title:"The Gleaners",
  artistId:"jean-francois-millet", year:{ display:"1857", sort:1857 },
  movements:["realism","barbizon-school"], techniques:["oil-painting"], nation:"france",
  museum:{ id:"musee-dorsay", name:"Musée d'Orsay", city:"Paris" },
  dims:"83.5 × 110 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg/500px-Jean-Fran%C3%A7ois_Millet_-_Gleaners_-_Google_Art_Project_2.jpg",
          page:"https://en.wikipedia.org/wiki/The_Gleaners", status:"pd" },
  coords:{ F:-85, D:-20, E:10, C:30, M:25 }, coordsSource:"override",
  description:"Three women bend to pick up what the harvest left. Gleaning was the right of the very poorest to take the leavings, and Millet gave those leavings the scale and the dignity that painting reserved for saints and generals. Behind them, deliberately, is the harvest itself — stacks, a cart, a man on a horse. The Salon of 1857 was not charmed. One critic said he saw in it the scaffolds of 1793.",
  notice:["The full harvest sits behind them, guarded, in the light",
          "Gleaning was a legal right of the poorest, not charity",
          "A critic called it the scaffolds of 1793"],
  tags:["everyday-life","landscape","group-scene","golden"] },

{ id:"the-heart-of-the-andes", tier:2,
  title:"The Heart of the Andes",
  artistId:"frederic-edwin-church", year:{ display:"1859", sort:1859 },
  movements:["hudson-river-school","romanticism"], techniques:["oil-painting","glazing"], nation:"usa",
  museum:{ id:"met", name:"The Metropolitan Museum of Art", city:"New York" },
  dims:"168 × 302.9 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Church_Heart_of_the_Andes.jpg/500px-Church_Heart_of_the_Andes.jpg",
          page:"https://en.wikipedia.org/wiki/Heart_of_the_Andes", status:"pd" },
  coords:{ F:-85, D:40, E:-20, C:30, M:85 }, coordsSource:"override",
  description:"No such place exists. Church spent two journeys in Ecuador and Colombia retracing Alexander von Humboldt's route, then assembled a continent — Chimborazo, a plain, a jungle — into one three-metre view. In New York in 1859 people queued and paid twenty-five cents to see it, in a darkened room, lit theatrically, in a floor-standing frame built to look like a window. He meant to ship it to Humboldt. Humboldt died that May.",
  notice:["The landscape is assembled; no single view looks like this",
          "New Yorkers paid 25 cents and queued around the block",
          "Its frame stood on the floor, framing it as a window"],
  tags:["landscape","monumental-scale","ecstatic","golden"] },

{ id:"frescoes-of-the-transfiguration-novgorod", tier:2,
  title:"Frescoes of the Church of the Transfiguration, Novgorod",
  worksKey:"Frescoes of the Transfiguration Church, Novgorod",
  artistId:"theophanes-the-greek", year:{ display:"1378", sort:1378 },
  movements:["icon-painting"], techniques:["fresco"], nation:"greece",
  museum:{ id:"transfiguration-ilyina-novgorod", name:"Church of the Transfiguration on Ilyina Street", city:"Veliky Novgorod" },
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/a/ac/Eleutherius_of_Illyria_%281378%2C_Theophanes_the_Greek%29.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Eleutherius_of_Illyria_(1378,_Theophanes_the_Greek).jpg", status:"pd" },
  coords:{ F:-55, D:35, E:30, C:40, M:45 }, coordsSource:"override",
  description:"A Byzantine painter walked into a Russian town and painted a church in a single season, and 1378 is not an estimate — a chronicle wrote it down. What survives is fragments: Christ in the dome, saints by the south door, the Old Testament Trinity in the west chamber. This picture is one of them, a martyr's head. Look at the whites: two or three flicked strokes make a cheekbone. Nobody in Russia was painting like that.",
  notice:["The date is documented, not deduced — a chronicle names 1378",
          "Highlights are struck on in two or three white flicks",
          "This is one figure; the cycle survives only in fragments"],
  tags:["sacred","gesture","texture","monumental-scale"] },

{ id:"portrait-of-doge-leonardo-loredan", tier:2,
  title:"Portrait of Doge Leonardo Loredan", worksKey:"Doge Leonardo Loredan",
  artistId:"giovanni-bellini", year:{ display:"c. 1501–1502", sort:1501 },
  movements:["early-renaissance","venetian-school"], techniques:["oil-painting"], nation:"italy",
  museum:{ id:"national-gallery-london", name:"The National Gallery", city:"London" },
  dims:"61.6 × 45.1 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg/500px-Giovanni_Bellini%2C_portrait_of_Doge_Leonardo_Loredan.jpg",
          page:"https://en.wikipedia.org/wiki/Portrait_of_Doge_Leonardo_Loredan", status:"pd" },
  coords:{ F:-90, D:-40, E:20, C:30, M:15 }, coordsSource:"override",
  description:"Loredan had just been elected Doge and would hold the office for twenty years. Bellini painted him almost square-on, which portraiture of the time avoided, and painted the office rather than the mood: the corno ducale over its linen cap, the damask robe, the buttons done in thick raised paint so they catch real light. The signature is on a painted scrap of paper along the ledge. It says only IOANNES BELLINVS.",
  notice:["The buttons are raised paint, and catch the room's light",
          "The hat is a doublet's hood, stiffened into a crown",
          "Signed on a painted slip of paper on the ledge"],
  tags:["portrait","quiet","blue"] },

{ id:"madame-de-pompadour", tier:2,
  title:"Madame de Pompadour",
  artistId:"francois-boucher", year:{ display:"1759", sort:1759 },
  movements:["rococo"], techniques:["oil-painting"], nation:"france",
  museum:{ id:"wallace-collection", name:"The Wallace Collection", city:"London" },
  dims:"91 × 68 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour%2C_1759.jpg/960px-Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour%2C_1759.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Fran%C3%A7ois_Boucher_-_Madame_de_Pompadour,_1759.jpg", status:"pd" },
  coords:{ F:-85, D:-20, E:-25, C:-45, M:20 }, coordsSource:"override",
  description:"Jeanne-Antoinette Poisson, marquise de Pompadour, had been the king's mistress and was by 1759 something harder to name — an official, in effect, running patronage. Boucher painted her many times and this is the garden version: a stone Venus behind her, roses on the ground, a spaniel on the bench watching her rather than us. Almost the whole picture is one dress. Count how much canvas the silk gets and how much the face does.",
  notice:["The dress takes more paint than everything else combined",
          "A stone Venus sits directly behind her head",
          "The spaniel is looking at her, not out at you"],
  tags:["portrait","pastel","quiet","tender"] },

{ id:"the-embarkation-for-cythera", tier:2,
  title:"The Embarkation for Cythera", worksKey:"Pilgrimage to Cythera",
  artistId:"antoine-watteau", year:{ display:"1717", sort:1717 },
  movements:["rococo"], techniques:["oil-painting","glazing"], nation:"france",
  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },
  dims:"129 × 194 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/L%27Embarquement_pour_Cyth%C3%A8re%2C_by_Antoine_Watteau%2C_from_C2RMF_retouched.jpg/500px-L%27Embarquement_pour_Cyth%C3%A8re%2C_by_Antoine_Watteau%2C_from_C2RMF_retouched.jpg",
          page:"https://en.wikipedia.org/wiki/The_Embarkation_for_Cythera", status:"pd" },
  coords:{ F:-80, D:15, E:55, C:-25, M:25 }, coordsSource:"override",
  description:"Watteau submitted this to the Académie in 1717 as his reception piece and it fitted no category they had, so they wrote him one: fête galante. Couples in silk drift between a statue of Venus and a boat. And nobody agrees which way they are going — the Louvre's own title calls it a pilgrimage TO the island, the English title says embarkation FOR it, and the couples nearest the statue are plainly reluctant to leave.",
  notice:["The Académie invented a whole genre to file this under",
          "Arriving or leaving? Two centuries and still no verdict",
          "A garlanded Venus watches the couples decide"],
  tags:["group-scene","landscape","tender","golden"] },

{ id:"forest-british-columbia", tier:2,
  title:"Forest, British Columbia",
  artistId:"emily-carr", year:{ display:"1931–1932", sort:1931 },
  movements:["expressionism"], techniques:["oil-painting"], nation:"canada",
  museum:{ id:"vancouver-art-gallery", name:"Vancouver Art Gallery", city:"Vancouver" },
  dims:"130 × 86.8 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg/500px-Emily_Carr_%281931%E2%80%9332%29_Forest%2C_British_Columbia.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Emily_Carr_(1931%E2%80%9332)_Forest,_British_Columbia.jpg", status:"pd" },
  coords:{ F:30, D:45, E:55, C:35, M:40 }, coordsSource:"override",
  description:"Carr went to New York in 1930, saw what O'Keeffe and the modernists were doing, came home to Vancouver Island and stopped describing forests. The trunks here have become carved folds, green and blue-black, closing over like heavy cloth. In the middle of it is a pale opening with light in it. It is a painting of undergrowth that behaves like the inside of a cathedral, and she is not documenting anything.",
  notice:["The trunks are painted as folds of cloth, not bark",
          "A pale gap at the centre is the only light there is",
          "Painted after a 1930 New York trip changed her mind"],
  tags:["landscape","unsettling","ecstatic","texture"] },

{ id:"the-papal-palace-avignon", tier:2,
  title:"The Papal Palace, Avignon",
  artistId:"paul-signac", year:{ display:"1909", sort:1909 },
  movements:["neo-impressionism"], techniques:["oil-painting","pointillism"], nation:"france",
  museum:{ id:"musee-dorsay", name:"Musée d'Orsay", city:"Paris" },
  dims:"73.3 × 91.9 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Paul_Signac_-_Avignon._Soir_%28le_ch%C3%A2teau_des_Papes%29_-_1909.jpg/960px-Paul_Signac_-_Avignon._Soir_%28le_ch%C3%A2teau_des_Papes%29_-_1909.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Paul_Signac_-_Avignon._Soir_(le_ch%C3%A2teau_des_Papes)_-_1909.jpg", status:"pd" },
  coords:{ F:-35, D:20, E:45, C:20, M:10 }, coordsSource:"override",
  description:"Twenty years after Seurat died, Signac was still working the theory out, and the dots had grown up into tiles. Each touch here is a square block of colour laid beside its neighbour without mixing, so the palace across the water is assembled rather than described — closer to mosaic than to brushwork. The Orsay's own title keeps the hour in it: Avignon. Evening. Stand back four paces and the stone reassembles itself.",
  notice:["The touches are square tiles, not Seurat's small dots",
          "Nothing is blended; the mixing happens in your eye",
          "Its Orsay title names the time of day: evening"],
  tags:["landscape","pattern","texture"] },

{ id:"the-beaneater", tier:2,
  title:"The Beaneater",
  artistId:"annibale-carracci", year:{ display:"c. 1580–1590", sort:1580 },
  movements:["baroque"], techniques:["oil-painting"], nation:"italy",
  museum:{ id:"palazzo-colonna", name:"Palazzo Colonna", city:"Rome" },
  dims:"57 × 68 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Carracci_-_Der_Bohnenesser.jpeg/500px-Carracci_-_Der_Bohnenesser.jpeg",
          page:"https://en.wikipedia.org/wiki/The_Beaneater", status:"pd" },
  coords:{ F:-92, D:5, E:45, C:-20, M:-25 }, coordsSource:"override",
  description:"A working man is eating beans, and you have interrupted him. The spoon is halfway to a mouth that is still open, and he has looked up. Around the bowl: spring onions, bread rolls, a vegetable pie, a striped jug, a glass of wine half gone. In Bologna in the 1580s nobody was giving a whole canvas to this. Carracci painted a still life and a portrait at once, and let the man catch you looking.",
  notice:["The spoon is in mid-air and his mouth is still open",
          "He is looking straight out — you interrupted the meal",
          "Still life and portrait in one, which nobody did yet"],
  tags:["everyday-life","portrait","still-life"] }

]);
