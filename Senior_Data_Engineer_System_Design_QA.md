# Senior Data Engineer System Design Interview Guide

## Detailed Questions, Model Answers, Trade-offs, and AI ERP Scenarios

**Audience:** Senior Data Engineers, Data Platform Engineers, Analytics Platform Engineers, and technical leads.

**Purpose:** This is a separate study and interview-practice document. The model answers demonstrate requirements clarification, capacity estimation, architecture, correctness, failure recovery, governance, cost, and senior-level trade-off reasoning.

---

## How to Answer a System-Design Question

Use this sequence:

1. **Clarify:** consumers, outputs, access patterns, latency, finality, retention, security, and budget.
2. **State assumptions:** make missing information explicit and invite correction.
3. **Estimate:** average/peak throughput, bytes/day, retained storage, state, cardinality, and growth.
4. **Define invariants:** what must never be violated, such as tenant isolation or balanced accounting.
5. **Draw the flow:** sources → ingestion → processing → storage → serving → consumers.
6. **Deep-dive:** keys, partitions, state, model grain, layout, and consistency.
7. **Design recovery:** retries, idempotency, quarantine, replay, backfills, rollback, and reconciliation.
8. **Add operations:** SLOs, monitoring, ownership, lineage, security, cost, and deployment.
9. **Test 10× scale:** identify the first bottleneck and the evolution path.
10. **Summarize:** requirement → decision → benefit → risk → mitigation.

> **Useful interview sentence:** “Because the dashboard requires p95 freshness below two minutes, I would use a streaming aggregation path. This adds state and operational complexity, so I would bound state with event-time windows, checkpoint progress, retain events for replay, and reconcile finalized results in the lakehouse.”

---

# Section 1 — Framing, Requirements, and Estimation

## Q1. You receive a vague prompt: “Design our enterprise analytics platform.” How do you begin?

### What the interviewer is testing

Your ability to navigate ambiguity and avoid choosing tools before understanding the business problem.

### Detailed answer

Start with consumers and decisions. Ask whether the platform serves analysts, operational teams, executives, applications, data scientists, auditors, or external customers. Clarify outputs: raw history, governed metrics, live dashboards, APIs, features, alerts, or exports.

Clarify freshness and finality separately. A dashboard may accept provisional values in two minutes but require reconciled daily results by 06:00. Ask whether latency is p95 or maximum, when the clock starts, and whether late data can revise prior values.

Ask about sources, records/day, record size, average and peak rates, largest source or tenant, growth, key cardinality, skew, retention, replay, legal deletion, residency, encryption, availability, RPO/RTO, budget, and team skills. State assumptions when information is unavailable and summarize them as measurable acceptance criteria before drawing architecture.

### Trade-offs and failure handling

Do not spend the whole interview gathering requirements. Prioritize questions that change architecture: consumer, SLA, scale, correctness, security, and retention. Ask what failure means; a delayed marketing report and an incorrect financial statement need different controls.

### Interview-ready answer

> “I will clarify users, outputs, measurable freshness and correctness, peak scale, retention, security, and recovery. I will state assumptions, estimate capacity, identify invariants, and then design the simplest architecture that meets those requirements.”

### Likely follow-ups

- Which three questions have the greatest architectural impact?
- What assumptions do you use when scale is not provided?
- How do you time-box requirements gathering?

## Q2. How do you translate business requirements into engineering SLOs?

### What the interviewer is testing

Whether you can turn “real time,” “accurate,” and “reliable” into measurable contracts.

### Detailed answer

Define a user-visible freshness SLO, for example: “95% of valid events appear in the dashboard within 120 seconds.” Break it into producer, ingestion, processing, sink, and refresh budgets. Monitor the end-to-end SLO plus stage indicators that explain a breach.

Define correctness and finality: “Daily revenue is final by 06:00 and reconciles to the source within an approved tolerance; all exclusions are accounted for.” Add completeness, uniqueness, validity, consistency, and late-arrival rules. For availability, define the actual service surface and whether stale data can be served with a timestamp. For recovery, define RPO and RTO.

Every SLO needs an owner, measurement, error budget, alert, and runbook. Use service tiers so an exploratory dataset does not receive the same expensive controls as a financial product.

### Trade-offs and failure handling

Lower latency and higher availability increase cost. Stronger finality may require waiting for late records. Alert on user impact, not only CPU or job status, and use stale-but-labeled output when allowed.

### Interview-ready answer

> “I define percentile-based end-to-end SLOs for freshness, correctness, availability, and recovery, allocate them across stages, and connect each SLO to an owner, error budget, and response.”

### Likely follow-ups

- What is the difference between an SLI, SLO, and SLA?
- When should stale data be served?
- How do you define finality for late data?

## Q3. Size a system receiving 500 million events per day.

### What the interviewer is testing

Whether you turn rough assumptions into architecture and capacity decisions.

### Detailed answer

The average rate is 500,000,000 ÷ 86,400 ≈ 5,800 events/second. If the peak is 5× average, plan for about 29,000 events/second plus headroom. Ask about burst duration and backlog recovery because the system may need to process new traffic while draining an outage backlog.

At 1 KB/event, raw volume is about 500 GB/day and 182.5 TB/year before compression, replication, metadata, checkpoints, failed records, and Silver/Gold copies. At 3× compression, raw analytical files may be about 61 TB, but total platform storage will be higher.

Estimate partitions from measured per-partition throughput, ordering requirements, consumer capacity, and target catch-up time. Estimate state as unique keys/window × bytes/state entry × retained windows plus overhead. Translate results into a partitioned log, distributed incremental processing, object storage, compaction, autoscaling, quotas, and peak tests.

### Trade-offs and failure handling

Autoscaling cannot instantly fix too few partitions, service quotas, or hot keys. Compression saves I/O and storage but consumes CPU. Include retries, duplication, regional concentration, and catch-up throughput in the load test.

### Interview-ready answer

> “Average is about 5.8K events/sec; at 5× peak I plan for roughly 29K plus headroom. At 1 KB, input is 500 GB/day. These figures drive partitioning, distributed processing, object storage, compaction, and explicit peak/backlog tests.”

### Likely follow-ups

