/* PIGMENT — the influence graph.

   Edge: [from, to, type] — or [from, to, type, source]. Types:
     taught      — from was to's teacher or formal mentor (directed)
     influenced  — from's work demonstrably shaped to's (directed)
     befriended  — friends, close colleagues, collaborators (symmetric)
     rivaled     — documented rivalry or feud (symmetric)
     partners    — partners in life and art (symmetric)

   THIS HEADER USED TO SAY "Every relationship is grounded in the artist bios
   elsewhere in the atlas." That was measured on 2026-08-24 (backlog E2,
   docs/INFLUENCE_SOURCING.md) and it was FALSE for 107 of 246 edges — 43%.
   Caravaggio shaped Velázquez and Rembrandt, and Giotto shaped Masaccio, but
   none of those three painters' prose in this atlas says so. The claims are
   sound art history; the stated grounding was not there.

   What is true now, and what tools/validate.jxa.js enforces:

     · An edge is GROUNDED if either endpoint's own prose in js/artists-*.js
       names the other painter, OR the edge carries a fourth element, a source
       string of at least 20 characters saying where the relationship is
       attested.
     · The validator counts the ungrounded edges on every run and FAILS if the
       count rises above the recorded ceiling. The number can fall; it cannot
       grow. A new edge must therefore be grounded one way or the other.

   Grounding by prose is preferred over a source string, because prose is the
   product: a reader learns the relationship, and the graph stops asserting
   something the site never tells them. A source string is the honest fallback,
   not the goal.

   OD-5: a source records where a relationship is ATTESTED. It is not a finding
   by this project, and "sourced" does not mean "verified true". */
