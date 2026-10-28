# Motion

How to set up GSAP and smooth scrolling correctly, an arsenal of techniques to compose from, and the pitfalls that break entries.

## Contents

1. Setup (CDN and npm, verified versions)
2. Bootstrap: GSAP + ScrollTrigger + Lenis + reduced motion
3. Choreography principles
4. The technique arsenal
5. Code sketches for the techniques that are easy to get wrong
6. Pitfalls checklist

---

## 1. Setup

Every GSAP plugin is free, including the ones that used to be paid (SplitText, MorphSVG, DrawSVG, ScrollSmoother, Inertia, ScrambleText). Use whichever the concept needs.

### Static sites (CDN)

Versions below were verified to resolve. Pin exact versions; if you use a newer one, check it resolves with `scripts/check_urls.py`.

```html
<!-- in <head>: lets CSS hide pre-animation states only when JS runs -->
<script>document.documentElement.classList.add('js');</script>

<!-- before </body>; include only the plugins you use -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/SplitText.min.js"></script>
<!-- Optional: Flip, DrawSVGPlugin, MorphSVGPlugin, MotionPathPlugin, Observer, CustomEase,
     ScrambleTextPlugin, TextPlugin, Draggable, InertiaPlugin, ScrollSmoother
     all at https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/<Name>.min.js -->
<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.27/dist/lenis.min.js"></script>
<script>if (!window.gsap) document.documentElement.classList.remove('js');</script>
<script src="js/main.js"></script>
```

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lenis@1.3.27/dist/lenis.css">
```

Keep local JS as classic scripts (not `type="module"` with a local `src`), because browsers block local module files opened from `file://`, and a static entry must open with a double-click.

### npm projects

```bash
npm i gsap lenis            # add @gsap/react for React and Next.js
```

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';
// other plugins: 'gsap/Flip', 'gsap/DrawSVGPlugin', 'gsap/MorphSVGPlugin', 'gsap/MotionPathPlugin', ...
gsap.registerPlugin(ScrollTrigger, SplitText);

import Lenis from 'lenis';
import 'lenis/dist/lenis.css';
```

Framework-specific wiring (React `useGSAP`, Next.js client components, Vue, Svelte, Astro) is in `stacks.md`.

### WebGL, only when the concept truly needs it

```html
<script type="importmap">
{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.min.js" } }
</script>
<script type="module">
  import * as THREE from 'three';
  // keep it lazy: start the scene only when its section approaches the viewport
</script>
```

WebGL earns its place when it expresses the concept (liquid, light, material, depth) and not as decoration. Always design a static fallback for when it fails or reduced motion is on.

---

## 2. Bootstrap

A solid base for vanilla JS. Adapt the same structure inside framework lifecycles.

```js
gsap.registerPlugin(ScrollTrigger, SplitText /* , Flip, DrawSVGPlugin, ... */);

const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Smooth scroll that ScrollTrigger stays in sync with
let lenis = null;
if (!prefersReduced) {
  lenis = new Lenis({ lerp: 0.1 }); // tune per concept: heavier worlds glide longer (lower lerp)
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
}

// Anchor links scroll through Lenis
document.querySelectorAll('a[href^="#"]').forEach((a) => {
  a.addEventListener('click', (e) => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    lenis ? lenis.scrollTo(target, { offset: -80 }) : target.scrollIntoView();
  });
});

// Responsive and reduced-motion variants; everything created inside reverts automatically
const mm = gsap.matchMedia();
mm.add(
  {
    desktop: '(min-width: 900px) and (prefers-reduced-motion: no-preference)',
    mobile: '(max-width: 899px) and (prefers-reduced-motion: no-preference)',
    reduced: '(prefers-reduced-motion: reduce)',
  },
  (ctx) => {
    const { desktop, mobile, reduced } = ctx.conditions;
    if (reduced) {
      gsap.set('[data-reveal]', { autoAlpha: 1 }); // show everything, calmly
      return;
    }
    // hero choreography, scroll scenes, signature moment...
  }
);