- How do you estimate stream state size?
- How does skew change partition count?
- How quickly should a six-hour backlog be drained?

## Q4. How do you choose technologies without producing a tool list?

### What the interviewer is testing

Whether you reason from required properties and compare alternatives.

### Detailed answer

Define each component's job before naming products. Ingestion may require durable buffering, replay, local ordering, and independent consumers. Processing may require event-time windows, batch recomputation, state, and checkpoint recovery. Storage may require ACID snapshots, schema evolution, pruning, and multiple engines. Serving may require point lookups, scans, high concurrency, or millisecond latency.

Compare two or three options on latency, correctness, scale, team skills, managed-service availability, operational burden, cost, ecosystem fit, and lock-in. Use conditional language: “I would choose a durable partitioned log if replay and multiple independent consumers are required. If volume is low and files are already durable, direct object-storage landing may be simpler.”

### Trade-offs and failure handling

A powerful tool can be wrong for a team that cannot operate it. Managed services reduce maintenance but may increase cost and lock-in. For every component, explain outage behavior, progress recovery, duplicate handling, and exit strategy.

### Interview-ready answer

> “I select capabilities first and products second. I compare alternatives on required properties, cost, operations, and recovery, and use product names only as implementation examples.”

### Likely follow-ups

- When would you build instead of buy?
- What lock-in matters most?
- How do you evaluate a managed service?

---

# Section 2 — Pipeline Architecture, Streaming, and CDC

## Q5. When should you use batch, streaming, or a hybrid design?

### What the interviewer is testing

Whether you can justify continuous processing and understand its correctness and operating cost.

### Detailed answer

Use batch when scheduled results meet the requirement. Bounded input is easier to retry, backfill, test, optimize, and finalize. It fits daily reporting, periodic model training, and many BI products.

Use streaming only for a named low-latency consumer such as fraud alerts, live inventory, online features, or operational monitoring. Streaming requires event-time semantics, out-of-order handling, watermarks, state retention, checkpoints, replay, and idempotent sinks.

Use a hybrid when consumers have different SLAs. A streaming path can publish provisional recent values to a low-latency store while raw data lands durably and a scheduled lakehouse path produces finalized, reconciled history. Reuse transformation definitions to reduce logic drift.

### Trade-offs and failure handling

Streaming reduces latency but adds always-on cost and stateful operations. Batch simplifies finality but cannot serve urgent decisions. Hybrid systems can duplicate logic. Define checkpointing, replay retention, correction behavior, and reconciliation between provisional and final values.

### Interview-ready answer

> “I default to incremental batch when it meets the SLA. I add streaming for a specific low-latency use case. If users need live and finalized results, I use durable raw truth, an idempotent live path, and a reconciled historical path.”

### Likely follow-ups

- How do you stop stream and batch logic diverging?
- What does “final” mean in streaming?
- How do watermarks affect correctness?

## Q6. How would you design a partitioned event-ingestion backbone?

### What the interviewer is testing

Ordering, parallelism, skew, retention, schema governance, and consumer independence.

### Detailed answer

First define event identity and the narrowest ordering scope. Global ordering is rarely needed. Choose a key such as order ID or tenant plus account ID that preserves required local ordering and distributes load. If one tenant dominates, use controlled sub-sharding where business ordering permits.

Size partitions from peak records and bytes/second, consumer throughput, catch-up target, and growth; validate with the selected service rather than quoting a universal per-partition rate. Use a versioned envelope with event ID/type, source, tenant, aggregate ID, occurred/produced time, schema version, and trace ID. Enforce compatibility through contracts or a schema registry.

Retain enough data for outage recovery and planned replay; archive longer history to object storage if event-log retention is expensive. Consumers assume duplicates and use idempotent writes. Quarantine poison records with payload, reason, and lineage rather than silently skipping them.

### Trade-offs and failure handling

More partitions increase parallelism but also metadata, connections, rebalances, and downstream small files. Key ordering can produce skew; random distribution sacrifices ordering. Monitor lag and key concentration by partition and test consumer rebuilds.

### Interview-ready answer

> “I choose the narrowest required ordering key, prove that it distributes peak load, size partitions for throughput and backlog recovery, govern a versioned envelope, retain replay data, and make every consumer idempotent.”

### Likely follow-ups

- What if one customer produces 30% of events?
- Can you change partition keys later?
- How do you avoid a poison record blocking progress?

## Q7. Compare Lambda, Kappa, and lakehouse-centered architectures.

### What the interviewer is testing

Whether you understand these patterns as processing and recovery models.

### Detailed answer

Lambda has a speed path for low latency and a batch path for complete historical recomputation. It supports fast provisional results and accurate restatement, but duplicate code can drift.

Kappa uses one stream-processing path and replays a retained event log for recomputation. It reduces duplicate processing models, but replaying months of stateful events may be expensive and slow; deterministic code and sufficient log retention are critical.

A lakehouse-centered architecture stores immutable data and ACID table snapshots in object storage. Batch and streaming engines share a durable data plane. This simplifies analytical truth and replay, but does not eliminate event buses, low-latency serving stores, compaction, or concurrency management.

Choose based on where durable truth lives, how a bad deployment is recovered, whether logic can be shared, and what the team can operate.

### Trade-offs and failure handling

Lambda duplicates paths; Kappa can make long replay difficult; lakehouses may not satisfy millisecond access or high-rate transactions. Maintain input, code, state, and output versions for reproducibility.

### Interview-ready answer

> “Lambda recomputes through a batch path, Kappa replays the event log, and a lakehouse uses durable table snapshots accessible to multiple engines. I choose the simplest recovery model that satisfies latency and operations.”

### Likely follow-ups

- Can a lakehouse replace Kafka?
- How long should the event log retain data?
- How do you share logic between paths?

## Q8. Design CDC from operational databases into a lakehouse.

### What the interviewer is testing

Snapshots, transaction ordering, updates/deletes, schema evolution, and reconciliation.

### Detailed answer

Use log-based CDC where possible. Capture database/table, primary key, operation, transaction ID, log sequence or offset, commit time, schema version, tenant, and before/after values where permitted. Preserve the immutable stream in Bronze.

