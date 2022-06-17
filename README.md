# Law Smells
Replication package for "Law Smells: Defining and Detecting Problematic Patterns in Legal Drafting" (Artificial Intelligence &amp; Law 2022)

## General

Below, we list the (derived) data and the code needed to reproduce our tables and figures.

For the file paths to match, the folder `us` is expected reside in the folder `../../legal-networks-data` (when viewed from the `notebooks` folder), and ZIP archives are expected to be unpacked.

The code is tested in a virtual environment with a Python 3.8 interpreter and the requirements from `requirements-dev.txt` installed via `pip install -r requirements-dev.txt`.

## Tables

- `table-duplicates`
  - data:
    - `../data/corpus_size_token_us.json` (created using `token_size_usc.ipynb`)
    - `../data/dupex_mf-10000_results_all-years.csv`
    - Dupex results (JSONs) with -mf 10000 for y in range(1998, 2020), examples for 2019 placed in `../dupex_mf-10000_results`
  - code:
    - Dupex code: [Zenodo Deposit](https://doi.org/10.5281/zenodo.5534329) 
    - `compute_compressions.py`
    - `dp_figures.ipynb` (uses smell_helpers.py)
- `table-long-elements`
  - data: `../../legal-networks-data/us/4_crossreference_graph`
  - code: longitem_analysis.ipynb (uses longitem_support.py), third code box under `Example 2` heading

## Figures

- `dp-compression`
  - data: see `table-duplicates`
  - code: see `table-duplicates`
- `longitem_icicles`
  - data: `../../legal-networks-data/us/4_crossreference_graph`
  - code: longitem_analysis.ipynb (uses longitem_support.py), under `Example 4`
    heading
- `operator_patterns_abs_us_splitted`
  - data:
    - `../../legal-networks-data/us/2_xml`
    - `../../legal-networks-data/us/4_crossreference_graph/detailed`
    - `../data/corpus_size_token_us.json`
    - `../data/pattern_abs.csv`
  - code:
    - `operational-binding.ipynb`
    - `operational-binding-analysis.ipynb`
- `operator_patterns_rel_us_splitted`
  - data: see previous figure
  - code: see previous figure
- `reference_tree_size_ref_edges_2dhist`
  - data:
    - `../../legal-networks-data/us/4_crossreference_graph/detailed`
    - `../data/reference_sets_{year}.csv`
  - code:
    - `reference-set.ipynb`
    - `lrt_figures.ipynb`
- `diverse-reference-tree`
  - data: input data only (traced manually)
  - code: none (traced manually)
- `named_entities_per_thousand_tokens`
  - data:
    - `../data/corpus_size_token_us.json`
    - `../ner_counts` data for 1998 and 2019
  - code:
    - `token_size_usc.ipynb`
    - `nlo_figures.ipynb`
    - `smell_helpers.py`
- `committees_per_thousand_tokens`
  - data: Dupex results (JSONs) with -mf 10000 for 2019, placed in `../dupex_mf-10000_results`
  - code: see previous figure