window.INFLUENCES = [
  /* ---- teachers & students ---- */
  ["theophanes-the-greek","andrei-rublev","taught"],
  ["titian","el-greco","taught"],
  ["michelangelo","sofonisba-anguissola","taught"],
  ["sofonisba-anguissola","anthony-van-dyck","taught"],
  ["peter-paul-rubens","anthony-van-dyck","taught"],
  ["annibale-carracci","guido-reni","taught"],
  ["francois-boucher","jean-honore-fragonard","taught"],
  ["jean-simeon-chardin","jean-honore-fragonard","taught"],
  ["jacques-louis-david","jean-auguste-dominique-ingres","taught"],
  ["camille-corot","berthe-morisot","taught"],
  ["camille-corot","camille-pissarro","taught"],
  ["camille-pissarro","paul-cezanne","taught"],
  ["camille-pissarro","paul-gauguin","taught"],
  ["edgar-degas","suzanne-valadon","taught"],
  ["gustave-moreau","henri-matisse","taught"],
  ["gustav-klimt","egon-schiele","taught"],
  ["jan-matejko","stanislaw-wyspianski","taught"],
  ["jan-matejko","jacek-malczewski","taught"],
  ["ilya-repin","zinaida-serebriakova","taught"],
  ["ibrahim-calli","bedri-rahmi-eyuboglu","taught"],
  ["fernand-leger","tarsila-do-amaral","taught"],
  ["arshile-gorky","willem-de-kooning","taught"],

  /* ---- lines of influence ---- */
  ["giotto","masaccio","influenced"],
  ["masaccio","michelangelo","influenced"],
  ["masaccio","piero-della-francesca","influenced"],
  ["jan-van-eyck","rogier-van-der-weyden","influenced"],
  ["leonardo-da-vinci","raphael","influenced"],
  ["hieronymus-bosch","pieter-bruegel","influenced"],
  ["hieronymus-bosch","salvador-dali","influenced"],
  ["hieronymus-bosch","zdzislaw-beksinski","influenced"],
  ["giuseppe-arcimboldo","salvador-dali","influenced"],
  ["albrecht-durer","hans-holbein","influenced"],
  ["hans-holbein","nicholas-hilliard","influenced"],
  ["titian","peter-paul-rubens","influenced"],
  ["titian","diego-velazquez","influenced"],
  ["titian","rembrandt","influenced"],
  ["titian","tintoretto","influenced"],
  ["michelangelo","tintoretto","influenced"],
  ["sofonisba-anguissola","lavinia-fontana","influenced"],
  ["caravaggio","artemisia-gentileschi","influenced"],
  ["caravaggio","diego-velazquez","influenced"],
  ["caravaggio","georges-de-la-tour","influenced"],
  ["caravaggio","rembrandt","influenced"],
  ["caravaggio","francisco-de-zurbaran","influenced"],
  ["caravaggio","joseph-wright-of-derby","influenced"],
  ["annibale-carracci","nicolas-poussin","influenced"],
  ["claude-lorrain","jmw-turner","influenced"],
  ["jacob-van-ruisdael","john-constable","influenced"],
  ["jacob-van-ruisdael","thomas-gainsborough","influenced"],
  ["pieter-bruegel","peter-paul-rubens","influenced"],
  ["peter-paul-rubens","antoine-watteau","influenced"],
  ["peter-paul-rubens","eugene-delacroix","influenced"],
  ["anthony-van-dyck","thomas-gainsborough","influenced"],
  ["anthony-van-dyck","joshua-reynolds","influenced"],
  ["diego-velazquez","francisco-goya","influenced"],
  ["diego-velazquez","edouard-manet","influenced"],
  ["diego-velazquez","john-singer-sargent","influenced"],
  ["diego-velazquez","francis-bacon","influenced"],
  ["diego-velazquez","pablo-picasso","influenced"],
  ["johannes-vermeer","vilhelm-hammershoi","influenced"],
  ["johannes-vermeer","salvador-dali","influenced"],
  ["rembrandt","kathe-kollwitz","influenced"],
  ["rembrandt","vincent-van-gogh","influenced"],
  ["rembrandt","lucian-freud","influenced"],
  ["antoine-watteau","francois-boucher","influenced"],
  ["jean-simeon-chardin","paul-cezanne","influenced"],
  ["nicolas-poussin","jacques-louis-david","influenced"],
  ["nicolas-poussin","paul-cezanne","influenced"],
  ["giambattista-tiepolo","francisco-goya","influenced"],
  ["william-hogarth","honore-daumier","influenced"],
  ["francisco-goya","edouard-manet","influenced"],
  ["francisco-goya","honore-daumier","influenced"],
  ["francisco-goya","otto-dix","influenced"],
  ["francisco-goya","kathe-kollwitz","influenced"],
  ["francisco-goya","pablo-picasso","influenced"],
  ["jmw-turner","claude-monet","influenced"],
  ["jmw-turner","ivan-aivazovsky","influenced"],
  ["john-constable","eugene-delacroix","influenced"],
  ["caspar-david-friedrich","mark-rothko","influenced"],
  ["eugene-delacroix","vincent-van-gogh","influenced"],
  ["eugene-delacroix","paul-signac","influenced"],
  ["jean-auguste-dominique-ingres","edgar-degas","influenced"],
  ["jean-auguste-dominique-ingres","pablo-picasso","influenced"],
  ["jean-auguste-dominique-ingres","tamara-de-lempicka","influenced"],
  ["jean-francois-millet","vincent-van-gogh","influenced"],
  ["jean-francois-millet","salvador-dali","influenced"],
  ["jean-francois-millet","park-soo-keun","influenced"],
  ["gustave-courbet","edouard-manet","influenced"],
  ["katsushika-hokusai","vincent-van-gogh","influenced"],
  ["katsushika-hokusai","claude-monet","influenced"],
  ["utagawa-hiroshige","vincent-van-gogh","influenced"],
  ["edgar-degas","henri-de-toulouse-lautrec","influenced"],
  ["edgar-degas","edward-hopper","influenced"],
  ["georges-seurat","camille-pissarro","influenced"],
  ["paul-cezanne","pablo-picasso","influenced"],
  ["paul-cezanne","georges-braque","influenced"],
  ["paul-cezanne","henri-matisse","influenced"],
  ["vincent-van-gogh","ernst-ludwig-kirchner","influenced"],
  ["vincent-van-gogh","egon-schiele","influenced"],
  ["vincent-van-gogh","francis-bacon","influenced"],
  ["vincent-van-gogh","anselm-kiefer","influenced"],
  ["paul-gauguin","pierre-bonnard","influenced"],
  ["paul-gauguin","henri-matisse","influenced"],
  ["paul-gauguin","edvard-munch","influenced"],
  ["paul-gauguin","amrita-sher-gil","influenced"],
  ["paul-signac","henri-matisse","influenced"],
  ["edvard-munch","ernst-ludwig-kirchner","influenced"],
  ["henri-de-toulouse-lautrec","pablo-picasso","influenced"],
  ["el-greco","pablo-picasso","influenced"],
  ["james-whistler","vilhelm-hammershoi","influenced"],
  ["james-whistler","olga-boznanska","influenced"],
  ["giorgio-de-chirico","salvador-dali","influenced"],
  ["giorgio-de-chirico","rene-magritte","influenced"],
  ["giorgio-de-chirico","max-ernst","influenced"],
  ["marcel-duchamp","jasper-johns","influenced"],
  ["marcel-duchamp","andy-warhol","influenced"],
  ["marcel-duchamp","banksy","influenced"],
  ["rene-magritte","jasper-johns","influenced"],
  ["pablo-picasso","arshile-gorky","influenced"],
  ["pablo-picasso","willem-de-kooning","influenced"],
  ["pablo-picasso","jackson-pollock","influenced"],
  ["pablo-picasso","fernand-leger","influenced"],
  ["pablo-picasso","david-hockney","influenced"],
  ["joan-miro","jackson-pollock","influenced"],
  ["joan-miro","arshile-gorky","influenced"],
  ["wassily-kandinsky","jackson-pollock","influenced"],
  ["piet-mondrian","agnes-martin","influenced"],
  ["piet-mondrian","victor-vasarely","influenced"],
  ["kazimir-malevich","lyubov-popova","influenced"],
  ["max-ernst","jackson-pollock","influenced"],
  ["jackson-pollock","helen-frankenthaler","influenced"],
  ["andy-warhol","takashi-murakami","influenced"],
  ["karl-bryullov","ivan-aivazovsky","influenced"],
  ["shen-zhou","bada-shanren","influenced"],
  ["bada-shanren","qi-baishi","influenced"],
  ["bada-shanren","zhang-daqian","influenced"],
  ["matrakci-nasuh","nakkas-osman","influenced"],
  ["nakkas-osman","levni","influenced"],
  ["osman-hamdi-bey","ibrahim-calli","influenced"],
  ["raja-ravi-varma","mf-husain","influenced"],
  ["amrita-sher-gil","mf-husain","influenced"],
  ["aaron-douglas","jacob-lawrence","influenced"],
  ["gustave-dore","vincent-van-gogh","influenced"],
  ["william-blake","odilon-redon","influenced"],
  ["william-blake","dante-gabriel-rossetti","influenced"],

  /* ---- friendships & alliances ---- */
  ["giorgione","titian","befriended"],
  ["albrecht-durer","raphael","befriended"],
  ["albrecht-durer","lucas-cranach","befriended"],
  ["claude-lorrain","nicolas-poussin","befriended"],
  ["joshua-reynolds","angelica-kauffman","befriended"],
  ["camille-corot","honore-daumier","befriended"],
  ["gustave-courbet","james-whistler","befriended"],
  ["edouard-manet","edgar-degas","befriended"],
  ["edouard-manet","claude-monet","befriended"],
  ["edouard-manet","berthe-morisot","befriended"],
  ["claude-monet","pierre-auguste-renoir","befriended"],
  ["claude-monet","john-singer-sargent","befriended"],
  ["claude-monet","gustave-caillebotte","befriended"],
  ["pierre-auguste-renoir","gustave-caillebotte","befriended"],
  ["edgar-degas","mary-cassatt","befriended"],
  ["georges-seurat","paul-signac","befriended"],
  ["vincent-van-gogh","paul-gauguin","befriended"],
  ["vincent-van-gogh","henri-de-toulouse-lautrec","befriended"],
  ["henri-rousseau","pablo-picasso","befriended"],
  ["john-singer-sargent","joaquin-sorolla","befriended"],
  ["akseli-gallen-kallela","edvard-munch","befriended"],
  ["wassily-kandinsky","paul-klee","befriended"],
  ["wassily-kandinsky","franz-marc","befriended"],
  ["paul-klee","franz-marc","befriended"],
  ["pablo-picasso","georges-braque","befriended"],
  ["pablo-picasso","joan-miro","befriended"],
  ["pablo-picasso","wifredo-lam","befriended"],
  ["pablo-picasso","zhang-daqian","befriended"],
  ["pablo-picasso","abidin-dino","befriended"],
  ["amedeo-modigliani","diego-rivera","befriended"],
  ["amedeo-modigliani","tsuguharu-foujita","befriended"],
  ["kurt-schwitters","hannah-hoch","befriended"],
  ["max-ernst","joan-miro","befriended"],
  ["leonora-carrington","remedios-varo","befriended"],
  ["frida-kahlo","georgia-okeeffe","befriended"],
  ["mark-rothko","barnett-newman","befriended"],
  ["andy-warhol","jean-michel-basquiat","befriended"],
  ["jean-michel-basquiat","keith-haring","befriended"],
  ["david-hockney","lucian-freud","befriended"],
  ["lucian-freud","francis-bacon","befriended"],
  ["georgia-okeeffe","yayoi-kusama","befriended"],
  ["qi-baishi","xu-beihong","befriended"],
  ["seker-ahmed-pasha","osman-hamdi-bey","befriended"],
  ["bedri-rahmi-eyuboglu","abidin-dino","befriended"],
  ["abidin-dino","fikret-mualla","befriended"],
  ["ivan-shishkin","ilya-repin","befriended"],
  ["natalia-goncharova","lyubov-popova","befriended"],
  ["jacob-lawrence","romare-bearden","befriended"],
  ["john-everett-millais","dante-gabriel-rossetti","befriended"],
  ["salvador-dali","rene-magritte","befriended"],

  /* ---- rivalries ---- */
  ["leonardo-da-vinci","michelangelo","rivaled"],
  ["michelangelo","raphael","rivaled"],
  ["annibale-carracci","caravaggio","rivaled"],
  ["frans-hals","judith-leyster","rivaled"],
  ["joshua-reynolds","thomas-gainsborough","rivaled"],
  ["jean-auguste-dominique-ingres","eugene-delacroix","rivaled"],
  ["jmw-turner","john-constable","rivaled"],
  ["katsushika-hokusai","utagawa-hiroshige","rivaled"],
  ["henri-matisse","pablo-picasso","rivaled"],
  ["kazimir-malevich","marc-chagall","rivaled"],
  ["jackson-pollock","willem-de-kooning","rivaled"],
  ["andy-warhol","roy-lichtenstein","rivaled"],
  ["andy-warhol","yayoi-kusama","rivaled"],

  /* ---- partners in life & art ---- */
  ["diego-rivera","frida-kahlo","partners"],
  ["jackson-pollock","lee-krasner","partners"],
  ["max-ernst","leonora-carrington","partners"],
  ["kitagawa-utamaro","mary-cassatt","influenced"],
  ["james-ensor","paul-klee","influenced"],
  ["ferdinand-hodler","gustav-klimt","influenced"],
  ["jmw-turner","frederic-edwin-church","influenced"],
  ["thomas-cole","frederic-edwin-church","taught"],
  ["andrea-mantegna","albrecht-durer","influenced"],
  ["dante-gabriel-rossetti","edward-burne-jones","taught"],
  ["john-singer-sargent","anders-zorn","rivaled"],
  ["peder-severin-kroyer","anna-ancher","befriended"],
  ["paul-cezanne","paula-modersohn-becker","influenced"],
  ["amedeo-modigliani","chaim-soutine","befriended"],
  ["ivan-aivazovsky","arkhip-kuindzhi","taught"],
  ["ilya-repin","vasily-surikov","befriended"],
  ["ilya-repin","valentin-serov","taught"],
["hans-hofmann","lee-krasner","taught"],
  ["hans-hofmann","helen-frankenthaler","taught"],
  ["hans-hofmann","joan-mitchell","taught"],
  ["helen-frankenthaler","morris-louis","influenced"],
  ["helen-frankenthaler","kenneth-noland","influenced"],
  ["morris-louis","kenneth-noland","befriended"],
  ["kenneth-noland","alma-thomas","influenced"],
  ["willem-de-kooning","franz-kline","befriended"],
  ["jackson-pollock","philip-guston","befriended"],
  ["mark-rothko","robert-motherwell","befriended"],
  ["clyfford-still","mark-rothko","influenced"],
  ["robert-motherwell","helen-frankenthaler","partners"],
  ["josef-albers","kenneth-noland","taught"],

  /* ---- added 2026-08-08 with the four painters of backlog B3 ----
     The edge schema is [from, to, type] and carries no source field, which is
     backlog E2 and is not fixed here. What can be done without re-typing shipped
     infrastructure is to say, once, what these particular edges rest on. All six
     are documented pupillage — a teaching relationship named in the standard
     reference literature, not a stylistic resemblance inferred from the pictures:
       verrocchio -> leonardo   Leonardo was apprenticed in his workshop and
                                painted at least one angel in The Baptism of Christ.
       bellini -> giorgione     both named as his pupils in the Venetian record;
       bellini -> titian        Bellini ran the workshop they came through.
       gerome -> osman-hamdi-bey, -> mary-cassatt
                                Gérôme's teaching roll at the École des Beaux-Arts.
       michelangelo -> vasari   Vasari worked in his orbit, wrote his Life, and
                                designed his tomb. This one is the weakest of the
                                six: it is documented association and advocacy
                                rather than formal training, and it is typed
                                "influenced" for that reason. */
  ["andrea-del-verrocchio","leonardo-da-vinci","taught"],
  ["giovanni-bellini","giorgione","taught"],
  ["giovanni-bellini","titian","taught"],
  ["jean-leon-gerome","osman-hamdi-bey","taught"],
  ["jean-leon-gerome","mary-cassatt","taught"],
  /* added with A3: Gérôme taught BOTH Ottoman painters in the atlas. Şeker Ahmed
     Paşa was sent to Paris by Sultan Abdülaziz to study under Gustave Boulanger
     and Gérôme, per the standard biography. */
  ["jean-leon-gerome","seker-ahmed-pasha","taught"],
  ["john-frederick-lewis","jean-leon-gerome","influenced"],
  ["michelangelo","giorgio-vasari","influenced"],

  /* ---- added 2026-08-24 with the E2 sourcing pass ---- */

  /* THE ATLAS'S FIRST EDGE BETWEEN TWO NON-WESTERN TRADITIONS. Before this line
     the graph had 246 edges and NOT ONE joined two different non-Western
     nations — measured, not assumed. See docs/INFLUENCE_SOURCING.md §4 for why
     the rest of that gap is downstream of E3 rather than of this file: you
     cannot draw Persia→Mughal without a Mughal painter in the roster. */
  ["tsuguharu-foujita","diego-rivera","befriended",
   "Foujita visited Rivera's studio soon after reaching Paris, and Rivera painted him in 'Portrait of Mr Kawashima and Foujita' (1914). Foujita's seven-month Mexican stay from November 1932 was drawn by the mural movement 'led by Diego Rivera, whom he had befriended in Paris'. en.wikipedia.org/wiki/Tsuguharu_Foujita, citing Lamia 2018 p.136 and Ikeda 2018 p.90."],

  /* Three relationships THIS ATLAS ALREADY TELLS ITS READERS and the graph did
     not carry. Masaccio's own record says Michelangelo, Leonardo and Raphael
     "all sketched there as students" in the Brancacci Chapel; only the
     Michelangelo edge existed. Bellini's record and Mantegna's each name the
     other. All three are grounded by prose and need no source string — which is
     the point of preferring prose. */
  ["masaccio","leonardo-da-vinci","influenced"],
  ["masaccio","raphael","influenced"],
  ["andrea-mantegna","giovanni-bellini","influenced"]
];