Bootstrap with a consistent snapshot tied to a source log position, then consume changes from that position so there is no gap. Apply changes in source transaction order within the required key scope. Build current-state Silver through idempotent MERGE and optionally retain append-only history for audit and temporal analysis.

Represent deletes as tombstones and define retention before physical removal. Tables without primary keys require a reliable source identity, full-row comparison, or redesign. Reconcile source row counts, control totals, checksums, CDC lag, and applied offsets. Treat DDL as a contract change.

### Trade-offs and failure handling

Before images improve audit but increase volume and sensitive-data exposure. MERGE can be expensive without pruning and compaction. Plan connector restart, source-log expiration, long transactions, schema changes, and resnapshot. Never advance durable progress before the target commit.

### Interview-ready answer

> “I tie a consistent snapshot to a source log position, retain immutable ordered CDC, build current state with idempotent MERGE, preserve delete/history semantics, and reconcile source totals with applied offsets.”

### Likely follow-ups

- How do you avoid the snapshot/CDC gap?
- What if source logs expire?
- How do you preserve cross-table transactions?

---

# Section 3 — Data Modeling, Storage, and Serving

## Q9. Design an analytical model for orders, payments, and shipments.

### What the interviewer is testing

Whether you define grain, separate business processes, choose keys, and avoid incorrect many-to-many joins.

### Detailed answer

Declare each fact's grain. An order-line fact has one row per line; a payment fact has one row per attempt or settlement; a shipment-event fact has one row per lifecycle event. Do not blindly join all facts into a wide table because multiple payments and shipments can multiply order rows and overstate revenue.

Use conformed customer, product, merchant, date, location, and currency dimensions. Preserve source business keys and use surrogate keys when SCD history or multi-source integration requires them. Separate additive measures from balances, ratios, and other non-additive values.

Define occurred time, recorded time, and effective business time. Model status as events, periodic snapshots, or an accumulating snapshot according to the question. Keep amount with currency and define conversion-rate source and effective time. Publish governed metrics such as booked revenue, settled revenue, refunds, and fulfillment duration.

### Trade-offs and failure handling

A star schema improves clarity but requires dimension management. A wide table can help one hot query but duplicates data. Validate grain uniqueness, missing dimension members, split payments, partial shipments, duplicate events, and currency behavior.

### Interview-ready answer

> “I model orders, payments, and shipments as separate facts with explicit grains and conformed dimensions. I avoid fact-to-fact row multiplication, define time/currency semantics, preserve lifecycle history, and expose governed business metrics.”

### Likely follow-ups

- When would you use an accumulating snapshot?
- How do you calculate order-to-delivery time?
- How do you handle partial shipments and refunds?

## Q10. How do you implement SCD Type 2 and late-arriving facts?

### What the interviewer is testing

Temporal joins, effective dates, version boundaries, and idempotent history maintenance.

### Detailed answer

Store surrogate key, business key, tracked attributes, effective_from, effective_to, is_current, source update time, and optionally an attribute hash. Use half-open intervals—start inclusive and end exclusive—to avoid boundary ambiguity.

When tracked attributes change, atomically close the current record at the new effective time and insert the new version. Enforce one current row per business key and no overlapping ranges. Make retrying the operation produce the same result.

A late fact joins to the dimension version valid at the fact's event time, not ingestion time. If that version is unavailable, use an inferred/unknown member and repair later, or defer publication according to the SLA. A late dimension correction may split an old interval and require fact re-keying or temporal joins at query time. Keep recorded time separately when the system must answer both “what was believed then?” and “what is effective now?”

### Trade-offs and failure handling

SCD2 preserves history but increases storage and complexity. Type 1 is better for nonhistorical corrections. Test overlapping intervals, duplicate current rows, out-of-order updates, time zones, and late corrections.

### Interview-ready answer

> “I maintain non-overlapping effective intervals through an atomic close-and-insert. Facts join by business event time. I define inferred-member repair and late-correction behavior and validate one-current-row and no-overlap invariants.”

### Likely follow-ups

- When is bitemporal modeling necessary?
- How do you correct a value effective six months ago?
- Can you avoid re-keying all affected facts?

## Q11. How do you choose event format, file format, table format, and layout?

### What the interviewer is testing

Whether you recognize that these choices solve different problems.

### Detailed answer

Use Avro or Protobuf for record exchange when compact serialization and schema compatibility matter. Use Parquet or ORC for analytics because engines can prune columns, use statistics, and compress repeated values.

Use Delta Lake or Iceberg when tables need ACID snapshots, concurrent commits, time travel, schema/partition evolution, and multi-engine access. Select according to engine and catalog compatibility, maintenance tools, concurrency behavior, and version support.

Partition on commonly filtered, manageable-cardinality fields—often business date. Avoid millions of customer partitions unless isolation requires them. Use clustering, sorting, or data skipping for frequently filtered keys. Define a target file-size range and compact small files. Maintain statistics, manifests/logs, snapshots, and vacuum policies that respect replay and time travel.

### Trade-offs and failure handling

Over-partitioning creates metadata and small-file overhead; under-partitioning increases scans. Clustering improves selected queries but costs rewrite compute. Aggressive vacuum can break readers or recovery. Monitor file-size distribution, file count, pruning effectiveness, bytes scanned, commit conflicts, and metadata growth.

### Interview-ready answer

> “I separate serialization, analytical files, and table management. I use columnar files for analytics, an ACID table layer for reliable updates/snapshots, and a layout driven by real filters, cardinality, and measured pruning.”

### Likely follow-ups

- Delta Lake or Iceberg?
- How do you solve streaming small files?
- When should an existing table be repartitioned?

## Q12. How do you choose serving layers for BI, APIs, and ML?

### What the interviewer is testing

Whether you match query shape, latency, concurrency, consistency, and update pattern to technology.

### Detailed answer

BI requires scans, joins, aggregations, governed metrics, and concurrency; use a warehouse, lakehouse SQL engine, or OLAP store. Operational APIs need predictable low-latency point/range access; use a key-value, relational, search, or low-latency OLAP system based on keys and consistency. ML needs versioned offline features and sometimes an online store with consistent definitions.

Publish stable products rather than raw Bronze. Add materialized views or pre-aggregations only for proven hot paths. Include authorization and tenant identity in cache keys. Refresh serving copies with idempotent upserts, versioned snapshots, or atomic pointer swaps and expose freshness/finality metadata.

