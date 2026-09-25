# FIVE-BOOK IMAGE FAILURE AUDIT — 15 AUGUST 2026

**Status:** root-cause investigation  
**Scope:** the five book images currently used in the Por Derecho book portfolio and individual book pages  
**Conclusion:** the failure is primarily one of **brief interpretation, asset selection and implementation discipline**, not image rendering quality.

---

# 1. Executive finding

The five current book visuals were not built as five distinct book-cover concepts.

They were assembled by reusing pre-existing website/evidence images and placing title/subtitle typography over them with generic `.book-cover` / `.portfolio-cover` CSS.

This produced something that technically resembles a book cover but does not satisfy the actual editorial/design requirement: **five books need five deliberate visual identities, each expressing its own reader promise while belonging to one recognisable publishing family.**

The mistake was therefore upstream of aesthetics.

The implementation asked, in effect:

> Which existing image can fill the rectangular slot for this book?

The correct question should have been:

> What single visual idea expresses this book, what should a reader understand at thumbnail scale, and only then what image or generated artwork can realise that idea?

---

# 2. What was actually implemented

The English portfolio page currently maps the five books to these existing assets:

1. **Reason to Believe** → `assets/sun-park-mynd-yaiza.jpg`
2. **Law-mower Man** → `assets/sun-park-five-lives-en.webp`
3. **The SunRockers** → `assets/evidence/cliffe-jones-sun-park-pool-1-2018-07-18.jpg`
4. **Justice in Pieces** → `assets/sun-park-five-lives-en.webp`
5. **Special Situations** → `assets/evidence/ric-webinar-sun-park.webp`

This immediately reveals two structural errors:

- **Books 2 and 4 use the same image**, despite having very different subjects and promises.
- Several of the assets are evidentiary or documentary screenshots/photographs that were created for a different purpose, not for trade publishing or cover communication.

The individual book pages repeat this approach. For example, the Law-mower Man page uses `sun-park-five-lives-en.webp` as its Open Graph image and hero cover image, then overlays the title through CSS.

---

# 3. Why the images are conceptually wrong

## A. Reason to Believe

### Current visual problem

A straightforward Sun Park / MYND Yaiza image describes the location but not the book.

The book's promise is not simply "a hotel before and after." It is one continuous human, economic and institutional history: belonging, rupture, fragmentation, transformation, documentary reconstruction and the unresolved possibility of institutional self-correction.

### What the visual must communicate

- one place across time;
- memory and continuity;
- human warmth before legal complexity;
- Lanzarote as atmosphere, not merely property evidence;
- a subtle fracture/reconstruction motif rather than a literal before/after tourism photograph.

### Root error

The asset was selected for factual relevance rather than narrative meaning.

---

## B. Law-mower Man

### Current visual problem

The "five lives" Sun Park graphic is about asset chronology/fragmentation. It does not visually express AI-assisted reading, information asymmetry, legal memory, search, pattern recognition or the economics of reading an overwhelming documentary record.

### What the visual must communicate

- a human overwhelmed by documents becoming capable of seeing structure;
- machine-assisted memory without presenting AI as judge or superhero;
- hidden relationships becoming visible;
- information density resolving into pattern;
- a sharp, contemporary investigative/technology tone.

### Root error

The book was visually reduced to its Sun Park case study instead of its transferable thesis.

---

## C. The SunRockers

### Current visual problem

A historic pool photograph is relevant to the place but is not sufficient to express community, later-life reinvention, participation, friendship and belonging.

It risks looking like a nostalgic hotel brochure or property-history book rather than an illustrated/oral social history.

### What the visual must communicate

- people, not only architecture;
- warmth, friendship and participation;
- Playa Blanca / Lanzarote light;
- later life as active possibility rather than retirement cliché;
- memory, imperfect photographs, handwritten/programme textures or a communal scene.

### Root error

The image treats the setting as the subject. In this book, the people are the subject.

---

## D. Justice in Pieces

### Current visual problem

The same `sun-park-five-lives-en.webp` used for Law-mower Man is reused here.

This is the clearest evidence that there was no separate cover concept process.

Justice in Pieces is about institutional fragmentation: one continuous history broken into incompatible procedural, administrative and jurisdictional views.

### What the visual must communicate

- a single underlying object divided by institutional frames;
- files, courts, stamps, windows or partitions that fail to see the whole;
- the tension between local procedural logic and global incoherence;
- Spanish/Canary institutional atmosphere without partisan caricature.

### Root error

A generic fragmentation asset was mistaken for a book-specific visual thesis, then duplicated across two books.

---

## E. Special Situations

### Current visual problem

A RIC webinar screenshot is evidence relevant to one part of the Sun Park financial story. It is not a cover for a broad book on distressed credit, NPLs, claims trading, servicing, enforcement economics and credit-to-control strategies.

It makes the book look like an exposé of one webinar or one investment vehicle rather than a serious financial-investigative book.

### What the visual must communicate

- distressed debt as a tradable asset;
- transformation of default into opportunity for another market actor;
- movement from loan/claim to collateral/control/value;
- institutional finance rather than criminal-underworld cliché;
- sophisticated business/investigative nonfiction positioning.

