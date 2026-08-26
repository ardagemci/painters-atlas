/* PIGMENT — atlas widening batch 5: the traditions the atlas had no room for.

   Backlog E3. Measured before it was written: of the 27 painters in the atlas
   born before 1500, FIFTEEN were Italian and three were not European. The era
   vocabulary began at 1300, so Song China — the first tradition E3 names — had
   no century to be filed in at all. A taxonomy that cannot hold a thing is a
   record of where its author was looking.

   Thirteen painters, and js/taxonomy.js gains what they need to exist: two eras
   before 1300, the nation `indonesia`, and five movements (`song-landscape`,
   `mughal-painting`, `joseon-painting`, `momoyama-painting`,
   `viceregal-painting`). Behzād needed nothing — `persian-miniature` was
   already there and empty of its greatest name.

   TWO OF E3's THREE NAMED TRANSMISSIONS CLOSE HERE, and that is the point of
   the batch rather than a side effect. Backlog E2 measured the influence graph
   and found not one edge joining two different non-Western traditions; it also
   found that most of the gap could not be drawn because the endpoints were
   missing. These are the endpoints:
     · China → Korea — Guo Xi → An Gyeon. The scholarship on 'Mongyu dowondo'
       turns on its relation to Guo Xi; the early Joseon court painted in his
       manner for a century.
     · Persia → Mughal — Behzād → Abd al-Samad → Basawan. Abd al-Samad carried
       the Safavid royal atelier's training to Akbar's workshop and ran it, and
       Basawan came up under him.
   Persia → Ottoman stays open. The influence is real and general, and no
   painter-to-painter link between the atlas's one Persian and its Ottoman
   miniaturists survives contact with a source, so none is drawn.

   DATES. Four of these painters have no recorded birth or death year. Where
   that is so, `years` displays what is actually known ('fl. …'), and `born` /
   `died` carry the first and last DOCUMENTED years so the timeline and the
   1955 image cutoff have something to sort on. That is a different convention
   from the one `nakkas-osman` uses, where `born` predates the floruit by a
   generation; the divergence is recorded here rather than silently copied.

   All thirteen died centuries before 1955. */
