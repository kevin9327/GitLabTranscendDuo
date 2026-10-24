# AGENTS.md — GreenOps Transcend Duo (9-Stage Post-Code Autonomous DevSecOps & GreenOps Agent)

This repository is governed by **GreenOps Transcend Duo**, an ambient multi-stage GitLab Duo Agent Platform workflow defined in [`.gitlab/duo/flows/greenops-transcend-flow.yml`](.gitlab/duo/flows/greenops-transcend-flow.yml) and [`.gitlab/duo/agent-config.yml`](.gitlab/duo/agent-config.yml).

## Mandatory 9-Stage Post-Code DevSecOps Rules

1. **Stage 1 — `plan` (Carbon Budget & Issue Triage)**:
   - Compute baseline Software Carbon Intensity ($\text{SCI} = ((E \times I) + M) / R$) per ISO/IEC 21031:2024 before approving architectural scope.
2. **Stage 2 — `create` (Diff Audit & Green Refactoring)**:
   - Detect N+1 queries, unbounded polling loops, uncached LLM prefills, and oversized Docker base images (`python:3.11` -> `python:3.11-slim`).
3. **Stage 3 — `verify` (Deterministic Test & Regression Gate)**:
   - Run `pytest` unit/integration tests and verify zero regression before packaging.
4. **Stage 4 — `package` (OCI Layer Right-Sizing & GBOM)**:
   - Strip build-time caches (`--no-cache-dir`), compress OCI layers, and emit a cryptographic **Green Bill of Materials (`GBOM`)**.
5. **Stage 5 — `secure` (SAST, Secret Detection & Dependency Audit)**:
   - Block any commit containing hardcoded credentials (`glpat-`, `AIza`, `ghp_`, `clk_live_`) or critical CVEs.
6. **Stage 6 — `release` (Semantic Changelog & Immutable Artifact Tagging)**:
   - Generate signed release notes with before/after SCI delta metrics.
7. **Stage 7 — `configure` (Google Cloud Carbon-Free Energy Region Routing)**:
   - Route stateless Cloud Run / GKE workloads to the highest Carbon-Free Energy (`CFE%`) Google Cloud region meeting latency SLOs (`europe-north1` Finland at `94% CFE`, `42 gCO2eq/kWh`) with `min-instances: 0` scale-to-zero configuration.
8. **Stage 8 — `monitor` (Live SLO, FinOps & Carbon Telemetry)**:
   - Track p95 latency, CPU/memory throttling, Cloud Run cost, and real-time $\text{gCO}_2\text{eq}$ savings.
9. **Stage 9 — `govern` (SHA-256 Compliance & ISO/IEC 21031 Attestation)**:
   - Publish a tamper-evident SHA-256 governance certificate to the GitLab Merge Request / Pipeline artifacts.
