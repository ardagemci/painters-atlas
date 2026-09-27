/* Pigment — how search compares text.

   searchFold(s) turns a name into the form search matches against: lower case,
   accents dropped, and the handful of letters that have no accent to drop
   spelled the way a visitor types them. Both sides go through it — the index
   (js/app.js, srKeys and metaKey) and the visitor's query — so "cezanne" finds
   Paul Cézanne and "ibrahim calli" finds İbrahim Çallı.

   Why this exists. Until 2026-09-27 search only lower-cased, so the query had
   to carry the same accents as the name. 51 of the atlas's 300 painters have
   accented names, including seven of its thirteen Turkish painters, and an
   ordinary keyboard search for "cezanne", "miro", "velazquez", "durer",
   "gerome", "zurbaran", "bocklin", "hammershoi" or "dogancay" returned nothing.
   "dali" returned Grande Odalisque, by substring. Turkish capitals were worse
   than accents: lower-casing "İ" gives "i" plus a combining dot, so "ibrahim"
   could not match İbrahim even letter for letter.

   What it does, in order:
   1. NFD splits a letter from its accent (é → e + ◌́, İ → I + ◌̇); the accents
      are then removed.
   2. Letters Unicode does not decompose are spelled out: ı ł ø æ œ ß đ ð þ.
   3. Hyphens and dashes become spaces, so "torres garcia" finds Torres-García,
      "toulouse lautrec" finds Toulouse-Lautrec, and a query may run across the
      dash in "Nocturne in Black and Gold — The Falling Rocket". Runs of spaces
      collapse.
   4. Lower case.

   Display is never folded; only the strings compared are.
   tests/test_searchfold.py runs this file and requires every artist, artwork,
   museum, movement, technique, era and nation name in the atlas to fold to
   plain ASCII — so a new name with a letter this table lacks fails the suite
   rather than silently becoming unfindable. */
var SEARCH_FOLD_LETTERS = {
  "ı":"i", "ł":"l", "Ł":"l", "ø":"o", "Ø":"o", "æ":"ae", "Æ":"ae",
  "œ":"oe", "Œ":"oe", "ß":"ss", "đ":"d", "Đ":"d", "ð":"d", "Ð":"d",
  "þ":"th", "Þ":"th"
};
function searchFold(s){
  return String(s == null ? "" : s)
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[ıłŁøØæÆœŒßđĐðÐþÞ]/g, function(c){ return SEARCH_FOLD_LETTERS[c]; })
    .replace(/[-\u2010-\u2015]/g, " ")
    .replace(/\s+/g, " ")
    .toLowerCase();
}
window.searchFold = searchFold;
