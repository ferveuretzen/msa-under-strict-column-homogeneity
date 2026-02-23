# SCH-MSA: Strict Column Homogeneity Multiple Sequence Alignment

A versatile Multiple Sequence Alignment (MSA) tool designed for discovering **100% conserved patterns** across diverse data types.

## Overview

This tool provides a **generic engine** for Strict Column Homogeneity, capable of aligning any data structured as a Python `list`. Rather than focusing on a specific field, it serves as a multipurpose framework where the user defines the "equality" of elements.

To demonstrate its versatility, this repository includes examples across various domains:

- **Genomics:** Identifying evolutionary "bottlenecks" in BAliBASE sequences.
- **NLP:** Analyzing textual consistency across different Bible versions.
- **Neural Networks:** Aligning 100+ layers of ResNet variants to detect structural evolution.

## Key Features

- **Data Agnostic:** Works with strings, integers, function objects, or Neural Network layers.
- **Customizable Comparison:** Inject your own logic via `compfunc` (similar to Python's `sort(key=...)`).
- **Numpy-Powered:** Leveraging `np.frompyfunc` for high-performance matrix operations.
- **Rich Visualization:** Generates side-by-side comparison reports with index alignment.

## How it Works

The core of this tool is a flexible MSA engine that prioritizes **Strict Column Homogeneity**.
It identifies invariant columns across multiple sequences based on user-defined equality.

### 1. Abstract List Representation
The engine treats any input as a `List[Any]`. This abstraction allows the same logic to align diverse data types:
- **Genomics:** A list of characters `["A", "C", "G", "T"]`.
- **NLP:** A list of word tokens `["God", "said", ",", "Let", "there", "be", "light"]`.
- **Deep Learning:** A list of `torch.nn.Module` objects (layers).

### 2. Customizable Comparison (`compfunc`)
You can inject custom comparison logic using the `compfunc` parameter, similar to Python's `sort(key=...)`.
- **Identity-based:** `lambda a, b: a == b` (Default)
- **Normalized:** Compare text tokens regardless of case (e.g., `.casefold()`).
- **Attribute-based:** Compare Neural Network layers by their parameters (e.g., `out_channels`).

### 3. Numpy-Powered Matrix Computation
To ensure performance even with deep models like ResNet-101 (200+ layers), the tool leverages **NumPy's vectorization**:
- It uses `np.frompyfunc` to lift your custom `compfunc` into a NumPy universal function (ufunc).
- High-speed outer product operations generate the alignment matrix efficiently.

## Benchmarking with Various Datasets

This tool is agnostic to the input data type. You can test it with:

- **Genomics:** BAliBASE 3.0 (https://www.lbgi.fr/balibase)
- **NLP:** Comparing different Bible versions [bc-abe/plain-test-bibles](https://github.com)
- **Neural Networks:** Resnet variants

To run the Genomics comparison:
1. Download the *.tfa files from (https://www.lbgi.fr/balibase)
2. Place them in your `data/BAliBASE3/bb3_release` directory with their original directory structure
3. Run `python examples/align_balibase3.py`
4. Check `examples/aligned_balibase3.out`

To run the Bible comparison: 
1. Download the text files from [bc-abe/plain-text-bibles](https://github.com).
2. Place them in your `data/plain-text-bibles/{kjv-bible-md/, web-bible-md/}` directories.
3. Run `python examples/align_bibles.py`
4. Check `examples/{filename.out}`

To run the ResNet comparison:
1. Install torchivision
2. Run `python examples/align_resnet.py`
3. Check `examples/aligned_resnet_by_{name, parameters}.out`