window.ARTISTS = (window.ARTISTS || []).concat([

{ id:"fan-kuan", name:"Fan Kuan", years:"c. 960–c. 1030", born:960, died:1030,
  nation:"china", eras:["before-1200"],
  movements:["song-landscape"],
  techniques:["ink-wash","silk-painting"], style:"tonal",
  palette:["#3e3a34","#7a7264","#b8ac94","#4a5a4e","#e8e2d4"],
  tagline:"He put a cliff where the subject should be, and left the people out of focus",
  works:[{t:"Travelers among Mountains and Streams",y:"c. 1000"},{t:"Sitting Alone by a Stream",y:"attributed"},{t:"Snowscape",y:"attributed"}],
  life:"Born Fan Zhongzheng, known by the nickname Kuan — 'generous', or 'easy-going' — which is most of what the record preserves of his character. He was a Daoist and a Neo-Confucian, and the anecdotes have him moving into the mountains to live among what he painted, on the reasoning that studying earlier painters teaches you painters, and studying nature teaches you nature.",
  career:"Travelers among Mountains and Streams is probably the only picture by him that survives, and it is enough. A rock face occupies two thirds of a two-metre hanging scroll; below it, a mule train the width of a finger comes out of the trees, and a temple roof hides in the woods. Northern Song landscape is built on this arrangement — near ground you stand on, a band of mist that hides the joins, a far peak that settles the argument about scale. Everything about it is deliberate, including how small you are.",
  outside:"His signature was found in 1958, hidden in the leaves of the foreground trees, where it had gone unread for nine centuries. Until then the attribution rested on connoisseurship alone; the picture had been the greatest Chinese painting in the world for a long time before anyone could prove whose it was.",
  facts:["The mule train is a few centimetres of a two-metre scroll — find it.",
    "His signature was only discovered in 1958, hidden among painted leaves.",
    "It is probably the sole surviving work by him.",
    "He is said to have moved into the mountains rather than copy other painters.",
    "This is monumental landscape three centuries before Europe attempts it."] },

{ id:"guo-xi", name:"Guo Xi", years:"c. 1020–c. 1090", born:1020, died:1090,
  nation:"china", eras:["before-1200"],
  movements:["song-landscape"],
  techniques:["ink-wash","silk-painting"], style:"tonal",
  palette:["#4a463c","#8a8272","#c4b8a0","#5e6e5a","#eae4d6"],
  tagline:"The court painter who wrote down how to move a viewer through a picture",
  works:[{t:"Early Spring",y:"1072"},{t:"Old Trees, Level Distance",y:"c. 1080"},{t:"Deep Valley",y:"undated"}],
  life:"A landscape painter from Henan who became a court professional under the Northern Song and was educated enough to argue about what he was doing in writing. His son recorded the way he prepared: a clean table by a bright window, incense lit on both sides, the best brushes chosen and the inkstone washed, hands washed — the whole ceremony of receiving an important guest — and then he waited until his mind was quiet before he began.",
  career:"Early Spring, dated 1072, is the demonstration piece: mist rising off thawing ground, trees written in his 'crab-claw' branches, and rock built from the curling strokes later painters copied by name. What he added to Fan Kuan's generation was movement. His treatise, The Lofty Message of Forest and Streams, sets out the 'angle of totality' — a picture is not one fixed viewpoint but a walk, and the eye should be able to travel into it, through it and out again. Europe would not attempt anything like that argument for centuries.",
  outside:"He is the reason Chinese landscape can be discussed in its own vocabulary rather than borrowed terms: high distance, deep distance, level distance — three ways of placing a viewer, named and distinguished in the eleventh century. Painters were still working to his categories eight hundred years later.",
  facts:["He wrote the first great manual of landscape painting, and it still reads.",
    "His 'three distances' are a theory of viewpoint, written around 1080.",
    "His son recorded the incense-and-clean-hands ritual before he painted.",
    "The curling 'crab-claw' branches are his, and were copied for centuries.",
    "He was a court professional and a scholar at once — unusual then, and later."] },

{ id:"huang-gongwang", name:"Huang Gongwang", years:"1269–1354", born:1269, died:1354,
  nation:"china", eras:["13th-century","14th-century"],
  movements:["literati-painting"],
  techniques:["ink-wash"], style:"tonal",
  palette:["#5e5648","#8a8272","#c4bca8","#3e4a44","#e8e2d2"],
  tagline:"Career closed, jailed, and then he took up painting at fifty",
  works:[{t:"Dwelling in the Fuchun Mountains",y:"c. 1350"},{t:"Nine Peaks after Snow",y:"1349"},{t:"Stone Cliff at the Pond of Heaven",y:"1341"}],
  life:"Born Lu Jian in Changshu. The Song fell to the Mongols when he was ten, which closed the examination route to office for his whole educated generation. He worked as a minor clerk, was caught up in a superior's disgrace, and spent time in prison. He came out, became a Daoist, took the name Dachi Daoren — 'A Silly Daoist' — and went to the mountains.",
  career:"He is the oldest of the Four Masters of the Yuan, and the reason the phrase 'literati painting' means something specific: not paintings made for money or for an emperor, but dry-brushed ink handed between friends, annotated with poems, and judged on character rather than finish. Dwelling in the Fuchun Mountains occupied his last years and is the most revered scroll in Chinese art. Shen Zhou and every scholar-painter after him worked in its shadow, and said so.",
  outside:"The Fuchun scroll was nearly destroyed in 1650 when a collector ordered it burned with him at his death; a nephew pulled it from the fire. It survives in two pieces, in two different museums on two sides of a strait, and was briefly reunited for an exhibition in 2011.",
  facts:["He started painting seriously in his fifties, after prison and a lost career.",
    "His sobriquet translates as 'A Silly Daoist'.",
    "The Fuchun scroll was rescued from a collector's funeral pyre in 1650.",
    "It survives in two pieces, held in Zhejiang and in Taipei.",
    "Shen Zhou and the whole Ming literati tradition work in his shadow."] },

{ id:"kamal-ud-din-behzad", name:"Kamāl ud-Dīn Behzād", years:"c. 1455–1535", born:1455, died:1535,
  nation:"iran", eras:["15th-century","16th-century"],
  movements:["persian-miniature"],
  techniques:["miniature-painting","gouache","gold-leaf"], style:"ornament",
  palette:["#1f6e8a","#c4663a","#caa43e","#2e6e5a","#e8dcc0"],
  tagline:"The summit of Persian painting, and a signature nobody can safely trust",
  works:[{t:"The Seduction of Yusuf",y:"1488"},{t:"Construction of the Castle of Khawarnaq",y:"c. 1494"},{t:"The Caliph Harun al-Rashid in the Bath",y:"1488"}],
  life:"Orphaned young and raised in the Herat of Sultan Husayn Bayqara, the last and most cultivated Timurid court, under the protection of the poet and vizier Mir Ali-Shir Nava'i. In 1486 the sultan appointed him head of the royal ateliers. When Herat fell in 1506 he eventually followed the Safavids west, and ended his career running the royal library at Tabriz.",
  career:"Persian painting before him is exquisite and airless; he opened it. He would leave a courtyard almost empty and set the figures dancing around the void, break a rigid architectural frame with a stairway going the wrong way, and give individual faces to the servants and labourers other painters treated as pattern. The Seduction of Yusuf, from a Bustan of Sa'di of 1488, is the case everybody cites: a palace of impossible geometry, a staircase spiralling, and two people at the top of it.",
  outside:"His fame in his own lifetime is the reason his work is hard to identify. Copies, homages and hopeful attributions multiplied for centuries, and later dealers added his signature to pictures he never touched. Scholars now argue over most of the corpus — a painter so admired that the admiration buried him.",
  facts:["He was made head of Herat's royal ateliers in 1486, by the sultan himself.",
    "He left large areas of a page empty, which Persian painting had not done.",
    "Later dealers forged his signature onto other painters' work for centuries.",
    "Most attributions to him are now disputed by somebody.",
    "The atelier tradition he led reached India, and became Mughal painting."] },

{ id:"abd-al-samad", name:"Abd al-Samad", years:"c. 1500–c. 1595", born:1500, died:1595,
  nation:"iran", nationNote:"Persian by training; his whole recorded career was spent in Mughal India.",
  eras:["16th-century"],
  movements:["mughal-painting","persian-miniature"],
  techniques:["miniature-painting","gouache","gold-leaf"], style:"ornament",
  palette:["#1f6e8a","#c4302a","#caa43e","#2e7a52","#e8dcc0"],
  tagline:"He carried Persian painting to India, then ran the workshop that changed it",
  works:[{t:"Akbar Presents a Painting to His Father Humayun",y:"c. 1550"},{t:"Princes of the House of Timur",y:"c. 1550–55"},{t:"Hamzanama illustrations",y:"c. 1562–77"}],
  life:"From Shiraz, trained in the Safavid royal atelier — the tradition Behzād had led — and recruited to the Mughal court by the exiled emperor Humayun, whom he taught to draw. He followed the dynasty to India and stayed. His birth and death years are approximate; what is documented is a Mughal career running from about 1550 to about 1595, and it is documented unusually well for a painter of his time and place.",
  career:"From around 1572 he headed Akbar's imperial workshop, and it was under his direction that the Mughal style arrived at itself: Persian colour and page design, Indian faces and appetite for the observed world, and modelling learned from European engravings the Jesuits brought. The Hamzanama — fourteen volumes, some fourteen hundred paintings on cloth, made by teams over fifteen years — was produced under his supervision. He later left painting for senior administration, including the imperial mint.",
  outside:"A leading specialist, Barbara Brend, has argued that he is the same man as Mirza Ali, a Persian painter whose documented career ends exactly when Abd al-Samad's Mughal one begins. The identification is contested, which is a useful reminder of how thin the ground is even for a painter whose career is comparatively well recorded.",
  facts:["He taught the emperor Humayun to draw, and followed him to India.",
    "He ran Akbar's imperial workshop from about 1572.",
    "He supervised the Hamzanama — some 1,400 paintings over fifteen years.",
    "He left painting for administration, and ran the imperial mint.",
    "One scholar argues he and the Persian painter Mirza Ali are one person."] },

{ id:"basawan", name:"Basawan", years:"fl. 1580–1600", born:1560, died:1600,
  nation:"india", eras:["16th-century"],
  movements:["mughal-painting"],
  techniques:["miniature-painting","gouache","gold-leaf"], style:"ornament",
  palette:["#c4302a","#1f6e8a","#caa43e","#2e7a52","#e8dcc0"],
  tagline:"Akbar's greatest painter of people, and one of four the chronicle bothered to name",
  works:[{t:"Akbarnama illustrations",y:"c. 1590–95"},{t:"A Camel Fight",y:"c. 1590"},{t:"The Infant Akbar Presented to Humayun",y:"c. 1590"}],
  life:"A Yadav from Uttar Pradesh who came into Akbar's workshop and rose under the Persian master Abd al-Samad. Little else about his life is recorded — but the Ain-i-Akbari, the official register of Akbar's empire, singles out exactly four painters for comment, and he is one of them. His son Manohar Das succeeded him as a court painter.",
  career:"Where the workshop's Persian inheritance made faces into pattern, Basawan made them into people: a crowd in an Akbarnama page has individuals in it, watching different things, and reacting at different speeds. He was among the first Indian painters to take an interest in European technique, from the paintings and engravings Jesuit missionaries brought to Akbar's court, and used its light and shade without ever letting it take the picture over. Akbar's historian Abu'l-Fazl wrote that in design, portraiture, colouring and illusion he had become unrivalled in the world.",
  outside:"Mughal pages were often the work of two or three hands — one artist for the composition, another for the faces — and inscribed accordingly, which is why Mughal painting is one of the very few pre-modern traditions outside Europe where individual artists can be named at all. Basawan's name appears on the design of pages whose faces are somebody else's.",
  facts:["The Ain-i-Akbari names only four painters, and he is one.",
    "He learned European light and shade from Jesuit gifts to Akbar's court.",
    "Mughal pages credit design and faces separately — often two artists.",
    "His son Manohar Das succeeded him at court.",
    "Abu'l-Fazl called him unrivalled in the world; he is barely known outside India."] },

{ id:"ustad-mansur", name:"Ustad Mansur", years:"fl. 1590–1624", born:1590, died:1624,
  nation:"india", eras:["16th-century","17th-century"],
  movements:["mughal-painting"],
  techniques:["miniature-painting","gouache","watercolor"], style:"ornament",
  palette:["#2e7a52","#c4302a","#caa43e","#1f6e8a","#e8dcc0"],
  tagline:"The first person to paint a dodo from life, in colour",
  works:[{t:"Dodo",y:"c. 1625"},{t:"Siberian Crane",y:"c. 1625"},{t:"Turkey Cock",y:"c. 1612"},{t:"Chameleon",y:"c. 1612"}],
  life:"Nothing is recorded of his birth, and his name is suffixed in early miniatures as Naqqash — painter, or carver — which suggests he came from a family in the trade. He worked first as a colourist on the Akbarnama, unnamed among the credited artists. Under Jahangir, who cared more about animals and plants than any other Mughal emperor, he became the court's naturalist.",
  career:"Jahangir gave him the title Nādir al-'Asr, Unequalled of the Age, and set him to record what arrived at court. He painted more than a hundred Kashmiri flowers on one journey. He made the earliest colour image of a dodo taken from a living bird, and the first painting of a Siberian crane. These are not decorative studies: the plumage is accurate enough that ornithologists still argue about the specimens, which is a strange afterlife for a court miniaturist.",
  outside:"In 1621 a zebra was presented to Jahangir, and the painting Mansur made of it appears to be his last. His work sits in an odd category — art history reads it as painting, natural history reads it as data, and it is genuinely both, four decades before the same argument began in Europe.",
  facts:["His dodo is one of very few colour images made from a living bird.",
    "He was the first artist to paint a Siberian crane.",
    "Jahangir titled him Nādir al-'Asr — Unequalled of the Age.",
    "He painted over a hundred flowers on a single trip to Kashmir.",
    "Ornithologists still cite his paintings as evidence."] },

{ id:"an-gyeon", name:"An Gyeon", years:"c. 1418 – after 1464", born:1418, died:1464,
  nation:"korea", eras:["15th-century"],
  movements:["joseon-painting"],
  techniques:["ink-wash","silk-painting"], style:"tonal",
  palette:["#e8e4d8","#4a5a54","#8a7a5e","#2e50a4","#b0503e"],
  tagline:"He painted a prince's dream in three days, and Korean landscape began",
  works:[{t:"Dream Journey to the Peach Blossom Land",y:"1447"},{t:"Four Seasons Landscapes",y:"attributed"},{t:"Landscape with Streams and Mountains",y:"attributed"}],
  life:"Born at Jigok in South Chungcheong province and taken into the Dohwaseo, the bureau of painters that served the Joseon court. His death year is not recorded; 1464 is simply the last year he can be shown to have been working. His patron was Grand Prince Anpyeong, a royal collector with the best library of Chinese painting in Korea and a taste for lending it out.",
  career:"In 1447 Anpyeong dreamed he had walked into the peach-blossom utopia of the poet Tao Yuanming, and asked An Gyeon to paint it. The scroll he produced is the oldest surviving Korean landscape painting, and it reads right to left, which is backwards — the dream is entered the wrong way round. He worked in the manner of the Northern Song master Guo Xi, whose curling rock and crab-claw trees the early Joseon court took as the standard, and out of him came a whole school of Korean painters working the same way for a century.",
  outside:"The painting is not in Korea. It has been at Tenri University in Japan since the colonial period, and requests for its return are a live cultural argument rather than a settled historical one. It comes home for exhibitions occasionally, and the queues are long.",
  facts:["He is said to have painted it in three days, from a description of a dream.",
    "It is the oldest surviving Korean landscape painting.",
    "The scroll reads right to left — you enter the dream backwards.",
    "It has been held at Tenri University in Japan since the colonial period.",
    "He worked in Guo Xi's manner, four centuries after Guo Xi."] },

{ id:"jeong-seon", name:"Jeong Seon", years:"1676–1759", born:1676, died:1759,
  nation:"korea", eras:["17th-century","18th-century"],
  movements:["joseon-painting"],
  techniques:["ink-wash","silk-painting"], style:"tonal",
  palette:["#3e4a44","#8a7a5e","#e8e4d8","#2e50a4","#c4302a"],
  tagline:"He stopped painting an imaginary China and went to look at Korea",
  works:[{t:"Inwangjesaekdo",y:"1751"},{t:"Geumgang jeondo",y:"1734"},{t:"Ingokjeongsa",y:"1742"}],
  life:"Known by the art name Gyeomjae, 'humble study', which was accurate about his position rather than his talent: he depended on aristocratic patrons and the name acknowledged it. He travelled — Mount Geumgang in 1711 with the local governor, and again the year after, producing albums of thirteen and then thirty paintings that were passed round and annotated with his patrons' poems.",
  career:"For three centuries Joseon painters had made landscapes of an idealised China most of them had never seen. Jeong Seon walked to the Diamond Mountains and painted the Diamond Mountains. Jingyeong sansuhwa — 'true-view' landscape — is the name for what he started, and it gave Korean painting a country: the Han river, the granite of Inwang mountain after rain in 1751, the actual shape of actual places. Kim Hong-do's crowds are the next move, from the landscape to the people standing in it.",
  outside:"Inwangjesaekdo was painted when he was seventy-five, after a summer downpour, and the wet black granite of the mountain is laid on in broad slabs of ink that behave nothing like the fine brushwork he was trained in. It is a National Treasure, and the argument for it is that he abandoned the manner he had spent a life perfecting.",
  facts:["He invented 'true-view' landscape — Korea painted from Korea.",
    "Inwangjesaekdo was painted at seventy-five, after rain, in slabs of wet ink.",
    "He toured Mount Geumgang in 1711 and made an album of thirteen paintings.",
    "His art name, Gyeomjae, means 'humble study'.",
    "His grandson Jeong Hwang carried the true-view style on."] },

{ id:"kano-eitoku", name:"Kanō Eitoku", years:"1543–1590", born:1543, died:1590,
  nation:"japan", eras:["16th-century"],
  movements:["momoyama-painting"],
  techniques:["ink-wash","gold-leaf","silk-painting"], style:"ornament",
  palette:["#caa43e","#2a2c30","#2e6e5a","#e8cd7a","#8a2620"],
  tagline:"Gold-ground screens at the scale of a castle, for the men who built them",
  works:[{t:"Cypress Trees",y:"c. 1590"},{t:"Chinese Lions",y:"c. 1590"},{t:"Views in and around Kyoto",y:"1565"}],
  life:"Grandson of Kanō Motonobu and trained inside the family workshop, he was painting at his grandfather's level in his early twenties. His patrons were the two men unifying Japan by force: Oda Nobunaga hired him at thirty-four, and Toyotomi Hideyoshi kept him. Keeping the Kanō school pre-eminent was as much an organisational feat as an artistic one, and he was good at both — he once intercepted a warlord's commission on its way to his rival Hasegawa Tōhaku.",
  career:"He painted the interiors of Nobunaga's Azuchi castle and Hideyoshi's Osaka Castle: pine and cypress and lions in heavy pigment on gold leaf, designed to be legible across a dark audience hall and to say what the room's owner could afford. Views in and around Kyoto, painted in 1565, was acquired by Nobunaga to demonstrate that he held the capital, and presented to a rival warlord as a message. Almost all the castle work is gone — Azuchi burned in 1582.",
  outside:"He died at forty-seven, worn out on a commission, and the standard account is straightforward overwork: the demand for gold screens in the unification years exceeded what one workshop could paint. What survives is a fraction, and most of the famous Momoyama interiors are known from documents rather than pictures.",
  facts:["He painted the inside of Azuchi castle; it burned seven years later.",
    "Views in and around Kyoto was used by Nobunaga as a political message.",
    "He intercepted a commission intended for his rival Tōhaku.",
    "He died at forty-seven, apparently of overwork.",
    "Cypress Trees and Chinese Lions are both National Treasures."] },

{ id:"hasegawa-tohaku", name:"Hasegawa Tōhaku", years:"1539–1610", born:1539, died:1610,
  nation:"japan", eras:["16th-century","17th-century"],
  movements:["momoyama-painting","zen-painting"],
  techniques:["ink-wash","gold-leaf","silk-painting"], style:"tonal",
  palette:["#2a2c30","#8a8276","#c4bcae","#5e6e5a","#ece8dc"],
  tagline:"A screen of pine trees in fog, and almost no paint at all",
  works:[{t:"Pine Trees",y:"c. 1595"},{t:"Maple",y:"1593"},{t:"Pine Tree and Flowering Plants",y:"c. 1593"}],
  life:"He came from Noto, a province away from the capital, and began as a painter of Buddhist images for provincial temples — portraits, devas, the working commissions of a religious painter. He arrived in Kyoto in middle age and set himself against the Kanō monopoly. Kanō Eitoku competed with him for Hideyoshi's patronage and beat him more than once; when Eitoku died in 1590, Tōhaku was left as the greatest living painter in Japan.",
  career:"He could do the gold: the Chishaku-in walls, painted in 1593 for a temple Hideyoshi raised for a dead child, are as opulent as anything the Kanō made, and one of them is by his son Kyūzō, who died at twenty-six the year after. And then there is Pine Trees — a pair of six-panel screens with nothing on them but ink, fog and the suggestion of trunks, an argument that a picture can be mostly absence. It is one of the most admired objects in Japan.",
  outside:"At sixty-seven he was summoned to Edo and given the priestly rank of hōgen by Tokugawa Ieyasu, and he stayed there for the rest of his life. He claimed descent from Sesshū's line and styled himself the fifth in that succession — a claim historians treat as ambition rather than genealogy.",
  facts:["Pine Trees is a National Treasure, and is very nearly empty.",
    "He lost commissions to Kanō Eitoku, then outlived him by twenty years.",
    "His son Kyūzō painted part of the Chishaku-in walls, and died at twenty-six.",
    "He claimed to be fifth in Sesshū's line of succession.",
    "Tokugawa Ieyasu gave him the priestly title hōgen at sixty-seven."] },

{ id:"raden-saleh", name:"Raden Saleh", years:"c. 1811–1880", born:1811, died:1880,
  nation:"indonesia", eras:["19th-century"],
  movements:["romanticism"],
  techniques:["oil-painting","glazing"], style:"romantic",
  palette:["#2a2620","#c4302a","#caa43e","#2e5a4a","#e0d2b4"],
  tagline:"He learned the European history picture, then turned it on the people who taught him",
  works:[{t:"The Arrest of Prince Diponegoro",y:"1857"},{t:"Boschbrand",y:"1849"},{t:"Lion Hunt",y:"1840"}],
  life:"Born near Semarang in Java into a noble Hadhrami family whose ancestors had reached the island from Arabia by way of Surat. The Belgian painter A.J. Payen taught him as a boy and persuaded the colonial government to send him to Europe; he arrived in 1829 and studied under Cornelis Kruseman and Andreas Schelfhout. He stayed more than twenty years, moved through the German courts, visited Algiers, and became a celebrity.",
  career:"The animal fights made his name — a lion tamer in The Hague named Henri Martin let him study a live lion, and the results, all teeth and rearing horses, sold across Europe as Delacroix's subject matter done properly. But the picture that matters is The Arrest of Prince Diponegoro, painted in 1857, after his return. A Dutch painter had already made the scene as a Dutch triumph. Saleh restaged it: the Javanese faces are individuals with their heads held up, the Dutch officers' heads are drawn slightly too large, and the prince is not surrendering. He gave it to the Dutch king.",
  outside:"He is the first modern artist of Indonesia by common consent, and the argument about him is whether a Javanese aristocrat painting European Romanticism for European patrons was a collaborator or a subverter. The Diponegoro picture is the reason the argument has never settled. Several of his paintings burned with the Dutch colonial pavilion in Paris in 1931.",
  facts:["He studied a live lion in The Hague, on loan from its tamer.",
    "The Arrest of Prince Diponegoro answers an earlier Dutch painting of the scene.",
    "He drew the Dutch officers' heads slightly too large — read it as you like.",
    "He gave that painting to the king of the Netherlands.",
    "Works of his were destroyed in the 1931 Paris colonial pavilion fire."] },

{ id:"miguel-cabrera", name:"Miguel Cabrera", years:"1695–1768", born:1695, died:1768,
  nation:"mexico", eras:["18th-century"],
  movements:["viceregal-painting","baroque"],
  techniques:["oil-painting","glazing"], style:"baroque",
  palette:["#8a2620","#caa43e","#2e4a8a","#e8dcc0","#3e3a2e"],
  tagline:"The most famous painter in the Americas, and Europe never heard of him",
  works:[{t:"Portrait of Sor Juana Inés de la Cruz",y:"c. 1750"},{t:"Casta painting",y:"1763"},{t:"Virgin of Guadalupe",y:"1760"}],
  life:"Born at Nueva Antequera, now Oaxaca, and in Mexico City from 1719. He may have trained under José de Ibarra or the Rodríguez Juárez brothers; the record is thin on how he started and clear on where he arrived. The archbishop of Mexico had his portrait painted by him twice, the Jesuits gave him commissions in volume, and he ran a workshop that produced everything from miniatures on copper to walls.",
  career:"His portrait of Sor Juana Inés de la Cruz — the nun, poet and scholar who had died fifty years before he painted her — is the image by which she is known everywhere, a woman at a desk in front of her own library, which was the argument. His casta paintings, sets of canvases labelling the offspring of every combination of Spanish, Indigenous and African parentage, are the finest examples of a genre that exists to sort people, and are studied now for exactly that reason.",
  outside:"In 1756 he and six other painters examined the image of the Virgin of Guadalupe as painters rather than as believers, and published the result. They identified four different techniques in the one image and concluded that no painter of their own century could have combined them, let alone one of the sixteenth. It is a strange, careful document: connoisseurship deployed on a relic.",
  facts:["His Sor Juana is the portrait by which she is known worldwide.",
    "He painted her fifty years after her death, from earlier images.",
    "In 1756 he examined the Guadalupe image technically, and published it.",
    "His casta paintings are the finest of a genre invented to classify people.",
    "In his lifetime he was called the greatest painter in the viceroyalty."] }

]);
