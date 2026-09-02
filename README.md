<!--
DIRECTION CONTRACT — Terminal/TUI (centered layout)
THESIS: The profile IS a zsh session. It refuses the badge-wall + hero-card
  template; every section is a command. Centered + contained top to bottom.
OWN-WORLD: Catppuccin Mocha (bg #11111b, base #1e1e2e) with a peach #fab387
  signature; mono is the native medium (real commands), not a costume.
  Header is a rendered terminal window (traffic lights, syntax coloring).
STORY: Visitor reads a backend/AI engineer driving a terminal — lands on the
  name, reads `cat about.txt`, then scans work, stack, activity as commands.
FIRST VIEWPORT: large terminal-window banner — `whoami --name` → VEDANTH M S,
  `cat role.txt` → role, last line TYPES rotating taglines (animated GIF) with
  a blinking peach cursor. Then `cat about.txt`, portfolio link, entry badges.
FORM: user-pinned Terminal/TUI (chosen from three concepts). Banner rendered
  deterministically by assets/banner-src/gen_banner.py (Pillow), not a screenshot;
  animated GIF for the typing loop, static PNG as the <picture> fallback.
-->

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-dark.gif">
  <source media="(prefers-color-scheme: light)" srcset="./assets/banner-light.gif">
  <img alt="Vedanth M S — Software Engineer" src="./assets/banner-dark.png" width="100%">
</picture>

</div>

```text
vedanth@portfolio ~ % cat about.txt

  Role ......... Backend & AI-Integrated Software Engineer
  Focus ........ rule engines · dev tooling · agentic systems
  Languages .... Java · Python · TypeScript · C
  Backend ...... Spring Boot · Node.js
  Frontend ..... React · Vite · Tailwind
  Data ......... MySQL · SQLite · Docker · Vercel
  AI ........... Gemini · Ollama · RAG
  Latency ...... decisions in single-digit milliseconds
  Currently .... shipping backend systems end to end
  Open to ...... backend & AI-integrated roles
```

<div align="center">

**[⟶ &nbsp;Step into the interactive 3D portfolio](https://vedanth1101-source.github.io/vedanth-portfolio/)**

<sub>a WebGL room you walk up to, boot a Windows-95 desktop, and explore the work from inside the monitor</sub>

<br>

[![Portfolio](https://img.shields.io/badge/portfolio-fab387?style=flat-square&logo=vercel&logoColor=11111b)](https://vedanth1101-source.github.io/vedanth-portfolio/)
[![LinkedIn](https://img.shields.io/badge/linkedin-313244?style=flat-square&logo=linkedin&logoColor=cdd6f4)](https://linkedin.com/in/vedanth-m-s)
[![GitHub](https://img.shields.io/badge/github-313244?style=flat-square&logo=github&logoColor=cdd6f4)](https://github.com/vedanth1101-source)
[![Email](https://img.shields.io/badge/email-313244?style=flat-square&logo=gmail&logoColor=cdd6f4)](mailto:vedanth1101@gmail.com)
&nbsp;
![Profile Views](https://komarev.com/ghpvc/?username=vedanth1101-source&label=profile+views&color=fab387&style=flat-square)

</div>

---

### $ ls ~/work

**[sentinelx/](https://github.com/vedanth1101-source/sentinelx)** &nbsp;·&nbsp; `configurable policy decision engine`<br>
Moves business rules out of code and into a database, then evaluates transactions against an in-memory rule set in **single-digit milliseconds** — no database read on the hot path. A lock-free `volatile` cache with synchronized write-through invalidation, strictest-wins severity escalation, and an adversarial stress-test endpoint that measures per-rule coverage. **34 tests.**<br>
<sub>`Java 21` · `Spring Boot` · `React` · `TypeScript` · `MySQL`</sub>

**[BugBuddy/](https://github.com/vedanth1101-source/BugBuddy)** &nbsp;·&nbsp; `AI developer diagnostics`<br>
Turns a raw stack trace into a plain-English diagnosis and a suggested fix with Gemini, keeping a MySQL cache in front so a repeated error never pays for the model twice. Per-IP rate limiting and optional API-key auth guard the one endpoint that spends quota.<br>
<sub>`Java 21` · `Spring Boot` · `React 19` · `Gemini` · `Railway` · `Vercel`</sub>

**[farm-manager/](https://github.com/vedanth1101-source/farm-manager-ai-poc)** &nbsp;·&nbsp; `local-first agentic platform`<br>
Translates plain-English questions into SQL over a local Ollama model, with a deterministic regex fallback for zero-downtime querying, a RAG knowledge base, and autonomous background agents.<br>
<sub>`Java` · `Spring Boot` · `SQLite` · `Ollama` · `RAG`</sub>

---

### $ cat stack.txt

**Languages**<br>
<img src="https://skillicons.dev/icons?i=java,python,ts,js,c&theme=dark" height="40" />

**Backend**<br>
<img src="https://skillicons.dev/icons?i=spring,nodejs&theme=dark" height="40" />

**Frontend**<br>
<img src="https://skillicons.dev/icons?i=react,vite,tailwind,html,css&theme=dark" height="40" />

**Data &amp; Infra**<br>
<img src="https://skillicons.dev/icons?i=mysql,sqlite,docker,vercel&theme=dark" height="40" />

**AI &amp; Tooling**<br>
<img src="https://skillicons.dev/icons?i=git,vscode,postman&theme=dark" height="40" />

`Gemini API` &nbsp;·&nbsp; `Ollama` &nbsp;·&nbsp; `RAG`

---

### $ git log --stat

<div align="center">

<img width="850" src="https://github-readme-stats-theta-gold-67.vercel.app/api?username=vedanth1101-source&show_icons=true&count_private=true&include_all_commits=true&hide_border=true&card_width=850&title_color=fab387&icon_color=89b4fa&text_color=cdd6f4&bg_color=1e1e2e&v=2" alt="GitHub stats" />

<img width="850" src="./assets/activity.svg" alt="Contribution activity graph" />

<img width="850" src="./assets/streak.svg" alt="Contribution streak" />


</div>

---

### $ ./heatmap 

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/heatmap-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/heatmap-light.svg">
  <img alt="Vedanth's contribution heatmap" src="./assets/heatmap-dark.svg" width="850">
</picture>

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:fab387,50:cba6f7,100:89b4fa&height=110&section=footer" />

<div align="center">
<sub>vedanth@portfolio ~ % &nbsp;open to backend &amp; AI-integrated software roles&nbsp; · &nbsp;final-year CS @ SSN College of Engineering</sub>
</div>
