# TODO — AI URBAN PLANNER CREW
> Phase‑gated backlog. [Code] deterministic | [Crew] agents/policies.

## Phase 0 — Repo, Infra, CI/CD
- [x] Monorepo: `apps/{frontend,gateway,orchestrator,workers}` + `packages/{sdk}`.
- [x] `docker-compose.dev.yml`: Postgres+PostGIS, Redis, NATS, MinIO; healthchecks.
- [x] GitHub Actions: lint/typecheck/unit; Docker build; SBOM + cosign; migration gate.
- [x] `.env.example` (DB, S3, Redis, NATS, JWT, OAuth); dev TLS.

## Phase 1 — DB & Contracts
- [x] SQL migrations for tables in ARCH; GIST indexes; SRID checks; RLS policies.
- [x] OpenAPI 3.1 + Zod parity; Problem+JSON wrapper; Idempotency middleware.
- [x] Auth.js + RBAC guards (Owner/Admin/Planner/Designer/Analyst/Facilitator/Viewer).

## Phase 2 — GIS & Parcelizer
- [x] `gis-ingest`: GeoJSON/Shapefile→PostGIS; topology fix (clean/union/snap); bounds & area sanity checks.
- [x] `parcelizer`: block→parcel splits; grid/irregular modes; auto attributes (phase, defaults).
- [x] [UI] **MapCanvas**, **DrawToolbar**, **LayerToggles**; hover/selection; batched edits.

## Phase 3 — Zoning & Capacity
- [x] Capacity engine (units, pop/jobs) and validation (mix sum=100%, setbacks feasible).
- [x] [UI] **ParcelInspector** (use mix, FAR, height, setbacks, inclusionary, phase); **ZoningPanel** with live capacity & ground‑floor activation coverage.

## Phase 4 — Network & Mobility
- [x] `network-analyzer` (graph, block stats, intersection density).
- [x] `mobility-model` (VMT/mode share, 15‑min access); policy inputs (parking ratio, bike protection, transit lanes).
- [x] [UI] **NetworkPanel**, **AccessHistogram**, live block metrics.

## Phase 5 — Utilities & Green‑Blue
- [x] `energy-model` (PV/storage siting & yield); `water-model` (demand, runoff, BMPs, reuse); `waste-model` (diversion, route length).
- [x] [UI] **UtilitiesPanel** (PV calc, storage sizing, cisterns/greywater), **GreenBluePanel** (parks/bioswales/greenways, canopy targets).

## Phase 6 — Budget, Score, KPIs
- [x] [Code] QTO generator; `budget-model` (CAPEX/OPEX/per‑HH by category).
- [x] [Code] `sustainability-score` with weights validation; category subscores.
- [x] [UI] **KPIGrid**, **WaterfallBudget**, category scorecards.

## Phase 7 — Trade‑offs & Optimizer
- [x] [Code] `optimizer` (param ranges → Pareto points for Score↑, CAPEX↓; constraints).
- [x] [UI] **TornadoChart**, **ParetoPlot**; "Adopt Scenario" (branch/clone + parameters).

## Phase 8 — Personas & Journeys
- [x] [Code] Citizen Advocate generator (child/senior/low‑income/assistive mobility personas); path quality heuristics; barrier detection.
- [x] [UI] **PersonaJourney** overlays; mitigation suggestions list.

## Phase 9 — Reports & Exports
- [x] [Code] `reporter` (MDX→PDF with maps/charts); `exporter` (GPKG/GeoJSON/DXF/CSV/ZIP) with signed URLs.
- [x] [UI] **ExportHub**; public read‑only share link toggle; artifact previews.

## Testing Matrix
- [x] **Unit**: geometry validation/repair; capacity math; access/VMT; PV yield; runoff/BMP deltas; QTO/budget; score normalization.
- [x] **Contract**: OpenAPI & Zod; Problem+JSON.
- [x] **E2E (Playwright)**: intake→parcelize→zoning→network→models→optimize→export.
- [x] **Load (k6)**: concurrent model runs & map edits; optimizer bursts.
- [x] **Chaos**: malformed GeoJSON, huge polygons, intersecting layers; network holes.
- [x] **Security**: ZAP; dependency & secret scans; object store scope tests.

## Seeds & Fixtures
- [x] [Code] 3 demo sites (≈1–3 km²): coastal flood‑adjacent, brownfield grid, greenfield edge.
- [x] [Code] Unit‑cost library (streets/utilities/parks/building shell incentives) with sources.
- [x] [Code] Persona narratives + amenity catalog; baseline policy presets.
- [x] [Code] Export theme (report layout) and sample bundles.

## Runbooks
- [x] SLO dashboards (parcelize, model runs, optimizer, exports).
- [x] Incident cards: WS degradation, NATS backlog, Redis eviction, PostGIS bloat.
- [x] Cost controls: queue concurrency caps; model sandbox limits; export size guard.

## Out of Scope (MVP)
- Detailed traffic assignment, flood/hydraulic engineering, or structural design.
- External regulatory DBs (upload overlays instead).
- Live map tile hosting; rely on in‑app basemap or user‑provided tiles.
