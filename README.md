# DIG DEEPER  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg?style=for-the-badge" alt="Version" /> <img src="https://komarev.com/ghpvc/?username=felixofabio-dig-deeper&label=Repo%20Views&color=blue&style=for-the-badge" alt="Repo Views" /> <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License: MIT" /> <img src="https://github.com/felixofabio/dig-deeper/actions/workflows/validate.yml/badge.svg?style=for-the-badge" alt="Validate plugin package" />
<p align="left">
  <img src="https://img.shields.io/badge/Claude_Code-8A2BE2?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Code" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white" alt="JSON" />
  <img src="https://img.shields.io/badge/YAML-CB171E?style=for-the-badge&logo=yaml&logoColor=white" alt="YAML" />
</p>

A Claude Code skill that turns a real personal experience into authentic
social media content, through a guided interview instead of a one-shot
prompt.

No clichéd copywriting, no generic "AI voice." The output sounds like the
person who lived the story, because it's built from their own words.

---

## What it does

Most AI-generated content about "personal experiences" reads generic,
because it asks for the topic once and starts writing immediately. `dig-deeper`
does the opposite: it interviews the person first, one question at a time,
and only writes once it has real material to work with.

The result can be a carousel, a single post, a Reels/Stories script, a
long-form video script, a thread, a long-form article, a podcast script, or
any other format the person names. The skill doesn't lock you into one
shape.

## How it works

### 1. An adaptive interview, not a fixed script

Instead of always asking the same five questions, `dig-deeper` works from a
bank of 20: five layers of the story, four question variants each. For every
layer, it picks the variant that best fits what the person already shared,
and skips any layer their opening message already answered.

| Layer | Focus | Sample question |
|---|---|---|
| 1. Triggering fact | What was going on | "What led up to that moment?" |
| 2. Concrete scene | The point it became unsustainable | "Was there a specific day you realized how bad it had gotten?" |
| 3. Turning point | What changed | "What actually pulled you out of it?" |
| 4. The lesson | Hindsight advice | "What would you tell someone in that exact spot today?" |
| 5. Audience & effect | Who it's for | "Who do you want this to reach, and what should they feel?" |

In practice, this usually lands somewhere between 3 and 6 questions,
depending on how much the person already shared up front, not a fixed count
and not all 20. If someone says they'd rather not go into detail about
something, the skill respects that without pushing and keeps the emotional
weight of the moment without the specifics they asked to leave out.

### 2. Format comes first, writing comes second

Before writing anything, the skill either uses the format the person named
or asks them directly what they have in mind. It never assumes a carousel by
default, and it treats its own list of format examples (carousel, single
post, Reels/Stories script, long-form video, thread, article, podcast
script) as a starting point, not a closed menu. Any format the person asks
for gets accepted, even ones outside that list.

### 3. One story arc, adapted to whatever format was chosen

Underneath every format is the same six-part arc: hook, context, low point,
turning point, lesson, closing. What changes is how it's distributed, across
separate slides, across paragraphs of a single block of text, across cuts in
a spoken script, or across numbered posts in a thread.

### 4. Style rules that keep it sounding human

- Never uses the "it's not about X, it's about Z" construction
- Never repeats the same idea across different parts of the content
- Avoids poetic or dramatic phrasing the person wouldn't actually use,
  reusing their own words from the interview instead
- Matches sentence length to the format chosen, instead of forcing one
  style onto every format
- Checks in on tone before moving forward, instead of assuming the first
  draft landed

### 5. A caption that continues the story instead of repeating it

When the format has a caption separate from the main content, the skill
writes it to add a new angle, not to summarize what was already said. It
also skips the default "comment below" call to action unless the person
explicitly asks for one.

### 6. Visual guidance, only when it's relevant

For formats with a visual component (carousels, video/Stories scripts), the
skill can suggest solid backgrounds over stock imagery, color alternation by
emotional weight, and framing notes for video, always favoring the
authenticity of the story over generic decoration.

## Why pair it with Humanizer

