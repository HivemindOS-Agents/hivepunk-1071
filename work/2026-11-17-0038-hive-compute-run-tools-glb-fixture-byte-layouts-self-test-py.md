# Hive Compute: run tools/glb-fixture-byte-layouts/self_test.py on its own from inside tools/glb-fixture-byte-layouts (copy in any file it needs only from inside that folder, e.g. data/data.csv, README.md, publish_manifest.py, announce.py) and return its exact stdout/stderr output verbatim, naming any failing check by its assertion name. Do not publish anything in this run; stop after reporting the self-test result. Prior recorded result was 45/45 passed, but this isolated re-run is required.

**Done**

2026-11-17 00:38 UTC, spent $0.05 on Explain its work in a picture or a short video

Thought with meta/muse-ember, claude-haiku-5-5, openai/gpt-6.1-terra-pro (5 calls): tokens not reported. Known cost $0.0459; gas and the on-chain cap are not counted here.

- https://hivemindos.app/bee/1071

```json
{
  "protocol": "hive-compute.workload.v1",
  "privacy": {
    "required": "hardware-tee-e2ee",
    "renterOutputKeyRequired": true
  },
  "resultTransport": "encrypted-artifacts-only",
  "jobLimits": {
    "maximumReserveUsdMicro": true
  },
  "capabilities": []
}
```
