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
1. `dashboard/src/components/MediaInput.jsx`
   - Added a Gaming Mode selector under Advanced Options.
   - Choices: General videos, PUBG / BGMI gameplay, Minecraft gameplay.
   - Sends the selected profile with the upload request.
   - Shows the advanced-options indicator when a gaming profile is selected.
2. `dashboard/src/App.jsx`
   - Passes `gaming_mode` to the backend for both file and URL submissions.
3. `app.py`
   - Accepts `gaming_mode` in multipart form and JSON requests.
   - Whitelists values: `off`, `pubg`, `minecraft`.
   - Sets `AVEN_GAMING_MODE` only for an enabled profile and clears inherited profile values first so general-video jobs do not accidentally use a server-wide gaming setting.
4. `gaming_profiles.py`
   - Extracts gaming mode validation and prompt profiles into a small dependency-light module so they can be tested without importing the heavy video stack.
   - Rejects unsupported values and provides `off`, `pubg`, and `minecraft` profiles.
5. `main.py`
   - Uses the shared game-aware prompt guidance in transcript scoring, detailed clip selection, and silent-video visual selection.
   - PUBG/BGMI guidance favors genuine clutches, squad wipes, headshots, sprays, sniper shots, final-circle plays, revives, escapes and funny failures; requires setup/payoff and forbids invented outcomes.
   - Minecraft guidance favors builds, redstone, discoveries, transformations, survival clutches, boss fights, speedruns, parkour, funny failures and secrets; forbids invented achievements/events.

## Important limitations / validation status
- The GitHub connector successfully wrote these files to the development branch.
- Added `tests/test_gaming_profiles.py` covering accepted modes, rejected values/aliases, general mode, PUBG and Minecraft prompt guidance, and environment normalization.
- Tests have NOT yet been executed in this session. The CI workflow now includes pushes to `aven-gaming-mode`, but GitHub currently reports zero workflow runs for this branch; verify Actions after the next push/PR.
- The project has NOT yet been built or run locally; frontend compilation, Python syntax/tests, and an end-to-end test with sample gaming footage are still required.
- Do not claim the app is deployed or production-ready.
- User's laptop has 8 GB RAM, so local AI inference may be slow; prefer a lightweight frontend test and consider remote/cloud inference for heavy video processing.

## Next work
1. Inspect the complete diff and run the project's available frontend and Python tests; confirm GitHub Actions starts on the development branch.
2. Run `pytest tests/test_gaming_profiles.py` and the full CI suite; fix any failures before adding more features.
3. Add a proper Gaming Mode UX (clear preset card, explain what it changes, retain user's last choice).
4. Test with one PUBG/BGMI recording and one Minecraft recording; verify clip selection is grounded in visible/audio evidence.
5. Continue branding the visible product as AVEN AI CLIPPER without removing upstream attribution or license notices.
6. Only after tests pass, prepare deployment instructions and ask the user for any required API keys/permissions.

## Working agreement
The assistant should make code changes directly on `aven-gaming-mode` where connector permissions allow, explain only when user action is required, and never say background work continues after the chat is closed.