`dig-deeper` already handles the vices specific to this kind of content:
the "it's not about X, it's about Z" cliché, tone that doesn't match the
person, repetition between parts. What it doesn't cover is the broader,
format-agnostic layer of AI-writing tics that can slip into any piece of
text, regardless of topic: excessive em dashes, the "rule of three,"
promotional language, vague attributions, superficial "-ing" analyses.

That's exactly what [Humanizer](https://github.com/blader/humanizer) is
built for. As the last step of its process, `dig-deeper` runs its output
through Humanizer, if it's installed, as one more pass before the content is
considered final. If Humanizer isn't available, this step is skipped
without blocking delivery, `dig-deeper`'s own style rules remain the
baseline either way.

**This repository does not redistribute Humanizer.** Install it from its
[original repository](https://github.com/blader/humanizer), so you always
get the current version with proper attribution to its author.

## Installation

### Option 1: Via Plugin Marketplace (Recommended for Claude Code)

```bash
/plugin marketplace add felixofabio/dig-deeper
/plugin install dig-deeper@dig-deeper-marketplace
```

### Option 2: Download ZIP via [Release](https://github.com/felixofabio/dig-deeper/releases) (Web UI)

1. Download the .zip file directly from the Releases page.
2. Open Claude.
3. Go to Customize -> Skills -> Add -> Upload Skill.
4. Select the downloaded .zip file.

### Option 3: Manual CLI Install

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/felixofabio/dig-deeper.git /tmp/dig-deeper
cp -r /tmp/dig-deeper/skills/dig-deeper ~/.claude/skills/
rm -rf /tmp/dig-deeper
```

### Humanizer (original repository, recommended)

```bash
git clone https://github.com/blader/humanizer.git ~/.claude/skills/humanizer
```

With both folders inside `~/.claude/skills/` (or the plugin installed via
marketplace), Claude Code picks up both automatically, no restart needed.

## Usage

Once installed, just describe a real experience you want to turn into
content, and Claude will pick up the skill on its own:

```
I want to turn a work mistake I made into a LinkedIn post. Can you interview
me about it?
```

If it was installed as a plugin, you can also invoke it directly:

```
/dig-deeper:dig-deeper
```

Claude will ask its first question. Answer at your own pace, one question
at a time, and the skill will let you know once it's ready to write.

## Repository structure

```
dig-deeper/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .github/
│   └── workflows/
│       └── validate.yml
├── scripts/
│   └── validate-package.py
├── LICENSE
├── README.md
└── SKILL.md
```

### Validating before publishing

```bash
pip install pyyaml
python scripts/validate-package.py
```

The script checks that `plugin.json` and `marketplace.json` are valid JSON,
that required fields are present, that names match between the two
manifests, and that each referenced `SKILL.md` has valid frontmatter with a
`name` matching its folder. The same check runs automatically in GitHub
Actions on every push or pull request to `main`, so if you (or a
contributor) forget to run it locally, the problem shows up in the PR
itself before it reaches anyone installing the skill.

## When not to use it

Not meant for institutional or product/service promotional content, or for
text that's already finished and just needs a review, use Humanizer directly
for that.

## License

The `dig-deeper` skill in this repository is licensed under MIT (see the
`LICENSE` file). Humanizer, referenced here but not included, is MIT-
licensed by [Blader](https://github.com/blader), see the
[original repository](https://github.com/blader/humanizer) for full terms.


---

## 👨‍💻 About the Developer

<div align="center">
  <h3>Developer focused on authentic storytelling and AI Agent creation.</h3>
  <p>Built with focus on authentic storytelling by <strong><a href="https://github.com/felixofabio" target="_blank">Fábio Félix</a></strong>.</p>
  <p>Let's connect or discuss building AI Agents and custom skills:</p>
  
  <a href="https://www.instagram.com/felixofabio">
  <img src="https://img.shields.io/badge/-Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" />
</a>
  &nbsp;&nbsp;
  <a href="mailto:contato.felixofabio@gmail.com">
    <img src="https://img.shields.io/badge/-Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
</div>