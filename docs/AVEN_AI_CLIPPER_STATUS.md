# AVEN AI CLIPPER — Development checkpoint

Last updated: 2026-11-27

## Repository
- GitHub repository: https://github.com/an897055/aven-ai-clipper
- Upstream base: https://github.com/mutonby/openshorts
- Active development branch: `aven-gaming-mode`
- Keep changes on this branch. Do not merge into `main` until the feature is tested.

## Product direction
Build a web-based AI clipping editor branded as AVEN AI CLIPPER, based on OpenShorts rather than rebuilding the existing application. Preserve upstream features and add creator-focused workflows, especially gaming clips for PUBG/BGMI and Minecraft.

## Implemented on `aven-gaming-mode`
1. `README.md`
   - Brands the fork as AVEN AI CLIPPER, documents PUBG/BGMI and Minecraft profiles as in-development features, and preserves clear upstream OpenShorts attribution.
2. `dashboard/src/components/MediaInput.jsx`
   - Added a Gaming Mode selector under Advanced Options.
   - Choices: General videos, PUBG / BGMI gameplay, Minecraft gameplay.
   - Sends the selected profile with the upload request.
   - Shows the advanced-options indicator when a gaming profile is selected.
3. `dashboard/src/App.jsx`
   - Passes `gaming_mode` to the backend for both file and URL submissions.
4. `app.py`
   - Accepts `gaming_mode` in multipart form and JSON requests.
   - Whitelists values: `off`, `pubg`, `minecraft`.
   - Validates the mode before creating the job directory or allocating processing resources.
   - Sets `AVEN_GAMING_MODE` only for an enabled profile and clears inherited profile values first so general-video jobs do not accidentally use a server-wide gaming setting.
   - Persists the selected profile in the resume manifest and restores it safely after an interrupted job; legacy/invalid manifests fall back to general mode.
5. `gaming_profiles.py`
   - Extracts gaming mode validation and prompt profiles into a small dependency-light module so they can be tested without importing the heavy video stack.
   - Rejects unsupported values and provides `off`, `pubg`, and `minecraft` profiles.
6. `main.py`
   - Uses the shared game-aware prompt guidance in transcript scoring, detailed clip selection, and silent-video visual selection.
   - PUBG/BGMI guidance favors genuine clutches, squad wipes, headshots, sprays, sniper shots, final-circle plays, revives, escapes and funny failures; requires setup/payoff and forbids invented outcomes.
   - Minecraft guidance favors builds, redstone, discoveries, transformations, survival clutches, boss fights, speedruns, parkour, funny failures and secrets; forbids invented achievements/events.

## Important limitations / validation status
- The GitHub connector successfully wrote these files to the development branch.
- Added `tests/test_gaming_profiles.py` covering accepted modes, rejected values/aliases, general mode, PUBG and Minecraft prompt guidance, environment normalization, and per-job environment isolation.
- Added `workflow_dispatch` so CI can also be started manually from GitHub Actions.
- Tests have NOT yet been executed in this session. A draft validation PR (#1) was opened from `aven-gaming-mode` to `main` to trigger pull-request CI without merging; it remains unmerged. GitHub still reports zero check runs/statuses, so confirm whether Actions is enabled for this fork.
- The project has NOT yet been built or run locally; frontend compilation, Python syntax/tests, and an end-to-end test with sample gaming footage are still required.
- Do not claim the app is deployed or production-ready.
- User's laptop has 8 GB RAM, so local AI inference may be slow; prefer a lightweight frontend test and consider remote/cloud inference for heavy video processing.

## Latest additional work
- Updated the README to present AVEN AI CLIPPER as the customized fork, explicitly label gaming profiles as in development, and retain upstream attribution.
- Added safe profile restoration for interrupted jobs: the selected mode is written into the resume manifest, restored on restart, and legacy/invalid manifests fall back to General.
- Moved gaming-mode validation ahead of job-directory creation so invalid API values fail with HTTP 400 before allocating job resources.
- Reviewed and simplified the new unit tests; no test execution has been performed.

## Next work
1. Inspect the complete diff and run the project's available frontend and Python tests; confirm GitHub Actions starts on the development branch.
2. Run `pytest tests/test_gaming_profiles.py` and the full CI suite; fix any failures before adding more features.
3. Verify that resumed jobs preserve PUBG/BGMI or Minecraft mode (implemented; automated tests added, execution pending).
4. Continue static review and add targeted tests for request validation and resume behavior where practical.
5. Test with one PUBG/BGMI recording and one Minecraft recording; verify clip selection is grounded in visible/audio evidence.
6. Continue branding the visible product as AVEN AI CLIPPER without removing upstream attribution or license notices.
7. Only after tests pass, prepare deployment instructions and ask the user for any required API keys/permissions.

## Working agreement
The assistant should make code changes directly on `aven-gaming-mode` where connector permissions allow, explain only when user action is required, and never say background work continues after the chat is closed.
