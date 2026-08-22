"""Backlog C2 — numbered data families must be DISCOVERED, not listed.

`catalog-5.js` was named in five separate places and `artists-18.js` in three.
A new `catalog-6.js` was then picked up by whichever lists someone remembered
and silently skipped by the rest — and the quiet ones were the rights audit and
the validator, where a miss is least visible. It is a real trap, not a
hypothetical: adding `artists-18.js` in this repository required editing three
files, and forgetting one would have left four painters invisible to a tool that
still reported success.

These tests assert the absence of hard-coded lists. They are deliberately about
SHAPE rather than behaviour, because the behaviour only breaks on the day
someone adds a file — which is exactly the day nobody is looking.
"""
import glob
import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


class FileDiscoveryTest(unittest.TestCase):
    #: A hard-coded member of a numbered family, e.g. "catalog-3.js" or
    #: "artists-12.js", appearing as a quoted string in a tool.
    MEMBER = re.compile(r'"(?:catalog|artists)-\d+\.js"')

    def test_jxa_tools_do_not_list_family_members(self):
        for tool in ("tools/validate.jxa.js", "tools/build_seo.jxa.js"):
            src = read(tool)
            hits = self.MEMBER.findall(src)
            self.assertEqual(hits, [], f"{tool} hard-codes {hits} — use familyFiles()")
            self.assertIn("familyFiles(", src, f"{tool} lost its discovery helper")

    def test_python_tools_do_not_list_family_members(self):
        for tool in ("tools/audit_artwork_rights.py", "tools/asset_inventory.py"):
            src = read(tool)
            # a list literal of members, not a docstring mention
            bad = re.findall(r'=\s*\[\s*"catalog-\d+\.js"', src)
            self.assertEqual(bad, [], f"{tool} hard-codes a catalog list")

    def test_discovery_is_numeric_not_lexical(self):
        """catalog-10 must follow catalog-9, not catalog-1."""
        for tool in ("tools/validate.jxa.js", "tools/build_seo.jxa.js"):
            src = read(tool)
            helper = src.split("function familyFiles(")[1].split("\n}")[0]
            self.assertIn("match(/\\d+/)", helper,
                          f"{tool}'s familyFiles sorts lexically; catalog-10 would load before catalog-2")

    def test_index_html_families_are_complete_and_contiguous(self):
        """index.html cannot glob, so build_seo regenerates its tags. If the page
        and the filesystem disagree, the browser is loading a different atlas
        from the one every tool validated."""
        html = read("index.html")
        for prefix in ("catalog", "artists"):
            on_disk = sorted(
                int(re.search(rf"{prefix}-(\d+)\.js", p).group(1))
                for p in glob.glob(os.path.join(ROOT, "js", f"{prefix}-*.js")))
            in_page = sorted(
                int(n) for n in re.findall(rf'<script src="js/{prefix}-(\d+)\.js', html))
            self.assertEqual(in_page, on_disk,
                             f"index.html {prefix} tags {in_page} != files on disk {on_disk}")
            self.assertEqual(on_disk, list(range(1, len(on_disk) + 1)),
                             f"{prefix} family has a gap: {on_disk}")

    def test_a_new_family_member_is_picked_up_with_no_edits(self):
        """The proof the rest of this file only approximates: drop a real file in
        and confirm the validator counts it, having changed nothing else."""
        probe = os.path.join(ROOT, "js", "catalog-9999.js")
        before = self._catalog_count()
        with open(probe, "w", encoding="utf-8") as fh:
            fh.write('window.CATALOG = (window.CATALOG || []).concat([\n'
                     '{ id:"c2-discovery-probe", tier:2, title:"Probe",\n'
                     '  artistId:"leonardo-da-vinci", year:{ display:"1500", sort:1500 },\n'
                     '  movements:["renaissance"], techniques:["oil-painting"], nation:"italy",\n'
                     '  museum:{ id:"louvre", name:"Musée du Louvre", city:"Paris" },\n'
                     '  image:{ status:"none" }, tags:["quiet"] }\n]);\n')
        try:
            after = self._catalog_count()
        finally:
            os.remove(probe)
        self.assertEqual(after, before + 1,
                         "a new js/catalog-*.js was not discovered by the validator")

    @staticmethod
    def _catalog_count():
        r = subprocess.run(
            ["osascript", "-l", "JavaScript", "tools/validate.jxa.js"],
            cwd=ROOT, capture_output=True, text=True, timeout=180)
        m = re.search(r"catalog: (\d+)", r.stdout)
        if not m:
            raise AssertionError("validator printed no catalog count:\n" + r.stdout[:400])
        return int(m.group(1))


if __name__ == "__main__":
    unittest.main()
