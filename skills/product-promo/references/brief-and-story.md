# Brief, storylines, SPEC

## Brief: one question at a time

Ask in this order, skipping anything the repo or the user already answered (a README, a DESIGN.md, store listing):

1. **What is it, and what's the one thing a viewer should remember?** (recommend one from the README)
2. **Where will it be posted?** This sets the formats:

| Destination | Format |
|---|---|
| Website, YouTube, X, a launch post, a PR | 16:9 |
| Reels, Shorts, TikTok, Stories | 9:16 |
| LinkedIn or Instagram feed | 4:5 or 1:1 |
| Product Hunt gallery, README GIF | 16:9 (+ 1:1) |

3. **Length:** 20–25 s for social, 30–40 s for a launch (recommended: 30 s).
4. **Call to action:** a store badge, URL, `brew install …`, "free and open source".
5. **Sound:** music only (recommended) or a voiceover, and a mood (driving, playful, calm).

"Go ahead" means infer the rest and state what you picked.

## STORYLINES.md: three distinct options

Each storyline differs in **form**, not just wording. Proven forms:
- **The day that breaks:** a chain of real pains, each fixed on its own screen. Relief stacks up.
- **Type on the beat:** huge words slam in and get struck out, each cutting to the screen that removes them.
- **One continuous take:** the camera starts tight on one result and rides the clicks through the whole product.

For each one, write: device and form · what the viewer sees · **the first two seconds** · beats (hook → tension →
reveal at ~25% → proof, one verb per shot → payoff → claim → end card) · look · sound. Mark one as recommended and
say why. Show them as an Artifact (a card per storyline with its first frame described), or in the question UI, and let
the user pick or mix.

## SPEC.md: locked before building

```
GOAL:    <who> thinks "<the one thought>" and remembers <product> (<where to get it>).
OUTPUT:  HyperFrames, <W x H>, 30 fps. Other formats: <list>, recomposed.
TIME:    <s>. Music: <track>, <bpm> BPM, fading out over the end card.
LOOK:    pain world: <colours>. Product world: <ground>, <accent> for the reveal flood, <text accent> on ONE word per title.
         Titles <font> 700 on a solid plate; numbers in <mono font>. Every product frame is live footage (recordings/).
SHOTS (<total> s):
  0.0-2.3   <id>: <what's on screen>; "<title>"
  ...
  <claim>  <end card: what holds for 2.5 s>
BANNED:  dark void with small floating UI; glow and particles; three cards in a row; titles that drift after landing;
         any invented product UI; naming competitors; unmeasured speed claims.
QA:      <one time per shot, in seconds>
MUSIC:   <file, source, licence>
```

Shot times come from the music: put cuts on beats (at 120 BPM a beat is 0.5 s, a bar is 2 s).
