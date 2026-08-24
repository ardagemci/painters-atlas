/* Pigment photo credits — GENERATED FILE, do not edit by hand.
   Regenerate with:  python3 tools/build_photo_credits.py
   Sources: protocol/tasks/PIG-001/evidence/museum-photo-rights.json
            protocol/tasks/PIG-001/evidence/artwork-image-rights.json
   Generated: 2026-08-24

   Two registries, both read by js/app.js:

   window.PHOTO_CREDITS — museum building photographs, keyed by venue id
     (js/venues.js). One entry per photograph in js/museums-1.js. 120
     entries, 102 of which carry a licence requiring attribution; the
     other 18 carry a Commons public-domain or CC0 assertion instead,
     and are credited as a courtesy.

   window.IMAGE_CREDITS — artwork images that require attribution, keyed by
     Commons file title as derived from the image URL (see commonsTitle() in
     js/app.js). 24 entries. Files whose Commons metadata asserts a
     public-domain or CC0 basis are deliberately absent: that assertion carries
     no attribution obligation, and the existing "image via Wikimedia Commons"
     source link already names their origin.

   Nothing in this file, and nothing generated from it, is a rights clearance.
   Every licence string is what the Commons file page asserts (OD-5, AC12).

   Credit shape: { author, license, licenseUrl, page, required }
     author      photographer / uploader, plain text (may be absent)
     license     licence short name, e.g. "CC BY-SA 4.0"
     licenseUrl  licence deed (absent where the asserted basis is a
                 public-domain tag, which has no deed)
     page        Commons file page — the "source" half of TASL
     required    true when the licence requires attribution

   All text is plain — Commons markup is stripped at build time — and js/app.js
   escapes it again on output. This file asserts no legal clearance (OD-5); it
   records what Commons asserts. */

