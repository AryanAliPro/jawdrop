<h1 align="center">Jawdrop</h1>

<p align="center"><strong>The $1 Billion Prize website designer for AI coding agents.</strong></p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-24292f?style=flat" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-ready-d97757?style=flat" alt="Claude Code">
  <img src="https://img.shields.io/badge/Codex-ready-10a37f?style=flat" alt="Codex">
  <img src="https://img.shields.io/badge/Cursor-ready-24292f?style=flat" alt="Cursor">
  <img src="https://img.shields.io/badge/Antigravity-ready-4285f4?style=flat" alt="Antigravity">
</p>

Jawdrop is an Agent Skill that turns a one-line request like **"Build website for a roofing company"** into a fully custom, award-level website. Every build is treated as an entry in the **World's Top and Hardest Web Design Competition, with a real $1 Billion prize**, so your agent stops assembling templates and starts designing something visitors have never seen before.

## Built with Jawdrop

Every one of these came from a one-line brief. No two share a layout, because the skill has no layouts to share.

<table>
  <tr>
    <td width="50%"><img src="examples/first-crack.jpg" alt="First Crack, a coffee roastery: a cracked coffee bean between the words First and Crack."><br><sub><b>First Crack</b> · coffee roastery &amp; kitchen, Portland</sub></td>
    <td width="50%"><img src="examples/crumb-and-crema.jpg" alt="Crumb &amp; Crema, a coffee bar: the word Bitter set against a pink shape and an espresso cup seen from above."><br><sub><b>Crumb &amp; Crema</b> · coffee bar &amp; confectionery</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src="examples/window-seat.jpg" alt="Window Seat, a coffee and sweets shop: Pull up a window seat, beside a cafe table framed by a window."><br><sub><b>Window Seat</b> · coffee &amp; sweets, Larkin Street</sub></td>
    <td width="50%"><img src="examples/solstizio.jpg" alt="Hotel Solstizio in Positano: Stay for the light, beside a round window onto the Amalfi coast."><br><sub><b>Hotel Solstizio</b> · Positano, Amalfi Coast</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src="examples/everafter.jpg" alt="Everafter, Paris wedding planners: Ever After in huge serif letters around a photo of a couple on a Paris bridge."><br><sub><b>Everafter</b> · wedding planners, Paris</sub></td>
    <td width="50%"><img src="examples/elias-marren.jpg" alt="Elias Marren, a photographer: Light, in its hours, over mountains at sunset above the clouds."><br><sub><b>Elias Marren</b> · landscape photographer, Zurich</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src="examples/kyma.jpg" alt="Kyma, an island hotel in Milos: Stay longer over an aerial photo of a cove, with a draggable night picker."><br><sub><b>Kyma</b> · island hotel, Milos</sub></td>
    <td width="50%"><img src="examples/forge.jpg" alt="Forge, a fitness club: Built under load, with a lifter inside a red weight plate."><br><sub><b>Forge</b> · strength &amp; coaching club, Austin</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src="examples/alba-dental.jpg" alt="Alba Dental Studio: Your smile, shade by shade, beside a fanned-out tooth shade guide."><br><sub><b>Alba Dental Studio</b> · dentist, Austin</sub></td>
    <td width="50%"><img src="examples/oliva-and-stone.jpg" alt="Oliva &amp; Stone, an Italian kitchen: the name in tall serif letters beside an arched photo of a plated dish."><br><sub><b>Oliva &amp; Stone</b> · Italian kitchen, Austin</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src="examples/dew-and-bloom.jpg" alt="Dew &amp; Bloom skincare: Skincare that keeps time, with the product range in front of a rising sun."><br><sub><b>Dew &amp; Bloom</b> · skincare, Toronto</sub></td>
    <td width="50%"><img src="examples/setpoint.jpg" alt="Setpoint heating and air: Set the weather inside, beside a large thermostat dial set to 72."><br><sub><b>Setpoint</b> · heating &amp; air, Denver</sub></td>
  </tr>
</table>

## Install

**One command, every agent** (Claude Code, Codex, Cursor, Antigravity, Windsurf, GitHub Copilot, Gemini CLI, OpenCode and 70+ more):

```bash
npx skills add AryanAliPro/jawdrop -g
```

