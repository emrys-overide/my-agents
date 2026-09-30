# Production readiness plan (2026-09-30)

## Estimate
**35% ready** (rough engineering judgment, not a measured completion metric). A working FastAPI UI and tests exist, but deployment, data durability, truthful fallback behavior, and access control are incomplete.

## Evidence
- `src/server.py` has public chat, engagement, ROI, and custom-agent mutation endpoints, with global in-memory state.
- When the LLM is unavailable, chat returns made-up ROI, architecture, coverage, and security scores as if measured.
- No dependency manifest, deployment config, CI workflow, auth, rate limits, or persistent engagement store appears in the default-branch tree.

## Execute on this branch
1. Replace fabricated fallback answers with an explicit service-unavailable response. **Immediate priority.**
2. Add a reproducible dependency manifest and CI job for existing tests.
3. Add API authentication and per-client rate limits before any public deployment.
4. Persist engagements and custom-agent definitions in an audited datastore with retention rules.
5. Validate bounded request fields and sanitize error responses; run threat and load tests.
6. Remove unsupported Deloitte branding/claims unless licensing and evidence are established.

## Production gate
Run all tests in CI; demonstrate auth and tenant isolation; verify output claims against artifacts; publish a deployment/runbook and backup/restore procedure. No public deployment until these gates pass.
