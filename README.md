# OAS 0.1.0 – Oromotor Asymmetry Score Engine

> # DISCLAIMER: Current code is VERY early in production and is not the entirety of OAS

> **Version:** 0.1.0  |  **Status:** Research prototype (still under development - see updates.md)

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [How OAS Works](#how-oas-works)
4. [Installation](#installation)
5. [Quick Start](#quick-start)
6. [Directory Layout](#directory-layout)
7. [Configuration](#configuration)
8. [Outputs](#outputs)
9. [Benchmarks](#benchmarks)
10. [Contributing](#contributing)
11. [Citation](#citation)
12. [License](#license)
13. [Contact](#contact)

---

## Overview

OAS 1.0 is an open‑source Python engine that quantifies **oromotor asymmetry**—differences in left‑ vs. right‑side mouth kinematics—using 2‑D landmark data from **OpenFace**. 

**Why it matters**

* **Potential Early detection** of speech‑motor disorders.
* **Language‑agnostic:** relies on geometric asymmetry, not phonological content.
* **Reproducible:** every step from raw video → score is scripted and logged.

> **Clinical disclaimer:** OAS 1.0 is a *research tool* ONLY.
---

## Key Features

*  **Landmark ingestion** from OpenFace CSV output.
*  **Head‑pose correction** of yaw, pitch, and roll (yaw and pitch significantly increase uncertainty).
*  **OAS metric**: normalized distance‑difference of oral commissures relative to a centralised anchor.
*  **Batch pipeline**: process several 4 K @ 120 fps videos in parallel (very computationally heavy).
*  **Plug‑in hooks** for Action‑Unit filtering, VOT analysis, curve fitting.

---

## How OAS Works

1. **Video → Landmarks**  `OpenFace` extracts 68 facial landmarks per frame.
2. **Pre‑cleaning**  Bad frames (low confidence) are removed.
3. **Head‑pose Correction**  Landmarks are rotated so the inter‑pupil line is horizontal.
4. **Left / Right Distances**  Compute Euclidean distance from nose‑tip → each mouth corner.
5. **Score**  

   $$
   \text{OAS}(t) \,=\, \frac{|d_R(t)-d_L(t)|}{\bigl(d_R(t)+d_L(t)\bigr)}
   $$
6. **Aggregates**  Mean, SD, velocity & acceleration over the target utterance.

---

## Installation

### 1. Prerequisites

| Requirement     | Tested Version                       |
| --------------- | ------------------------------------ |
| Python          |  3.10 – 3.12                         |
| OpenFace        |  2.2.0                               |
| FFmpeg          |  6.1                                 |
| (Optional) CUDA |  11.8 for faster landmark extraction |

### 2. Clone the repo

```bash
git clone https://github.com/Harry-S-W/OAS.git
cd OAS
```

### 3. Create a virtual env & install deps

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

*Or use the Conda environment file provided.*

### 4. Install OpenFace (if you haven’t)

Follow the [official OpenFace build guide](https://github.com/TadasBaltrusaitis/OpenFace).

---

## Quick Start

```bash
# 2 Run OAS engine
python cli.py \
  --mode init --file "test/folder/path.csv" --force

```

---

## Directory Layout

```text
coming soon
```

---

## Configuration

```
coming soon
```
---

## Outputs

```
coming soon
```

Aggregate stats are written to `output/summary.csv`.

---

## Benchmarks

| Hardware       | Data                 | Runtime                     |
| -------------- | -------------------- | --------------------------- |
| coming soon    | coming soon          | coming soon                 |

---

## Contributing

1. Fork → feature branch → pull request.
2. Run `pytest` and `ruff` before pushing.
3. For major changes, open an issue first to discuss scope.
4. By contributing you agree to license your work under Creative Commons Attribution 4.0 International.
---

## License

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)

---

