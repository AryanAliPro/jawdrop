# Stacks

The design process is identical in every stack. Only the wiring changes. Read the section for the stack you're building in.

## Contents

1. Existing projects
2. Static single page (the default)
3. Static multi-page
4. React (Vite)
5. Next.js (App Router)
6. Vue and Nuxt
7. Svelte and SvelteKit
8. Astro
9. Tailwind CSS (with any of the above)

---

## 1. Existing projects

When the user is already inside a project, the site has to feel native to it.

- Read `package.json`, the folder structure and a few existing components before writing anything. Match the framework and version, TypeScript or JavaScript, the styling approach (CSS Modules, Tailwind, styled-components, Sass), naming, and file layout.
- Install with the package manager the lockfile implies: `pnpm-lock.yaml` means pnpm, `yarn.lock` means yarn, `bun.lockb` or `bun.lock` means bun, otherwise npm.
- Put user-provided assets where the project keeps static files (often `public/`).
- Finish by running the project's own build (and lint, if configured) and fixing what fails.

## 2. Static single page (the default)

```
site/
├── index.html
├── css/styles.css
├── js/main.js
└── assets/            # user assets, custom SVGs, favicon
```

- Load GSAP and Lenis from the CDN (see `motion.md`), and `main.js` as a classic `<script>` so the page works when opened straight from disk.
- Fonts via `<link>` from Google Fonts or Fontshare, with `preconnect`.
- Include `<title>`, meta description, Open Graph tags, a theme color and a favicon (an inline SVG favicon drawn for the concept is a nice touch).
- If the user explicitly wants one file, inline the CSS and JS into `index.html`.

## 3. Static multi-page

```
site/
├── index.html
├── services.html      # whatever pages the business needs
├── about.html
├── contact.html
├── css/styles.css     # shared design system
├── js/main.js         # shared setup, then page-specific scenes
└── assets/
```

- **One concept, many pages.** Every page shares the design system, navigation, footer and motion language, and each page still gets its own hero moment so the visitor keeps discovering.
- Pick page-specific code with a data attribute: `<body data-page="services">`, then in `main.js` run the shared setup and the scenes for `document.body.dataset.page`.
- Header and footer markup are repeated in each file (no build step). Keep them identical and mark the active page in the nav with `aria-current="page"`.
- Page transitions: add `@view-transition { navigation: auto; }` to the shared CSS and give persistent elements such as the logo a `view-transition-name`, so they morph between pages in supporting browsers. A GSAP overlay that plays on link click (then navigates) and again on the next page's load works everywhere.
- Every page passes the jury on its own: one `h1`, real content, working links between all pages.

## 4. React (Vite)

```bash
npm create vite@latest my-site -- --template react   # or react-ts
cd my-site && npm i gsap @gsap/react lenis
```

```jsx
import { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
gsap.registerPlugin(useGSAP, ScrollTrigger);

export default function Hero() {
  const root = useRef(null);
  useGSAP(() => {
    // selectors are scoped to root; everything is reverted on unmount
    gsap.from('.hero-line', { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: 0.08 });
  }, { scope: root });
  return <section ref={root}>{/* ... */}</section>;
}
```

Event-driven animations created later (in click handlers) go through `contextSafe` from `useGSAP` so they get cleaned up too.

Lenis in React, synced to GSAP's ticker and ScrollTrigger:

```jsx
import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { ReactLenis, useLenis } from 'lenis/react';
import 'lenis/dist/lenis.css';

export function SmoothScroll({ children }) {
  const lenisRef = useRef(null);
  useLenis(() => ScrollTrigger.update());
  useEffect(() => {
    const update = (time) => lenisRef.current?.lenis?.raf(time * 1000);
    gsap.ticker.add(update);
    gsap.ticker.lagSmoothing(0);
    return () => gsap.ticker.remove(update);
  }, []);
  return <ReactLenis root options={{ autoRaf: false }} ref={lenisRef}>{children}</ReactLenis>;
}
```

Skip Lenis entirely when `prefers-reduced-motion` is set.

## 5. Next.js (App Router)

