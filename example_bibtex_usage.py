"""
Example usage script for bibtex_creator module
"""

from bibtex_creator import create_bibtex_from_dois, BibtexCreator

def example_usage():
    """
    Example of how to use the bibtex_creator module
    """
    
    # Example 1: Using the convenience function
    print("=== Example 1: Using convenience function ===")
    
    sample_dois = [
        "10.1145/3411764.3445648",  # CHI 2021 paper
        "10.1016/j.ijhcs.2021.102899"  # IJHCS paper
    ]
    
    bibtex_entries = create_bibtex_from_dois(
        dois=sample_dois,
        email="your.email@example.com",  # Replace with your email for better API access
        key_prefix="paper",
        delay=1.0  # 1 second delay between requests
    )
    
    print(f"Created {len(bibtex_entries)} BibTeX entries")
    
    # Save to file
    with open("example_bibliography.bib", "w", encoding="utf-8") as f:
        for entry in bibtex_entries:
            f.write(entry)
            f.write("\n")
    
    print("Saved to example_bibliography.bib")
    
    # Example 2: Using the class directly for more control
    print("\n=== Example 2: Using BibtexCreator class ===")
    
    creator = BibtexCreator(
        email="your.email@example.com",  # Replace with your email
        delay=0.5  # Shorter delay for faster processing
    )
    
    # Process single DOI
    single_doi = "10.1145/3411764.3445648"
    paper_data = creator.fetch_paper_data(single_doi)
    
    if paper_data:
        print(f"Successfully fetched: {paper_data.get('title', ['Unknown'])[0]}")
        
        # Convert to BibTeX
        entry = creator.crossref_to_bibtex_entry(paper_data, "custom_key")
        print(f"Entry type: {entry['ENTRYTYPE']}")
        print(f"Authors: {entry.get('author', 'Unknown')}")
        print(f"Year: {entry.get('year', 'Unknown')}")

def batch_process_dois_from_file():
    """
    Example of processing DOIs from a file
    """
    print("\n=== Example 3: Processing DOIs from file ===")
    
    # Create a sample DOI file
    sample_dois_text = """10.1145/3411764.3445648
10.1016/j.ijhcs.2021.102899
10.1145/3359996.3364706"""
    
    with open("sample_dois.txt", "w") as f:
        f.write(sample_dois_text)
    
    # Read DOIs from file
    with open("sample_dois.txt", "r") as f:
        dois = [line.strip() for line in f.readlines() if line.strip()]
    
    print(f"Processing {len(dois)} DOIs from file...")
    
    # Process all DOIs
    bibtex_entries = create_bibtex_from_dois(
        dois=dois,
        email="your.email@example.com",
        key_prefix="batch",
        delay=1.0
    )
    
    # Save results
    with open("batch_bibliography.bib", "w", encoding="utf-8") as f:
        for entry in bibtex_entries:
            f.write(entry)
            f.write("\n")
    
    print(f"Processed {len(bibtex_entries)} entries, saved to batch_bibliography.bib")

if __name__ == "__main__":
    example_usage()
    batch_process_dois_from_file()
