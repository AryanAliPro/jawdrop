# The Jury

The real jury will open your entry on a phone, hover every button, scroll to the very bottom and check the console. So you do it first. Round 0 is a gate: a site that fails it is disqualified however beautiful it is. Rounds 1 and after are where it becomes a winner.

## Round 0: Technical gate

1. **Every external URL resolves.**

   ```bash
   python3 scripts/check_urls.py <project-dir>
   ```

   Zero broken images, scripts, stylesheets or fonts. Fix and re-run until clean.

2. **Render it and look at it.** Reading your own code is not looking.

   - **With browser tools** (built-in browser, Chrome, Playwright or similar): serve the site (a static site with `python3 -m http.server`, a framework with its dev server), then view it at about 1440px wide and at about 390px wide. Look at the first viewport, scroll through the whole page slowly, hover the key elements and read the console.
   - **Without browser tools**: run

     ```bash
     python3 scripts/snapshot.py <path/to/index.html or http://localhost:PORT> --out <scratch-dir>
     ```

     It saves desktop and mobile screenshots with headless Chrome and prints console errors. Open the PNGs and look at them. Use `--sizes 1440x2400` and similar for taller captures.

   Look for: overlapping or clipped text, content stuck invisible, horizontal scroll on mobile, broken or irrelevant images, fonts falling back to a default, unreadable contrast, empty-looking sections, anything that looks unfinished.

3. **Framework projects build.** `npm run build` (or the project's equivalent) passes, and lint passes if it's configured.

4. **Code-level checks**:
   - A reduced-motion path exists and leaves every piece of content visible.
   - No `markers: true` and no leftover debug logging.
   - Every hover-only piece of information has a touch equivalent. Custom cursors are hidden on touch devices.
   - Visible `:focus-visible` styles, keyboard-reachable navigation and menu.
   - One `h1` per page, semantic landmarks (`header`, `nav`, `main`, `footer`), alt text on images.
   - `<title>`, meta description, Open Graph tags and a favicon on every page.
   - Placeholders (phone, address, testimonials) are marked in code comments.

## Round 1 and after: The Panel

Five judges score the entry from 1 to 10. Judge it against the best website you have ever seen, not against other AI-made sites, and be harsh: an inflated score loses the prize. Every score below 9 comes with one concrete, specific fix ("the services section uses the same centered heading + grid as the process section; turn it into a pinned sequence where each service is a step of the roof going up"), never a vague one ("make it more creative").

### 1. The Art Director (Awwwards, Webflow and Framer showcase juror)
Originality and visual craft.
- Is the concept genuinely unseen, or a familiar layout in new colors?
- Does every section have its own intentional composition? Do neighbors differ?
- Is the typography confident, characterful and well set (scale contrast, line length, spacing, rag)?
- Did anything from the burned list or the AI house styles sneak in?
- Would this win Site of the Day?

### 2. The Motion Director
Choreography and interaction.
- Is the signature moment truly new, and does it mean something about the business?
- Is the motion vocabulary varied, with each element type moving in a way that suits it?
- Do easing and timing feel physical and on-brand? Is anything janky, sluggish or gratuitous?
- Do SVG animations exist and serve the concept?
- Do the micro-interactions reward every hover, focus and click?

### 3. The Industry Insider (20 years in this business)
Vibe and credibility.
- Would an insider say "they get us"? Is the vocabulary right?
- Are the images specific and believable for this business, consistently graded?
- Would a customer trust this business with their money, their home, their health or their event?

### 4. The Conversion Lead
Hierarchy and clarity.
- In five seconds, does a visitor know what this is, who it's for and what to do?
- Is the primary action visible in the first viewport and reachable everywhere?
- Is the page easy to scan, with readable text and a sensible order of information?
- Do forms and contact paths work, with clear feedback?
- Does the wow ever get in the way of the visitor's goal?

### 5. The Engineer
Performance and robustness.
- Motion runs at 60fps (transforms, opacity, clip-path), and there's no layout shift.
- Images are sized, lazy-loaded where appropriate, and every URL resolves.
- It is responsive from 320px to ultrawide, with a designed mobile layout.
- Reduced motion, touch input, keyboard use and JavaScript failure all leave a working site.
- The console is clean, and animations are cleaned up in single-page apps.
- It runs the way it's meant to: a double-click for static sites, a clean build for frameworks.

## The fix loop

1. Fix every issue a judge raised, starting with the lowest score.
2. Re-run the Round 0 checks for whatever changed.
3. Re-score honestly.
4. Stop when every judge gives 9 or more, or after three rounds. If something stays below 9, say what and why at hand-over. Don't report scores the entry didn't earn.

Put the final scores on one line at hand-over:

```
Jury: Art Director 9 · Motion 9 · Industry Insider 9 · Conversion 9 · Engineer 10
```
