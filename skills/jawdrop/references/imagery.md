# Imagery

Images carry most of a site's industry vibe, so they deserve as much care as the layout. The order of preference never changes: the user's own assets first, then relevant public images, all verified before they ship.

For a business with a physical product, place or service, well art-directed real photos are usually the fastest route to a premium, believable site, and a quick vector redraw of the same thing rarely holds up next to them. Finding and verifying photos takes effort. That's expected, and it isn't a reason to draw the subject instead.

## Contents

1. The user's assets
2. Public image sources
3. Finding real images
4. Verify and look
5. Art direction: making mixed sources feel like one shoot
6. Photos in motion: making the photo the signature moment
7. Implementation details
8. Never use

---

## 1. The user's assets

Look everywhere the user might have put them: attachments in the conversation, files they name, project folders (`assets/`, `public/`, `images/`, `img/`, `media/`, `src/assets/`, `brand/`, `static/`), and a current website if they mention one.

- **Logo**: use the real file. If it's an SVG, animate its paths (draw, assemble, morph) as part of the first impression. If it's a raster image, reveal it with masks or motion rather than redrawing it. Sample its colors for the palette.
- **Photos**: the hero and key sections belong to them. Choose crops with `object-fit: cover` and `object-position` aimed at the subject. If their photos are weak (low light, phone shots, inconsistent), art-direct them (section 5) rather than replacing them. A real client photo builds more trust than polished stock.
- **Brand guide, colors, fonts**: treat as constraints the concept works with. A brand palette can still be used in an unexpected way: proportion, texture, unusual pairings with neutrals.
- **Copy**: use their words. Edit only for typos, and tell them if you did.
- Copy assets into the project's asset folder with clean, descriptive filenames. Leave the originals untouched.
- If a file they mention can't be found, ask rather than silently substituting stock.
- If they provided some assets but not enough, fill the gaps with public images chosen and graded to match theirs.

## 2. Public image sources

Prefer these, because their licenses allow free commercial use and their CDNs are built for hotlinking:

| Source | URL pattern | License notes |
|---|---|---|
| Unsplash | `https://images.unsplash.com/photo-<ID>?auto=format&fit=crop&w=1600&q=80` | Free for commercial use, attribution appreciated, not required |
| Pexels | `https://images.pexels.com/photos/<ID>/pexels-photo-<ID>.jpeg?auto=compress&cs=tinysrgb&w=1600` | Free for commercial use, attribution not required |
| Wikimedia Commons | `https://upload.wikimedia.org/...` (from the file page or API) | Varies per file. CC BY and BY-SA need credit. Best for real places, landmarks, history, science |
| Openverse | Whatever URL the API returns (often Flickr or Commons) | Varies per file. Prefer CC0, PDM and CC BY. Skip NC and ND licenses for business sites |

Both Unsplash and Pexels accept a width parameter (`w=`), so request the size you need: about 800 for cards, 1600 to 2400 for full-bleed.

## 3. Finding real images

Image IDs recalled from memory are frequently wrong or point at unrelated photos. Use them only as candidates and verify all of them (section 4). Ways to find good ones, from most to least reliable:

**A. The bundled search script**

```bash
python3 scripts/find_images.py "roofer installing slate tiles" --count 8 --orientation landscape
```

It uses the official Unsplash and Pexels APIs when `UNSPLASH_ACCESS_KEY` or `PEXELS_API_KEY` is set in the environment, and keyless Openverse and Wikimedia Commons otherwise. Every result is verified to load. It prints JSON with URL, size, description, license and credit. Sources that are unreachable or rate-limited are skipped with a note, so run several specific queries (the subject, its materials, its people at work, its results) rather than one broad one.

**B. Web search for Pexels photo pages**

Pexels photo pages, and the many mirror sites that republish them, have URLs shaped like `/photo/<description-words>-<ID>/`. Search for something like `pexels photo <specific subject>`. The description words tell you what the photo shows, and the trailing number is the ID, which you drop into the Pexels pattern above. This works without any API key.

**C. A browser, if you have one**

Search Unsplash or Pexels directly, open a photo, and copy its image address.

**D. Memory**

Unsplash or Pexels IDs you remember go into the candidate list, and they pass only if verification and a look at the thumbnail both confirm them.

Search specifically. "Bakery" returns the same croissant photo every other entrant used. "Flour dust in morning light on a wooden bench", "baker's hands shaping a boule", "scored sourdough crust close-up" return images with vibe.