### Trade-offs and failure handling

More stores improve workload fit but increase synchronization and cost. Direct lakehouse access is simpler but may not satisfy API latency. Precomputation lowers query time but increases staleness and invalidation complexity. Define whether failure serves last-valid labeled data, falls back to a slower source, or fails closed.

### Interview-ready answer

> “I select serving by access pattern: analytical engines for scans, operational stores for predictable low latency, and feature stores for point-in-time ML features. Each copy has refresh, correction, authorization, freshness, and fallback behavior.”

### Likely follow-ups

- When is an OLAP store preferable to a warehouse?
- How do online and offline features remain consistent?
- How should dashboards represent provisional values?

---

# Section 4 — Reliability, Quality, and Operations

## Q13. What does exactly-once mean, and how do you create an idempotent outcome?

### What the interviewer is testing

Whether you distinguish transport guarantees from end-to-end business correctness.

### Detailed answer

Define the boundary: message processing, state update, sink commit, or business result. Many systems use at-least-once delivery and achieve an effectively exactly-once table through stable identity, source deduplication, deterministic transforms, atomic writes, and progress tracking.

Use a key at the intended grain. Avoid uncontrolled current timestamps or randomness. Deduplicate before MERGE so one target row cannot match multiple source rows unpredictably. Persist offsets, file IDs, or batch IDs without advancing them before the output commit. Reconcile accepted, rejected, and target counts.

A checkpoint does not make two external systems one transaction. For multi-system side effects use an outbox/inbox, write-ahead ledger, or saga with idempotency keys and compensating actions.

### Trade-offs and failure handling

Deduplication state has cost and a retention horizon. Distributed transactions increase coupling and may reduce availability. Test failures before, during, and immediately after a write but before acknowledgement.

### Interview-ready answer

> “I define exactly-once at the business-output boundary, assume duplicate delivery, and use stable keys, deterministic logic, source dedupe, atomic writes, and committed progress. Cross-system effects use an outbox or saga.”

### Likely follow-ups

- How long do you retain dedupe state?
- What if an event ID is reused?
- Can a stream engine guarantee exactly-once into every sink?

## Q14. How do you handle late and out-of-order streaming data?

### What the interviewer is testing

Event time, watermarks, state, finality, and correction policy.

### Detailed answer

Carry occurred_at, produced_at, and ingested_at. Use event time for windows that describe when business activity happened. A watermark bounds how long state is retained; it does not guarantee that older events cannot arrive.

Choose allowed lateness from observed delay and business impact. Events within it update the current window. Very late events should be routed to a correction/recomputation path unless the business explicitly permits dropping them. Label outputs provisional or final. Prevent older arrivals from overwriting newer state using event version or update time.

### Trade-offs and failure handling

Long watermarks increase completeness but also state and finalization delay. Short watermarks reduce cost but create more corrections. Monitor delay distribution, watermark lag, state size, very-late counts, and provisional/final differences. Test replay and clock skew.

### Interview-ready answer

> “I separate event, production, and ingestion time; aggregate by event time; set allowed lateness from business needs and observed delay; label provisional results; and send very late events through an idempotent correction path.”

### Likely follow-ups

- What happens beyond the watermark?
- How do you join streams with different lateness?
- How do you test event-time logic?

## Q15. Design a safe two-year backfill framework.

### What the interviewer is testing

Whether you treat reprocessing as a governed production capability.

### Detailed answer

Create a manifest with run ID, dataset, tenant/scope, dates, immutable input version, code version, expected outputs, dependencies, owner, and status. Reuse normal transformation code with parameters. Split into resumable date/tenant chunks and isolate skewed tenants.

Use separate compute and quotas so live SLOs remain safe. Make every chunk idempotent through MERGE or atomic partition replacement. Before publication, validate counts, checksums, uniqueness, nulls, and business control totals. Publish atomically, retain rollback snapshots, record output versions, and trigger dependents in order.

### Trade-offs and failure handling

Large chunks are efficient but costly to retry; small chunks are resumable but create commit overhead. Throttle if live lag or cost exceeds limits. Never publish mixed code versions inside an output partition without explicit version semantics.

### Interview-ready answer

> “I use an audited manifest, immutable input, shared versioned transforms, resumable chunks, isolated capacity, idempotent writes, reconciliation, atomic publication, rollback, and dependency-aware downstream refresh.”

### Likely follow-ups

- How do you pick chunk size?
- How do you backfill a stateful stream?
- How do you prove unaffected data did not change?

## Q16. How do you evolve schemas without breaking consumers?

### What the interviewer is testing

Technical compatibility, semantics, ownership, and migration planning.

### Detailed answer

Use contracts covering schema, nullability, keys, semantics, units, SLOs, owner, and compatibility. Bronze preserves raw payload and schema version and rescues unexpected data. Silver parses an explicit expected schema and quarantines incompatibility. Gold is stable and versioned.

Adding a nullable field is often compatible. Rename, drop, type narrowing, key change, or semantic change is breaking. For breaking changes, publish a new version, dual-run or provide compatibility views, migrate and measure consumers, then retire the old version. Avoid global permissive auto-merge as governance.

### Trade-offs and failure handling

Strict enforcement protects correctness but can reduce availability. Permissive raw capture preserves evidence but delays trusted output. Monitor drift, rescued data, compatibility failures, and deprecated-version usage; test rollback and replay.

### Interview-ready answer

> “I preserve unexpected raw data but enforce explicit contracts in trusted layers. Breaking changes use a versioned dual-run migration with ownership, consumer adoption metrics, and controlled retirement.”

### Likely follow-ups

- What if a producer changes a type without notice?
- How do nested schemas evolve?
- When is schema-on-read appropriate?

## Q17. Design quality and observability for a critical data product.

### What the interviewer is testing

Whether you detect user impact, diagnose it, and recover.

### Detailed answer

At ingestion check parsing, envelope fields, source counts, checksums, and duplicates. In Silver check grain uniqueness, type/domain validity, references, completeness, freshness, and distributions. In Gold check business invariants and reconcile authoritative totals.

