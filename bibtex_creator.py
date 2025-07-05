"""
BibTeX Creator Module

This module provides functionality to fetch paper data from CrossRef API using DOIs
and convert them to BibTeX format.
"""

import requests
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from typing import List, Dict, Optional
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BibtexCreator:
    """
    A class to handle fetching paper data from CrossRef API and converting to BibTeX format.
    """
    
    def __init__(self, email: Optional[str] = None, delay: float = 1.0):
        """
        Initialize the BibtexCreator.
        
        Args:
            email (Optional[str]): Email address for CrossRef API (recommended for better rate limits)
            delay (float): Delay between API requests in seconds (default: 1.0)
        """
        self.base_url = "https://api.crossref.org/works/"
        self.email = email
        self.delay = delay
        self.session = requests.Session()
        
        # Set up headers for better API access
        headers = {
            'User-Agent': 'BibtexCreator/1.0 (https://github.com/user/repo; mailto:user@example.com)'
        }
        if email:
            headers['User-Agent'] = f'BibtexCreator/1.0 (mailto:{email})'
        
        self.session.headers.update(headers)
    
    def fetch_paper_data(self, doi: str) -> Optional[Dict]:
        """
        Fetch paper data from CrossRef API using DOI.
        
        Args:
            doi (str): The DOI of the paper to fetch
            
        Returns:
            Optional[Dict]: Paper data from CrossRef API, or None if failed
        """
        try:
            # Remove DOI prefix if present
            clean_doi = doi.replace('https://doi.org/', '').replace('http://doi.org/', '')
            
            url = f"{self.base_url}{clean_doi}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('message', {})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for DOI {doi}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for DOI {doi}: {e}")
            return None
    
    def crossref_to_bibtex_entry(self, paper_data: Dict, entry_key: str) -> Dict:
        """
        Convert CrossRef paper data to BibTeX entry format.
        
        Args:
            paper_data (Dict): Paper data from CrossRef API
            entry_key (str): BibTeX entry key
            
        Returns:
            Dict: BibTeX entry dictionary
        """
        entry = {
            'ID': entry_key,
            'ENTRYTYPE': 'article'  # Default to article, can be refined based on type
        }
        
        # Map CrossRef fields to BibTeX fields
        if 'title' in paper_data and paper_data['title']:
            entry['title'] = paper_data['title'][0]
        
        if 'author' in paper_data:
            authors = []
            for author in paper_data['author']:
                if 'family' in author and 'given' in author:
                    authors.append(f"{author['family']}, {author['given']}")
                elif 'family' in author:
                    authors.append(author['family'])
                elif 'name' in author:
                    authors.append(author['name'])
            if authors:
                entry['author'] = ' and '.join(authors)
        
        if 'container-title' in paper_data and paper_data['container-title']:
            entry['journal'] = paper_data['container-title'][0]
        
        if 'published-print' in paper_data:
            date_parts = paper_data['published-print'].get('date-parts', [[]])[0]
            if date_parts:
                entry['year'] = str(date_parts[0])
        elif 'published-online' in paper_data:
            date_parts = paper_data['published-online'].get('date-parts', [[]])[0]
            if date_parts:
                entry['year'] = str(date_parts[0])
        
        if 'volume' in paper_data:
            entry['volume'] = str(paper_data['volume'])
        
        if 'issue' in paper_data:
            entry['number'] = str(paper_data['issue'])
        
        if 'page' in paper_data:
            entry['pages'] = str(paper_data['page'])
        
        if 'DOI' in paper_data:
            entry['doi'] = paper_data['DOI']
        
        if 'URL' in paper_data:
            entry['url'] = paper_data['URL']
        
        if 'abstract' in paper_data:
            entry['abstract'] = paper_data['abstract']
        
        if 'publisher' in paper_data:
            entry['publisher'] = paper_data['publisher']
        
        if 'ISSN' in paper_data and paper_data['ISSN']:
            entry['issn'] = paper_data['ISSN'][0]
        
        # Handle different publication types
        if 'type' in paper_data:
            pub_type = paper_data['type'].lower()
            if 'conference' in pub_type or 'proceedings' in pub_type:
                entry['ENTRYTYPE'] = 'inproceedings'
                if 'container-title' in paper_data and paper_data['container-title']:
                    entry['booktitle'] = paper_data['container-title'][0]
                    # Remove journal field for proceedings
                    if 'journal' in entry:
                        del entry['journal']
            elif 'book' in pub_type:
                entry['ENTRYTYPE'] = 'book'
                if 'journal' in entry:
                    del entry['journal']
        
        return entry
    
    def create_bibtex_from_dois(self, dois: List[str], key_prefix: str = "ref") -> List[str]:
        """
        Create BibTeX entries from a list of DOIs.
        
        Args:
            dois (List[str]): List of DOIs to fetch and convert
            key_prefix (str): Prefix for BibTeX entry keys (default: "ref")
            
        Returns:
            List[str]: List of BibTeX entries as strings
        """
        bibtex_entries = []
        
        for i, doi in enumerate(dois):
            if not doi or not doi.strip():
                logger.warning(f"Empty DOI at index {i}, skipping")
                continue
                
            logger.info(f"Fetching data for DOI: {doi}")
            
            # Fetch paper data
            paper_data = self.fetch_paper_data(doi)
            if not paper_data:
                logger.warning(f"Could not fetch data for DOI: {doi}")
                continue
            
            # Create BibTeX entry
            entry_key = f"{key_prefix}{i+1:03d}"
            bibtex_entry = self.crossref_to_bibtex_entry(paper_data, entry_key)
            
            # Convert to BibTeX string
            db = BibDatabase()
            db.entries = [bibtex_entry]
            
            writer = BibTexWriter()
            writer.indent = '  '  # 2 spaces for indentation
            writer.align_values = True
            
            bibtex_string = writer.write(db)
            bibtex_entries.append(bibtex_string)
            
            logger.info(f"Successfully converted DOI {doi} to BibTeX")
            
            # Add delay between requests to be respectful to the API
            if i < len(dois) - 1:  # Don't delay after the last request
                time.sleep(self.delay)
        
        return bibtex_entries


def create_bibtex_from_dois(dois: List[str], email: Optional[str] = None, 
                           key_prefix: str = "ref", delay: float = 1.0) -> List[str]:
    """
    Convenience function to create BibTeX entries from DOIs.
    
    Args:
        dois (List[str]): List of DOIs to fetch and convert
        email (Optional[str]): Email address for CrossRef API (recommended)
        key_prefix (str): Prefix for BibTeX entry keys (default: "ref")
        delay (float): Delay between API requests in seconds (default: 1.0)
        
    Returns:
        List[str]: List of BibTeX entries as strings
    """
    creator = BibtexCreator(email=email, delay=delay)
    return creator.create_bibtex_from_dois(dois, key_prefix)


if __name__ == "__main__":
    # Example usage
    sample_dois = [
        "10.1145/3411764.3445648",
        "10.1016/j.ijhcs.2021.102899"
    ]
    
    bibtex_entries = create_bibtex_from_dois(
        sample_dois, 
        email="your.email@example.com",  # Replace with your email
        key_prefix="example"
    )
    
    for entry in bibtex_entries:
        print(entry)
        print("-" * 50)
