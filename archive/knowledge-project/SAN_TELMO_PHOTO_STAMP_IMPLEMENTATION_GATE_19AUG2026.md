# Corrected San Telmo photo stamp — implementation gate

The corrected visual may move to `READY` only when all of the following are true:

- Eduardo Sánchez's user-authorized image is imported and byte-locked.
- The user-authorized Sun Park image is imported and byte-locked as a distinct variant.
- Borja's existing canonical repository image remains unchanged in the AC slot.
- The composite slot map resolves left = Eduardo, centre = Sun Park, right = Borja.
- The shared San Telmo/RICPE component renders the correct images and the exact lead statement.
- The visual-asset validator and publication-integrity gate pass.
- Temporary base64 staging files and one-time import workflows are removed before merge.

The prior incorrect generated draft remains rejected and may not be reused.