Every rule has an owner, threshold, severity, and action: warn, quarantine, stop a partition, hold publication, or page. Preserve rejected data with reason and lineage.

Combine data signals (freshness, volume), pipeline signals (duration, lag, watermark, retries), platform signals (CPU, memory, shuffle, throttling), and business signals (orders, balances, revenue). Alerts should link to lineage, affected consumers/partitions, recent deployments, and runbooks.

### Trade-offs and failure handling

Blocking every anomaly harms availability; warning on everything causes alert fatigue. Set behavior by criticality and measure time to detect, mitigate, recover, and reconcile.

### Interview-ready answer

> “I combine structural, entity-level, and business reconciliation checks, each with an owner and action. Observability spans data, pipeline, platform, and user impact, and every alert links to lineage and recovery.”

### Likely follow-ups

- When should publication be blocked?
- How do you detect partial data loss?
- How do you reduce false anomaly alerts?

## Q18. The workload grows 10×. How do you scale while controlling cost?

### What the interviewer is testing

Bottleneck diagnosis, horizontal scaling, skew, workload isolation, and cost discipline.

### Detailed answer

Identify what grew: records, bytes, tenants, keys, concurrency, retention, or model complexity. Profile source quotas, partitions and skew, state, shuffle, file counts, metadata, sink rate, query concurrency, and caches. Scale only the constrained stage.

Use durable buffering, sufficient partitions, distributed consumers, hot-key mitigation, incremental processing, pruning, pre-aggregation, right-sized files, autoscaling, workload isolation, and tenant quotas. Control cost with lifecycle policies, compression, preemptible capacity for restartable work, schedule-aware scaling, query budgets, and cost attribution per data product or tenant.

### Trade-offs and failure handling

More partitions increase coordination and file fragmentation. Caches and aggregates reduce query cost but add staleness. Dedicated isolation protects critical workloads but lowers utilization. Test peak plus backlog drain and preserve correctness under pressure.

### Interview-ready answer

> “I determine what dimension grew and profile the actual bottleneck. I scale that stage, fix skew, isolate workloads, reduce bytes processed, attribute cost, and load-test both peak traffic and recovery.”

### Likely follow-ups

- What metrics reveal a hot partition?
- When does vertical scaling help?
- How do you charge back platform cost?

## Q19. Design disaster recovery for a critical data platform.

### What the interviewer is testing

Whether you translate RPO/RTO into a tested plan and separate authoritative from rebuildable assets.

### Detailed answer

Classify source transactions, raw data, audit evidence, schema/catalog, policies, keys, and checkpoints as critical where appropriate. Aggregates, caches, features, embeddings, and indexes may be rebuildable. Assign RPO/RTO by class.

Design for process, cluster, zone, region, operator error, credential compromise, and logical corruption. Use versioned infrastructure/code, protected object storage, recoverable metadata, isolated backups, and permitted regional copies. Restore identity/policy and schemas before publication; reconcile offsets and target versions before resuming.

Exercise failover and restore. Measure actual time, data loss, DNS, credentials, quotas, and consumer reconnection. Logical corruption often needs time travel or rebuild from immutable Bronze rather than regional failover.

### Trade-offs and failure handling

Active-active lowers failover time but adds conflict complexity. Active-passive costs less but increases RTO. Protect backups from production deletion credentials.

### Interview-ready answer

> “I classify authoritative and rebuildable assets, assign RPO/RTO by class, cover infrastructure and logical failures, restore identity and metadata before publication, reconcile progress, and prove recovery through regular drills.”

### Likely follow-ups

- Active-active or active-passive?
- How do you recover logical corruption?
- What is commonly omitted from data-platform DR?

---

# Section 5 — AI-Based ERP System Design

## Q20. Design near-real-time analytics for a multi-tenant AI ERP platform.

### What the interviewer is testing

Whether you combine SaaS isolation, ERP semantics, mixed SLAs, noisy-neighbor control, and scalable analytics.

### Detailed answer

Clarify ERP modules, tenant count and size, regions, legal entities, currencies, custom fields, dashboards, financial finality, and AI use cases. State invariants: no cross-tenant exposure, balanced financial outputs, reproducible as-of results, authorized field access, and audited changes.

Capture CDC and events from finance, procurement, inventory, HR, and order modules into a durable log. Every envelope carries tenant, source transaction identity, aggregate key, occurred/commit time, and schema version. Preserve regional Bronze; map source records into canonical Silver parties, legal entities, transactions, resources, journals, and periods; publish governed Gold metrics.

Stream live operations into a low-latency OLAP/cache and use the lakehouse/warehouse for reconciled reporting. Apply tiered isolation: shared tables with mandatory policies for small tenants, namespace/database isolation for higher-risk tenants, and dedicated stacks for the largest or regulated customers. Tenant identity must also exist in object paths, partitions, checkpoints, caches, vector indexes, telemetry, and support tools.

### Trade-offs and failure handling

Shared infrastructure improves utilization but raises policy and noisy-neighbor risk. Dedicated infrastructure costs more and complicates upgrades. Test cross-tenant negative access, tenant restore, hot-tenant load, regional residency, custom schemas, and correlated month-end peaks.

### Interview-ready answer

> “I use tenant-identified CDC into immutable regional Bronze, canonical ERP Silver, and governed Gold. Streaming serves live operations and the lakehouse produces reconciled history. Tiered isolation, policy-as-code, tenant-aware caches/indexes, quotas, and per-tenant SLOs protect the fleet.”

### Likely follow-ups

- Shared tables or database per tenant?
- How do you restore one tenant?
- How do you prevent noisy neighbors?

## Q21. How do you guarantee financial correctness from CDC through reporting?

### What the interviewer is testing

Whether you understand that reliable change delivery is not the same as accounting correctness.

### Detailed answer

Capture tenant, legal entity, ledger, journal/document ID, line ID, source transaction ID, currency, accounting period, LSN/offset, operation, and commit order. Preserve raw changes and apply them in source transaction order using the complete business key. Make MERGE idempotent and associate consumed source ranges with target versions.

Keep append-only journal history. Posted entries are not overwritten; corrections use reversal or adjustment entries. Preserve recorded and effective accounting time so the system can answer “what was known then?” and “what is effective for that period?”

