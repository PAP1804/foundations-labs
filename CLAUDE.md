# Repo conventions

When a lab is marked complete:

1. In `weekN/README.md`, mark the day **done** under Progress and add a `## Day N` section with:
   - the run command (from the repo root, e.g. `python3 weekN/dayN.py`);
   - the actual output, copied from a real run;
   - a `### Takeaways` list: 3-5 concrete lessons tied to this data or code (gotchas found, why a choice was made), not generic summaries.
2. In the root `README.md`, set the day's status to Done and link the script. Add a new week section when a week starts.
3. Any new dataset gets a row in the root README's Data table (file, source, license, where used).

Scripts locate their data relative to their own file (`Path(__file__).parent`), so they run from any folder.