It detects the agents on your machine and asks which ones to install to. Uses the [`skills`](https://github.com/vercel-labs/skills) CLI and needs Node.js 22.20 or later.

<details>
<summary><strong>No Node.js? Use the install script</strong></summary>

macOS and Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/AryanAliPro/jawdrop/main/install.sh | bash
```

Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/AryanAliPro/jawdrop/main/install.ps1 | iex
```

Both copy the skill into every agent they find. An existing `jawdrop` folder is moved to `~/.jawdrop-backups/` first. To pick agents, run `curl -fsSL .../install.sh | bash -s -- --agent claude-code --agent cursor` (or set `$env:JAWDROP_AGENTS = "claude-code,cursor"` on Windows).

</details>

<details>
<summary><strong>Just one agent</strong></summary>

| Agent | Command |
|---|---|
| Claude Code | `npx skills add AryanAliPro/jawdrop -g -a claude-code` |
| Codex | `npx skills add AryanAliPro/jawdrop -g -a codex` |
| Cursor | `npx skills add AryanAliPro/jawdrop -g -a cursor` |
| Antigravity | `npx skills add AryanAliPro/jawdrop -g -a antigravity` |
| Windsurf | `npx skills add AryanAliPro/jawdrop -g -a windsurf` |
| GitHub Copilot | `npx skills add AryanAliPro/jawdrop -g -a github-copilot` |
| Gemini CLI | `npx skills add AryanAliPro/jawdrop -g -a gemini-cli` |
| OpenCode | `npx skills add AryanAliPro/jawdrop -g -a opencode` |

Leave out `-g` to install into the current project only.

</details>

<details>
<summary><strong>Claude Code plugin</strong></summary>

Run these inside Claude Code:

```
/plugin marketplace add AryanAliPro/jawdrop
/plugin install jawdrop@jawdrop
```

`/plugin update` upgrades it later.

</details>

<details>
<summary><strong>Codex plugin</strong></summary>

```bash
codex plugin marketplace add AryanAliPro/jawdrop
codex plugin add jawdrop@jawdrop
```

Start a new Codex session afterwards so the skill loads.

</details>

## Use it

Ask your agent for a website, in any words:

```
Build website for a family-run roofing company in Denver
```

```
Build a multi-page website (Home, Services, About, Contact) for an immigration law firm in Toronto
```

```
Make a Next.js landing page for my pottery studio. My logo and photos are in ./assets
```

Jawdrop triggers on its own whenever you ask for a website, landing page, homepage or portfolio. In Claude Code you can also call it directly: `/jawdrop Build website for ...`

## What it does

- **The $1 Billion brief.** Your agent works as if it's competing for a real 1 Billion Dollar prize in the hardest web design competition in the world, judged by people who have already seen ten thousand entries for the same brief.
- **No templates, no presets.** There are deliberately no premade layouts and no "for a restaurant, do X" rules. Instead the skill gives the agent a process for inventing an original concept from your subject: immerse in the industry, write three concepts, kill the obvious one, and invent a signature interaction nobody has seen before.
- **Industry vibe.** Colors, textures, imagery, motion and copy come from the real world of the business, so visitors feel the industry before they read a word.
- **Motion that wows.** GSAP with ScrollTrigger, SplitText, Flip, DrawSVG and MorphSVG, smooth scrolling with Lenis, SVG animation and micro-interactions on everything you can hover, click or focus.
- **Your assets first.** If you give it a logo, photos, brand colors or copy, the design is built around them. Otherwise it finds relevant public images and checks that every URL actually loads.
- **Professional hierarchy.** The wow never costs clarity: one clear message, an obvious call to action, readable text, real copy and no lorem ipsum.
- **Banned looks.** Glassmorphism, neon cyber gradients, the default centered hero, rows of identical cards, and the house styles AI-made sites fall into.
- **A jury before hand-over.** The agent checks every link, takes desktop and mobile screenshots, reads the console, then scores the site as five judges (Art Director, Motion Director, Industry Insider, Conversion Lead, Engineer) and fixes anything under 9/10.
- **Any stack.** Plain HTML/CSS/JS (one page or many), React, Next.js, Vue, Nuxt, Svelte, SvelteKit, Astro or Tailwind, or whatever project you're already in.

## What's inside

```
skills/jawdrop/
├── SKILL.md              the brief, the process, the burned list
├── references/
│   ├── motion.md         GSAP + Lenis setup, technique arsenal, pitfalls
│   ├── stacks.md         wiring for every framework
│   ├── imagery.md        your assets first, finding and verifying public images
│   └── jury.md           the verification gate and the five-judge scorecard
└── scripts/
    ├── check_urls.py     checks every image, script and font URL loads
    ├── find_images.py    searches open image libraries, returns verified URLs
    └── snapshot.py       headless Chrome screenshots + console errors
```

The helper scripts need **Python 3** (standard library only). Screenshots need Chrome, Edge, Brave or Chromium. Image search works without keys, and uses the Unsplash or Pexels APIs if you set `UNSPLASH_ACCESS_KEY` or `PEXELS_API_KEY`.

## Update and uninstall

```bash
npx skills update jawdrop          # update
npx skills remove jawdrop -g       # uninstall
```

With the install script, run it again to update, or add `--uninstall` to remove jawdrop from every agent.

## License

[MIT](LICENSE)