window.PHOTO_CREDITS = {
"accademia-florence": { author:"Rhododendrites", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:David_at_the_Galleria_dell%27Accademia_(61351).jpg", required:true },
"accademia-venice": { author:"Didier Descouens", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Accademia_(Venice).jpg", required:true },
"albertina": { author:"C.Stadler/Bwag", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Wien_-_Albertina.JPG", required:true },
"alte-pinakothek": { author:"Andreas Praefcke", license:"CC BY 3.0", licenseUrl:"https://creativecommons.org/licenses/by/3.0", page:"https://commons.wikimedia.org/wiki/File:Alte_Pinakothek_2009.jpg", required:true },
"art-institute-chicago": { author:"Ken Lund from Reno, Nevada, USA", license:"CC BY-SA 2.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/2.0", page:"https://commons.wikimedia.org/wiki/File:Art_Institute_of_Chicago_Building,_Chicago,_Illinois_(11004251406).jpg", required:true },
"ateneum": { author:"Htm", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Ateneum_main_facade.jpg", required:true },
"baltimore-museum-of-art": { author:"Nrswanson (talk) at en.wikipedia", license:"Public domain", page:"https://commons.wikimedia.org/wiki/File:Baltimore_Museum_of_Art_entrance.jpg" },
"barnes-foundation": { author:"ajay_suresh", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Barnes_Foundation_(53574516274).jpg", required:true },
"belvedere": { author:"Diego Delso", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Palacio_Belvedere,_Viena,_Austria,_2020-02-01,_DD_93-95_HDR.jpg", required:true },
"brera": { author:"Jean-Christophe BENOIST", license:"CC BY 3.0", licenseUrl:"https://creativecommons.org/licenses/by/3.0", page:"https://commons.wikimedia.org/wiki/File:Milan_-_Pinacoth%C3%A8que_de_Brera_-_Cour_int%C3%A9rieure.jpg", required:true },
"buffalo-akg": { author:"BuffaloAKG14222", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:2024.10.10_AKGCampusExteriorDronePhotos-1001.jpg", required:true },
"capodimonte": { author:"IlSistemone", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:ReggiaCapodimonte.JPG", required:true },
"centre-pompidou": { author:"Stefan Drößler", license:"CC BY 4.0", licenseUrl:"https://creativecommons.org/licenses/by/4.0", page:"https://commons.wikimedia.org/wiki/File:L%C3%BCftungsrohre_Place_George_Pompidou_Paris.jpg", required:true },
"courtauld-gallery": { author:"Mike Peel (www.mikepeel.net)", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Coultauld_Galleries.jpg", required:true },
"czartoryski": { author:"Zygmunt Put", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Czartoryski_Palace,_17-19_%C5%9Bwi%C4%99tego_Jana_street,_Old_Town,_Krak%C3%B3w,_Poland.jpg", required:true },
"dali-museum-florida": { author:"Ebyabe", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:St._Pete_Dali_Museum03.jpg", required:true },
"dallas-museum-art": { author:"cliff williams", license:"CC BY-SA 2.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/2.0", page:"https://commons.wikimedia.org/wiki/File:Entrance_of_Dallas_Museum_-_Mar_3,_2009.jpg", required:true },
"detroit-institute-of-arts": { author:"Michael Barera", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Detroit_Institute_of_Arts_August_2011_01.jpg", required:true },
"doria-pamphilj": { author:"Fiat 500e", license:"CC BY 4.0", licenseUrl:"https://creativecommons.org/licenses/by/4.0", page:"https://commons.wikimedia.org/wiki/File:Palazzo_Doria_Pamphilj.jpg", required:true },
"galleria-borghese": { author:"José Luiz", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Facade_-_Galleria_Borghese_-_Rome_-_Italy_2015.JPG", required:true },
"gemaldegalerie-berlin": { author:"Andreas Praefcke", license:"CC BY 3.0", licenseUrl:"https://creativecommons.org/licenses/by/3.0", page:"https://commons.wikimedia.org/wiki/File:Berlin_Kulturforum_2002a.jpg", required:true },
"gemaldegalerie-dresden": { author:"Ingersoll", license:"Public domain", page:"https://commons.wikimedia.org/wiki/File:Dresden-Zwinger-Courtyard.11.JPG" },
"getty": { author:"Jelson25", license:"Public domain", page:"https://commons.wikimedia.org/wiki/File:Aerial_Getty_Museum.jpg" },
"glenstone": { author:"Fuzheado", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Glenstone-2018-10-13-courtyard-1.jpg", required:true },
"groeningemuseum": { author:"Navy8300", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Brugge_-_Dijver_12_-Voormalig_poortgebouw_van_de_proosdij_van_Onze-Lieve-Vrouw,_heden_ingang_van_het_Groeningemuseum_-_82339.jpg", required:true },
"guggenheim-ny": { author:"Ajay Suresh from New York, NY, USA", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Solomon_R._Guggenheim_Museum_(48059131351).jpg", required:true },
"harry-ransom-center": { author:"Larry D. Moore", license:"CC BY 4.0", licenseUrl:"https://creativecommons.org/licenses/by/4.0", page:"https://commons.wikimedia.org/wiki/File:Harry_ransom_center_2012.jpg", required:true },
"hermitage": { author:"GAlexandrova", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:5174-3._St._Petersburg._Greater_Hermitage.jpg", required:true },
"hirshhorn": { author:"Quadell", license:"CC BY-SA 3.0", licenseUrl:"http://creativecommons.org/licenses/by-sa/3.0/", page:"https://commons.wikimedia.org/wiki/File:Hirshhorn_Museum_and_Sculpture_Garden_-_exterior.jpg", required:true },
"isabella-stewart-gardner": { author:"Amoran002", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:IsabellaStewartGardenerMuseumMainLobby.jpg", required:true },
"k20-dusseldorf": { author:"Leoni1234", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Bild_K20_aktuell.jpg", required:true },
"kelvingrove": { author:"瑞丽江的河水", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Kelvingrove_Art_Gallery_and_Museum_-_aerial_-_2025-04-17.jpg", required:true },
"kenwood-house": { author:"MrsEllacott", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Kenwood_House_2.jpg", required:true },
"kimbell-art-museum": { author:"Carol M. Highsmith", license:"Public domain", page:"https://commons.wikimedia.org/wiki/File:Kimbell_Art_Museum_Highsmith.jpg" },
"kode-bergen": { author:"Forbes Johnston", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:BERGEN_Norway_Lille_Lungeg%C3%A5rdsvannet_KODE_Art_Museum_Kunsthall_Grieghallen_Foreningsgaten_Nyg%C3%A5rdsg._etc_View_from_Mount_Floyen_2019-08-28_by_Forbes_Johnston_Flickr_Some_rights_reserved.jpg", required:true },
"kroller-muller": { author:"Gerardus", license:"Public domain", page:"https://commons.wikimedia.org/wiki/File:Entrance_Kr%C3%B6ller-M%C3%BCller_Museum.JPG" },
"kunsthalle-mannheim": { author:"Immanuel Giel", license:"Public domain", page:"https://commons.wikimedia.org/wiki/File:Kunsthalle_Mannheim_Eingangsportal.jpg" },
"kunsthistorisches": { author:"Hubertl", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:AT_13763_Exterior_of_the_Kunsthistorisches_Museum,_Vienna-4.jpg", required:true },
"kunstmuseum-basel": { author:"Wladyslaw Sojka", license:"FAL", licenseUrl:"http://artlibre.org/licence/lal/en", page:"https://commons.wikimedia.org/wiki/File:Basel_-_2017_-_Kunstmuseum_Basel_-_Neubau.jpg", required:true },
"kunstmuseum-den-haag": { author:"Choinowski", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Kunstmuseum_Den_Haag.jpg", required:true },
"lazaro-galdiano": { author:"Luis García (Zaqarbal)", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Museo_L%C3%A1zaro_Galdiano_(Madrid)_02.jpg", required:true },
"leopold-museum": { author:"Gugerell", license:"CC0", licenseUrl:"http://creativecommons.org/publicdomain/zero/1.0/deed.en", page:"https://commons.wikimedia.org/wiki/File:Wien_07_Leopold_Museum_a.jpg" },
"louvre": { author:"Benh LIEU SONG (Flickr)", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Louvre_Museum_Wikimedia_Commons.jpg", required:true },
"mak-vienna": { author:"Gugerell", license:"CC0", licenseUrl:"http://creativecommons.org/publicdomain/zero/1.0/deed.en", page:"https://commons.wikimedia.org/wiki/File:Wien_01_Museum_f%C3%BCr_angewandte_Kunst_a.jpg" },
"masp": { author:"Mauro Cateb", license:"CC BY-SA 2.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/2.0", page:"https://commons.wikimedia.org/wiki/File:Novo_MASP.jpg", required:true },
"mauritshuis": { author:"Michielverbeek", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Den_Haag,_het_Mauritshuis_RM17650_foto5_2015-08-05_19.06.jpg", required:true },
"met": { author:"Hugo Schneider", license:"CC BY-SA 2.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/2.0", page:"https://commons.wikimedia.org/wiki/File:Metropolitan_Museum_of_Art_(The_Met)_-_Central_Park,_NYC.jpg", required:true },
"mfa-boston": { author:"ajay_suresh", license:"CC BY 4.0", licenseUrl:"https://creativecommons.org/licenses/by/4.0", page:"https://commons.wikimedia.org/wiki/File:Museum_of_Fine_Arts,_Boston_(54954248311).jpg", required:true },
"minneapolis-institute-of-art": { license:"Public domain", page:"https://commons.wikimedia.org/wiki/File:Facade_from_the_East,_Minneapolis_Institute_of_Arts_-_DPLA_-_ed3a5aee7eed55bb80f51eb4be6a763b.jpg" },
"mnaa-lisbon": { author:"Fulviusbsas", license:"CC BY-SA 3.0", licenseUrl:"http://creativecommons.org/licenses/by-sa/3.0/", page:"https://commons.wikimedia.org/wiki/File:MNAA.jpg", required:true },
"moa-museum-of-art": { author:"663highland", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:231007_MOA_Museum_of_Art_Atami_Japan09s3.jpg", required:true },
"moca-la": { author:"Grandave-1986", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Moca-exterior.jpg", required:true },
"moderna-museet": { author:"Emmawickstrm", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:MODERN_MUSEUM_MODERNA_MUSEET_STOCKHOLM_(19).jpg", required:true },
"moma": { author:"hibino", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:MoMa_NY_USA_1.jpg", required:true },
"munch-museum": { author:"Premeditated", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:The_new_Munch_Museum_(white_color_sign).jpg", required:true },
"musee-dorsay": { author:"Sanchezn", license:"CC BY-SA 3.0", licenseUrl:"http://creativecommons.org/licenses/by-sa/3.0/", page:"https://commons.wikimedia.org/wiki/File:North_side_of_Orsay_Museum_building,_4_August_2007.jpg", required:true },
"musee-marmottan": { author:"Gerda Arendt", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Mus%C3%A9e_Marmottan_Monet,_Paris,_from_street.jpg", required:true },
"musee-pau": { author:"Patrice Bon", license:"CC0", licenseUrl:"http://creativecommons.org/publicdomain/zero/1.0/deed.en", page:"https://commons.wikimedia.org/wiki/File:Mus%C3%A9e_des_Beaux-Arts_de_Pau.jpg" },
"musee-picasso-paris": { author:"LPLT", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:H%C3%B4tel_Sal%C3%A9.JPG", required:true },
"museo-arte-moderno-mexico": { author:"Gobierno CDMX", license:"CC0", licenseUrl:"http://creativecommons.org/publicdomain/zero/1.0/deed.en", page:"https://commons.wikimedia.org/wiki/File:Museo_de_Arte_Moderno_DSC0023_(35557149325).jpg" },
"museo-dolores-olmedo": { author:"Juan Carlos Fonseca Mata", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Museo_Dolores_Olmedo,_Xochimilco,_Ciudad_de_M%C3%A9xico_-_Entrada.jpg", required:true },
"museo-frida-kahlo": { author:"Nachtwächter", license:"CC BY-SA 3.0", licenseUrl:"http://creativecommons.org/licenses/by-sa/3.0/", page:"https://commons.wikimedia.org/wiki/File:Museo_Frida_Kahlo.JPG", required:true },
"museu-picasso-barcelona": { author:"uayebt", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Museu_Picasso_Barcelona.jpg", required:true },
"museum-ludwig": { author:"Thomas Robbin", license:"CC BY-SA 3.0", licenseUrl:"http://creativecommons.org/licenses/by-sa/3.0/", page:"https://commons.wikimedia.org/wiki/File:Museum_Ludwig_002.jpg", required:true },
"nasjonalmuseet-oslo": { author:"Premeditated", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Nye_Nasjonalmuseet_(2022)_(2).jpg", required:true },
"national-gallery-australia": { author:"Thennicke", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:National_Gallery_from_SW,_Canberra_Australia.jpg", required:true },
"national-gallery-dc": { author:"ajay_suresh", license:"CC BY 4.0", licenseUrl:"https://creativecommons.org/licenses/by/4.0", page:"https://commons.wikimedia.org/wiki/File:National_Gallery_of_Art_-_2026_(55255088792).jpg", required:true },
"national-gallery-london": { author:"Diego Delso", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Galer%C3%ADa_Nacional,_Londres,_Inglaterra,_2014-08-07,_DD_036.JPG", required:true },
"national-museum-korea": { author:"Jinah78", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Front_view_of_national_museum_of_korea.jpg", required:true },
"national-museum-warsaw": { author:"Wistula", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:WarsawNationalMuseumDSC_2528.JPG", required:true },
"neue-galerie": { author:"Gryffindor", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:1048_5th_Avenue_001.JPG", required:true },
"ngma-new-delhi": { author:"Gryffindor", license:"CC0", licenseUrl:"http://creativecommons.org/publicdomain/zero/1.0/deed.en", page:"https://commons.wikimedia.org/wiki/File:Jaipur_House_2019_(2).jpg" },
"ny-carlsberg-glyptotek": { author:"kallerna", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Ny_Carlsberg_Glyptotek_winter_garden_1.jpg", required:true },
"orangerie": { author:"Homonihilis", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Mus%C3%A9e_de_l%E2%80%99Orangerie_exterior.JPG", required:true },
"oslo-university-aula": { author:"Riksarkivet (National Archives of Norway) from Oslo, Norway", license:"No restrictions", licenseUrl:"https://www.flickr.com/commons/usage/", page:"https://commons.wikimedia.org/wiki/File:Festakt._Universitetets_aula._(8612632859).jpg" },
"palazzo-barberini": { author:"PubblicUsername", license:"CC BY 4.0", licenseUrl:"https://creativecommons.org/licenses/by/4.0", page:"https://commons.wikimedia.org/wiki/File:Palazzo_Barberini_-_esterno.jpg", required:true },
"palazzo-colonna": { author:"Vadim Zhivotovsky", license:"CC BY 3.0", licenseUrl:"https://creativecommons.org/licenses/by/3.0", page:"https://commons.wikimedia.org/wiki/File:Palazzo_Colonna_-_panoramio.jpg", required:true },
"pera-museum": { author:"Tatiana Matlina", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Istanbul_Beyoglu_Pera_museum.jpg", required:true },
"philadelphia-museum-of-art": { author:"User:Rgordon6~commonswiki", license:"CC0", licenseUrl:"http://creativecommons.org/publicdomain/zero/1.0/deed.en", page:"https://commons.wikimedia.org/wiki/File:Philadelphia_Museum_of_Art_2005.jpg" },
"phoenix-art-museum": { author:"Chanel Wheeler", license:"CC BY-SA 2.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/2.0", page:"https://commons.wikimedia.org/wiki/File:Main_entrance_to_Phoenix_Art_Museum_-_19_June_2008.jpg", required:true },
"pio-monte-della-misericordia": { author:"Giuseppe Guida", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Pio_Monte_della_Misericordia._(8067).jpg", required:true },
"prado": { author:"Emilio J. Rodríguez Posada", license:"CC BY-SA 2.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/2.0", page:"https://commons.wikimedia.org/wiki/File:Museo_del_Prado_2016_(25185969599).jpg", required:true },
"pushkin-museum": { author:"user:Ghirlandajo", license:"CC BY-SA 3.0", licenseUrl:"http://creativecommons.org/licenses/by-sa/3.0/", page:"https://commons.wikimedia.org/wiki/File:Gmii.jpg", required:true },
"reina-sofia": { author:"Benjamín Núñez González", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Museo_Nacional_Centro_de_Arte_Reina_Sof%C3%ADa,_detalles_del_exterior,_Madrid,_Espa%C3%B1a,_2016_01.JPG", required:true },
"rijksmuseum": { author:"Trougnouf (Benoit Brummer)", license:"CC BY 4.0", licenseUrl:"https://creativecommons.org/licenses/by/4.0", page:"https://commons.wikimedia.org/wiki/File:South_facade_of_the_Rijksmuseum_Amsterdam_(DSCF0528).jpg", required:true },
"rothko-chapel": { author:"David Van Horn from Boston, MA, USA", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Rothko_Chapel_-_1_August_2010.jpg", required:true },
"royal-collection": { author:"Diliff", license:"CC BY 2.5", licenseUrl:"https://creativecommons.org/licenses/by/2.5", page:"https://commons.wikimedia.org/wiki/File:Windsor_Castle_at_Sunset_-_Nov_2006.jpg", required:true },
"royal-museums-brussels": { author:"Michel wal", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Mus%C3%A9es_Royaux_des_Beaux-Arts_Belgique_1101.jpg", required:true },
"russian-museum": { author:"Екатерина Борисова", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9_%D0%B4%D0%B2%D0%BE%D1%80%D0%B5%D1%86,_%D0%B4%D0%B2%D0%BE%D1%8003.jpg", required:true },
"san-luigi-dei-francesi": { author:"Chabe01", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:%C3%89glise_San_Luigi_Francesi_-_Rome_(IT62)_-_2021-08-28_-_2.jpg", required:true },
"santa-maria-delle-grazie": { author:"Marcin Białek", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Santa_Maria_delle_Grazie_Milan_2013.jpg", required:true },
"santa-maria-novella": { author:"Joseolgon", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Santa_Maria_Novella_(Florence)_-_Facade_(3).jpg", required:true },
"santo-tome": { author:"Jose Luis Filpo Cabana", license:"CC BY 3.0", licenseUrl:"https://creativecommons.org/licenses/by/3.0", page:"https://commons.wikimedia.org/wiki/File:Iglesia_de_Santo_Tom%C3%A9_(Toledo)._Torre.jpg", required:true },
"schloss-weissenstein": { author:"Carsten Steger", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Aerial_image_of_the_Schloss_Wei%C3%9Fenstein.jpg", required:true },
"scottish-national-gallery": { author:"瑞丽江的河水", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Scottish_National_Gallery_-_aerial_-_2025-04-19_01.jpg", required:true },
"secession-vienna": { author:"Thomas Ledl", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Secession_2016,_Vienna.jpg", required:true },
"sfmoma": { author:"Beyond My Ken", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:2017_SFMOMA_from_Yerba_Buena_Gardens.jpg", required:true },
"sistine-chapel": { author:"The original uploader was Snowdog at Italian Wikipedia", license:"CC BY-SA 3.0", licenseUrl:"http://creativecommons.org/licenses/by-sa/3.0/", page:"https://commons.wikimedia.org/wiki/File:Sistina-interno.jpg", required:true },
"skagens-museum": { author:"Zejo", license:"Public domain", page:"https://commons.wikimedia.org/wiki/File:Skagens_museum.jpg" },
"st-bavo-cathedral": { author:"Mylius", license:"CC BY-SA 3.0", licenseUrl:"http://creativecommons.org/licenses/by-sa/3.0/", page:"https://commons.wikimedia.org/wiki/File:Gent-Sint-Baafskathedraal_vom_Belfried_aus_gesehen.jpg", required:true },
"st-johns-co-cathedral": { author:"Matthew Axiak", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:St_John%27s_Co-Cathedral,_Valletta_001.jpg", required:true },
"st-peters-basilica": { author:"Alvesgaspar", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Basilica_di_San_Pietro_in_Vaticano_September_2015-1a.jpg", required:true },
"stadel": { author:"DrKssn", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Frankfurt_Staedel_Museum_dk2243.jpg", required:true },
"stanley-museum-iowa": { author:"w_lemay", license:"CC BY-SA 2.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/2.0", page:"https://commons.wikimedia.org/wiki/File:Stanley_Museum_of_Art,_Burlington_Street_and_Museum_Drive,_Iowa_City,_IA.jpg", required:true },
"tate-britain": { author:"Tony Hisgett from Birmingham, UK", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Tate_Britain_(5822081512)_(2).jpg", required:true },
"tate-modern": { author:"Acabashi", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Tate_Modern_-_Bankside_Power_Station.jpg", required:true },
"thyssen-bornemisza": { author:"Kyle Magnuson from Los Angeles, United States", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Site_of_the_Retiro_and_the_Prado_in_Madrid_49_(29684554308).jpg", required:true },
"tokyo-national-museum": { author:"Wiiii", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Tokyo_National_Museum,_Honkan_2010.jpg", required:true },
"toledo-cathedral": { author:"Fernando", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:FP_Toledo_Cathedral_2025_-_West_fa%C3%A7ade.jpg", required:true },
"transfiguration-ilyina-novgorod": { author:"Катерина Фёдорова", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:%D0%A6%D0%B5%D1%80%D0%BA%D0%BE%D0%B2%D1%8C_%D0%A1%D0%BF%D0%B0%D1%81%D0%B0_%D0%9F%D1%80%D0%B5%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F_%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4.jpg", required:true },
"tretyakov": { author:"A.Savin", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Moscow_05-2012_TretyakovGallery.jpg", required:true },
"uffizi": { author:"Verum3414", license:"CC BY 4.0", licenseUrl:"https://creativecommons.org/licenses/by/4.0", page:"https://commons.wikimedia.org/wiki/File:Piazzale_degli_Uffizi_perspective_view,_Florence,_Italy,_August_2025.jpg", required:true },
"van-gogh-museum": { author:"C messier", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Van_Gogh_Museum_7206_rt_HDR.jpg", required:true },
"vancouver-art-gallery": { author:"Dietmar Rabich", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Vancouver_(BC,_Canada),_Art_Gallery_--_2022_--_1923.jpg", required:true },
"vatican-museums": { author:"Américo Toledano", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Museos_Vaticanos_-_Entrada_-_001.jpg", required:true },
"villa-farnesina": { author:"Jean-Pierre Dalbéra from Paris, France", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:La_villa_Farnesina_(Rome)_(34029492720).jpg", required:true },
"wallace-collection": { author:"Dylan Moore", license:"CC BY-SA 2.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/2.0", page:"https://commons.wikimedia.org/wiki/File:Hertford_House,_Manchester_Square,_Marylebone_-_geograph.org.uk_-_7235353.jpg", required:true },
"whitney": { author:"Jim.henderson", license:"CC0", licenseUrl:"http://creativecommons.org/publicdomain/zero/1.0/deed.en", page:"https://commons.wikimedia.org/wiki/File:Gansevoort_Whitney_April_2013_jeh.jpg" },
"wien-museum": { author:"Christine Koblitz", license:"CC0", licenseUrl:"http://creativecommons.org/publicdomain/zero/1.0/deed.en", page:"https://commons.wikimedia.org/wiki/File:Wien_Museum_Neu.jpg" },
"yale-university-art-gallery": { author:"Ragesoss", license:"Public domain", page:"https://commons.wikimedia.org/wiki/File:Yale_University_Art_Gallery_exterior.jpg" }
};

window.IMAGE_CREDITS = {
"File:'David'_by_Michelangelo_Fir_JBU004.jpg": { author:"Jörg Bittner Unna", license:"CC BY 3.0", licenseUrl:"https://creativecommons.org/licenses/by/3.0", page:"https://commons.wikimedia.org/wiki/File:%27David%27_by_Michelangelo_Fir_JBU004.jpg", required:true },
"File:4_hilma_af_klint,_the_ten_largest,_no_9.jpg": { author:"Hilma af Klint", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:4_hilma_af_klint,_the_ten_largest,_no_9.jpg", required:true },
"File:Amsterdam_-_Rijksmuseum_1885_-_The_Gallery_of_Honour_(1st_Floor)_-_The_Windmill_at_Wijk_bij_Duurstede_c._1670_by_Jacob_van_Ruisdael.png": { author:"Txllxt TxllxT", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Amsterdam_-_Rijksmuseum_1885_-_The_Gallery_of_Honour_(1st_Floor)_-_The_Windmill_at_Wijk_bij_Duurstede_c._1670_by_Jacob_van_Ruisdael.png", required:true },
"File:Arezzo_Piero_general_04.JPG": { author:"Miguel Hermoso Cuesta", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Arezzo_Piero_general_04.JPG", required:true },
"File:Chaïm_soutine,_il_piccolo_pasticcere,_1922-23_ca..JPG": { author:"Sailko", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Cha%C3%AFm_soutine,_il_piccolo_pasticcere,_1922-23_ca..JPG", required:true },
"File:Degas_Little_Dancer_PMA(05c)_(15675423180).jpg": { author:"Regan Vercruysse from Stewartsville, New Jersey, USA", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Degas_Little_Dancer_PMA(05c)_(15675423180).jpg", required:true },
"File:Flickr_-_…trialsanderrors_-_Utamaro,_Young_lady_blowing_on_a_poppin,_1790.jpg": { author:"…trialsanderrors", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Flickr_-_%E2%80%A6trialsanderrors_-_Utamaro,_Young_lady_blowing_on_a_poppin,_1790.jpg", required:true },
"File:Grieving_parents_(16127037905).jpg": { author:"Thomas Quine", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Grieving_parents_(16127037905).jpg", required:true },
"File:Ida_Rubinstein_by_V._Serov_(GRM)_FRAME_by_shakko_01.jpg": { author:"Shakko", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Ida_Rubinstein_by_V._Serov_(GRM)_FRAME_by_shakko_01.jpg", required:true },
"File:Isenheimer_Altar_(Colmar)_jm01221_deriv.jpg": { author:"joergens.mi", license:"CC BY-SA 3.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/3.0", page:"https://commons.wikimedia.org/wiki/File:Isenheimer_Altar_(Colmar)_jm01221_deriv.jpg", required:true },
"File:Katsushika_Hokusai,_tempesta_sotto_la_vetta,_dalla_serie_delle_36_vedute_del_monte_fuji,_1831_ca.jpg": { author:"Sailko", license:"CC BY 3.0", licenseUrl:"https://creativecommons.org/licenses/by/3.0", page:"https://commons.wikimedia.org/wiki/File:Katsushika_Hokusai,_tempesta_sotto_la_vetta,_dalla_serie_delle_36_vedute_del_monte_fuji,_1831_ca.jpg", required:true },
"File:Mantegna_-_Camera_degli_Sposi.jpg": { author:"Gonzaloferjar", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Mantegna_-_Camera_degli_Sposi.jpg", required:true },
"File:Max_Beckmann,_Departure.jpg": { author:"Max Beckmann", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Max_Beckmann,_Departure.jpg", required:true },
"File:Mrs._Siddons_as_the_Tragic_Muse_(3051182537).jpg": { author:"Joshua Reynolds", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:Mrs._Siddons_as_the_Tragic_Muse_(3051182537).jpg", required:true },
"File:Osman_I_miniature_by_Nakkaş_Osman.jpg": { author:"Nakkaş Osman", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Osman_I_miniature_by_Nakka%C5%9F_Osman.jpg", required:true },
"File:Paul_gauguin,_vahine_no_te_tiare_(la_donna_coi_fiori),_1891,_MIN_1828,_02.jpg": { author:"Francesco Bini", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Paul_gauguin,_vahine_no_te_tiare_(la_donna_coi_fiori),_1891,_MIN_1828,_02.jpg", required:true },
"File:Peter_Paul_Rubens_-_Descent_from_the_cross_(1617).jpg": { author:"Sailko", license:"CC BY 3.0", licenseUrl:"https://creativecommons.org/licenses/by/3.0", page:"https://commons.wikimedia.org/wiki/File:Peter_Paul_Rubens_-_Descent_from_the_cross_(1617).jpg", required:true },
"File:Piero_della_Francesca_The_Resurrection_detail_VlRan.jpg": { author:"VlRan", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Piero_della_Francesca_The_Resurrection_detail_VlRan.jpg", required:true },
"File:Pieta_de_Michelangelo_-_Vaticano.jpg": { author:"original file by Stanislav Traykov", license:"CC BY 2.5", licenseUrl:"https://creativecommons.org/licenses/by/2.5", page:"https://commons.wikimedia.org/wiki/File:Pieta_de_Michelangelo_-_Vaticano.jpg", required:true },
"File:ROUSSEAU,_Henri_Sleeping_Gypsy_(detail)_1897.jpg": { author:"carulmare", license:"CC BY 2.0", licenseUrl:"https://creativecommons.org/licenses/by/2.0", page:"https://commons.wikimedia.org/wiki/File:ROUSSEAU,_Henri_Sleeping_Gypsy_(detail)_1897.jpg", required:true },
"File:Stubbs_Anatomy_of_the_Horse_2.JPG": { author:"Warburg1866", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Stubbs_Anatomy_of_the_Horse_2.JPG", required:true },
"File:The_Felicity_of_the_Regency_(Skizze_zum_Medici-Zyklus)_-_Peter_Paul_Rubens.jpg": { author:"GoldenArtists", license:"CC BY 4.0", licenseUrl:"https://creativecommons.org/licenses/by/4.0", page:"https://commons.wikimedia.org/wiki/File:The_Felicity_of_the_Regency_(Skizze_zum_Medici-Zyklus)_-_Peter_Paul_Rubens.jpg", required:true },
"File:The_Swing_(P430).jpg": { author:"Ajc994", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:The_Swing_(P430).jpg", required:true },
"File:Triumph_of_Death_Brueghel.jpg": { author:"Pieter Brueghel the Elder", license:"CC BY-SA 4.0", licenseUrl:"https://creativecommons.org/licenses/by-sa/4.0", page:"https://commons.wikimedia.org/wiki/File:Triumph_of_Death_Brueghel.jpg", required:true }
};
