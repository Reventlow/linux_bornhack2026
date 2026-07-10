# Linux for the Curious — BornHack 2026

Workshop deck for the BornHack 2026 workshop **"Linux for the Curious"** —
a 2-hour, hands-on intro to Linux for complete newcomers.
Host: Gorm Reventlow.

Sibling deck to [Docker for the Curious](https://github.com/Reventlow/docker_bornhack2026);
same visual system (matcha palette), same repo layout, same publishing pipeline.

## Run the deck

```sh
docker run -d -p 8080:80 elohite/bornhack-linux-deck
# open http://localhost:8080 — arrow keys / space to navigate, "f" toggles fullscreen
```

The deck is fully self-contained (fonts inlined) and works offline.
Browser print gives one page per slide.

## Repository layout

```
deck/index.html        ← the deck, compiled single-file bundle. Do not hand-edit.
Dockerfile             ← deck image (nginx:alpine serving deck/index.html)
source/                ← editable design source (.dc.html + runtime scripts)
scripts/build-deck.py  ← bundler: source → deck/index.html (inlines JS + fonts)
.github/workflows/     ← CI: build + push the image to Docker Hub
```

Edits to the deck happen in `source/Linux for the Curious.dc.html`; rebuild
the served bundle with:

```sh
python3 scripts/build-deck.py
```

The build extracts the 28 slide sections, inlines `deck-stage.js`, embeds the
Google Fonts (JetBrains Mono, IBM Plex Sans) as base64 `@font-face` rules, and
adds the tab title, Tux favicon, and the "f" fullscreen toggle.

## CI / publishing

Every push to `main` builds and pushes `elohite/bornhack-linux-deck:latest`
(linux/amd64 + linux/arm64) to Docker Hub. A version tag (`git tag v1.0 &&
git push --tags`) additionally publishes `:1.0`.

Required repository secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.

## Deployment

The deck runs on the ZimaOS box as app `bornhack-linux-deck`, pulling
`elohite/bornhack-linux-deck:latest` from Docker Hub. After CI publishes a
new image, refresh the app to the new image (e.g. via the ZimaOS UI or the
zimaos MCP `update_app_image` tool).
