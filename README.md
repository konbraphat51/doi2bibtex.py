# BibTeX Creator Module

A Python module for fetching academic paper data from the CrossRef API using DOIs and converting them to BibTeX format.

## Features

- Fetch paper metadata from CrossRef API using DOIs
- Convert CrossRef data to properly formatted BibTeX entries
- Handle different publication types (articles, conference papers, books)
- Respectful API usage with configurable delays
- Batch processing of multiple DOIs
- Comprehensive error handling and logging

## Installation

The module requires the following dependencies (already included in pyproject.toml):

```
bibtexparser>=1.4.3
requests>=2.32.4
```

## Usage

### Quick Start

```python
from bibtex_creator import create_bibtex_from_dois

# List of DOIs to process
dois = [
    "10.1145/3411764.3445648",
    "10.1016/j.ijhcs.2021.102899"
]

# Create BibTeX entries
bibtex_entries = create_bibtex_from_dois(
    dois=dois,
    email="your.email@example.com",  # Optional but recommended
    key_prefix="ref",
    delay=1.0  # Delay between API requests
)

# Save to file
with open("bibliography.bib", "w", encoding="utf-8") as f:
    for entry in bibtex_entries:
        f.write(entry)
        f.write("\n")
```

### Advanced Usage

```python
from bibtex_creator import BibtexCreator

# Create instance with custom settings
creator = BibtexCreator(
    email="your.email@example.com",
    delay=0.5
)

# Fetch individual paper data
paper_data = creator.fetch_paper_data("10.1145/3411764.3445648")

# Convert to BibTeX entry
if paper_data:
    entry = creator.crossref_to_bibtex_entry(paper_data, "custom_key")
    print(f"Title: {entry.get('title', 'Unknown')}")
    print(f"Authors: {entry.get('author', 'Unknown')}")
```

## API Reference

### `create_bibtex_from_dois(dois, email=None, key_prefix="ref", delay=1.0)`

Convenience function to create BibTeX entries from a list of DOIs.

**Parameters:**

- `dois` (List[str]): List of DOIs to fetch and convert
- `email` (Optional[str]): Email address for CrossRef API (recommended for better rate limits)
- `key_prefix` (str): Prefix for BibTeX entry keys (default: "ref")
- `delay` (float): Delay between API requests in seconds (default: 1.0)

**Returns:**

- `List[str]`: List of BibTeX entries as strings

### `BibtexCreator` Class

#### `__init__(email=None, delay=1.0)`

Initialize the BibtexCreator.

**Parameters:**

- `email` (Optional[str]): Email address for CrossRef API
- `delay` (float): Delay between API requests in seconds

#### `fetch_paper_data(doi)`

Fetch paper data from CrossRef API using DOI.

**Parameters:**

- `doi` (str): The DOI of the paper to fetch

**Returns:**

- `Optional[Dict]`: Paper data from CrossRef API, or None if failed

#### `crossref_to_bibtex_entry(paper_data, entry_key)`

Convert CrossRef paper data to BibTeX entry format.

**Parameters:**

- `paper_data` (Dict): Paper data from CrossRef API
- `entry_key` (str): BibTeX entry key

**Returns:**

- `Dict`: BibTeX entry dictionary

#### `create_bibtex_from_dois(dois, key_prefix="ref")`

Create BibTeX entries from a list of DOIs.

**Parameters:**

- `dois` (List[str]): List of DOIs to fetch and convert
- `key_prefix` (str): Prefix for BibTeX entry keys

**Returns:**

- `List[str]`: List of BibTeX entries as strings

## Supported Fields

The module maps CrossRef data to the following BibTeX fields:

- `title`: Paper title
- `author`: Authors (formatted as "Last, First and Last2, First2")
- `journal`: Journal name (for articles)
- `booktitle`: Conference/proceedings name (for conference papers)
- `year`: Publication year
- `volume`: Volume number
- `number`: Issue number
- `pages`: Page range
- `doi`: DOI
- `url`: URL
- `abstract`: Abstract
- `publisher`: Publisher
- `issn`: ISSN

## Publication Types

The module automatically detects and handles different publication types:

- **Articles**: Journal papers (`@article`)
- **Conference Papers**: Conference proceedings (`@inproceedings`)
- **Books**: Book publications (`@book`)

## Error Handling

The module includes comprehensive error handling:

- Network errors are caught and logged
- Invalid DOIs are skipped with warnings
- Missing data fields are handled gracefully
- API rate limiting is respected with configurable delays

## Best Practices

1. **Provide an email address**: This helps with CrossRef API rate limits
2. **Use appropriate delays**: Don't overwhelm the API (1+ second delays recommended)
3. **Handle errors**: Check return values for None/empty results
4. **Validate DOIs**: Ensure DOIs are properly formatted before processing

## Examples

See `example_bibtex_usage.py` for comprehensive usage examples including:

- Basic usage with the convenience function
- Advanced usage with the BibtexCreator class
- Batch processing DOIs from a file
- Saving results to BibTeX files

## Dependencies

- `requests`: For HTTP requests to CrossRef API
- `bibtexparser`: For BibTeX formatting and writing
- `typing`: For type hints (built-in)
- `time`: For rate limiting (built-in)
- `logging`: For error logging (built-in)