**When photos are hard to find**, keep looking before you give up on a section. Search 5 to 10 times with different, specific queries (materials, hands at work, details, the place, the result), use method B and a browser if you have one, and try Wikimedia Commons for real places and equipment. If a section still has no fitting photo, carry it with type, color, layout and graphics, or reuse a strong photo you already have with a different crop.

## 4. Verify and look

```bash
python3 scripts/check_urls.py site/ --thumbs /path/to/scratch/thumbs
```

This finds every external URL in the build (images, scripts, stylesheets, fonts), confirms each one loads, reports broken ones with the file and line where they appear, and saves small thumbnails of every image. Then open the thumbnails and look at them. A URL that loads can still show the wrong thing.

The relevance bar:

- **Specific to the subject**: a roofing site shows roofs, roofers, materials and weather on rooftops, not a handshake in an office.
- **A range of shots**: establishing or wide, detail and texture macros, people at work, outcomes and happy customers, place and atmosphere.
- **One light and one mood**: color temperature and contrast close enough that, once graded, they could be one shoot.
- **No visible watermarks or other brands' logos.**

Replace anything broken, irrelevant or off-mood, and re-run the check until it passes.

## 5. Art direction: making mixed sources feel like one shoot

- **Unified grade**: apply the same treatment to every image, such as a CSS filter (`contrast()`, `saturate()`, `sepia()`), a duotone made with a brand-colored overlay and `mix-blend-mode`, or a shared grain layer.
- **Crops with intent**: extreme crops for texture details, tall crops for people, wide crops for place. Shape masks with the concept, through SVG `clipPath` or `clip-path` polygons, where it fits.
- **Image as material**: images can be textures inside type (`background-clip: text`), layers revealed by the cursor, or frames in a scroll-driven sequence. They don't always have to be rectangles in a grid.
- **Consistency over quantity**: six excellent, consistently graded images beat twenty mismatched ones.

## 6. Photos in motion: making the photo the signature moment

When the concept needs a real object to move, react or transform, these techniques make the photo itself the interaction:

- **Mask reveals**: `clip-path` (inset, circle, polygon) or an SVG `clipPath` shaped by the concept opens, wipes or traces across the photo with scroll or cursor.
- **Strips and tiles**: split one photo into slices (repeated elements with shifted `background-position`) that drift, stagger, ripple or reassemble with scroll velocity.
- **Layered cutouts**: two or three versions of the same photo (background, subject and foreground cropped or masked) moving at different depths with scroll or pointer, for real parallax depth.
- **Scrubbed frame sequences**: a handful of real photos of a process (pour, pull, fold, build, before and after) swapped or crossfaded by scroll, or a short real video scrubbed with `currentTime`.
- **Cursor-driven layers**: a spotlight or lens that reveals a second photo (raw and finished, day and night, before and after) under the cursor.
- **Distortion**: an SVG `feDisplacementMap`, or a WebGL plane when the concept truly needs it, applied to the photo for liquid, heat, glass or ripple effects.
- **Grow and settle**: a photo scales from a small slot to full-bleed (or back) with Flip or a pinned timeline, carrying the story into the next section.
- **Graphics on top**: thin SVG lines that trace the photo's edges, dimension lines, gauges, labels and counters that read what's in it, routes that cross it.

## 7. Implementation details

- `width` and `height` attributes (or CSS `aspect-ratio`) on every image, to prevent layout shift.
- `loading="lazy"` and `decoding="async"` below the fold, `fetchpriority="high"` on the hero image.
- `srcset` using the CDN width parameter for large images, for example `...&w=800 800w, ...&w=1600 1600w, ...&w=2400 2400w`.
- Alt text that describes what matters about the image in this context. Purely decorative images get `alt=""`.
- **Graceful failure**: give every image container a designed background (brand color, pattern or gradient) so a failed load still looks intentional. Optionally swap in a fallback with `onerror`.
- **Credits**: list sources at hand-over, and add a credit line in the footer or a credits section for any image whose license requires attribution.
- In Next.js, Nuxt or Astro, allow the remote image hosts in the framework config (see `stacks.md`), or the build fails or the images never render.

## 8. Never use

- `source.unsplash.com`: shut down, returns errors.
- `via.placeholder.com`, `placeholder.com`, `placehold.it`: dead or unreliable, and they look like placeholders.
- `picsum.photos`: random photos with nothing to do with the subject.
- Google Images thumbnails (`encrypted-tbn*.gstatic.com`): unlicensed and they expire.
- Shutterstock, Getty, Adobe Stock or iStock previews: watermarked and licensed.
- Instagram, Facebook or Pinterest CDN links: they expire and aren't licensed for reuse.
- Images taken from competitors' or other businesses' websites.
