# Embedded Engineering Skills 2.0 identity migration

The user authorized the name `embedded-engineering-skills` on 2026-10-15.
Display name remains **Embedded Engineering Skills**. This is a breaking plugin
namespace change; existing Arduino-specific skill names stay compatible.

## Verified remote and local state

- GitHub repository renamed to
  [wedsamuel1230/embedded-engineering-skills](https://github.com/wedsamuel1230/embedded-engineering-skills).
  PATCH acknowledgement and subsequent reads retain repository ID `1127657037`.
- The old web URL returns HTTP 301 to the new repository. Reading the old API
  endpoint returns the same ID and new full name. The main ref remains
  `d6e77bb2461a2126267e0e00b697b28abe0c0ea2`; existing history was not replaced.
- Local source directory is now `embedded-engineering-skills`; origin uses the
  new HTTPS Git URL. All four plugin manifests and three marketplace adapters
  use the new ID and 2.0.0 candidate version.
- Root `plugin.json` uses portable Agent Plugins 1.0 with OpenAI presentation in
  `extensions.com.openai`. The Codex overlay is synchronized. Logo fields remain
  bundled `interface.logo`/`interface.composerIcon`.

The 2.0 candidate is delivered through review branch
`codex/universal-embedded-skills`. Existing main/releases retain their prior
code until human review and merge; no 2.0 release tag or host cache upgrade is
part of this branch delivery.

## Existing installations

A GitHub redirect does not migrate plugin IDs, namespaces, manager locks, saved
local project paths or installed version caches. The current installed old-ID
cache is not edited as part of source authoring.

1. Record the old installed plugin/version/release for rollback.
2. Use the host's supported UI/CLI to disable/remove that old installation.
3. Register the new verified repository or this local source, then install
   `embedded-engineering-skills@embedded-engineering-skills` where that host uses
   marketplace-qualified names. Use its current CLI help for supported commands.
4. Check one harmless skill invocation and confirm only one copy of each skill
   is discovered. Re-add a saved local project path if it points at the old
   directory. Do not assume all hosts have identical update mechanics.

No protected global host configuration, install locks or installed caches were
rewritten. Host installation/discovery execution is separate from package
checks. Keep old immutable tags/releases available for rollback; do not create
a duplicate legacy plugin entry that implicitly loads the same skills twice.

Sources: [OpenAI package format](https://developers.openai.com/plugins/build/plugins),
[GitHub repository rename](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository),
[Claude plugin reference](https://code.claude.com/docs/en/plugins-reference).
