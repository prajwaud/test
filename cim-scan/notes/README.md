# Note store

One markdown file per scanned CIM that cleared the note gate (tier >= 2, or tier <= 1
with portfolio relevance). Format and frontmatter schema: `../SCAN.md` step 3.

This is the accumulation layer the weekly digest reads (spec section 4): notes accumulate
as CIMs land; the Friday digest is a collection of accumulated notes, not a batch job.

Naming: `YYYY-MM-DD_<codename-or-company-slug>.md` where the date is the document's
doc_date (filename-corrected if flagged).

Storage decision (spec section 16, question 1): the repo is the note store. Simplest
durable option - survives the week, queryable by date via filename, versioned, and
reviewable in diffs. Revisit only if a second writer (a non-repo process) ever needs to
append notes.
