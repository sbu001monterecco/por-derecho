# RICPE original-PDF entrypoint repair

The first browser artifact passed the two core RICPE routes and two documentary-accountability routes, then stopped at the board/shareholder perimeter. Direct source inspection identified that both perimeter pages and the shared evidence reader have no site.js loader. A global loader addition alone cannot enhance those three standalone pages.

The repair adds only a direct, deferred reference to the scoped module on those three pages. Their pre-existing HTML is checked against the baseline after removing precisely that one script. It does not load the entire unrelated runtime into standalone readers. The original/redacted source assets remain unchanged. This supersedes the earlier assumption that every target already inherited site.js.

The browser harness also isolates each page/width in a fresh process and records crash diagnostics. No missed route is waived or counted as passing. The new source entrypoint gate must run alongside the 19-route browser and all prior checks. The original source-stage manifest remains REMOTE_SOURCE until actual controller and live verification receipts establish otherwise.
