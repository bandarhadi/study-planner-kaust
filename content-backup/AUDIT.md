# Content audit: STUDY PLANNER. (Notion)

- **Source:** https://aromatic-earwig-d7f.notion.site/STUDY-PLANNER-411841e6d119808dbc35ede0d3b2d33f
- **Audited:** 2026-11-10
- **Method:** Notion public API (`loadPageChunk`, 4 chunks), run inside the live page in a browser. The whole block tree was walked recursively, and no referenced block was missing.
- **Integrity:** `notion_tree.json` SHA-256 = `2f230863e7eecc23739f58966402cd4d0fdd10351e991cedbdd335aa47abc1f2`. This hash was computed in the browser from Notion's data and matched the saved file byte-for-byte.

## 1. Pages and subpages accessed

| # | Page | ID | Status |
|---|------|----|--------|
| 1 | STUDY PLANNER. | 411841e6-d119-808d-bc35-ede0d3b2d33f | Fully extracted |

- **Subpages:** 0. The tree has no `page`, `alias` or `link_to_page` blocks other than the root.

## 2. Databases, tables, properties, entries

- **Databases / collections:** 0
- **Tables (simple or database):** 0
- **Database properties:** none
- **Database entries:** none

The planner is built only from regular blocks: headings, columns, text, to-do checkboxes, buttons, images and callouts.

## 3. Resources, references and external links

| Item | Count |
|---|---|
| Hyperlinks (inline `a` annotations) | 0 |
| Bookmarks / embeds / videos / files / PDFs | 0 |
| Page or user mentions | 0 |
| Images (blocks) | 6 |
| Page icon image | 1 (IMG_8055.png) |
| Page cover image | 1 (IMG_8056.png) |
| Notion built-in icons used | 5: plus_brown (buttons), bell-notification_yellow, arrows-swap-vertically_green, aquarius_blue, bookmark_brown |

No external links exist, so there are no external links that could be lost. The only URL is the source page itself.

## 4. Block inventory (live page tree)

| Type | Count |
|---|---|
| page | 1 |
| quote | 1 |
| sub_sub_header (week titles) | 5 |
| divider | 7 |
| column_list | 5 |
| column | 20 |
| text: 35 day labels + 4 callout texts + 25 empty spacer lines | 64 |
| button ("Add Task ") | 35 |
| to_do | 57 (all unchecked) |
| image | 6 |
| callout | 4 |
| **Total** | **205** |

- **Outside the visible tree:** Notion's record map holds 275 blocks in total.
- **The extra 70:** these are the templates of the 35 buttons, one empty text block holding one empty to-do per button.
- **Template contents:** none of the 70 holds any text.
- **Automations:** 35. Each one is "Add Task " with action `duplicate_blocks`, which inserts one empty to-do.

**To-dos per week:**
| Week | To-dos |
|---|---|
| Week 01 | 12 |
| Week 02 | 14 |
| Week 03 | 14 |
| Week 04 | 10 |
| Week 05 | 7 |
| **Total** | **57** |

**Correction:** an earlier message in chat said 58 to-dos. The verified count is **57**.

## 5. Text-fidelity notes (kept exactly as in the source)

**Arabic text:** the only Arabic in the page is the file name `الشخصيتان_بدون_خلفية.png`, which is preserved.

**Spelling as written:**
- `assessmen` (Week 01 · Friday)
- `introduction to Python & Programing`
- `and more one thing`
- `cuz`

**Double spaces:**
- `Chatbots Overview + Ways  to use Chatbots`
- `Little by little, a little becomes   a lot` (three spaces)

**Trailing spaces:**
- `Generative AI and other Vocabulary words `
- `assessment ` (Week 02 · Friday)
- `Revision for linear equations, projection, and linear regression `
- `Because it’s taking time, does not mean it’s not `
- the button label `Add Task `

**Callout text:** the Week 04 callout ends at "…does not mean it’s not " in the source itself. It is not cut off by the extraction.

**Day labels:** each one has leading spaces and a different number of spaces around ✦. Exact strings are in `CONTENT.md` and `content.json`.

**Curly apostrophes:** the Week 03 and Week 04 callouts use ’ (U+2019).

**Formatting:**
- Bold: week titles, day labels, callout texts
- Teal background highlight on the date quote
- Red text on `this day is the deadline` (Week 04 · Saturday) and `The date of the EXAM` (Week 05 · Saturday)

**Day label colors:**
| Day | Color |
|---|---|
| Sunday | brown_background |
| Monday | yellow_background |
| Tuesday | teal_background |
| Wednesday | teal_background |
| Thursday | orange_background |
| Friday | brown_background |
| Saturday | red_background |

**Callouts:** all 4 use gray_background.

## 6. Missing, inaccessible or partial

| Item | Status | Why / what is needed |
|---|---|---|
| Image files (8): IMG_8055.png (icon), IMG_8056.png (cover), IMG_8104.PNG, IMG_8113.PNG, IMG_8115.PNG, IMG_8114.PNG, الشخصيتان_بدون_خلفية.png, IMG_8108.PNG | **Metadata only.** Name, size, display width, aspect ratio and position are saved, but the files are not | Notion serves them through a cross-origin redirect that blocks downloading. **Needs the user to export or send the 8 image files.** |
| Size of icon and cover images | Unknown | Notion does not expose a size for page icon or cover |
| Page comments, discussions, version history | Not checked | Not visible on a public notion.site link |
| Notion built-in icon artwork (5 icons) | Not copied | These are Notion's own icons, not user content. Only their names are recorded. |
| Text, structure, formatting, colors, buttons | **Complete** | Verified with a hash match |

## 7. Files in this backup

| File | What it is |
|---|---|
| `notion_tree.json` | Exact block tree as returned by Notion: IDs, raw rich-text arrays and formats (hash-verified) |
| `content.json` | The same content reorganized as page → weeks → columns → days → to-dos, plus images, callouts and footer. Every text keeps its raw Notion form too. |
| `CONTENT.md` | Human-readable verbatim copy. Spaces are shown as "·" next to each string. |
| `assets_manifest.json` | The 8 images with their Notion attachment IDs, sizes and locations |
| `AUDIT.md` | This report |

## 8. Known differences in the current prototype app (not changed yet)

The web app published earlier differs from the source in these ways. They are listed so they can be fixed during the build.

**Text:**
- `assessmen` was corrected to `assessment`
- `Ways  to` and `becomes   a lot` lost their extra spaces
- trailing spaces were trimmed

**Formatting:**
- the red highlights are missing
- callout icons are emoji instead of Notion icons
- the button says "＋ إضافة مهمة" instead of `Add Task `

**Layout:**
- days are shown in date order instead of Notion's 4-column order
- the images are missing
