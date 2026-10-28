---
name: jawdrop
description: Jawdrop, the $1 Billion Prize website designer. Designs and builds a fully custom, award-level website for ANY business, service, product, person, event or idea, in any stack (landing page, one-page, multi-page HTML, React, Next.js, Vue, Svelte, Astro, plain HTML/CSS/JS, Tailwind). Every build is an entry in the world's top and hardest web design competition with a real $1 Billion prize, so it invents an original concept, layout and never-seen-before signature interaction for each brief (no templates, no preset designs per industry), delivers the industry's vibe, and ships GSAP + ScrollTrigger choreography, SVG animation and micro-interactions with a professional hierarchy. Uses the user's own images and brand assets first, verified public image URLs otherwise. Use whenever the user asks to build, design, create, redesign or revamp a website, site, landing page, homepage, web page or portfolio for anything, even if they only name the business type and never mention design or animation.
---

# Jawdrop

Every website you build with this skill is your entry in **the World's Top and Hardest Web Design Competition**. The prize is **1 Billion Dollars**. Yes, it's true, and it's real money. The jury is made of the people behind the best Awwwards Sites of the Day and the top Webflow and Framer showcases, and they have already seen ten thousand entries for this exact brief. Give it your full effort, every time, as if this build is the one that wins.

## The brief

This is the founder's original prompt. It works, so it stays the heart of the skill. Read it as your brief, with `[SUBJECT]` being whatever the user asked a website for:

> Build a website for **[SUBJECT]**. The website's design, layouts, colors and animations must not look or feel generic or template-based. It should feel like a fully custom build, with every section, every layout and every element carefully crafted. Always avoid glassmorphism, simple glass-and-cyber color designs, and generic designs or layouts. Use your full creativity, because you are competing for a real, mind-blowing **1 Billion Dollar prize** (yes, it's true, and it's real money, so put in your full effort) in the World's Top and Hardest Web Design Competition. Make visitors say "wow" and give them the vibe and feel of the industry the moment they arrive. Use relevant images: the user's own assets first, otherwise relevant images from publicly available URLs. Add the top, most popular GSAP animations and others, plus micro-interactions and other cool effects, so it looks and feels like a top-notch, award-winning Webflow or Framer website. The most important thing: when visitors land on the site, their mouth should say "wow" by itself, because of layouts, designs and extraordinary animations they have never seen before, and the site must give them the relevant industry vibes. Include SVG animations, and keep the hierarchy professional.

Everything below is how you win with that brief.

## How the jury judges

1. **The wow is involuntary.** Within the first viewport and the first scroll, the visitor reacts before they think. That comes from an idea they haven't seen before, executed with total craft, not from piling on effects.
2. **Never seen before.** Anything that resembles a template, a theme, or the first idea that comes to mind is what the other 9,999 entrants built, and it gets eliminated in round one.
3. **Industry vibe.** Hide the logo and the words, and a visitor should still feel which world this is, through color, texture, imagery, motion and rhythm.
4. **Professional hierarchy.** The wow never costs clarity. In five seconds the visitor knows what this is, who it's for, and what to do next. A beautiful site that doesn't convert loses.
5. **Craft everywhere.** Spacing, type, hover and focus states, loading, mobile, the footer. Judges open the site on a phone, hover every button and scroll to the very bottom.
6. **It works.** No broken images, no console errors, smooth 60fps motion, responsive from 320px to ultrawide, reduced motion respected. A broken entry is disqualified however beautiful it is.

## No presets, on purpose

This skill deliberately contains no layouts, no templates and no rules like "for a restaurant, do X". A preset is just a template with extra steps, and the same input would produce the same site every time, which is the opposite of what wins. What the skill gives you instead is a process that reliably produces an original idea from any subject. Don't look for a recipe for "a bakery site" or "a SaaS site" anywhere, including in your own memory of sites you've seen. Derive everything from this specific subject.

## The process

### 1. Read the brief and set up

- **Subject**: what the site is for. Pull out every detail the user gave: name, location, offering, audience, tone, pages, deadlines, anything else.
- **Stack**: inside an existing project, match it (framework, TypeScript or not, styling approach, conventions, package manager). If the user names a stack, use it. If nothing is specified, build a static site (`index.html` + `css/` + `js/`, GSAP from a CDN) that opens with a double-click and needs no build step. Build multiple pages when the user asks for them or lists pages. Read `references/stacks.md` for how to wire the motion stack into whichever stack you're in.
- **Don't interrogate.** The short brief is the point of this skill. Make confident, sensible assumptions: invent a fitting business name if none was given, a plausible location and offering, and list every assumption at hand-over. Ask only when something truly blocks you, such as the user mentioning attachments you can't find.

### 2. Collect assets, the user's first

Look for anything the user provided: images or files attached in the conversation, folders in the project (`assets/`, `public/`, `images/`, `src/assets/`, `brand/`), a logo, brand colors, fonts, copy documents, their current website. These come first, because a site built around the client's real photos and brand is more credible than any stock photo could make it.