// Layout changes after images and fonts load, so re-measure
window.addEventListener('load', () => ScrollTrigger.refresh());
document.fonts && document.fonts.ready.then(() => ScrollTrigger.refresh());
```

Elements hidden this way must be revealed with `gsap.to(el, { autoAlpha: 1 })` or `fromTo`, because `gsap.from` animates *to* the current state, which is hidden. When a hidden wrapper holds split text, show the wrapper first (`gsap.set(wrapper, { autoAlpha: 1 })`) and then animate the lines.

```css
/* Hide only what JS will reveal, and only when JS is running */
.js [data-reveal] { visibility: hidden; }   /* revealed with autoAlpha */

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

---

## 3. Choreography principles

- **Motion language comes from the dossier.** Heavy materials move with weight and settle; liquids overshoot and wobble; precise instruments snap; organic things grow with gentle irregularity. Pick eases to match: `expo.out` and `power4.out` for confident reveals, `back.out` or `elastic.out` sparingly for playful worlds, `CustomEase` for the signature moment so it has its own personality.
- **Timing**: big reveals around 0.8 to 1.4s, micro-interactions around 0.2 to 0.35s, staggers around 0.04 to 0.12s. Overlap tweens on a timeline (`'-=0.6'` or `'<0.2'`) so sequences flow instead of queueing.
- **Hierarchy in motion**: the most important element moves first or most. Secondary elements follow. Body text arrives quickly and quietly, because people want to read it.
- **Contrast**: a still moment makes the next motion land. Not everything moves all the time.
- **Variety**: each element type gets a motion that suits its nature. Headlines rise through line masks, images wipe or unmask, numbers count, lines draw, cards stack or flip, icons morph. One reveal used everywhere is the most common template tell.

---

## 4. The technique arsenal

These are ingredients, not a checklist. Choose what serves the concept, combine and transform them, and invent new ones. The signature moment should usually be something you build from these parts rather than one of them used as-is.

**On load**
- Line-masked headline rise with SplitText (`mask: 'lines'`), per-character variants for short display words
- Text scramble into the final words (ScrambleTextPlugin)
- Image unmasking with `clip-path` (inset, polygon, circle) or SVG `clipPath` shaped by the concept
- Logo or illustration drawn stroke by stroke with DrawSVG, then filled
- A preloader that transforms into the hero with Flip instead of disappearing
- Counters rolling to their value
- Layered depth entrance: background, midground and foreground arriving at different speeds

**Scroll-driven (scrub and pin)**
- A pinned sequence where a timeline scrubs through a transformation (an object assembling, a process step by step, a before-and-after)
- A horizontal track inside a pinned section, with nested triggers via `containerAnimation`
- Full-bleed media that scales down into its slot in a grid, or grows from a slot into full-bleed
- Cards that stack, pile, peel or fan as you scroll
- Text that fills with color word by word as the visitor reads
- An SVG path that draws itself along the scroll, or an object traveling a route with MotionPath
- Shape morphing driven by scroll (MorphSVG)
- Sticky split-screen where one side stays and the other swaps content
- Zoom-through: a mask or opening grows until it becomes the next section
- Theme shifts: background and text colors tween as sections enter
- Parallax layers at different speeds, kept subtle on text
- Image sequence on canvas, for product rotations or processes, when you have frames

**Scroll velocity and direction**
- Skew or stretch that responds to scroll speed and eases back to rest
- Marquees that speed up with scroll and reverse with scroll direction

**Cursor**
- A custom cursor that changes state over different content (text, image, link, drag), desktop only
- Magnetic buttons and links
- An image trail or hover previews that follow the cursor through a list
- A spotlight or mask that reveals a hidden layer around the cursor
- Pointer-driven tilt and parallax of layered elements
- Letters that react to proximity (weight, offset, rotation), especially with variable fonts

