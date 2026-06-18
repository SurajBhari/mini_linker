# Mini Linker

![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=flat&logo=youtube&logoColor=white)

A small Flask service that creates **permanent short links that always redirect to a YouTube channel's *latest* content** — newest video, newest Short, or current/most-recent livestream. Share one link once; it never goes stale.

On mobile it opens the YouTube app directly via deep links (`vnd.youtube://` on Android, `youtube://` on iOS); on desktop it falls back to a normal `youtube.com` URL.

## Link format

```text
/<channel_id>/<type>
```

| Type | Meaning |
|------|---------|
| `l` (or `live`, `stream`) | Latest / live stream |
| `v` (or `video`) | Latest video |
| `s` (or `short`) | Latest Short |

**Example** (channel `UC5XTxQsO3KapW09nOVE1TJQ`):

- Live → `/UC5XTxQsO3KapW09nOVE1TJQ/l`
- Video → `/UC5XTxQsO3KapW09nOVE1TJQ/v`
- Short → `/UC5XTxQsO3KapW09nOVE1TJQ/s`

![Mini Linker](https://github.com/SurajBhari/mini_linker/assets/45149585/30a725b6-d975-42dd-ba41-7c3ebc63ad15)

## How it works

The latest content for a channel is fetched with [`scrapetube`](https://github.com/dermasmid/scrapetube) and `youtube-search-python`, then the request is redirected to the right URL based on the requesting device. Resolved IDs are cached so repeat hits are fast.

## Run locally

```bash
pip install -r requirements.txt
python main.py
```
