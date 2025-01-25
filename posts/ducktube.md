---
Title: ducktube
Date: 2025-01-25
---

Over the holiday I participated in a hackathon.

This was something fun to hack on and got me thinking outside the box of what is typically implemented using a database. My idea was to play videos using duckdb and additionally host them using motherduck. And to make this something usable for the layperson, the “video player” is implemented courtesy of duckdb’s WASM module. 

Everything lives in the browser!

The way this was done was by storing a video’s pixels - literally each one - encoded as an X, Y coordinate. Each coordinate pair would then reference which frame it belonged to. To play the video, the coordinates are called with sql where each row in the table is iterated over. More or less a flip book. 

Motherduck is perfect to use as a host. The subject matter is pretty unconventional given the sql nature of things, but this fit MDs idea of abstracting local and cloud compute fit the bill. Especially the WebAssembly aspects.

Here's the repo: https://github.com/patricktrainer/ducktube
