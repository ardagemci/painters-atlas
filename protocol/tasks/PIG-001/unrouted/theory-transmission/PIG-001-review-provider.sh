#!/bin/sh
set -eu

case "${PIGMENT_PHASE:-}" in
  review)
    exec /usr/bin/python3 -c '
import json, os
path = "/Users/ardagemci/Claude/PIG-001-theory-transmission/PIG-001-theoretical-review.json"
with open(path, encoding="utf-8") as handle:
    message = json.load(handle)
expected = json.loads(os.environ["PIGMENT_EXPECTED_MESSAGE"])
message["created_at"] = expected["created_at"]
print(json.dumps(message))
'
    ;;
  theory-liaison:build_review)
    exec /usr/bin/python3 -c '
import json, os
path = "/Users/ardagemci/Claude/PIG-001-theory-transmission/PIG-001-theoretical-review-liaison.json"
with open(path, encoding="utf-8") as handle:
    packet = json.load(handle)
expected = json.loads(os.environ["PIGMENT_EXPECTED_ANALYST"])
for key, value in expected.items():
    packet[key] = value
print(json.dumps(packet))
'
    ;;
  *)
    printf 'Unsupported Pigment provider phase: %s\n' "${PIGMENT_PHASE:-unset}" >&2
    exit 2
    ;;
esac
