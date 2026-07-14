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

## Offline fallback (if the hosted site is down)

Download the slides ahead of time while you have internet — the image
contains everything, so once pulled you need no network at all:

```sh
docker pull elohite/bornhack-linux-deck
```

Then serve them locally whenever you need them:

```sh
docker run -d -p 8080:80 --name linux-deck elohite/bornhack-linux-deck
# open http://localhost:8080
```

No Docker on the presentation machine? Extract the single HTML file from
the image and open it straight in a browser — no web server required:

```sh
docker create --name deck-tmp elohite/bornhack-linux-deck
docker cp deck-tmp:/usr/share/nginx/html/index.html linux-deck.html
docker rm deck-tmp
# open linux-deck.html in any browser (double-click or drag into a window)
```

`linux-deck.html` is one ~720 KiB file with fonts and scripts embedded;
copy it to a USB stick as a belt-and-braces backup for the workshop.

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
`elohite/bornhack-linux-deck:latest` from Docker Hub. A label-scoped
Watchtower on the box (`--label-enable`, 10-minute interval) auto-pulls the
new image after CI publishes — the deck service carries the
`com.centurylinklabs.watchtower.enable` label, so pushes to `main` reach
the box within ~10 minutes with no manual step.
