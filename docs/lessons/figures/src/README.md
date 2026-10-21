# Reproducing the lesson figures

Run commands from the repository root unless an absolute script path is used. Python 3, NumPy and matplotlib are already available in the working environment. Nothing was installed. `-B` avoids bytecode caches; the temporary matplotlib cache can be selected with `MPLCONFIGDIR=/tmp/v1a-mpl` when the default cache is not writable.

## Numerical charts

```sh
python3 -B docs/lessons/figures/src/lesson_charts.py all
```

Use `00`, `01`, `02`, `04`, `05`, `06`, `07` or `08` instead of `all` to regenerate only that lesson's charts. The script produces **16 charts**. Each figure identifies numerical assumptions, units and evidence limits. Source values are pinned in [FACTCHECK_LOG](../../FACTCHECK_LOG.md) and [VISUAL_REBUILD_LOG](../../VISUAL_REBUILD_LOG.md).

The pilot's six numerical fault/margin charts are produced by:

```sh
python3 -B docs/lessons/figures/src/make_figures.py
```

`fault_model.py` is reused from the pilot, not replaced with a newly invented fault model. Its trajectories omit harness/ESR and use constant L/C; before protection acts, its convention omits protected capacitance and load current. A commanded source cutoff at 10 µs is an **assumption**, not a designed autonomous trigger. Do not interpret favorable curves as physical validation. Lesson 03 and its model/chart sources are reserved for Claude during this resume and are left unchanged.

## Exact circuit excerpts

The owner's final feedback explicitly permits code for simple exact schematic excerpts. These scripts draw captured subsets of the review PDF; they do not draw analogies, realistic scenes or a new PCB. The common helper is `circuit_drawing.py`.

| Script | Output in `docs/lessons/figures/` | Captured subset |
|---|---|---|
| `circuit_00.py` | `v2-00-circuit-boundary.png` | R401 force path, upstream U402 supply branch, J502 |
| `circuit_01.py` | `v2-01-circuit-dividers.png` | UVLO/OVP dividers and U101 input-pin endpoints |
| `circuit_02.py` | `v2-02-circuit-feedback.png` | R202/R203 DC feedback branch and U201 FB |
| `circuit_04.py` | `v2-04-circuit-sense-filter.png` | Kelvin filter and separate VBUS tap |
| `circuit_05.py` | `v2-05-circuit-connectors.png` | J502 and J503 logical pin connections |
| `circuit_06.py` | `v2-06-circuit-bypass.png` | C203/C204 and both U201 VIN/PGND pairs |
| `circuit_07.py` | `v2-07-circuit-test-nets.png` | TP501–TP504 voltage-test nets |
| `circuit_08.py` | `v2-08-circuit-input-boundary.png` | J501, F101 and C101 boundary |

Run an individual script, for example:

```sh
python3 -B docs/lessons/figures/src/circuit_04.py
```

Each output names its source page, omissions and teaching-only status. Each has a companion ChatGPT image prompt in [BATCH_F](../../../illustrations/BATCH_F.md). The prompt filenames intentionally differ from the `v2-` code outputs; the owner can generate a companion without overwriting the exact excerpt. These scripts require **no schemdraw installation**.

## PDF renders and owner artwork

`v2-review-p01.png`, `p02`, `p03`, `p05` and `p06` are unchanged page renders of the [review PDF](/Users/quockaiser/Desktop/Research/V1A_review_2026-09-29/V1A_REVIEW_READABLE.pdf). They are source reading aids, not matplotlib drawings or annotated figures. All six PDF pages were inspected; page 4 belongs to the reserved Lesson 03 work.

`export_review_pages.m` uses macOS PDFKit/AppKit. To reproduce the source exports into a temporary directory:

```sh
clang -fobjc-arc -framework Foundation -framework PDFKit -framework AppKit docs/lessons/figures/src/export_review_pages.m -o /tmp/v1a-export-review
/tmp/v1a-export-review /Users/quockaiser/Desktop/Research/V1A_review_2026-09-29/V1A_REVIEW_READABLE.pdf /tmp/v1a-lesson-review
```

The output is `page-1.png` through `page-6.png` plus extracted `pages.txt`. Only intentionally selected page PNGs are copied into this lesson folder; the temporary executable and extracted text are not repository artifacts.

Analogy, 3D and concept pictures continue to use exact filename embeds from the owner's read-only `V1A-Lessons/images/`. Generate new companions with the [BATCH_F prompts](../../../illustrations/BATCH_F.md), preserving those filenames. No owner image was changed or overwritten; no annotated image was needed for this continuation because the unchanged PDF, exact excerpt and adjacent pin walkthrough supply the reading guidance.

**Separate Lesson 03 handoff:** `docs/lessons/code/draw_sheet03_simplified.py` predates this resume and targets `docs/lessons/images/p03-12-simplified-circuit.png`. That image is not present here, and schemdraw is not installed. The lesson-03 owner must reconcile its output path/dependency; this reserved script and its lesson are untouched. The other lessons' new figures are ready and reproducible without it.
