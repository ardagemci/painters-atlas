/* PIGMENT — artwork catalog 5 (ARTWORK_SCHEMA v1).
   The twenty-two records specified in docs/CATALOG_BATCH_01.md (10, one artwork per
   zero-artwork nation) and docs/CATALOG_BATCH_02.md (12, ranked by consequence),
   with the `description` and `notice` copy from docs/CATALOG_BATCH_COPY.md.

   All 22 are Tier 2. Each carries hand-scored coords (coordsSource:"override"),
   a description and exactly 3 notice bullets, so each meets §4's FIELD
   requirements for Tier 1 — they are held at Tier 2 by §8's inbound-link rule
   alone, which is the Curator's call. Promotion is purely additive and the URL
   never changes.

   `image.status:"pd"` is a rendering token, not a legal finding (§3, OD-5): it
   records that a Commons file page asserts a public-domain basis. Every dims
   string here was sanity-checked by the specification; a-burial-at-ornans is
   CONVERTED FROM METRES (Wikidata unit Q11573) — see ARTWORK_SCHEMA §7.1 rule 1,
   the unit bug this batch found. red-and-white-plum-blossoms carries the word
   "each" that Wikidata's own figure does not (§7.1 rule 3). */
window.CATALOG = (window.CATALOG || []).concat([

{ id:"the-tortoise-trainer", tier:2,
  title:"The Tortoise Trainer",
  artistId:"osman-hamdi-bey", year:{ display:"1906", sort:1906 },
  movements:["realism"], techniques:["oil-painting"], nation:"turkey",
  museum:{ id:"pera-museum", name:"Pera Museum", city:"Istanbul" },
  dims:"221.5 × 120 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg/500px-Osman_Hamdi_Bey_-_The_Tortoise_Trainer_-_Google_Art_Project.jpg",
          page:"https://en.wikipedia.org/wiki/The_Tortoise_Trainer", status:"pd" },
  coords:{ F:-85, D:-40, E:-25, C:45, M:10 }, coordsSource:"override",
  description:"A man in Ottoman dress stands stooped over his tortoises, a naqareh drum slung on his back, waiting for them to learn something. They do not hurry. Nothing in the picture moves at all. Osman Hamdi Bey built it to be read rather than felt, and gave two and a quarter metres of canvas to the slowest lesson in the room.",
  notice:["The drum on his back is a naqareh",
          "Nothing in this picture is in a hurry",
          "That the trainer wears the painter's own face — widely repeated, unestablished"],
  tags:["interior","quiet","monumental-scale"] },

{ id:"stanczyk", tier:2,
  title:"Stańczyk",
  artistId:"jan-matejko", year:{ display:"1862", sort:1862 },
  movements:["romanticism"], techniques:["oil-painting"], nation:"poland",
  museum:{ id:"national-museum-warsaw", name:"National Museum in Warsaw", city:"Warsaw" },
  dims:"88 × 120 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Jan_Matejko%2C_Sta%C5%84czyk.jpg/500px-Jan_Matejko%2C_Sta%C5%84czyk.jpg",
          page:"https://en.wikipedia.org/wiki/Sta%C5%84czyk_(painting)", status:"pd" },
  coords:{ F:-85, D:35, E:-60, C:40, M:-15 }, coordsSource:"override",
  description:"A court ball is going on through the doorway behind him, bright and busy. The jester sits apart in red, out of the light, and does not perform. He has read the dispatch; the dancers have not. Matejko painted it in 1862 in entirely conventional means, and gave the loudest man at court the only silence in the room.",
  notice:["The ball is bright; his corner is not",
          "In costume, and the only figure not performing",
          "He has read the dispatch; the dancers haven't"],
  tags:["historical","interior","lonely","red"] },

{ id:"senecio", tier:2,
  title:"Senecio",
  artistId:"paul-klee", year:{ display:"1922", sort:1922 },
  movements:["expressionism","abstract-art"], techniques:["oil-painting"], nation:"switzerland",
  museum:{ id:"kunstmuseum-basel", name:"Kunstmuseum Basel", city:"Basel" },
  dims:"40.3 × 37.4 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg/500px-Paul_Klee%2C_1922%2C_Senecio%2C_oil_on_gauze%2C_40.3_%C3%97_37.4_cm%2C_Kunstmuseum_Basel.jpg",
          page:"https://en.wikipedia.org/wiki/Senecio_(Klee)", status:"pd" },
  coords:{ F:35, D:-20, E:65, C:15, M:-70 }, coordsSource:"override",
  description:"A head, still legible as a head, assembled out of squares and wedges the way a bricklayer would build one. The gaze is level and it holds. Klee was teaching at the Bauhaus in 1922, laying colour down as a system rather than as a description — and the system came out amused. Forty centimetres square. You could carry it under one arm.",
  notice:["A head built from squares and wedges",
          "The gaze is level, and it holds yours",
          "Oil on gauze, or oil and canvas — sources disagree"],
  tags:["portrait","geometry","flatness","playful"] },

