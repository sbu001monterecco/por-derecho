# Preservation authorization records

This directory is intentionally empty of authorization JSON until Gil Marer expressly authorizes a deletion, rename, route removal, first-read demotion or material replacement affecting a protected repository path.

An authorization record must be a JSON object with:

- `authorization_id`;
- `change_id`, unique to the proposed change;
- `base_sha`, the exact current `main` SHA from which the authorized change begins;
- `status` equal to `EXPLICIT_USER_AUTHORIZATION`;
- `authorized_by` equal to `Gil Marer`;
- `authorized_on`;
- `reason`; and
- `paths`, an array of exact old repository paths covered by the authorization.

The authorization JSON must be newly added in the same proposed change as the deletion or rename. Earlier authorization records cannot be reused. For a rename or replacement, the record should also identify the replacement path or redirect. A general request to improve, simplify, redesign or reorganize does not authorize deletion.
