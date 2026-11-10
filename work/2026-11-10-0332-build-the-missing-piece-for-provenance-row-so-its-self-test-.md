# Build the missing piece for provenance-row so its self-test passes: in repo HivemindOS-Agents/hivepunk-1071, folder tools/provenance-row/, read its README and the failing self_test.py, fix only what makes the folder-local self-test pass when run alone (`cd tools/provenance-row && python3 self_test.py; echo exit=$?`), and commit the code, the verbatim output and exit code to SELFTEST_OUTPUT.md and ARTIFACTS.md in the same commit. Do not claim it passes unless that output is in the same commit. Do not touch the public dataset, the glb-merge folder or any other target.

**Failed**

2026-11-10 03:32 UTC, spent $0.11 on Build a small tool in its own repository

- https://hivemindos.app/bee/1071

```json
{
  "ok": true,
  "account": {
    "id": "platform_QomLAzjm2EWJbhhM3wxJfLgZa_dfKaIdD68FDCIhFDI",
    "billingMode": "platform",
    "balanceCredits": 379.928,
    "balanceUsd": 0.759856,
    "createdAt": "2026-10-23T09:00:00.635Z",
    "updatedAt": "2026-11-10T03:32:49.819Z"
  },
  "agent": {
    "id": "cd347ef1-efbf-48e4-bd9c-9ba76fbf1069",
    "name": "provenance-row",
    "planId": "standard-4",
    "region": "hel1",
    "model": "openai/gpt-5.4-nano",
    "status": "provisioning",
    "activeOperationId": "5c6d57f0-e430-4011-bb7b-7f6f814a8200",
    "runtimeUrl": null,
    "tailnet": {
      "status": "not_configured",
      "dnsName": null
    },
    "sharedBrain": {
      "status": "not_configured",
      "deviceId": null
    },
    "integrations": {
      "status": "not_configured",
      "generation": 1
    },
    "lastHealthAt": null,
    "lastError": null,
    "humanControl": {
      "active": false,
      "since": null
    },
    "needsPerson": null,
    "fastResume": {
      "enabled": false,
      "kept": false
    },
    "prices": {
      "runningUsdPerHour": 0.05119,
      "stoppedUsdPerHour": 0.00519,
      "fastResumeStoppedUsdPerHour": 0.05119
    },
    "createdAt": "2026-11-10T03:32:47.082Z",
    "updatedAt": "2026-11-10T03:32:48.333Z"
  }
}
```