Enforce invariants: debit equals credit by journal and currency, accounts/entities are valid, periods are open for posting, document totals reconcile to lines/tax, and source control totals equal accepted plus rejected records. Hold final publication on critical failure. Version close snapshots with source cutoff, transformation version, approvals, and restatement lineage.

### Trade-offs and failure handling

Reconciliation can delay freshness. Append-only correction complicates current-state queries. Test duplicate/reordered CDC, missing lines, rollback, rounding, late adjustments, period reopening, and retry after target commit but before acknowledgement.

### Interview-ready answer

> “I preserve source identity/order, write idempotently, retain append-only journal history, enforce accounting invariants, reconcile control totals, and version close snapshots. Correctness is proved by reproducible balances and explicit restatement lineage.”

### Likely follow-ups

- What if lines arrive before the header?
- How do you handle a reopened period?
- How do you reconcile currencies?

## Q22. Design a secure ERP copilot over structured data and documents.

### What the interviewer is testing

Permission-aware retrieval, grounding, business semantics, evaluation, and safe action boundaries.

### Detailed answer

Place an AI gateway between users and models. Authenticate tenant, user, role, purpose, and current entitlements. Classify requests as informational, analytical, or action-oriented. Use governed semantic queries or typed tools for structured calculations and permission-filtered hybrid retrieval for invoices, contracts, policies, and other documents.

Copy tenant, ACL, field sensitivity, effective dates, source, and version to every indexed chunk. Apply policy before context reaches the model. For high-risk customers use dedicated indexes; for shared indexes make tenant filters mandatory and impossible for application code to omit. Cache keys include tenant, entitlement version, query, and data version.

Provide citations, freshness, units, currency, fiscal period, and provisional/final status. Use deterministic tools for arithmetic. Require citation or abstention when evidence is weak. Redact sensitive traces.

Evaluate retrieval recall, authorization correctness, citation support, groundedness, business-rule accuracy, freshness, abstention, latency, and cost by tenant, role, module, and risk. For write-back, treat the model as an untrusted planner: convert the proposal into a typed command, validate ERP rules, require approval by risk tier, attach an idempotency key, and audit before/after state.

### Trade-offs and failure handling

More context improves recall but raises cost and exposure risk. Shared indexes are efficient but increase isolation burden. Strict abstention is safer but may reduce user satisfaction. Test adversarial cross-tenant prompts, entitlement changes, cache invalidation, index deletion, prompt injection, and model kill switches.

### Interview-ready answer

> “I use an AI gateway that authorizes before retrieval, combines governed SQL with ACL-filtered document search, includes citations/freshness, evaluates business correctness, and abstains when evidence is weak. Any write-back is typed, validated, approved, idempotent, and audited.”

### Likely follow-ups

- How do you prevent cross-tenant vector leakage?
- How do you evaluate hallucinations in financial answers?
- How do entitlement changes invalidate caches and indexes?

---

# Section 6 — Campfire-Focused System Design and Interview Preparation

> **Context source:** The company profile, mission, values, and interview expectations in this section are based on the Campfire Candidate Interview Prep Guide summary supplied by the user. They are used to tailor preparation, not presented as independently verified current facts.

## Q23. Design a real-time financial intelligence platform for Campfire's accounting and finance customers.

### What the interviewer is testing

Whether you can translate Campfire's mission—automating manual finance work and providing timely insights—into a financially correct, multi-tenant data platform.

### Detailed answer

Clarify personas and decisions: controllers monitoring close, accountants investigating reconciliations, finance leaders viewing cash and performance, and AI features explaining anomalies. Separate provisional operational freshness from finalized financial truth. Example targets might be sub-five-minute operational insight, hourly reconciliation, and versioned period-close snapshots.

Capture ordered CDC and domain events from general ledger, accounts payable/receivable, cash, expense, and operational modules. Every record carries tenant, legal entity, book, currency, source transaction, line identity, LSN/offset, occurred/commit time, and schema version. Preserve immutable Bronze, build canonical Silver journals, invoices, payments, accounts, entities, periods, and exchange rates, then publish governed Gold measures.

Use streaming for recent exceptions and operational balances and a lakehouse/warehouse path for reconciled statements and historical analysis. Enforce tenant and role policy at every store, cache, and query. Validate debit/credit balance, document totals, period status, currency conversion, and source control totals. Attach freshness, finality, source cutoff, and lineage to every metric shown to users or AI.

### Trade-offs and failure handling

Lower latency can expose incomplete transactions or late adjustments. Label provisional results and use a finalized reconciliation path. Test duplicate/reordered CDC, a missing journal line, exchange-rate correction, tenant restore, and month-end load spikes.

### Interview-ready answer

> “I would combine tenant-identified ordered CDC, immutable raw history, canonical finance entities, streaming exception detection, and reconciled Gold statements. Every metric carries freshness/finality and lineage, and accounting invariants prevent fast but incorrect financial intelligence.”

### Likely follow-ups

- How do you define “real time” for a general ledger?
- How do provisional and final values coexist?
- What happens when a closed period is restated?

## Q24. Design AI-assisted accounting automation with safe human control.

### What the interviewer is testing

Whether you can automate repetitive work while protecting financial systems from hallucinated, unauthorized, or duplicate actions.

### Detailed answer

Separate evidence, recommendation, approval, and execution. Ingest invoices, receipts, contracts, policies, and prior coding decisions with tenant/document ACLs and lineage. Extract structured fields using deterministic parsing plus models, preserve the original document, and attach confidence to every field.

The AI can propose an account, entity, tax treatment, match, explanation, or journal entry. It must retrieve authorized evidence and governed ERP context, cite the source, and expose confidence and alternatives. Convert the proposal into a typed command; do not let free-form model output call the ERP directly. Validate permissions, period status, balanced debits/credits, duplicate document identity, amount tolerances, and policy rules.

Use risk tiers. Low-risk, high-confidence suggestions may be auto-applied if reversible and contractually allowed. Material or unusual actions require approval. Every execution has an idempotency key, before/after state, actor/model/prompt/data versions, and compensating or reversal procedure. Feedback becomes labeled evaluation data only after privacy and quality controls.

### Trade-offs and failure handling

