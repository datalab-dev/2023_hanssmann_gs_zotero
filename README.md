<!--
DataLab Project Template

Replace allcaps text with your project details. PROJECT_NAME should be your
project's short name.

On GitHub, name the project repository according to the following format:

YEAR_COLLABORATOR_PROJECT_NAME

The project's Google Drive directory should also follow this format.

In the listing of directories, delete anything that isn't relevant to your
project.
-->

# FJHC Gender Studies Zotero Project

This repository contains code for the Feminist Health Justice Collective's Zotero project. The
project involves migrating citation data for health resources from a Notion database to a Zotero 
database for management and storage. Once this is complete, FHJC will be able to add data to their
database using Zotero's browser plugins, and will have an easy way to export their data for backup.

Links:

* [Google Drive][google]
* [Meeting Notes][meeting]
* [Notion-Zotero Documentation][docs]
* [Zotero Database][zotero_db]
* [FHJC Website][fhjc]
* [BibLatex][bibtex]

[google]: https://drive.google.com/drive/folders/1M7pJgameInSk76bCYVXtMFXs0orcbB0N
[meeting]: https://docs.google.com/document/d/1pKjNsDqv-b0AZuQaIt6QKViyeDv0skGOBL2rFsALok0
[docs]: https://docs.google.com/document/d/1_DqvkqctqpUFcQPRD5KfqOlEobT_hj-m-mGbFdALN9o
[zotero_db]: https://www.zotero.org/groups/5178293/feministhealthjusticecollective/library
[fhjc]: https://www.feministhealthjustice.com/
[bibtex]: https://mirrors.ibiblio.org/CTAN/macros/latex/contrib/biblatex/doc/biblatex.pdf



## File and Directory Structure

The directory structure for the project is:

```
README.md
data/         Data sets (files > 1MB go on Google Drive)
src/          python code
```

## Process Notion CSV Export

“Resource Name” Column is the key. It will be the title in the Zotero database

1. Export data from Notion database as CSV (make note of the date this was done)
2. Split Structural Framework by comma
3. Determine Item Type based on Resource Type (primer will have to be collapsed)
4. Extract Author list from Authors column
5. Get URL from Links column
6. Get tags list from Topics Column
7. Parse out Full Citation to extract (as available):
    * Date and Year
    * Journal, volume and issue
    * Series Name
    * Publisher
    * Editor
    * Location/Place
9. Create a BibLatex entry for each resource using the data you previously extracted
   * Tags should include all of the Resource’s topics as well as “notion”
   * Create a list of resources for each Structural Framework
10. Write a .bib file for each Structural Framework containing the BibLatex entries for each resource in that framework.


<!--
The files in the `data/` directory are:

```

```
-->