**Click and drag**
- Draggable carousels with inertia
- Flip transitions between states: filtering a grid, expanding a card into a detail view
- Before-and-after sliders, configurators, interactive SVG diagrams
- Full-screen menus treated as a choreographed moment, not a dropdown

**Ambient life**
- Animated grain or paper texture (SVG `feTurbulence`)
- Slow drift of concept shapes, breathing SVG elements
- Time-aware details: the light or palette shifts with the visitor's local time when that fits the concept

**Between pages (multi-page)**
- Cross-document View Transitions (`@view-transition { navigation: auto; }`) with named elements that morph between pages
- A GSAP overlay transition built from the concept's shapes

---

## 5. Code sketches

Short, correct starting points for techniques that are commonly broken. Restyle and re-time them for your concept.

### SplitText headline (3.13+ API)

```js
SplitText.create('.hero-title', {
  type: 'lines, words',
  mask: 'lines',
  autoSplit: true,                       // re-splits on resize and font load
  onSplit(self) {                        // return the animation so it can be rebuilt on re-split
    return gsap.from(self.lines, { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: 0.08 });
  },
});
```

### Word-by-word fill while reading

```js
SplitText.create('.manifesto', {
  type: 'words',
  autoSplit: true,
  onSplit(self) {
    return gsap.from(self.words, {
      opacity: 0.15, stagger: 0.1, ease: 'none',
      scrollTrigger: { trigger: '.manifesto', start: 'top 75%', end: 'bottom 45%', scrub: true },
    });
  },
});
```

### Pinned horizontal track

```js
const section = document.querySelector('.h-section');
const track = section.querySelector('.h-track');
const distance = () => track.scrollWidth - window.innerWidth;

const horizontal = gsap.to(track, {
  x: () => -distance(),
  ease: 'none',
  scrollTrigger: {
    trigger: section, pin: true, scrub: 1, anticipatePin: 1,
    end: () => '+=' + distance(), invalidateOnRefresh: true,
  },
});

// a trigger inside the moving track
gsap.from('.h-track .panel img', {
  scale: 1.3,
  scrollTrigger: { trigger: '.h-track .panel', containerAnimation: horizontal, start: 'left right', scrub: true },
});
```

On mobile, consider a native horizontal scroll-snap row instead of pinning.

### Clip-path image reveal

```js
gsap.utils.toArray('[data-unmask]').forEach((el) => {
  gsap.fromTo(el,
    { clipPath: 'inset(100% 0% 0% 0%)' },
    { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.2, ease: 'expo.out',
      scrollTrigger: { trigger: el, start: 'top 80%' } });
  gsap.from(el.querySelector('img'), { scale: 1.25, duration: 1.6, ease: 'expo.out',
    scrollTrigger: { trigger: el, start: 'top 80%' } });
});
```

### Custom cursor and magnetic elements

```js
if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
  const cursor = document.querySelector('.cursor');
  gsap.set(cursor, { xPercent: -50, yPercent: -50 });
  const xTo = gsap.quickTo(cursor, 'x', { duration: 0.35, ease: 'power3' });
  const yTo = gsap.quickTo(cursor, 'y', { duration: 0.35, ease: 'power3' });
  window.addEventListener('pointermove', (e) => { xTo(e.clientX); yTo(e.clientY); });

  document.querySelectorAll('[data-magnetic]').forEach((el) => {
    const mx = gsap.quickTo(el, 'x', { duration: 0.6, ease: 'elastic.out(1, 0.4)' });
    const my = gsap.quickTo(el, 'y', { duration: 0.6, ease: 'elastic.out(1, 0.4)' });
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      mx((e.clientX - (r.left + r.width / 2)) * 0.35);
      my((e.clientY - (r.top + r.height / 2)) * 0.35);
    });
    el.addEventListener('pointerleave', () => { mx(0); my(0); });
  });
}
```

### Velocity skew that settles