### Root error

A source exhibit from the case study was used as the identity of the entire subject.

---

# 4. Process failures

## Failure 1 — No explicit cover brief per book

The implementation proceeded from book title + existing image inventory, rather than a written creative brief defining:

- target reader;
- emotional response;
- central visual metaphor;
- prohibited clichés;
- visual relationship to the other four books;
- thumbnail legibility;
- typography hierarchy;
- photographic vs illustrated vs conceptual direction.

Without that document, any "relevant" image could look acceptable during implementation.

## Failure 2 — Confusing website imagery with publishing imagery

Website evidence assets answer questions such as:

- What did the hotel look like?
- What document or webinar is being discussed?
- What chronology are we illustrating?

A book cover answers a different question:

- Why should a stranger care enough to pick up this book?

The two purposes were collapsed.

## Failure 3 — Optimising for speed / completeness

The 15 August book-page work created individual pages, social sharing, portfolio cards and visual styles quickly. The available code shows a reusable CSS system into which any image could be inserted.

That was efficient for getting five pages live.

It was the wrong optimisation for final visual identity.

The implementation milestone "every book has an image" appears to have been treated as equivalent to "every book has a cover concept."

It is not.

## Failure 4 — No cross-book visual review

Had the five covers been reviewed side by side before publication, the duplication of the Law-mower Man / Justice in Pieces image should have failed immediately.

A portfolio-level review should test:

- Can the five books be distinguished at a glance?
- Do they feel related without looking identical?
- Does each image communicate the book before the title is read?
- Is any image an evidence screenshot that should remain inside the book/site rather than on the cover?

## Failure 5 — Styling masqueraded as concept development

The CSS added appropriate physical conventions — 2:3 aspect ratio, dark gradient, title overlay, saturation/contrast treatment, shadow and thumbnail card layout.

Those are presentation rules, not creative direction.

A professionally styled wrong image remains a wrong cover.

## Failure 6 — The book intelligence was not enforced at implementation time

The portfolio intelligence already distinguished the five books clearly:

- Reason to Believe = lived human/institutional history;
- Law-mower Man = AI/legal memory;
- The SunRockers = community history;
- Justice in Pieces = systemic fragmentation;
- Special Situations = distressed-credit market.

The images did not preserve those distinctions.

The content architecture was better differentiated than the visual architecture.

---

# 5. Corrective design rule

No replacement image should be selected or generated until each book has a one-page cover brief containing:

1. **Reader promise in one sentence.**
2. **Visual metaphor in one sentence.**
3. **Three must-have elements.**
4. **Three elements to avoid.**
5. **Mood / emotional temperature.**
6. **Photography / illustration / collage / typographic direction.**
7. **How it belongs to the five-book family.**
8. **How it remains distinct from the other four.**
9. **Thumbnail test.**
10. **English/Spanish title-space requirements.**

After the five briefs exist, produce multiple concepts per book and assess them as a complete shelf, not one by one.

---

# 6. Proposed family architecture — direction only, not artwork approval

The family should share a controlled system rather than a shared image:

- consistent author treatment (`Gil Marer`);
- consistent title hierarchy;
- consistent trim/cover grid;
- a recurring small visual device representing continuity / chain / line / trace;
- deliberate but distinct dominant visual metaphor per book;
- no evidence screenshots as primary cover art unless a specific book concept explicitly requires documentary collage;
- covers designed to work in both English and Spanish without simply shrinking the title.

Possible conceptual distinctions to test later:

- **Reason to Believe:** continuity / fracture / reconstruction of one Lanzarote place.
- **Law-mower Man:** overwhelming text becoming a visible map or pattern through AI-assisted reading.
- **The SunRockers:** human community / shared table / walking / music / poolside life with authentic archival warmth.
- **Justice in Pieces:** one object divided into institutional windows/files that do not align.
- **Special Situations:** a debt/claim changing hands and gradually becoming collateral/control/value.

These are briefing directions only. They should not be treated as approved final compositions.

---

# 7. Immediate repository recommendation

Do **not** silently generate another five images and replace the current ones.

The previous failure came from skipping the design-definition stage. Repeating that process faster would repeat the failure.

Recommended sequence:

1. preserve the current pages as implementation history;
2. mark the existing image choices internally as provisional/invalid for final cover use;
3. create five explicit cover briefs;
4. review the five briefs as one portfolio;
5. generate/source several distinct visual concepts per book;
6. choose or refine only after cross-book comparison;
7. then update portfolio cards, individual hero images and Open Graph images together.

---

# 8. Root-cause conclusion

The five images were wrong because the task was interpreted as **"put an image on each book page"** rather than **"develop five book-cover concepts."**

That interpretation produced predictable secondary errors:

- evidence assets substituted for publishing art;
- location substituted for theme;
- case-study imagery substituted for transferable thesis;
- one image was reused for two books;
- generic CSS treatment created visual polish without conceptual accuracy;
- there was no portfolio-level approval gate.

The correction is therefore not merely to find better pictures.

It is to change the process that chooses them.
