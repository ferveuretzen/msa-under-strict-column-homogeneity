## Benchmarking with Various Datasets

This tool is agnostic to the input data type. You can test it with:

- **Genomics:** BAliBASE 3.0 (https://www.lbgi.fr/balibase)
- **NLP:** Comparing different Bible versions [bc-abe/plain-test-bibles](https://github.com)
- **Source Code:** [Project CodeNet](https://github.com)

To run the Genomics comparison:
1. Download the *.tfa files from (https://www.lbgi.fr/balibase)
2. Place them in your `data/BAliBASE3/bb3_release` directory with their original directory structure
3. Run `python examples/align_balibase3.py`
4. Check `examples/aligned_balibase3.out`

To run the Bible comparison: 
1. Download the text files from [bc-abe/plain-text-bibles](https://github.com).
2. Place them in your `data/plain-text-bibles/{kjv-bible-md/, web-bible-md/}` directories.
3. Run `python examples/align_bibles.py`
4. Check alined outputs on `examples/{filename.out}`