{ id:"sunlight-in-the-blue-room", tier:2,
  title:"Sunlight in the Blue Room",
  artistId:"anna-ancher", year:{ display:"1891", sort:1891 },
  movements:["impressionism"], techniques:["oil-painting"], nation:"denmark",
  museum:{ id:"skagens-museum", name:"Skagens Museum", city:"Skagen" },
  dims:"65.2 × 58.8 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg/500px-Anna_Ancher_-_Sunlight_in_the_blue_room_-_Google_Art_Project.jpg",
          page:"https://en.wikipedia.org/wiki/Sunlight_in_the_Blue_Room", status:"pd" },
  coords:{ F:-80, D:-70, E:-10, C:-45, M:-60 }, coordsSource:"override",
  description:"A child sits in a blue room, and the event of the picture is sunlight arriving on the wall behind her. That is the whole plot. Ancher painted it in 1891 at sixty-five centimetres — a corner of a house rather than a scene — and gave the light more attention than the sitter, which is why your eye goes to the wall first.",
  notice:["The wall holds the light; the child holds still",
          "Blue throughout, warmed only where the sun lands",
          "Sixty-five centimetres: a corner, not a scene"],
  tags:["interior","quiet","everyday-life","blue"] },

{ id:"three-girls", tier:2,
  title:"Three Girls", worksKey:"Three Girls",
  artistId:"amrita-sher-gil", year:{ display:"1935", sort:1935 },
  movements:["post-impressionism"], techniques:["oil-painting"], nation:"india",
  museum:{ id:"ngma-new-delhi", name:"National Gallery of Modern Art", city:"New Delhi" },
  dims:"99.5 × 73.5 cm",
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Amrita_Sher-Gil_Group_of_Three_Girls.jpg/500px-Amrita_Sher-Gil_Group_of_Three_Girls.jpg",
          page:"https://en.wikipedia.org/wiki/Three_Girls_(painting)", status:"pd" },
  coords:{ F:-85, D:-50, E:10, C:-20, M:-35 }, coordsSource:"override",
  description:"Three young women sit close together and not one of them looks at another, or at you. Nothing happens. Sher-Gil trained in Paris and turned that training on an Indian subject — modern in its colour and its flattening, conventional in every other means — so the picture works by mood instead of by argument. A metre of canvas, three figures, no story offered.",
  notice:["Nobody meets anybody's eye, including yours",
          "Modern in colour and flattening, conventional in means",
          "Reportedly won a gold medal from the Bombay Art Society"],
  tags:["group-scene","quiet","everyday-life"] },

{ id:"the-artist-and-his-mother", tier:2,
  title:"The Artist and His Mother",
  artistId:"arshile-gorky", year:{ display:"c. 1926–1936", sort:1926 },
  movements:["modernism"], techniques:["oil-painting"], nation:"armenia",
  museum:{ id:"whitney", name:"Whitney Museum of American Art", city:"New York" },
  image:{ src:"https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg/960px-Arshile_Gorky%2C_The_Artist_and_His_Mother.jpg",
          page:"https://commons.wikimedia.org/wiki/File:Arshile_Gorky,_The_Artist_and_His_Mother.jpg", status:"pd" },
  coords:{ F:-45, D:-25, E:45, C:25, M:-5 }, coordsSource:"override",
  description:"Gorky worked from a childhood photograph taken in Van: himself as a boy, standing beside his mother. In the aftermath of the genocide she died of starvation in Yerevan, in 1919. He painted this over roughly a decade and never called it finished. The surfaces are scraped back and laid again, the faces pressed towards outline and plane. Two versions exist. This is the one at the Whitney.",
  notice:["Painted from a childhood photograph taken in Van",
          "Scraped back and repainted for a decade, never finished",
          "A second version is in Washington"],
  tags:["portrait","mourning","flatness"] }

]);