```js
const proxy = { skew: 0 };
const setSkew = gsap.quickSetter('[data-skew]', 'skewY', 'deg');
const clamp = gsap.utils.clamp(-12, 12);
ScrollTrigger.create({
  onUpdate(self) {
    const skew = clamp(self.getVelocity() / -300);
    if (Math.abs(skew) > Math.abs(proxy.skew)) {
      proxy.skew = skew;
      gsap.to(proxy, { skew: 0, duration: 0.8, ease: 'power3', overwrite: true, onUpdate: () => setSkew(proxy.skew) });
    }
  },
});
```

### SVG line drawing and morphing

```js
gsap.registerPlugin(DrawSVGPlugin, MorphSVGPlugin);
gsap.from('.route path', { drawSVG: 0, duration: 2, ease: 'power2.inOut',
  scrollTrigger: { trigger: '.route', start: 'top 70%', end: 'bottom 30%', scrub: true } });
gsap.to('#shape-a', { morphSVG: '#shape-b', duration: 1.2, ease: 'power3.inOut' });
```

Give stroked paths `vector-effect: non-scaling-stroke` when the SVG scales, so line weights stay consistent.

### Cursor spotlight reveal

```js
const stage = document.querySelector('.reveal-stage');
stage.addEventListener('pointermove', (e) => {
  const r = stage.getBoundingClientRect();
  stage.style.setProperty('--x', `${e.clientX - r.left}px`);
  stage.style.setProperty('--y', `${e.clientY - r.top}px`);
});
```

```css
.reveal-stage .hidden-layer {
  mask-image: radial-gradient(circle 180px at var(--x, 50%) var(--y, 50%), #000 40%, transparent 100%);
}
```

### Flip state change

```js
const state = Flip.getState('.grid .item');
grid.classList.toggle('is-expanded');       // change the DOM or classes
Flip.from(state, { duration: 0.8, ease: 'power3.inOut', absolute: true, nested: true });
```

### Counters

```js
gsap.from('.stat-value', {
  textContent: 0, duration: 2, ease: 'power1.inOut', snap: { textContent: 1 },
  scrollTrigger: { trigger: '.stats', start: 'top 75%' },
});
```

### Grain overlay

```css
.grain {
  position: fixed; inset: -50%; pointer-events: none; z-index: 100; opacity: 0.07;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  animation: grain 0.8s steps(4) infinite;
}
@keyframes grain { 0% { transform: translate(0, 0); } 50% { transform: translate(-5%, 3%); } 100% { transform: translate(3%, -4%); } }
```

---

## 6. Pitfalls checklist

- **Animate cheap properties**: transform, opacity, clip-path. Avoid animating width, height, top, left, box-shadow, or large blur filters.
- **Layout shift**: give images `width` and `height` or `aspect-ratio`, then `ScrollTrigger.refresh()` after load and after fonts are ready.
- **Pinning**: don't pin an element inside a transformed parent. Create ScrollTriggers in page order (or set `refreshPriority`). Use `anticipatePin: 1` to avoid jumps.
- **Invisible content**: anything hidden for a reveal must have a guaranteed path to visible (reduced motion, JS failure, trigger never firing at the bottom of the page). Check the last section especially.
- **Mobile**: use `svh` and `dvh` instead of `100vh` for full-height sections, call `ScrollTrigger.config({ ignoreMobileResize: true })`, keep pin chains short, and avoid scroll-jacking that fights the thumb.
- **Touch**: hover-only content needs a tap or always-visible equivalent. Hide custom cursors on touch devices.
- **Scrollable inner elements** (menus, modals) need `data-lenis-prevent` so they scroll natively.
- **Debug leftovers**: no `markers: true`, no `console.log` noise.
- **Missing targets**: guard `querySelector` results before animating. GSAP's "target not found" warnings count as console noise.
- **Single-page apps**: wrap animations in `gsap.context()` or `useGSAP` and revert them on unmount or route change.
- **Performance budget**: one heavy effect (WebGL, canvas sequence, large pinned scene) at a time on screen. Pause offscreen loops with ScrollTrigger `onToggle` or IntersectionObserver.
