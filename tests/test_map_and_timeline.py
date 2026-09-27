"""Two places where a painter can exist in the data and still not appear.

The world map (#/nations) pins a nation only if js/taxonomy.js gives it a
NATION_COORDS anchor. Indonesia entered the taxonomy with Raden Saleh in the E3
batch and received no anchor, so for a month the map showed 41 of 42 nations and
nothing complained: the validator checks that ids resolve, not that they are
drawn.

The grand timeline (#/timeline) drew every painter from a hard-coded axis start
of 1240, so Fan Kuan (b. 960) and Guo Xi (b. 1020) sat entirely off its left
edge. The axis is now derived from the data in js/app.js; this file guards that
the derivation stays, and that the data it reads never produces an off-canvas
bar.
"""
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_jxa(expression):
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    files = [s for s in re.findall(r'<script src="js/([^"?]+)', html) if s != "app.js"]
    script = r'''
ObjC.import("Foundation");
function read(p){ return ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null)); }
var window = {};
%s.forEach(function(f){ eval(read(%s + f)); });
JSON.stringify(%s);
''' % (json.dumps(files), json.dumps(str(ROOT / "js") + "/"), expression)
    with tempfile.NamedTemporaryFile("w", suffix=".jxa.js", delete=False, encoding="utf-8") as f:
        f.write(script)
        path = Path(f.name)
    try:
        out = subprocess.run(["osascript", "-l", "JavaScript", str(path)],
                             capture_output=True, text=True, timeout=120)
    finally:
        path.unlink(missing_ok=True)
    if out.returncode:
        raise AssertionError("JXA failed: " + (out.stderr or out.stdout))
    return json.loads(out.stdout.strip())


UNPINNED = r'''(function(){
  var used = {};
  window.ARTISTS.forEach(function(a){ used[a.nation] = true; });
  var ids = {};
  window.NATIONS.forEach(function(n){ ids[n.id] = true; });
  return {
    nations: window.NATIONS.length,
    unpinned: Object.keys(used).filter(function(id){ return !window.NATION_COORDS[id]; }).sort(),
    stray: Object.keys(window.NATION_COORDS).filter(function(id){ return !ids[id]; }).sort()
  };
})()'''


class TestWorldMapPins(unittest.TestCase):
    def test_every_nation_with_a_painter_has_a_pin(self):
        r = run_jxa(UNPINNED)
        self.assertGreaterEqual(r["nations"], 42)          # vacuity: the taxonomy loaded
        self.assertEqual(r["unpinned"], [], "nations with painters but no NATION_COORDS anchor")
        self.assertEqual(r["stray"], [], "NATION_COORDS entries for no nation")

    def test_negative_control_a_removed_anchor_is_caught(self):
        r = run_jxa("(delete window.NATION_COORDS.indonesia, " + UNPINNED + ")")
        self.assertEqual(r["unpinned"], ["indonesia"])


class TestTimelineAxis(unittest.TestCase):
    APP = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    def test_axis_start_is_derived_from_the_painters(self):
        m = re.search(r"const TL_Y0 = (.+);", self.APP)
        self.assertIsNotNone(m)
        self.assertIn("a.born", m.group(1), "TL_Y0 is a literal again; painters born before it vanish")

    def test_no_painter_is_born_before_the_axis(self):
        """Evaluate the same expression js/app.js uses against the real roster."""
        expr = re.search(r"const TL_Y0 = (.+);", self.APP).group(1)
        r = run_jxa("(function(){ var A = window.ARTISTS; var y0 = %s; "
                    "return { y0: y0, finite: isFinite(y0), n: A.length, "
                    "early: A.filter(function(a){ return !(a.born >= y0); }).map(function(a){ return a.name; }) }; })()"
                    % expr)
        # vacuity: a NaN start would make every comparison false and "early" empty
        self.assertTrue(r["finite"], "TL_Y0 evaluated to %r" % r["y0"])
        self.assertGreaterEqual(r["n"], 300)
        self.assertEqual(r["early"], [], "painters drawn off the timeline's left edge")


if __name__ == "__main__":
    unittest.main()