Higher automation improves speed but increases control risk. Conservative thresholds reduce errors but leave more manual work. Measure precision at each automation tier, override rate, time saved, downstream corrections, and user trust—not only model accuracy.

### Interview-ready answer

> “I treat the model as an untrusted planner. It retrieves authorized evidence, produces a typed cited proposal, passes accounting and policy validation, receives risk-based approval, executes idempotently, and records complete audit and rollback information.”

### Likely follow-ups

- What can be safely auto-approved?
- How do you evaluate suggestions with delayed ground truth?
- How do you prevent duplicate invoice payment?

## Q25. Design multi-entity and multi-currency consolidation with late adjustments.

### What the interviewer is testing

Temporal financial modeling, currency semantics, elimination entries, close finality, and reproducibility.

### Detailed answer

Model tenant, legal entity, book, chart of accounts, fiscal calendar, accounting period, transaction currency, functional currency, reporting currency, exchange-rate type, and consolidation hierarchy. Preserve journal-line grain. Store original amount/currency and derived translated amounts with rate ID, effective date, rate type, and calculation version.

Ingest entity ledgers incrementally, map local accounts to the group chart, translate using the correct method, and create explicit elimination and consolidation adjustment entries. Keep ownership and hierarchy as effective-dated dimensions. Produce period snapshots with input cutoff, mapping/rate versions, transformation code, approvals, and lineage.

Late adjustments do not overwrite a published close. Post a reversal or adjustment, identify affected entity/period/currency, recompute bounded aggregates, run control totals, and create a new report version. Consumers can compare original and restated versions and understand why the value changed.

### Trade-offs and failure handling

Pre-translating improves query speed but increases storage and restatement work. Query-time translation is flexible but can be slow and inconsistent. Test missing rates, hierarchy changes, rounding, intercompany mismatch, partial entity arrival, and reopened periods.

### Interview-ready answer

> “I retain journal-line truth, effective-dated entity and account mappings, explicit rate identity, and versioned consolidation snapshots. Eliminations and corrections are auditable entries, and late changes create a reconciled restatement rather than silently rewriting history.”

### Likely follow-ups

- Which exchange rate applies to balance-sheet versus income-statement accounts?
- How do hierarchy changes affect old periods?
- How do you investigate an intercompany imbalance?

## Q26. How would you support customer-specific workflows without fragmenting the platform?

### What the interviewer is testing

Customer-centric innovation, multi-tenant extensibility, schema governance, and long-term operability.

### Detailed answer

Separate stable platform primitives from customer configuration. Keep canonical finance entities and invariant controls shared. Represent customer fields, dimensions, approval routes, mappings, and rules as versioned metadata with typed schemas, ownership, effective dates, and validation. Promote only widely reused extensions into the shared canonical model.

Use a configuration interpreter or rules engine with safe bounded capabilities rather than tenant-specific code forks. Compile or validate configuration before activation. Evaluate changes against historical samples, use preview/dry-run results, and apply tenant-scoped feature flags. Record which configuration version produced every output or decision.

Design the data layout so extensions do not create one physical column or pipeline per tenant. Use typed extension structures for sparse custom fields, and index/materialize selected fields only when query value justifies cost. Enforce quotas and execution limits so one complex workflow cannot degrade the fleet.

### Trade-offs and failure handling

Configuration accelerates customer response but can become an unsafe programming language. Too little flexibility drives forks; too much creates unpredictable performance. Support rollback, version comparison, impact analysis, and tenant-specific canaries.

### Interview-ready answer

> “I keep core finance semantics and controls shared, express customer variation as typed versioned configuration, validate and preview changes, deploy with tenant feature flags, and retain lineage from output to configuration version. I avoid per-customer code and schema forks.”

### Likely follow-ups

- When should a customer request become a platform feature?
- How do you migrate thousands of tenant configurations?
- How do you test a rules engine safely?

## Q27. How do you demonstrate “Quality with Velocity” during a major data-platform migration?

### What the interviewer is testing

Whether you can ship rapidly while preserving financial correctness and customer trust.

### Detailed answer

Define the smallest valuable vertical slice—for example, one module, tenant cohort, and report—rather than waiting for a big-bang platform. Establish non-negotiable quality gates: source/target control totals, grain uniqueness, accounting invariants, schema contracts, lineage, security tests, and rollback.

Run old and new paths in parallel. Compare row-level samples and business-level metrics, classify differences, and publish a migration scorecard. Use tenant-scoped canaries and feature flags. Start with internal or willing low-risk customers, monitor SLOs and support feedback, then expand cohorts. Automate deployment, contract tests, data reconciliation, and rollback to reduce cycle time.

Be explicit about what is temporary. Track migration debt with owners and dates. Share risks and discrepancies directly rather than hiding them to preserve schedule. Customer feedback should influence sequence and usability, while platform invariants remain protected.

### Trade-offs and failure handling

Dual-running costs money and time but lowers migration risk. Small slices may delay architectural economies. A fast launch without reconciliation can destroy trust. Stop or roll back automatically when critical financial or tenant-isolation checks fail.

### Interview-ready answer

> “Quality with velocity means small end-to-end slices, automated financial and security gates, parallel comparison, tenant canaries, feature flags, observable outcomes, and rapid rollback—not skipping correctness to meet a date.”

### Likely follow-ups

- What metric determines readiness to expand the cohort?
- How long do you dual-run?
- How do you handle unexplained differences?

## Q28. A deployment produces incorrect financial metrics for some customers. What do you do?

### What the interviewer is testing

Transparent accountability, customer empathy, incident leadership, and technical recovery.

### Detailed answer

Protect customers first. Stop publication or automation for the affected product, mark values as unavailable or potentially incorrect, and roll back or pin the last valid snapshot. Do not silently continue. Establish an incident lead, technical workstreams, customer/support communication, and a decision log.

Identify scope using lineage: affected code version, datasets, tenants, periods, reports, AI answers, exports, and downstream actions. Preserve evidence. Compare source control totals and prior versions, fix the defect, and run a bounded idempotent backfill on isolated compute. Validate financial invariants and customer-specific samples before atomic republishing.

Communicate directly with known facts, uncertainty, impact, mitigation, and next update time. Own mistakes without blaming an individual. After recovery, provide affected-version lineage and restatement details. Run a blameless review that identifies missing test, observability, rollout, and ownership controls. Add durable prevention, such as canary reconciliation or publication gates, and verify completion.

