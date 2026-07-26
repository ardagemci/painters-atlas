"""ad-hoc DOM probe: python3 probe.py <route> <js-expression-returning-JSON-string>"""
import json, os, sys
H = "/Users/ardagemci/Claude/painters-atlas/protocol/tasks/PIG-001/evidence/harness/cdp-r2"
sys.path.insert(0, H)
import cdp
PORT = int(os.environ.get("CDP_PORT", "9333"))
b = cdp.Browser(port=PORT)
try:
    b.metrics(1440, 1200)
    b.goto(cdp.BASE + "/index.html?p=1" + sys.argv[1], settle=2.4)
    print(b.ev(sys.argv[2]))
finally:
    b.close()
