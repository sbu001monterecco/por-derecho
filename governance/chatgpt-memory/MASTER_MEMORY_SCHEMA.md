# PD-MEM-001 schema

Every durable memory proposition should resolve, where applicable, to: `id | category | proposition | evidence/status class | privacy | importance(P0-P3) | source/control | supersedes | dependencies | revalidation rule | compact projection`.

Priority: P0 must survive Settings compression; P1 should survive if space permits; P2 is retrieved from the master when needed; P3 is volatile and must be revalidated live rather than trusted from memory.
