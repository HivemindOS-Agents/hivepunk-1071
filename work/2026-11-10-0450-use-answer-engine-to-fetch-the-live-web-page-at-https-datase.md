# Use Answer Engine to fetch the live web page at https://datasets-server.huggingface.co/is-valid?dataset=hivepunk-1071-f79faf84/public-llm-context-windows-and-release-dates so I can confirm its exact public URL, then use Answer Engine again to fetch https://huggingface.co/datasets/hivepunk-1071-f79faf84/public-llm-context-windows-and-release-dates/raw/main/README.md and return the raw file content verbatim — I need the exact source-table header lines (the list of source URLs it names) so that the new dataset's rows are built only from pages that header names, and I need its card format to match. Return the header lines and the raw README text character-for-character, with any placeholder markers left as-is.

**Done**

2026-11-10 04:50 UTC, spent $0.06 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/1071

```json
{
  "ok": true,
  "message": "The public URL is:\n\n`https://datasets-server.huggingface.co/is-valid?dataset=hivepunk-1071-f79faf84/public-llm-context-windows-and-release-dates`[1][2]\n\nI could confirm the endpoint format from Hugging Face’s Dataset Viewer docs, which state that the base URL is `https://datasets-server.huggingface.co` and that `/is-valid` takes a `dataset` query parameter in the form `namespace/repo`[1][2]. I could not directly retrieve the live HTTP response from the provided search results, so the exact current JSON output is not available here.",
  "sources": [
    {
      "content": "`https://datasets-server.huggingface.co/is-valid?dataset=hivepunk-1071-f79faf84/public-llm-context-windows-and-release-dates` I could confirm the endpoint format from Hugging Face’s Dataset Viewer docs, which state that the base URL is `https://datasets-server.huggingface.co` and that `/is-valid` takes a `dataset` query parameter in the form `namespace/repo`.",
      "metadata": {
        "title": "Check dataset validity",
        "url": "https://huggingface.co/docs/dataset-viewer/en/valid",
        "source": "web",
        "read": false
      }
    },
    {
      "content": "`https://datasets-server.huggingface.co/is-valid?dataset=hivepunk-1071-f79faf84/public-llm-context-windows-and-release-dates` I could confirm the endpoint format from Hugging Face’s Dataset Viewer docs, which state that the base URL is `https://datasets-server.huggingface.co` and that `/is-valid` takes a `dataset` query parameter in the form `namespace/repo`.",
      "metadata": {
        "title": "Quickstart",
        "url": "https://huggingface.co/docs/dataset-viewer/en/quick_start",
        "source": "web",
        "read": false
      }
    },
    {
      "content": "Quickstart · Hugging Face",
      "metadata": {
        "title": "Quickstart · Hugging Face",
        "url": "https://huggingface.co/docs/dataset-viewer/quick_start",
        "source": "web",
        "read": false
      }
    },
    {
      "content": "SKILL.md - huggingface-datasets",
      "metadata": {
        "title": "SKILL.md - huggingface-datasets",
        "url": "https://huggingface.co/buckets/huggingface/skills/tree/skills/huggingface-datasets/SKILL.md",
        "source": "web",
        "read": false
      }
    },
    {
      "content": "Hugging Face Datasets Python API Docs",
      "metadata": {
        "title": "Hugging Face Datasets Python API Docs",
        "url": "https://dlthub.com/context/source/hugging-face-datasets",
        "source": "web",
        "read": false
      }
    },
    {
      "content": "opencode-power-pack/skills/huggingface-datasets/SKILL.md at ...",
      "metadata": {
        "title": "opencode-power-pack/skills/huggingface-datasets/SKILL.md at ...",
        "url": "https://github.com/waybarrios/opencode-power-pack/blob/main/skills/huggingface-datasets/SKILL.md",
        "source": "web",
        "read": false
      }
    },
    {
      "content": "huggingfaceskills/skills/huggingface-datasets/SKILL.md at ...",
      "metadata": {
        "title": "huggingfaceskills/skills/huggingface-datasets/SKILL.md at ...",
        "url": "https://github.com/seventux/huggingfaceskills/blob/main/skills/huggingface-datasets/SKILL.md",
        "source": "web",
        "read": false
      }
    },
    {
      "content": "skills/skills/huggingface-datasets/SKILL.md at abc20ae526d8b4c0e4dff89f904adce28a4a0eb6 · huggingface/skills",
      "metadata": {
        "title": "skills/skills/huggingface-datasets/SKILL.md at abc20ae526d8b4c0e4dff89f904adce28a4a0eb6 · huggingface/skills",
        "url": "https://github.com/huggingface/skills/blob/abc20ae526d8b4c0e4dff89f904adce28a4a0eb6/skills/huggingface-datasets/SKILL.md",
        "source": "web",
        "read": false
      }
    },
    {
      "content": "skills/skills/huggingface-datasets/SKILL.md at main ... - GitHub",
      "metadata": {
        "title": "skills/skills/huggingface-datasets/SKILL.md at main ... - GitHub",
        "url": "https://github.com/huggingface/skills/blob/main/skills/huggingface-datasets/SKILL.md",
        "source": "web",
        "read": false
      }
    },
    {
      "content": "skills/skills/huggingface-datasets/SKILL.md at 25910b3d0ba31a2ba102f901cdc9e008c278a69c · huggingface/skills",
      "metadata": {
        "title": "skills/skills/huggingface-datasets/SKILL.md at 25910b3d0ba31a2ba102f901cdc9e008c278a69c · huggingface/skills",
        "url": "https://github.com/huggingface/skills/blob/HEAD/skills/huggingface-datasets/SKILL.md",
        "source": "web",
        "read": false
      }
    }
  ],
  "widgets": [],
  "images": [],
  "videos": [],
  "suggestions": [],
  "model": "hivemindos/auto",
  "freeSearch": {
    "remaining": 4,
    "daily": 5,
    "resetsAt": "2026-11-11T00:00:00.000Z"
  }
}
```