```bash
npx create-next-app@latest my-site   # accept the project's preferences, or match the existing project
npm i gsap @gsap/react lenis
```

- Keep `page.tsx` files as server components that hold content. Put animation in small client components marked `'use client'` that use `useGSAP`.
- Wrap the app in the `SmoothScroll` component above (a client component) inside `app/layout.tsx`.
- Fonts: `next/font/google` (self-hosted, no layout shift), or `next/font/local` for Fontshare or user-provided font files placed in the project.
- **Remote images**: `next/image` refuses hosts that aren't allowed in `next.config`. Add the hosts you use:

  ```js
  // next.config.mjs (or .ts)
  const nextConfig = {
    images: {
      remotePatterns: [
        { protocol: 'https', hostname: 'images.unsplash.com' },
        { protocol: 'https', hostname: 'images.pexels.com' },
        { protocol: 'https', hostname: 'upload.wikimedia.org' },
      ],
    },
  };
  export default nextConfig;
  ```

  User-provided images go in `public/` and are referenced as `/file.jpg`.
- SplitText and anything that measures the DOM run inside `useGSAP` (after mount), so server and client markup match and there are no hydration warnings.
- Heavy WebGL: load it with `next/dynamic` and `{ ssr: false }` from inside a client component.
- Route transitions: `app/template.tsx` re-mounts on navigation, so an entrance animation there plays on every page change.
- Add `metadata` exports (title, description, Open Graph) in layouts and pages.
- Verify with `npm run build` and fix every error and warning it reports.

## 6. Vue and Nuxt

```js
import { onMounted, onUnmounted, ref } from 'vue';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

const root = ref(null);
let ctx;
onMounted(() => {
  ctx = gsap.context(() => {
    gsap.from('.hero-line', { yPercent: 110, stagger: 0.08, ease: 'expo.out' });
  }, root.value);
});
onUnmounted(() => ctx && ctx.revert());
```

- In Nuxt, start Lenis in a client-only plugin (`plugins/lenis.client.ts`) and sync it to GSAP's ticker as in `motion.md`.
- Static assets go in `public/`. Use `@nuxt/image` only if the project already does, and allow the remote image hosts in its config.

## 7. Svelte and SvelteKit

```svelte
<script>
  import { onMount } from 'svelte';
  import gsap from 'gsap';
  import { ScrollTrigger } from 'gsap/ScrollTrigger';
  gsap.registerPlugin(ScrollTrigger);

  let root;
  onMount(() => {
    const ctx = gsap.context(() => {
      gsap.from('.hero-line', { yPercent: 110, stagger: 0.08, ease: 'expo.out' });
    }, root);
    return () => ctx.revert();
  });
</script>

<section bind:this={root}>...</section>
```

- `onMount` only runs in the browser, so it's the safe place for GSAP, Lenis and anything touching `window`.
- Reusable reveals work well as Svelte actions (`use:reveal`) that return a `destroy` cleanup.

## 8. Astro

- Component `<script>` tags are bundled and run in the browser once per page. Import GSAP and Lenis there.
- With Astro's client router (`<ClientRouter />`), scripts don't re-run on navigation. Initialize on the `astro:page-load` event and clean up on `astro:before-swap`.
- Use islands (`client:visible`) only for components that need a framework. Plain scripts are enough for most motion.
- Remote images with `astro:assets` need the hosts listed under `image.domains` or `image.remotePatterns` in `astro.config`.

## 9. Tailwind CSS

Tailwind is a fine tool for layout and spacing, but its defaults produce the most recognizable template look on the web. So:

- Define the concept's design tokens (colors, fonts, type scale, spacing rhythm, radii, easing) in the theme: `@theme` in CSS for Tailwind v4, `theme.extend` in `tailwind.config` for v3. Then use only those tokens.
- The default palette (slate, gray, indigo, violet), `rounded-2xl shadow-lg` cards and `bg-gradient-to-r from-purple-500 to-blue-500` are on the burned list.
- Write custom CSS for complex effects (masks, clip-paths, grain, blend modes) instead of stretching utilities.
- Animation still runs through GSAP. Tailwind's `animate-*` utilities are too generic for the hero.
