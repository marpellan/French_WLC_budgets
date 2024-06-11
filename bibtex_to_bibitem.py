import bibtexparser

def format_author(authors):
    formatted_authors = []
    for author in authors.split(' and '):
        parts = author.split(', ')
        if len(parts) == 2:
            last_name = parts[0]
            first_names = parts[1].split()
            formatted_initials = ''.join([f'{name[0]}.' for name in first_names])
            formatted_authors.append(f'{last_name}, {formatted_initials}')
        else:
            formatted_authors.append(author)  # Leave as is if the format is unexpected
    return '; '.join(formatted_authors)

def format_reference(entry):
    try:
        authors = format_author(entry['author'])
        title = entry['title']
        year = entry.get('year', 'n.d.')  # Use 'n.d.' (no date) as default if year is missing
        doi = entry.get('doi', '')  # Include DOI if available
        url = entry.get('url', '')
        citation_key = entry['ID']

        if 'journal' in entry:
            journal = entry['journal']
            volume = entry.get('volume', '')
            pages = entry.get('pages', 'n.d.')  # Use 'n.d.' if pages are missing
            if volume and pages:
                return f"\\bibitem[{authors}({year})]{{{citation_key}}}\n{authors}. {title}. \\emph{{{journal}}} {year}, \\emph{{{volume}}}, {pages}. {format_doi_or_url(doi, url)}"
            elif volume:
                return f"\\bibitem[{authors}({year})]{{{citation_key}}}\n{authors}. {title}. \\emph{{{journal}}} {year}, \\emph{{{volume}}}. {format_doi_or_url(doi, url)}"
            else:
                return f"\\bibitem[{authors}({year})]{{{citation_key}}}\n{authors}. {title}. \\emph{{{journal}}} {year}. {format_doi_or_url(doi, url)}"
        elif 'institution' in entry:  # Assuming 'institution' field for technical reports
            institution = entry['institution']
            address = entry.get('address', '')
            report_number = entry.get('number', '')
            return f"\\bibitem[{authors}({year})]{{{citation_key}}}\n{authors}. {title}; {institution}: {address}, {year}. {report_number}. {format_doi_or_url(doi, url)}"
        else:
            return f"\\bibitem[{authors}({year})]{{{citation_key}}}\n{authors}. {title}. {year}. {format_doi_or_url(doi, url)}"
    except KeyError as e:
        print(f"Missing required field {e} in entry {entry['ID']}")
        return None

def format_doi_or_url(doi, url):
    if doi:
        return f"\\href{{https://doi.org/{doi}}}{{https://doi.org/{doi}}}"
    elif url:
        return f"\\href{{{url}}}{{{url}}}"
    else:
        return ""

def main():
    with open('ipcc_reference.bib', 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)

    formatted_references = []
    for i, entry in enumerate(bib_database.entries, 1):
        formatted_ref = format_reference(entry)
        if formatted_ref:
            formatted_references.append(f"%Reference {i}\n{formatted_ref}")

    references_content = "\\begin{thebibliography}{999}\n"
    references_content += "\n\n".join(formatted_references)
    references_content += "\n\\end{thebibliography}"

    with open('formatted_references_ipcc.tex', 'w', encoding='utf-8') as outfile:
        outfile.write(references_content)

    print("Formatted references have been written to formatted_references.tex")

if __name__ == "__main__":
    main()
