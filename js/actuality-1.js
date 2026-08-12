/* PIGMENT — Actuality (docs/ACTUALITY.md). Backlog B2.

   A monthly editorial ritual that answers the news out of the collection. Two
   product types:

     kind:"list"     a blockbuster-news list — works connected to the story by
                     art-historical association, each with its own paragraph.
                     `listId` points at an EDITORIAL_LISTS entry.
     kind:"article"  the photo-to-painting comparison, joined by visual rhyme.
                     The article is mostly about the PAINTING; one or two lines
                     touch the news photo. `workId` points at a catalog record.

   Hard rules, all of them load-bearing:

   * NOTHING here illustrates the news. Pigment cannot licence a news
     photograph, and that constraint is the reason the format is any good: the
     list has to answer the story out of the atlas instead of decorating it.
   * `source` is a real, checkable report and the entry states only what that
     report states. No entry is written from memory.
   * `published` is the cadence date. Copy must never imply the site knows what
     happened today — it does not, and there is no backend that could.
   * `sensitive:true` suppresses the comic register (ACTUALITY.md §5). Default
     to true when unsure. No entry at all about a person's death, crime,
     illness or legal trouble.
   * Living people are named only as the cited report names them, and the joke
     lands on the situation, never on the person (ACTUALITY.md §6). */
window.ACTUALITY = [

{ id:"lebron-to-philadelphia-2026",
  kind:"list",
  published:"2026-07-24",
  headline:"LeBron James signs with the Philadelphia 76ers",
  newsline:"Announced 24 July 2026: a two-year, $8m deal with a player option, at forty-one, for a record twenty-fourth NBA season alongside Joel Embiid and Tyrese Maxey.",
  source:{ name:"ESPN", url:"https://www.espn.com/nba/story/_/id/49440164/lebron-chooses-76ers-sign-2-year-8-million-contract" },
  hook:"The King goes to Philadelphia. So did a lot of paintings.",
  listId:"the-king-goes-to-philadelphia",
  coverStyle:"mary-cassatt",   // generated in her manner; shown on BOTH the card and the list page
  sensitive:false }

,

{ id:"amazon-deforestation-2026",
  kind:"list",
  published:"2026-08-10",
  headline:"Amazon deforestation falls to its lowest in a decade",
  newsline:"Reported 10 July 2026 by Brazil's National Institute for Space Research (INPE): 1,295 square kilometres cleared between January and June 2026, a 38% fall on the same period in 2025 and the lowest figure for that stretch since 2016.",
  source:{ name:"AFP via Phys.org", url:"https://phys.org/news/2026-07-brazil-deforestation-amazon.html" },
  hook:"Good news about a forest. Painters have been inventing them for centuries.",
  listId:"the-forest-that-stopped-shrinking",
  coverStyle:"henri-rousseau",
  sensitive:false }

];