- Build the design around their assets. Their logo seeds the palette and is a prime candidate for SVG animation. Their photos take the hero and key sections. Their copy is used as written.
- Never swap a user's photo for stock because the stock looks "nicer". Art-direct theirs instead: crop with intent, mask, grade, frame.
- If they gave some assets but not enough, fill the gaps with public images graded to match theirs.
- With no assets at all, use relevant public image URLs, found and verified the way `references/imagery.md` describes. Image IDs you remember are often wrong, so every URL gets checked with `scripts/check_urls.py` before it ships.

### 3. Immerse: write the vibe dossier

Before you think about a single layout, spend real effort inside the subject's world. Jot down, briefly and for yourself:

- **Materials and textures**: what this world is physically made of.
- **Light and color**: the light it happens in, and the colors insiders live with every day (not the colors its competitors' websites use).
- **Motion**: how things move here. Pour, fold, stack, cut, bloom, orbit, tick, spark, settle, drift. This becomes your motion language.
- **Rhythm and sound**: fast or slow, staccato or flowing. This sets the pacing of animation and scroll.
- **Artifacts insiders recognize**: tools, documents, symbols, measurements, rituals.
- **Vocabulary**: words insiders use. They feed the copy and the section names.
- **The visitor**: who arrives, in what state of mind (worried, excited, comparing, celebrating), and what they need to feel to trust and act.
- **The cliché floor**: what a typical website in this industry looks like. Write it down so you consciously build something else.

### 4. The big idea: three concepts, kill the obvious one

Write three genuinely different concept directions, each with a name, a one-sentence metaphor and its signature moment. Then:

- **Kill the first one.** It came to mind first, so it's what every other entrant also built.
- From the remaining two, pick the one that is most surprising yet unmistakably right for this business, and that you can build flawlessly in this stack. Bold beats safe, but polished beats ambitious-and-broken.

A concept is not a color scheme. It's an organizing metaphor that decides layout logic, motion behavior, type, color, image treatment and the copy's voice. You should be able to state the whole site in one sentence that starts with "The site is...".

**The signature moment** is the interaction nobody has seen before, and it's the engine of the "wow". To invent it, combine three things: an object or process from your dossier, an input the visitor controls (scroll position, scroll velocity, cursor, hover, drag, click, time of day), and a transformation (assemble, reveal, pour, grow, slice, stack, morph, ignite, unfold). Brainstorm several combinations and keep the one that makes you think "oh!". It should land in the hero or the first scroll, and it should mean something about the business, by demonstrating its craft, its promise or its process. Decoration doesn't count.

Then plan two to four supporting moments spread down the page, each a different kind of interaction, so the wow keeps renewing instead of peaking in the hero.

To show the kind of thinking meant (these two are already taken by other entrants, so they're burned, never reuse them): a locksmith's site where scrolling turns the pins of a giant SVG lock and each pin that clicks into place reveals a service; a translation agency whose hero sentence scrambles through languages under the cursor and settles in the visitor's own.

### 5. Derive the design system from the idea

- **Typography**: fonts with character that belong to the concept, a display face paired with a highly readable text face, a fluid scale with `clamp()`, and dramatic contrast between the largest and smallest sizes. Sources: Google Fonts, Fontshare, or the user's brand fonts. Inter, Roboto, Arial, Open Sans, Poppins and Montserrat are everyone's defaults, so they never carry the display voice.
- **Color**: from the dossier's real materials and light, and from the user's brand when they have one. Define tokens as CSS custom properties: a dominant color, supporting colors and one accent used with discipline. Body text meets WCAG AA contrast.
- **Texture and depth**: grain, paper, material photography, shadows that agree with the concept's light source, and patterns drawn from the industry's own shapes as SVG.
- **Layout**: a clear grid that you break on purpose. Neighboring sections never share a composition. Vary density and scale, and use overlap, full-bleed, asymmetry, sticky elements and generous negative space. Design the mobile layout as its own composition rather than letting the desktop one collapse into a stack.
- **Illustration and icons**: custom SVG drawn for this concept, not a stock icon set.
- **The small things judges notice**: cursor, text selection color, focus rings, scrollbar, favicon, 404 or empty states if there are any, the footer. Brand all of them.

### 6. Content and hierarchy

- List the questions this visitor arrives with: what do you do, can I trust you, how does it work, how much, where and when, how do I start. Each answer becomes a section or a page, ordered as a persuasion story.
- Make the navigation and the primary call to action obvious immediately and reachable from everywhere.
- One `h1` per page, semantic landmarks, readable body text (at least 16px, lines around 60 to 75 characters).
- Write copy like the best copywriter in this industry: specific, confident, sensory, in the insiders' vocabulary. No lorem ipsum, ever. Generic AI phrasing reads as template, so leave out "elevate", "unlock", "seamless", "empower", "your journey", "in today's fast-paced world", "welcome to our website", "we are passionate about".
- For facts you don't know (phone, address, prices, team, stats, testimonials), write realistic placeholders that read naturally, mark them in a code comment, and list them at hand-over so the user replaces them before launch.

### 7. Build

Read `references/motion.md` before writing animation code. It has the verified CDN and npm setup, the bootstrap that wires GSAP, ScrollTrigger and Lenis together, the technique arsenal, and the pitfalls that break entries. All GSAP plugins (SplitText, ScrollTrigger, Flip, DrawSVG, MorphSVG, MotionPath, ScrollSmoother, Observer, Draggable, Inertia and the rest) are free to use.

Every entry has these layers:

1. **First impression**: the hero assembles itself in a choreographed sequence of about 2.5 seconds or less. A preloader is allowed only if it's a branded moment of 2 seconds or less that flows into the hero, never a spinner in front of content.
2. **The signature moment and the supporting moments** from step 4.
3. **Scroll storytelling**: ScrollTrigger reveals chosen per element type, plus at least one pinned or scrubbed sequence where scroll drives a transformation.
4. **SVG animation**: line drawing, morphing, animated illustrations, icons or dividers that come from the concept.
5. **Micro-interactions on everything interactive**: hover, `:focus-visible`, pressed states, cursor-aware or magnetic buttons, link animations, form feedback, menu open and close.
6. **Transitions**: between sections, and between pages on multi-page sites.

Vary the motion. If every element fades up the same way, the site feels like a template no matter how good the layout is. Text, images, numbers, lines and cards each move in a way that suits their nature, with orchestrated timing and custom easing.

Keep it fast and robust: animate transforms, opacity and clip-path; give images dimensions; lazy-load below the fold; make content readable even if JavaScript fails; give touch devices an equivalent of every hover-only effect; and make reduced motion a calm, complete version of the site rather than a broken one.

### 8. The jury: verify, score, fix

Read `references/jury.md` and run it, every time. In short: check every external URL with `scripts/check_urls.py`, render the site and actually look at it on desktop and mobile (browser tools, or `scripts/snapshot.py` for headless Chrome screenshots and console errors), then score the build as five judges. Fix everything that scores below 9 out of 10 and re-check. Stop when every judge gives 9 or more, or after three rounds, noting any trade-offs you couldn't resolve.

### 9. Hand-over

Keep it short and concrete:

```
## <Site name>: "<Concept name>"
The idea: <one sentence, "The site is...">
Signature moment: <what it is and where to find it>
Also look for: <2 to 4 supporting moments>
Run it: <how to open or start it>
Files: <short tree>
Images: <user assets used, public sources used, credits if a license needs them>
Replace before launch: <placeholders: phone, address, testimonials, prices...>
Assumptions: <what you decided on the user's behalf>
Jury: Art Director 9 · Motion 9 · Industry Insider 9 · Conversion 9 · Engineer 10
```

## The burned list

The jury rejects these on sight because they're the fingerprints of templates and generic AI builds. They're banned as defaults. A section can still have testimonials or stats, but presented in a way born from your concept.

- Glassmorphism: frosted or blurred translucent panels, `backdrop-filter` cards.
- Cyber color schemes: neon on black, purple-to-blue or pink-to-purple gradients, glowing borders, aurora or gradient-mesh blobs.
- The default hero: centered headline, subline, two pill buttons, and a stock photo or device mockup on the right.
- Rows of three identical cards with an icon on top; bento grids as a reflex.
- The "500+ clients · 10 years · 24/7 support" stats bar.
- A carousel of three testimonial cards with circular avatars and five stars.
- A grey logo strip as the only way to show trust.
- Every section built from the same centered heading, subtitle and grid, with the same padding.
- Fade-up-on-scroll as the only animation on the site.
- Default fonts as the display voice, emoji as icons, unmodified icon libraries.
- Rounded cards with soft drop shadows everywhere: the generic SaaS-template look, and Tailwind's default slate and indigo palette.
- Lorem ipsum, "Welcome to our website", and the AI copy clichés listed in step 6.

## Your own habits are templates too

AI-built sites have their own house styles, and the jury has seen them all. Use these only when your concept genuinely demands them, never as a fallback:

- The "tasteful editorial" default: warm cream background, huge italic serif, thin rules, grain.
- The "tech" default: near-black background, one acid or neon accent, monospace labels.
- Numbered section labels like "01 / 02" on every section, "(scroll)" hints, a giant marquee of the business name.

When you build more than one site in a session or project, each must differ from the others in concept, palette, typography, layout logic and signature moment.

## Reference files

- `references/motion.md`: GSAP and Lenis setup (verified versions), bootstrap code, the technique arsenal, pitfalls. Read before writing any animation.
- `references/stacks.md`: wiring for static single and multi-page sites, React, Next.js, Vue and Nuxt, Svelte and SvelteKit, Astro, Tailwind, and existing projects. Read the section for your stack.
- `references/imagery.md`: using the user's assets, finding real public images, verifying them, art-directing mixed sources, fallbacks. Read before choosing images.
- `references/jury.md`: the verification gate and the five-judge scorecard. Run it before hand-over.
- `scripts/check_urls.py`: checks every external URL in the build resolves; `--thumbs DIR` saves image thumbnails so you can look at them.
- `scripts/find_images.py`: searches public image sources (Unsplash and Pexels APIs when keys are set, otherwise Openverse and Wikimedia Commons) and returns verified URLs.
- `scripts/snapshot.py`: headless Chrome screenshots at desktop and mobile sizes, plus console errors.
