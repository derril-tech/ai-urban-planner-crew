AI URBAN PLANNER CREW — END‑TO‑END PRODUCT BLUEPRINT
(React 18 + Next.js 14 App Router; CrewAI multi‑agent orchestration; TypeScript‑first contracts.)
1) Product Description & Presentation
One‑liner
A multi‑agent planning studio that turns a brief like “Design a smart eco‑friendly neighborhood for 5,000 residents” into a fully specified concept plan: parcel‑level zoning, density & land‑use mix, street & mobility network, energy/water/waste systems, green‑blue infrastructure, CAPEX/OPEX budget & phasing, a sustainability score, and a citizen experience storyboard—all as interactive maps + exportable CAD/GIS/CSV/PDF bundles.
What it produces
•
Zoning plan (parcels, FAR, heights, setbacks, land‑use mix, inclusionary housing).
•
Mobility plan (street hierarchy, transit priority, bike/ped grid, 15‑minute access).
•
Utilities & resilience (solar microgrid, storage, greywater, stormwater BMPs, waste diversion).
•
Open space network (parks ratio, tree canopy, heat‑island mitigation).
•
Budget & phasing (CAPEX line items, OPEX, public‑private mix, timetable).
•
Sustainability score (LEED/Envision‑inspired composite).
•
Citizen journey (daily flows for diverse personas).
•
Exports: PDF report, GeoPackage/GeoJSON, CAD‑ready DXF, CSV model outputs.
2) Target User
•
City planners & urban design teams (public agencies / consultancies).
•
Developers/master‑planners doing site concepts & quick feasibility.
•
Universities/NGOs for scenario teaching & participatory planning.
•
Infrastructure & mobility planners exploring cross‑sector trade‑offs.
3) Features & Functionalities (Extensive)
Intake & Context
•
Site intake: boundary (draw/upload GeoJSON), gross area, slope/elevation (optional DEM upload), existing parcels, right‑of‑way, protected areas, flood zones, wetlands, protected trees.
•
Brief: target population (e.g., 5,000 residents), jobs target, land‑use goals, affordability %, height/FAR caps, parking policy, mode share targets, renewable energy target, water reuse target, GHG budget.
•
Constraints: regulatory overlays (setbacks, view corridors), hazardous buffers, easements, historic districts.
•
Context data connectors: base map tiles, optional OSM extracts (if user provides), CSVs of background demand, cost libraries.
Scenario Authoring
•
Zoning editor: draw/auto‑parcelize; assign use mix, FAR, height, setbacks, lot coverage, inclusionary %, ground‑floor activation.
•
Street network: add/modify links; classify (arterial, collector, local, ped‑mall, cycleway), turn restrictions, transit priority lanes, curb management.
•
Transit & micro‑mobility: designate BRT stops, micromobility docks, parking max/min, EV‑ready %.
•
Green‑blue: park hierarchy, greenways, bioswales, detention basins, green roofs %, tree canopy targets.
•
Utilities: solar siting (roof/ground/awning), battery storage siting, district heating/cooling flag, water reuse (greywater, blackwater), solid waste (MRF/sortation / organics).
•
Phasing: phase polygons, phase budgets, dependency graph.
Analytics & Simulation (fast, explainable)
•
Population & jobs allocation (by land‑use intensity, FAR, unit mix; vacancy assumptions).
•
15‑minute access index (walk time to key amenities).
•
Mobility KPIs: VKT/VMT estimates (sketch model), mode share, intersection density, block size stats, bike LOS heuristic.
•
Energy: potential PV capacity (kWp), annual yield, storage adequacy, self‑sufficiency %, grid import/export estimate.
•
Water: demand (per capita, non‑res), stormwater runoff reduction via BMPs, reuse %, green roof area.
•
Waste: diversion %, compostables capture, collection route length heuristic.
•
Budget: CAPEX by component (streets, utilities, parks, buildings shell incentives), OPEX; per‑household costs; financing mix.
•
Sustainability score: weighted composite (energy, water, mobility, land‑use mix, social inclusion, resilience, biodiversity, heat island).
Trade‑off Explorer
•
Sliders: affordability %, FAR caps, parking ratios, PV coverage, green roof %, bike lane km, tree canopy % → live recompute with tornado/sensitivity charts.
•
Pareto frontier: optimize for (sustainability score ↑) and (CAPEX ↓) subject to constraints.
Collaboration & Governance
•
Roles: Lead Planner, Designer (site/zoning), Utilities, Mobility, Economist, Community Facilitator, Viewer.
•
Comments, mentions, versioning (scenario branches), change diffs (parcel/zoning deltas).
•
Public share (read‑only) link for workshops (toggle PII safety banners).
Export & Reporting
•
Narrative report (PDF/MDX): concept, KPIs, budget, phasing, sustainability scoring, risks.
•
Data: GeoPackage/GeoJSON for layers; DXF for CAD handoff; CSV for line items; JSON for model configs.
4) Backend Architecture (Extremely Detailed & Deployment‑Ready)
4.1 Topology
•
Frontend/BFF: Next.js 14 (Vercel) with server actions for light writes & signed uploads.
•
API Gateway: Node/NestJS (REST, OpenAPI 3.1, Zod/AJV validation, RBAC, rate limits, Idempotency‑Key, Problem+JSON).
•
Auth: Auth.js (OAuth/passwordless) + short‑lived JWT (rotating refresh); SAML/OIDC; SCIM optional.
•
Orchestration: CrewAI Orchestrator (Python FastAPI) coordinating agents:
o
Architect (massing logics, ground‑floor activation, parcel patterns)
o
City Planner (zoning rules, land‑use mix, street hierarchy, compliance)
o
Sustainability Expert (energy/water/waste/green‑blue, resilience)
o
Economist (CAPEX/OPEX, financing mix, feasibility)
o
Citizen Advocate (personas, 15‑minute experience, equity lens)
•
Workers (Python):
o
gis-ingest (GeoJSON/Shapefile → PostGIS; topology checks)
o
parcelizer (split/merge polygons; block → parcel heuristics)
o
network-analyzer (graph build, centrality, block sizes, intersection density)
o
mobility-model (sketch VMT/mode share, walk/bike LOS)
o
energy-model (roof area → PV kWp/yield; battery E/P sizing; self‑sufficiency)
o
water-model (demand & runoff; BMP impact; reuse %)
o
waste-model (diversion heuristics; route length approximate)
o
budget-model (unit costs library × quantities; CAPEX/OPEX; per‑hh)
o
sustainability-score (weighted composite; category subscores)
o
optimizer (Pareto/search over parameters)
o
reporter (PDF/MDX maps + charts)
o
exporter (GPKG/GeoJSON/DXF/CSV/ZIP)
•
Event Bus: NATS (site.*, parcel.*, network.*, mobility.*, energy.*, water.*, waste.*, budget.*, score.*, export.*).
•
Task Queue: Celery (NATS/Redis broker), lanes: interactive (sliders), models, exports.
•
DB: Postgres + PostGIS (geometries) + Timescale (optional for time series) + pgvector (design precedent embeddings, persona narratives).
•
Object Storage: S3/R2 (uploads, tiles, report/export bundles).
•
Cache: Upstash Redis (hot scenario state, computed KPIs, tile manifests).
•
Realtime: WebSocket gateway (NestJS) + SSE fallback (model progress, optimizer ticks).
•
Observability: OpenTelemetry traces; Prometheus/Grafana; Sentry; structured JSON logs.
•
Secrets: Cloud Secrets Manager/Vault; KMS for keys; no plaintext secrets.
4.2 CrewAI Agents & Tool Surface
Agents
•
Architect — parcel patterns, block sizes, setbacks, massing & ground‑floor program.
•
City Planner — zoning conformance, inclusionary policy, parking rules, street hierarchy.
•
Sustainability Expert — PV/Storage siting, BMPs, tree canopy, heat‑island, resilience.
•
Economist — quantity take‑offs → CAPEX/OPEX, funding structure, phasing affordability.
•
Citizen Advocate — personas (child, senior, low‑income worker, wheelchair user), 15‑minute access/path quality, nighttime safety cues.
Tool Interfaces (strict)
•
GIS.import(file|geojson) → layers {boundary, parcels?, roads?, water?, slope?}
•
Parcel.plan(boundary, densityGoals, constraints) → parcel polygons + zoning defaults
•
Network.design(boundary, typologyParams) → graph + classified links
•
Mobility.estimate(graph, landUse, policies) → {VMT, modeShare, LOS, accessIndex}
•
Energy.simulate(parcels, massing, pvParams, storageParams) → {kWp, kWh/yr, storage sizing, selfSuff%}
•
Water.simulate(landCover, demandParams, BMPs) → {demand, runoff, capture/reuse%}
•
Waste.simulate(pop, landUse, diversionParams) → {diversion%, routeLen}
•
Budget.compute(qto, unitCosts, financeMix) → {CAPEX, OPEX, perHH}
•
Score.compute(kpis, weights) → category + composite scores
•
Optimize.search(paramRanges, objectives, constraints) → Pareto set
•
Report.render(planId); Export.bundle(planId, targets[])
4.3 Data Model (Postgres + PostGIS + pgvector)
-- Tenancy & Identity CREATE TABLE orgs ( id UUID PRIMARY KEY, name TEXT NOT NULL, plan TEXT, created_at TIMESTAMPTZ DEFAULT now() ); CREATE TABLE users ( id UUID PRIMARY KEY, org_id UUID REFERENCES orgs(id), email CITEXT UNIQUE, name TEXT, role TEXT, tz TEXT, created_at TIMESTAMPTZ DEFAULT now() ); CREATE TABLE memberships ( user_id UUID REFERENCES users(id), org_id UUID REFERENCES orgs(id), workspace_role TEXT CHECK (workspace_role IN ('owner','admin','planner','designer','analyst','facilitator','viewer')), PRIMARY KEY (user_id, org_id) ); -- Plans / Scenarios CREATE TABLE plans ( id UUID PRIMARY KEY, org_id UUID, title TEXT, site_area_ha NUMERIC, target_population INT, target_jobs INT, status TEXT CHECK (status IN ('created','authoring','simulating','optimizing','approved','exported','archived')) DEFAULT 'created', created_by UUID, created_at TIMESTAMPTZ DEFAULT now() ); CREATE TABLE scenarios ( id UUID PRIMARY KEY, plan_id UUID REFERENCES plans(id), name TEXT, base_of TEXT, is_primary BOOLEAN DEFAULT FALSE, notes TEXT,
created_at TIMESTAMPTZ DEFAULT now() ); -- Site & Context CREATE TABLE site_boundary ( scenario_id UUID PRIMARY KEY REFERENCES scenarios(id), geom geometry(Polygon, 4326) ); CREATE TABLE context_layers ( id UUID PRIMARY KEY, scenario_id UUID, kind TEXT, -- 'roads','water','slope','parcels','flood','trees' geom geometry(GEOMETRY, 4326), props JSONB ); -- Parcels & Zoning CREATE TABLE parcels ( id UUID PRIMARY KEY, scenario_id UUID, geom geometry(Polygon, 4326), area_m2 NUMERIC, phase INT, land_use TEXT, -- 'res','mix','office','retail','civic','park','utility' far NUMERIC, height_m NUMERIC, setbacks JSONB, lot_coverage NUMERIC, inclusionary NUMERIC, -- 0..1 ground_floor TEXT, -- 'active','standard','service' notes TEXT ); CREATE INDEX parcels_gix ON parcels USING GIST (geom); -- Network CREATE TABLE links ( id UUID PRIMARY KEY, scenario_id UUID, geom geometry(LineString, 4326), length_m NUMERIC, class TEXT, -- 'arterial','collector','local','bike','ped','transit' lanes INT, speed_kph INT, transit_priority BOOLEAN, bike_protected BOOLEAN ); CREATE INDEX links_gix ON links USING GIST (geom); -- Open Space / Green-Blue CREATE TABLE open_space (
id UUID PRIMARY KEY, scenario_id UUID, geom geometry(Polygon, 4326), type TEXT, -- 'park','plaza','greenway','bioswale','detention' area_m2 NUMERIC, tree_canopy_target NUMERIC ); CREATE INDEX open_space_gix ON open_space USING GIST (geom); -- Energy / Water / Waste (aggregated siting + params) CREATE TABLE energy_assets ( id UUID PRIMARY KEY, scenario_id UUID, geom geometry(GEOMETRY, 4326), type TEXT, -- 'pv_roof','pv_ground','battery','dhc_plant' capacity NUMERIC, unit TEXT, meta JSONB ); CREATE TABLE water_assets ( id UUID PRIMARY KEY, scenario_id UUID, geom geometry(GEOMETRY, 4326), type TEXT, -- 'greywater','blackwater','cistern','bioswale' capacity NUMERIC, unit TEXT, meta JSONB ); CREATE TABLE waste_assets ( id UUID PRIMARY KEY, scenario_id UUID, geom geometry(GEOMETRY, 4326), type TEXT, -- 'mrf','organics','collection_depot' capacity NUMERIC, unit TEXT, meta JSONB ); -- KPIs (per scenario) CREATE TABLE kpis ( id UUID PRIMARY KEY, scenario_id UUID, name TEXT, value NUMERIC, unit TEXT, category TEXT, meta JSONB ); -- Budget & Phasing CREATE TABLE unit_costs ( id UUID PRIMARY KEY, org_id UUID, item TEXT, unit TEXT, cost_per_unit NUMERIC, source TEXT ); CREATE TABLE qto ( -- Quantity Takeoffs id UUID PRIMARY KEY, scenario_id UUID, item TEXT, quantity NUMERIC,
unit TEXT, source TEXT ); CREATE TABLE budget ( id UUID PRIMARY KEY, scenario_id UUID, capex NUMERIC, opex_year NUMERIC, per_household NUMERIC, finance_mix JSONB, notes TEXT ); CREATE TABLE phases ( id UUID PRIMARY KEY, scenario_id UUID, number INT, start_year INT, end_year INT, capex NUMERIC, description TEXT ); -- Personas (for Citizen Advocate) CREATE TABLE personas ( id UUID PRIMARY KEY, scenario_id UUID, label TEXT, profile JSONB, narrative TEXT, embedding VECTOR(1536) ); -- Collaboration & Exports CREATE TABLE comments ( id UUID PRIMARY KEY, scenario_id UUID, layer TEXT, feature_id UUID, author_id UUID, body TEXT, created_at TIMESTAMPTZ DEFAULT now() ); CREATE TABLE exports ( id UUID PRIMARY KEY, scenario_id UUID, kind TEXT, -- 'pdf','gpkg','geojson','dxf','csv','zip' s3_key TEXT, meta JSONB, created_at TIMESTAMPTZ DEFAULT now() ); CREATE TABLE audit_log ( id BIGSERIAL PRIMARY KEY, org_id UUID, user_id UUID, scenario_id UUID, action TEXT, target TEXT, meta JSONB, created_at TIMESTAMPTZ DEFAULT now() );
Indexes & Constraints
•
GIST on all geometry tables; check geometry types/SRID 4326.
•
Foreign‑key cascade on scenarios deletions to child layers.
•
Service‑level constraints: population feasibility must equal housing capacity (± tolerance) before approval; weights in sustainability score sum to 1.
4.4 API Surface (REST /v1, OpenAPI)
Auth & Orgs
•
POST /v1/auth/login / POST /v1/auth/refresh
•
GET /v1/me / GET /v1/orgs/:id
Plans & Scenarios
•
POST /v1/plans {title,target_population,target_jobs}
•
POST /v1/plans/:id/scenarios {name, base_of?}
•
GET /v1/scenarios/:id / list by plan
GIS & Layers
•
POST /v1/scenarios/:id/site (GeoJSON/zip)
•
POST /v1/scenarios/:id/context (kind + file)
•
POST /v1/scenarios/:id/parcelize {method, grid?} → parcel set
•
POST /v1/scenarios/:id/parcels {features[]} (create/update)
•
POST /v1/scenarios/:id/links {features[]}
•
POST /v1/scenarios/:id/open-space {features[]}
•
POST /v1/scenarios/:id/assets/:domain (energy|water|waste) {features[]}
Model Runs
•
POST /v1/scenarios/:id/mobility/run {policies, networkParams}
•
POST /v1/scenarios/:id/energy/run {pvParams, storageParams}
•
POST /v1/scenarios/:id/water/run {demandParams, bmpParams}
•
POST /v1/scenarios/:id/waste/run {diversionParams}
•
POST /v1/scenarios/:id/budget/run {costLibraryId?, financeMix}
•
POST /v1/scenarios/:id/score/run {weights}
•
POST /v1/scenarios/:id/optimize {paramRanges, objectives, constraints}
KPIs & QTO
•
GET /v1/scenarios/:id/kpis
•
GET /v1/scenarios/:id/qto
Collab
•
POST /v1/comments {scenario_id, layer, feature_id?, body}
•
GET /v1/comments?scenario_id=
Exports
•
POST /v1/scenarios/:id/export {targets:['pdf','gpkg','geojson','dxf','csv','zip']}
•
GET /v1/exports/:id → signed URL
Conventions
•
Mutations require Idempotency‑Key.
•
Errors: Problem+JSON with remediation.
•
Cursor pagination; strict RLS by org/plan/scenario.
4.5 Orchestration Logic (CrewAI)
State machine
created → authoring → simulating → optimizing → approved → exported → archived
Typical run
1.
Import boundary/context → parcelizer generates a base parcel fabric; network‑analyzer proposes a street grid.
2.
Agents propose policies (parking max, inclusionary %) and defaults (FAR/height by sub‑district).
3.
Models run: mobility, energy, water, waste → KPIs.
4.
Economist computes CAPEX/OPEX from QTO + unit costs; Sustainability computes score.
5.
Citizen Advocate generates persona journeys & 15‑minute access maps.
6.
If trade‑offs requested: optimizer produces Pareto candidates; user adopts a candidate.
7.
reporter/exporter produce artifacts.
4.6 Background Jobs
•
GISIngest(scenarioId, file) → vector import, topology fix.
•
Parcelize(scenarioId, method) → create parcels.
•
RunModel(domain, scenarioId, params) per domain.
•
OptimizeScenario(scenarioId, ranges, objectives) → Pareto set.
•
BuildReport(scenarioId) → PDF/MDX.
•
ExportBundle(scenarioId, targets[]).
•
Periodics: TileBake (raster/mbtiles if needed), CostLibraryRefresh, RetentionSweep, AlertOnFailure.
4.7 Realtime
•
WS channels:
o
scenario:{id}:gis (ingest/parcelize progress)
o
scenario:{id}:models (domain run ticks, KPI deltas)
o
scenario:{id}:opt (optimizer Pareto points stream)
o
scenario:{id}:export (artifact statuses)
•
Presence & lock: prevent conflicting layer edits; section locks per layer.
4.8 Caching & Performance
•
Redis caches: tile manifests, last KPIs, QTO, most recent Pareto front.
•
Model SLOs (typical 1–3 km² site):
o
Parcelize < 3 s P95.
o
Single domain model < 5 s P95.
o
Full recompute (all domains) < 15 s P95.
o
Optimizer first 10 Pareto points < 12 s P95.
o
Report render < 20 s P95.
4.9 Observability
•
OTel traces: endpoint → orchestrator → worker; tags: scenario_id, domain, token/cost.
•
Metrics: compute times per domain, KPI stability, optimization iterations, export success rate.
•
Logs: JSON w/ correlation ids; PII‑safe; audit_log for edits, runs, exports.
5) Frontend Architecture (React 18 + Next.js 14)
5.1 Tech Choices
•
Next.js 14 App Router, TypeScript.
•
UI: shadcn/ui + Tailwind.
•
Map & GIS: MapLibre GL (vector tiles) with geojson‑vt for local slicing; @turf for geometry ops; WGS84 (EPSG:4326) storage.
•
Charts: Recharts (tornado, waterfall, access histograms).
•
State/data: TanStack Query for server cache; Zustand for canvas tools (draw/edit), selection, optimizer panel state.
•
Realtime: WebSocket client (auto‑reconnect/backoff) + SSE fallback.
•
File handling: signed S3 URLs for uploads/exports; CSV/GeoJSON parsing in web worker.
5.2 App Structure
/app /(marketing)/page.tsx /(app) dashboard/page.tsx plans/ new/page.tsx [planId]/ page.tsx // Plan overview & scenarios scenarios/ new/page.tsx [scenarioId]/ page.tsx // Scenario overview site/page.tsx // Boundary & context zoning/page.tsx // Parcels & zoning editor network/page.tsx // Streets & transit greenblue/page.tsx // Parks & BMPs utilities/page.tsx // Energy/Water/Waste kpis/page.tsx // KPI dashboard budget/page.tsx // QTO, CAPEX/OPEX, phasing optimize/page.tsx // Trade-offs & Pareto personas/page.tsx // Citizen journeys & 15-min access
exports/page.tsx admin/cost-library/page.tsx admin/audit/page.tsx /components MapCanvas/* LayerToggles/* DrawToolbar/* ParcelInspector/* ZoningPanel/* NetworkPanel/* TransitStopsEditor/* GreenBluePanel/* UtilitiesPanel/* KPIGrid/* AccessHistogram/* TornadoChart/* WaterfallBudget/* ParetoPlot/* PersonaJourney/* ExportHub/* CommentThread/* /lib map/style.ts api-client.ts ws-client.ts turf-helpers.ts zod-schemas.ts rbac.ts /store useScenarioStore.ts useMapStore.ts useOptimizerStore.ts useRealtimeStore.ts
5.3 Key Pages & UX Flows
Dashboard
•
Cards: “Start Plan”, “Active Scenarios”, “Recent Exports”.
•
KPI mini‑cards: avg sustainability score, avg CAPEX per HH.
Scenario Overview
•
Status stepper; KPI chips (population capacity vs 5,000 target; 15‑min access; self‑sufficiency; CAPEX/HH).
Site
•
MapCanvas with boundary draw/upload; context layer upload; topology check badges.
Zoning
•
DrawToolbar to split/merge parcels; ParcelInspector to edit FAR/height/use/setbacks/inclusionary/phase.
•
ZoningPanel shows capacity calc: units by type, population, jobs; ground‑floor activation coverage.
Network
•
NetworkPanel: add/edit links; set class/lanes/speed; bike protected toggle; BRT stops; curb mgmt.
•
Live metrics: intersection density, avg block length, km of protected bike.
Green‑Blue
•
GreenBluePanel: draw parks/bioswales/greenways; tree canopy target; shows park hectares/1k residents, runoff reduction gauge.
Utilities
•
UtilitiesPanel: place PV/battery/DHC, water assets (cisterns, greywater), waste depots; capacity & coverage summaries.
KPI Dashboard
•
KPIGrid (sortable with categories); AccessHistogram; TornadoChart for sensitivities.
Budget
•
WaterfallBudget (CAPEX categories); QTO table (editable if allowed); phases timeline with costs.
Optimize
•
ParetoPlot (CAPEX vs Sustainability Score); sliders for parameters (parking ratio, PV %, inclusionary %); “Adopt Scenario” button sets new scenario branch.
Personas
•
PersonaJourney: pick persona → path lines appear; 15‑minute coverage map; barriers list (e.g., unsafe crossings); mitigation suggestions.
Exports
•
ExportHub: choose artifacts; progress list; signed links; “share read‑only” link toggle.
5.4 Component Breakdown (Selected)
•
MapCanvas/Layer.tsx
Props: { id, geojson, style, editable }; supports hit‑testing, hover tooltips, selection outlines; batched updates to avoid layout thrash.
•
ParcelInspector/Fields.tsx
Props: { parcel }; FAR, height, use mix (% by category), inclusionary %, setbacks (N/E/S/W), lot coverage; validation (sum mix=100%, setbacks feasible).
•
NetworkPanel/Editor.tsx
Props: { link }; class, lanes, speed, transitPriority, bikeProtected; warns if geometry intersects parks without bridge/underpass metadata.
•
UtilitiesPanel/PVCalculator.tsx
Props: { roofArea, tilt, azimuth }; estimates kWp → shows annual kWh & % of load covered.
•
ParetoPlot/Scatter.tsx
Props: { points, selectedId }; click to inspect parameters; “Adopt” clones scenario with chosen parameter set.
5.5 Data Fetching & Caching
•
Server Components for scenario read views (layers lists, KPIs, costs).
•
TanStack Query for mutations (layer edits, model runs, optimizer runs); optimistic updates when editing geometries.
•
WS pushes update KPIGrid, WaterfallBudget, ParetoPlot in place (queryClient.setQueryData).
•
Prefetch heavy neighbors (zoning ↔ network ↔ KPI dashboard).
5.6 Validation & Error Handling
•
Shared Zod schemas for GeoJSON features (geometry type SRID 4326), parcel attributes, network attributes, asset params, budget forms, weights.
•
Problem+JSON renderer with remediation tips (e.g., “population capacity below target; increase FAR or reduce setbacks”).
•
Guardrails: export disabled if geometry invalid or population capacity deviates >5% from target unless override justified.
5.7 Accessibility & i18n
•
Keyboard shortcuts for draw tools; ARIA labels on sliders/charts; focus‑visible rings.
•
High‑contrast map themes; color‑blind safe palettes for layers.
•
next-intl scaffolding; metric/imperial toggles; localized currency.
6) Integrations
•
Storage: Google Drive/SharePoint (optional) for data in/out.
•
Map tiles: use in‑app basemap (no external key required); optionally allow user‑provided tile URL.
•
Comms: Slack/Email notifications (model run complete, export ready).
•
Identity/SSO: Auth.js; SAML/OIDC; SCIM (orgs).
•
Payments (SaaS): Stripe (seats + metered model runs).
•
No external regulatory databases by default; users may upload their overlays.
7) DevOps & Deployment
•
FE: Vercel (Next.js 14).
•
APIs/Workers: Render/Fly.io (simple) or GKE (scale: CPU pool for GIS/modeling; memory pool for exports; burst pool for optimizer).
•
DB: Managed Postgres with PostGIS + pgvector; PITR; migrations gated.
•
Cache: Upstash Redis.
•
Object Store: S3/R2 with lifecycle policies (retain exports; purge temp tiles).
•
Event Bus: NATS (managed/self‑hosted).
•
CI/CD: GitHub Actions — lint/typecheck/unit/integration; Docker build; SBOM + cosign; blue/green deploy; migration approvals.
•
IaC: Terraform modules (DB, Redis, NATS, buckets, secrets, DNS/CDN).
•
Testing
o
Unit: geometry validation, capacity math, mobility/energy/water heuristics, budget aggregation, score normalization.
o
Contract: OpenAPI.
o
E2E (Playwright): intake→parcelize→zoning→network→models→optimize→export.
o
Load: k6 (concurrent model runs & tile rendering).
o
Chaos: malformed GeoJSON, invalid topology, huge polygons.
o
Security: ZAP; container & dependency scans; secret scanning.
•
SLOs (reinforce §4.8): parcelize <3s; single domain <5s; full recompute <15s; first 10 Pareto pts <12s; export <20s; 5xx <0.5%/1k.
8) Success Criteria
Product KPIs
•
Time to first viable plan (meets 5,000 target & constraints) ≤ 30 min median.
•
Sustainability score improvement vs. baseline ≥ +20% within 3 iterations.
•
Workshop readiness: report + exports delivered with ≥99% success.
•
Engagement: ≥ 70% of sessions use trade‑off sliders.
Engineering SLOs
•
WS reconnect < 2 s P95; map interaction latency < 16 ms frame budget (60 fps feel).
•
Export success ≥ 99%; geometry validity errors < 1% of edits (with auto‑repair).
9) Security & Compliance
•
RBAC: Owner/Admin/Planner/Designer/Analyst/Facilitator/Viewer; layer‑level edit locks.
•
Encryption: TLS 1.2+; AES‑256 at rest; KMS envelopes for secrets; signed URLs for uploads/exports.
•
Privacy: no personal data required; if workshop emails used, store separately w/ minimal scope.
•
Tenant isolation: Postgres RLS; S3 prefix isolation per org.
•
Auditability: immutable audit_log for layer edits, model runs, optimizer decisions, exports.
•
Supply chain: SLSA provenance; image signing; pinned deps; Dependabot.
•
Disclaimers: outputs are conceptual simulations, not engineering drawings or legal approvals.
10) Visual/Logical Flows
A) Intake → Fabric
Upload/draw boundary → gis-ingest → parcelizer builds parcel fabric → network‑analyzer proposes base grid.
B) Zoning & Capacity
Edit FAR/height/use/inclusionary → capacity calc updates (units/pop/jobs); guard if <5,000 target → prompt to raise FAR or adjust mix.
C) Models & KPIs
Run mobility, energy, water, waste → KPIs populate (15‑min access, PV self‑suff %, runoff reduction, diversion %, VMT).
D) Budget & Score
budget-model assembles QTO × unit costs → WaterfallBudget; sustainability-score computes composite + categories; weak categories highlighted.
E) Trade‑offs
Move sliders (parking ratio, PV %, green roof %, inclusionary %) → WS triggers partial recomputes; TornadoChart shows sensitivity; ParetoPlot suggests optimal parameter sets.
F) Personas
Select persona → Citizen Advocate generates day path & barriers → mitigation prompts (crossing safety, lighting, benches, shade).
G) Exports
reporter renders MDX/PDF (maps, charts); exporter bundles GeoPackage/GeoJSON/DXF/CSV/ZIP → signed URLs → share link.