### Trade-offs and failure handling

Failing closed protects correctness but reduces availability. Serving last-valid data may be better if clearly timestamped. Fast communication may contain uncertainty; label it explicitly rather than waiting for perfect information.

### Interview-ready answer

> “I stop incorrect publication, preserve the last valid state, establish ownership and transparent communication, use lineage to scope customers and outputs, fix and backfill idempotently, reconcile before republishing, and convert the incident into measurable preventive controls.”

### Likely follow-ups

- When do you notify customers?
- Who decides whether stale data can be served?
- What would make the post-incident action plan credible?

# Campfire Values: Evidence to Show in the Interview

| Campfire value from supplied guide | What to demonstrate | Strong story evidence |
|---|---|---|
| Transparent Accountability | State assumptions and risks; own mistakes; communicate incidents directly | You found an error, contained impact, informed stakeholders, repaired data, and added prevention |
| Customer-Centric Innovation | Start from finance-user pain and measurable outcomes | You observed a manual workflow, simplified it, and measured hours saved or faster close |
| Growth Mindset | Show how feedback or failure changed your design | You learned a new domain/tool, changed your view, and improved the result |
| Quality with Velocity | Ship small slices with automated correctness and rollback | Canary, parallel run, reconciliation gates, feature flags, and rapid iteration |
| Collaborative Excellence | Bring accounting, product, security, and engineering together | Shared decision, clear ownership, conflict resolution, and team outcome |
| Low ego / directness | Present alternatives and admit uncertainty | You changed course when evidence or a teammate's idea was better |

## Prepare Three Outcome-Driven Stories

### Story 1 — Customer empathy and innovation

Use a finance or operations user whose manual process you understood directly. Explain the original pain, why existing data was insufficient, the smallest useful solution, and a measured result such as reduced close time, fewer reconciliations, faster investigation, or higher trust.

### Story 2 — Quality with velocity

Choose a migration or launch where correctness mattered. Explain how you divided the work into slices, automated tests and reconciliation, used canaries or feature flags, and shipped quickly without creating hidden risk.

### Story 3 — Transparent accountability and collaboration

Choose an incident or mistake. State your contribution clearly, how you communicated uncertainty and impact, how the team recovered, what changed afterward, and how you shared credit.

For each story prepare: situation, customer stakes, your specific decision, alternatives, action, measurable result, what went wrong, what you learned, and what you would do differently.

## Thoughtful Questions to Ask Campfire Interviewers

- Which accounting workflows create the most manual effort for customers today, and how is data engineering expected to reduce it?
- How does the platform distinguish provisional real-time intelligence from finalized financial results?
- Which financial invariants and reconciliation gates are considered non-negotiable?
- How are customer-specific configurations represented without creating tenant-specific code paths?
- Where does the team draw the boundary between AI recommendation, automatic action, and human approval?
- How are AI answers evaluated for financial accuracy, citations, freshness, and tenant authorization?
- What are the largest scaling pressures today: month-end concurrency, data volume, global residency, or customer customization?
- How does the team practice “Quality with Velocity” when changing core financial data models?
- What would excellent impact from a senior data engineer look like after three and twelve months?
- How do accounting/domain experts, product, and engineering resolve disagreements about metric semantics?

---

# Senior-Level Evaluation Rubric

A strong answer demonstrates the following:

| Area | Strong signal | Weak signal |
|---|---|---|
| Requirements | Defines consumers, outputs, SLOs, correctness, and assumptions | Starts by naming tools |
| Scale | Calculates average/peak, storage, state, skew, and growth | Says “it scales horizontally” |
| Architecture | Connects each component to a required property | Draws components without data flow |
| Data model | States grain, keys, time, history, and semantic ownership | Lists tables without grain |
| Correctness | Defines idempotency, ordering, finality, and reconciliation | Claims “exactly once” without a boundary |
| Failure handling | Covers retry, replay, quarantine, backfill, rollback, and DR | Describes only the happy path |
| Operations | Defines SLOs, telemetry, owners, runbooks, and cost | Mentions monitoring generally |
| Security | Enforces identity and policy through all stores and caches | Adds security as a final box |
| Trade-offs | Explains alternatives and switch conditions | Presents one design as universally correct |
| Communication | Uses requirement → decision → risk → mitigation | Gives a product-focused tool list |

# Final Interview Checklist

Before ending your design, verify that you have answered:

- Who consumes the output and what decision does it support?
- What are the p95 freshness, finality, availability, RPO, and RTO targets?
- What are average rate, peak rate, bytes/day, retention, state, and growth?
- What is the record grain and stable identity?
- What ordering and consistency are actually required?
- Where does immutable truth live and how is it replayed?
- How are duplicates, late data, deletes, and corrections handled?
- How do schema and semantic changes reach consumers safely?
- What quality invariants prove the result is correct?
- What is monitored, who owns it, and what is the recovery runbook?
- How are security, privacy, tenancy, and residency enforced end to end?
- What is the first bottleneck at 10× scale?
- What is the largest cost driver and how is cost attributed?
- Which alternative design would you choose if the SLA or scale changed?
- Can you summarize the design in two minutes using requirement → decision → trade-off → mitigation?

# Additional Practice Prompts

1. Design a customer-360 platform that merges CDC, events, and SaaS APIs while supporting deletion requests.
2. Design an inventory-availability platform with sub-minute updates and daily financial reconciliation.
3. Design a feature platform for demand forecasting with point-in-time-correct training data.
4. Design a data-sharing product that exposes tenant-isolated datasets to external partners.
5. Design a migration from nightly warehouse loads to a lakehouse without stopping existing reports.
6. Design a metadata and lineage platform that can identify every consumer affected by a breaking schema change.
7. Design an anomaly-detection system for journal entries with analyst feedback and model retraining.
8. Design an ERP action copilot that proposes purchase orders but cannot submit unauthorized or duplicate transactions.

---

**Study recommendation:** Practice drawing each answer in 10–15 minutes, then explain one deep-dive and one failure scenario. Record yourself and remove tool names that are not connected to a requirement or trade-off.
