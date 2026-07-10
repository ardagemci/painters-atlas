/* PIGMENT — venue registry (ARTWORK_SCHEMA §5b).
   Stable slugs for museums, churches, palaces and sites. References are permanent:
   renames are forbidden (add an alias instead). Museum PAGES arrive with the
   Museums deliverable; these ids are load-bearing from day one.
   Sentinels: private-collection · lost · unknown. */
window.VENUES = [
  /* ---- sentinels ---- */
  { id:"private-collection", name:"Private collection", city:null, country:null, type:"site" },
  { id:"lost", name:"Lost or destroyed", city:null, country:null, type:"site" },
  { id:"unknown", name:"Location unknown", city:null, country:null, type:"site" },

  /* ---- Europe ---- */
  { id:"louvre", name:"Musée du Louvre", city:"Paris", country:"France", type:"museum" },
  { id:"musee-dorsay", name:"Musée d'Orsay", city:"Paris", country:"France", type:"museum" },
  { id:"orangerie", name:"Musée de l'Orangerie", city:"Paris", country:"France", type:"museum" },
  { id:"musee-marmottan", name:"Musée Marmottan Monet", city:"Paris", country:"France", type:"museum" },
  { id:"centre-pompidou", name:"Centre Pompidou", city:"Paris", country:"France", type:"museum" },
  { id:"prado", name:"Museo del Prado", city:"Madrid", country:"Spain", type:"museum" },
  { id:"reina-sofia", name:"Museo Reina Sofía", city:"Madrid", country:"Spain", type:"museum" },
  { id:"uffizi", name:"Gallerie degli Uffizi", city:"Florence", country:"Italy", type:"museum" },
  { id:"galleria-borghese", name:"Galleria Borghese", city:"Rome", country:"Italy", type:"museum" },
  { id:"vatican-museums", name:"Vatican Museums", city:"Vatican City", country:"Vatican", type:"museum" },
  { id:"sistine-chapel", name:"Sistine Chapel", city:"Vatican City", country:"Vatican", type:"church" },
  { id:"san-luigi-dei-francesi", name:"Contarelli Chapel, San Luigi dei Francesi", city:"Rome", country:"Italy", type:"church" },
  { id:"santa-maria-delle-grazie", name:"Santa Maria delle Grazie", city:"Milan", country:"Italy", type:"church" },
  { id:"scrovegni-chapel", name:"Scrovegni Chapel", city:"Padua", country:"Italy", type:"church" },
  { id:"museo-civico-sansepolcro", name:"Museo Civico", city:"Sansepolcro", country:"Italy", type:"museum" },
  { id:"national-gallery-london", name:"The National Gallery", city:"London", country:"United Kingdom", type:"museum" },
  { id:"tate-modern", name:"Tate Modern", city:"London", country:"United Kingdom", type:"museum" },
  { id:"tate-britain", name:"Tate Britain", city:"London", country:"United Kingdom", type:"museum" },
  { id:"rijksmuseum", name:"Rijksmuseum", city:"Amsterdam", country:"Netherlands", type:"museum" },
  { id:"van-gogh-museum", name:"Van Gogh Museum", city:"Amsterdam", country:"Netherlands", type:"museum" },
  { id:"mauritshuis", name:"Mauritshuis", city:"The Hague", country:"Netherlands", type:"museum" },
  { id:"st-bavo-cathedral", name:"St Bavo's Cathedral", city:"Ghent", country:"Belgium", type:"church" },
  { id:"alte-pinakothek", name:"Alte Pinakothek", city:"Munich", country:"Germany", type:"museum" },
  { id:"stadel", name:"Städel Museum", city:"Frankfurt", country:"Germany", type:"museum" },
  { id:"kunsthistorisches", name:"Kunsthistorisches Museum", city:"Vienna", country:"Austria", type:"museum" },
  { id:"belvedere", name:"Österreichische Galerie Belvedere", city:"Vienna", country:"Austria", type:"museum" },
  { id:"hermitage", name:"The State Hermitage Museum", city:"St Petersburg", country:"Russia", type:"museum" },
  { id:"tretyakov", name:"Tretyakov Gallery", city:"Moscow", country:"Russia", type:"museum" },
  { id:"nasjonalmuseet-oslo", name:"Nasjonalmuseet", city:"Oslo", country:"Norway", type:"museum" },
  { id:"munch-museum", name:"Munch Museum", city:"Oslo", country:"Norway", type:"museum" },
  { id:"oslo-university-aula", name:"University of Oslo Aula", city:"Oslo", country:"Norway", type:"site" },
  { id:"kode-bergen", name:"KODE Bergen Art Museum", city:"Bergen", country:"Norway", type:"museum" },

  /* ---- United States ---- */
  { id:"met", name:"The Metropolitan Museum of Art", city:"New York", country:"United States", type:"museum" },
  { id:"moma", name:"The Museum of Modern Art", city:"New York", country:"United States", type:"museum" },
  { id:"neue-galerie", name:"Neue Galerie", city:"New York", country:"United States", type:"museum" },
  { id:"art-institute-chicago", name:"The Art Institute of Chicago", city:"Chicago", country:"United States", type:"museum" },
  { id:"national-gallery-dc", name:"National Gallery of Art", city:"Washington, D.C.", country:"United States", type:"museum" },
  { id:"getty", name:"The Getty Center", city:"Los Angeles", country:"United States", type:"museum" },
  { id:"mfa-boston", name:"Museum of Fine Arts", city:"Boston", country:"United States", type:"museum" },
  { id:"phillips-collection", name:"The Phillips Collection", city:"Washington, D.C.", country:"United States", type:"museum" },

  /* ---- Türkiye ---- */
  { id:"pera-museum", name:"Pera Museum", city:"Istanbul", country:"Türkiye", type:"museum" },
  { id:"istanbul-modern", name:"İstanbul Modern", city:"Istanbul", country:"Türkiye", type:"museum" },
  { id:"sakip-sabanci", name:"Sakıp Sabancı Museum", city:"Istanbul", country:"Türkiye", type:"museum" },
  { id:"istanbul-resim-heykel", name:"İstanbul Resim ve Heykel Müzesi", city:"Istanbul", country:"Türkiye", type:"museum" },

  /* ---- rest of the world ---- */
  { id:"nmwa-tokyo", name:"National Museum of Western Art", city:"Tokyo", country:"Japan", type:"museum" },
  { id:"ngv", name:"National Gallery of Victoria", city:"Melbourne", country:"Australia", type:"museum" },
  { id:"masp", name:"São Paulo Museum of Art", city:"São Paulo", country:"Brazil", type:"museum" }
];
