# Photograph intake

`pending/` — a batch dropped here by the upload page starts the intake
workflow (`.github/workflows/intake.yml`). It fetches the photographs, shrinks
them into `hyp/assets/img/`, geocodes the place once, and appends the entries
to `build/uploads.json`, which the map reads.

`done/` — batches already processed, kept as a record of what arrived when.

Nothing here is served: the site never reads these files at runtime.
