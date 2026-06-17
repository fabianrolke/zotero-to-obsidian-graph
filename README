# Zotero Markdown Exporter for Obsidian (Annotator)

## Overview

This script extracts data from your Zotero SQLite database (`zotero.sqlite`) and converts it into Markdown files with linked terms based on a custom vocabulary. It is compatible with the Obsidian Annotator plugin.

https://github.com/fabianrolke/zotero-to-obsidian-graph/blob/main/demo.mp4

## Workflow

You:
1. Set the path to your `zotero.sqlite` file and the desired `output_folder` in `variables.py`

The script:
1. Connects to `zotero.sqlite`
2. Queries:
   - Publication titles
   - Highlighted text
   - Comment text
3. Matches results against terms defined in `termList.py`
   - The number of variants per tag controls graph density (more variants → denser graph)
4. Wraps matched terms in Obsidian-style links  
   (processing may take up to ~1 minute for ~100 publications, since titles, highlights, and comments are matched against all terms)
5. Writes one Markdown file per attachment into the output folder

## File Structure

- `markdownFileMaker.py` – Main script that generates Markdown output files
- `zoteroDataFetcher.py` – Handles SQLite querying and extraction from Zotero
- `termList.py` – Defines keyword/term mappings used for linking
- `variables.py` – Stores configuration paths (Zotero DB, output directory)

## Output

- Markdown files (`.md`) formatted for Obsidian
- Files follow the Annotator plugin format, enabling PDF viewing and annotation inside Obsidian
  - Zotero-originated comments are not yet displayed inside the PDF preview (see limitations)
- Automatic term linking:
  `Here is a term [[Term]] in an example sentence.`

## Current Limitations

- No live sync or plugin-style integration with Obsidian
  - Currently, all items are re-exported on each run
  - Incremental export (only new Zotero items) would prevent overwriting edited Markdown files
- All output files are written into a single flat folder (no hierarchy by author, year, or collection)
- PDF annotation mapping is incomplete:
  - Zotero uses rectangular highlight regions
  - Obsidian Annotator requires start/end text offsets
  - Current implementation does not map highlights to exact PDF text positions
  - Possible future approach:
    - Match highlighted text against extracted PDF text
    - Derive character start/end indices for true inline annotation mapping

## Requirements

- Python 3.9+
- No external dependencies required (standard library only unless extended modules are added)

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy...
(full MIT License applies)