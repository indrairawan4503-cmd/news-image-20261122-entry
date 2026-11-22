// "The World in One Day — 22 November 2026": a photo-montage front page
// for the news-image-20261122 bounty. The finished montage is entry.png,
// built beforehand and shipped beside this file. This entrypoint does one
// thing: hand that exact image to the judge by placing it in the output
// directory as entry.png. Node 22, standard library only, ESM.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const sourceDir = dirname(fileURLToPath(import.meta.url));
const destinationDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const imageName = "entry.png";

mkdirSync(destinationDir, { recursive: true });
copyFileSync(
  join(sourceDir, imageName),
  join(destinationDir, imageName),
);
console.log(`Wrote ${join(destinationDir, imageName)}`);
