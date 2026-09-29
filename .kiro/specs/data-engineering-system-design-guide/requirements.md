# Requirements Document

## Introduction

This document defines the requirements for a standalone Markdown guide that teaches readers how to design data-engineering systems from business needs through production operations. The future guide will synthesize the workspace materials into one coherent learning resource rather than reproduce each document. The guide will be accessible to readers learning system design while retaining the depth expected from senior data engineers in interviews and real projects.

The source set contains generated, repaired, compacted, and organization-tailored variants. The future guide must therefore preserve unique ideas, remove duplicated explanations, resolve guidance that depends on context, and distinguish durable engineering principles from time-sensitive organization-specific preparation.

### In-Scope Source Material

| Source family | Workspace source items | Primary contribution |
|---|---|---|
| Repository context | `README.md` | Repository purpose and output context |
| Senior question-and-answer guide | `Senior_Data_Engineer_System_Design_QA.md`, `Senior_Data_Engineer_System_Design_QA.docx`, `Campfire_Senior_Data_Engineer_System_Design_QA.docx`, `build_qa_doc.py` | Detailed design reasoning, trade-offs, failure handling, AI ERP scenarios, interview rubric, and practice prompts |
| System-design playbook presentations | `Data_Engineering_System_Design_Playbook.pptx`, `Data_Engineering_System_Design_Playbook  -  Repaired.pptx`, `Campfire_Data_Engineering_System_Design_Playbook.pptx`, `Campfire_Data_Engineering_System_Design_Playbook  -  Repaired.pptx`, `build_ppt.py` | Six-step framework, decision matrices, diagrams, calculations, interview cadence, and concise narration |
| Speaker-note variants | `notes_ppt.docx`, `notes_ppt.pdf`, `notes_ppt_compact.docx`, `update_notes_ppt.py`, `compact_notes_ppt.py` | Concept explanations, examples, key takeaways, AI ERP relevance, Campfire context, and source-freshness caveats |

This phase specifies the guide only. Design and implementation artifacts are outside the scope of this phase.

## Glossary

- **Access_Pattern**: The shape, frequency, latency target, and consistency need of reads or writes performed by a Consumer.
- **AI_ERP**: An enterprise resource planning platform that uses artificial intelligence while preserving financial, authorization, and audit controls.
- **AI_Gateway**: A controlled service boundary that authenticates requests, authorizes data access, invokes models or tools, and records AI interactions.
- **Architecture_Pattern**: A reusable organization of processing paths, durable data, and recovery behavior.
- **Assumption**: A stated value or condition used when a scenario does not supply required information.
- **Atomic_Publication**: A publication operation that exposes either the previous complete output or the new complete output, without exposing a partial mixture.
- **Audit_Trail**: An immutable or protected record of actors, inputs, decisions, changes, and timestamps.
- **Backfill**: Governed reprocessing of a bounded historical scope.
- **Backlog_Drain**: Processing accumulated work after an interruption while current work continues to arrive.
- **Batch_Processing**: Processing bounded data on a schedule or explicit trigger.
- **Bitemporal_Data**: Data that records both business-effective time and system-recorded time.
- **Bronze_Layer**: The source-faithful, replayable layer of a Medallion_Architecture.
- **Capacity_Estimate**: A calculation of throughput, storage, state, concurrency, retention, or growth used to constrain a design.
- **Cardinality**: The number of distinct values in a field or key space.
- **CDC**: Change data capture; the ordered capture of inserts, updates, and deletes from a source system.
- **Checkpoint**: Durable processing progress and state used to resume work after a failure.
- **Clustering**: Co-locating related table values to improve data skipping without creating a directory partition for each value.
- **Compaction**: Combining small data files into fewer files sized for efficient reads and metadata operations.
- **Consumer**: A person, application, analytical tool, model, or downstream system that uses a data output.
- **Cost_Attribution**: Assignment of platform usage and expense to a Data_Product, workload, team, or tenant.
- **Cross_Reference**: A navigable link from one guide section to a related heading, table, example, or glossary entry.
- **Data_Contract**: A versioned agreement covering structure, meaning, quality, service objectives, ownership, and change policy.
- **Data_Finality**: The declared point after which an output is treated as complete unless a versioned correction occurs.
- **Data_Grain**: The precise business meaning represented by one record.
- **Data_Lineage**: Traceable relationships from source inputs through transformations and versions to outputs and Consumers.
- **Data_Model**: The definition of entities, facts, dimensions, keys, relationships, measures, and time semantics.
- **Data_Platform**: The end-to-end system that ingests, processes, stores, governs, and serves data.
- **Data_Product**: An owned, documented, discoverable data output with a defined contract and Consumers.
- **Data_Quality**: Measured fitness of data across completeness, validity, uniqueness, consistency, freshness, and business correctness.
- **Data_Residency**: A constraint specifying geographic locations in which data may be stored or processed.
- **Data_Skipping**: Avoidance of irrelevant files or blocks through metadata, statistics, ordering, or indexes.
- **Decision_Framework**: A repeatable method that compares alternatives against requirements, risks, cost, and operating constraints.
- **Decision_Matrix**: A table that compares alternatives using named evaluation criteria.
- **Deduplication**: Detection and consolidation of repeated records at a declared identity and time horizon.
- **Delivery_Semantics**: The duplicate, loss, ordering, and commit guarantees at a named processing boundary.
- **Design_Workflow**: The ordered sequence used to move from an ambiguous problem to a justified and operable system design.
- **Dimension**: Descriptive analytical context used to group, filter, or interpret Facts.
- **Disaster_Recovery**: Restoration of required service and data after a major infrastructure, security, operator, or logical failure.
- **Encryption**: Protection that renders data unreadable without authorized cryptographic keys.
- **ERP**: Enterprise resource planning; software that manages connected financial and operational business processes.
- **Error_Budget**: The allowed amount of service-objective failure within a measurement period.
- **Event_Backbone**: A durable, partitioned event transport that buffers producers, supports replay, and serves independent Consumers.
- **Event_Time**: The time at which a business event occurred.
- **Fact**: An analytical record representing a business event, transaction, or periodic measurement at a declared Data_Grain.
- **Failure_Mode**: A specific way in which a component, process, data set, or business outcome can fail.
- **Feature_Store**: A serving system that manages consistent machine-learning feature definitions for offline and online use.
- **File_Format**: The physical representation of records in a file, such as a row-oriented or columnar encoding.
- **Financial_Invariant**: A financial rule that valid outputs must preserve, such as balanced debit and credit totals within a journal and currency.
- **General_Guidance**: Engineering guidance intended to apply independently of a named employer or product.
- **Gold_Layer**: The governed, Consumer-oriented Data_Product layer of a Medallion_Architecture.
- **Grounding**: Constraining an AI response to authorized evidence and governed data.
- **Guide**: The future `data-engineering-system-design-guide` Markdown learning resource specified by this document.
- **Headroom**: Capacity reserved above expected peak demand for uncertainty, bursts, and recovery.
- **Human_Approval**: An explicit authorized decision required before a proposed high-risk action executes.
- **Hybrid_Processing**: A design that combines Batch_Processing and Stream_Processing for different latency or finality needs.
- **Idempotency**: The property that repeating an operation with the same identity produces no additional business effect.
- **Interview_Cadence**: A time-boxed sequence for presenting a complete system-design answer during an interview.
- **Interview_Narration**: A concise explanation connecting a requirement, constraint, decision, Trade_Off, risk, and Mitigation.
- **Invariant**: A measurable condition that valid system state and outputs must preserve.
- **Kappa_Architecture**: An Architecture_Pattern that uses one stream-processing model and event replay for recomputation.
- **Lakehouse_Centered_Architecture**: An Architecture_Pattern that uses object storage and transactional table metadata as the shared analytical data plane.
- **Lambda_Architecture**: An Architecture_Pattern with separate speed and historical recomputation paths.
- **Late_Data**: Data that arrives after the expected event-time progress or publication boundary.
- **Least_Privilege**: Granting only the permissions required for a defined responsibility and duration.
- **Medallion_Architecture**: Data progression through Bronze_Layer, Silver_Layer, and Gold_Layer responsibilities.
- **Mitigation**: A control that reduces the probability or impact of a named risk.
- **Non_Functional_Requirement**: A measurable constraint on quality attributes such as latency, availability, security, recovery, or cost.
- **Observability**: Signals and context that reveal user impact, system state, root-cause candidates, and recovery progress.
- **OLAP**: Online analytical processing optimized for scans, filters, joins, and aggregations.
- **Ordering_Scope**: The smallest business key boundary within which event order must be preserved.
- **Organization_Specific_Context**: Interview, mission, value, funding, location, or product information tied to a named organization.
- **Partition_Key**: A field or field combination that assigns records to parallel data or processing partitions.
- **Partitioning**: Physical grouping of data or work into independently processed units.
- **Peak_Factor**: The ratio of peak demand to average demand.
- **PII**: Personally identifiable information that can identify or be linked to a person.
- **Point_In_Time_Correctness**: Use of only information that was valid and available at the relevant historical time.
- **Processing_Time**: The time at which a processing system handles a record.
- **Provenance_Note**: A statement identifying a claim's source family, context, and verification status.
- **Quarantine**: Retention of rejected data with the rejection reason and Data_Lineage for correction or replay.
- **RBAC**: Role-based access control; permission assignment through defined roles.
- **Reader**: A learner, interview candidate, data engineer, platform engineer, technical lead, or project stakeholder using the Guide.
- **Reconciliation**: Comparison of source, accepted, rejected, and output totals or identities to prove completeness and correctness.
- **Replay**: Reprocessing retained immutable input from a known position or version.
- **RPO**: Recovery point objective; the maximum permitted data-loss interval after a disruption.
- **RTO**: Recovery time objective; the maximum permitted time to restore a defined service after a disruption.
- **Runbook**: A maintained operational procedure for detection, diagnosis, containment, recovery, and verification.
- **Schema_Contract**: The structural subset of a Data_Contract defining fields, types, nullability, keys, and compatibility rules.
- **SCD**: Slowly changing dimension; a method for managing changes to Dimension attributes over time.
- **Semantic_Layer**: Governed definitions of business measures, dimensions, units, and access rules exposed consistently to Consumers.
- **Serialization_Format**: A record encoding used for data exchange between producers and Consumers.
- **Serving_Layer**: A storage or query surface optimized for a Consumer's Access_Pattern.
- **Silver_Layer**: The typed, deduplicated, conformed, reusable entity layer of a Medallion_Architecture.
- **SLI**: Service-level indicator; a measured value representing service behavior.
- **SLO**: Service-level objective; a target range or threshold for an SLI over a defined period.
- **Source_Family**: A group of source files containing the same core material in different formats, repairs, or contextual variants.
- **Source_Inventory**: A mapping from every in-scope Source_Item to the Guide sections and unique contributions informed by the Source_Item.
- **Source_Item**: One file listed in the In-Scope Source Material table.
- **Source_Material**: The complete set of Source_Items listed in this document.
- **Stable_Identity**: A deterministic business or event key that remains constant across retries and reprocessing.
- **State_Size**: The memory and durable storage required for retained keys, windows, joins, or Deduplication.
- **Stream_Processing**: Continuous processing of unbounded records as records arrive.
- **Surrogate_Key**: A generated Dimension identifier independent of source business identifiers.
- **Switch_Condition**: A measurable change in requirements or constraints that favors a different design alternative.
- **Table_Format**: Metadata and transaction rules layered over data files to provide snapshots, concurrent commits, evolution, and maintenance.
- **Tenant_Isolation**: Prevention of unauthorized data access or resource interference between customers sharing a platform.
- **Trade_Off**: A benefit gained and a corresponding cost, limitation, or risk accepted by a design decision.
- **Typed_Command**: A schema-validated action request with explicit fields, authorization context, and Idempotency identity.
- **Watermark**: An event-time progress estimate used to bound state and classify Late_Data.
- **Worked_Example**: An end-to-end scenario that applies the Design_Workflow and shows calculations, decisions, risks, and operating behavior.
- **Workload_Isolation**: Controls that prevent one workload or tenant from consuming capacity reserved for another workload or tenant.
- **Abstention**: An AI response behavior that declines to answer or act when evidence, authorization, or confidence is insufficient.
- **Allowed_Lateness**: The event-time interval during which delayed records may update a result before a separate correction policy applies.
- **Apache_Iceberg**: An open Table_Format that manages analytical table snapshots, transactions, schema evolution, and partition evolution.
- **Architecture_Decision_Record**: A versioned record of a design decision, alternatives, evidence, consequences, and review triggers.
- **Avro**: A row-oriented binary Serialization_Format with an explicit schema.
- **Cache**: A faster temporary copy of data whose identity, freshness, invalidation, and authorization behavior require definition.
- **Canary_Release**: A rollout that exposes a change to a bounded Consumer or tenant cohort before broader release.
- **Canonical_ERP_Model**: A shared representation of core ERP concepts such as entities, accounts, journals, invoices, payments, currencies, and periods.
- **Citation**: A reference connecting an AI statement to the authorized evidence supporting the statement.
- **Column_Pruning**: Reading only the columns required by a query.
- **Consistent_Snapshot**: A source image whose records correspond to one recoverable source position.
- **Control_Plane**: Metadata, identity, policy, configuration, catalog, and coordination services required to operate a Data_Platform.
- **Cross_System_Transaction**: One logical business operation whose effects span systems without a shared atomic commit boundary.
- **Data_Vault**: A history-preserving integration Data_Model organized around stable business keys, relationships, and descriptive changes.
- **Delta_Lake**: A Table_Format that adds transactional snapshots, evolution, and maintenance metadata to analytical data files.
- **Dual_Run**: Concurrent execution of old and new paths so outputs can be compared before migration.
- **Elimination_Entry**: An auditable consolidation entry that removes intercompany effects from group-level financial results.
- **Event_Envelope**: Standard metadata carried with an event to identify source, identity, time, version, tenancy, and tracing context.
- **Fail_Closed**: Refusal of a request or publication when authorization or critical correctness cannot be established.
- **Feature_Flag**: A versioned control that enables or disables behavior for a bounded scope without a separate code deployment.
- **Hot_Key**: A Partition_Key value whose disproportionate volume or state creates a processing bottleneck.
- **Horizontal_Scaling**: Increasing capacity by adding parallel workers or partitions.
- **Incremental_Processing**: Processing only data added or changed since a recorded progress boundary.
- **Index**: An auxiliary structure that accelerates lookup at the cost of storage, update work, and synchronization.
- **Logical_Corruption**: Internally consistent but semantically incorrect data caused by faulty logic, inputs, policy, or operator action.
- **One_Big_Table**: A wide denormalized analytical Data_Model optimized for a bounded set of query paths.
- **ORC**: A columnar File_Format designed for compressed analytical scans and predicate filtering.
- **Orchestration**: Coordination of schedules, dependencies, retries, parameters, ownership, and bounded reruns across data work.
- **Parquet**: A columnar File_Format that supports compression, column pruning, and analytical statistics.
- **Partition_Pruning**: Excluding physical partitions that cannot satisfy a query filter.
- **Pre_Aggregation**: Materializing grouped results before query time to reduce repeated computation.
- **Production_Time**: The time at which a producer emits a record, distinct from Event_Time and Processing_Time.
- **Protobuf**: A schema-based binary Serialization_Format for compact record exchange.
- **Restatement**: A new version of a previously published financial result after a governed correction.
- **Reversal_Entry**: An auditable financial entry that offsets a previously posted entry rather than overwriting the prior entry.
- **Snowflake_Schema**: An analytical Data_Model that normalizes Dimension hierarchies into related tables.
- **Source_Position**: A durable source log offset or sequence that identifies captured progress.
- **Star_Schema**: An analytical Data_Model with Facts connected to denormalized Dimensions.
- **Tenant**: A customer or customer boundary that shares a multi-tenant platform while requiring isolated data and resources.
- **Tenant_Canary**: A Canary_Release restricted to named tenants.
- **Text_Format**: A human-readable record representation such as CSV or JSON.
- **Trace_Identity**: A correlation value used to connect related activity across system stages.
- **Transaction**: A set of changes committed as one atomic unit within a defined system boundary.
- **Vector_Index**: An Index over numerical representations used for similarity retrieval.
- **Vertical_Scaling**: Increasing capacity by assigning more resources to an existing worker or node.

## Requirements

### Requirement 1: Source Synthesis, Reconciliation, and Provenance

**User Story:** As a reader, I want one reconciled guide derived from all workspace materials, so that I can learn without navigating duplicate or contradictory documents.

#### Acceptance Criteria

1. WHEN Source_Material is synthesized, THE Guide SHALL incorporate the unique instructional contribution of every Source_Family.
2. IF Source_Items contain equivalent guidance, THEN THE Guide SHALL consolidate the equivalent guidance into one explanation.
3. IF Source_Items present context-dependent or conflicting recommendations, THEN THE Guide SHALL state the assumptions and Switch_Conditions that resolve the difference.
4. WHEN a claim originates from an external framework or Organization_Specific_Context, THE Guide SHALL attach a Provenance_Note to the claim or containing section.
5. WHEN Organization_Specific_Context is retained, THE Guide SHALL separate Organization_Specific_Context from General_Guidance.
6. IF Organization_Specific_Context contains a time-sensitive claim without current verification, THEN THE Guide SHALL label the claim as requiring verification and identify the supplied source context.
7. THE Guide SHALL include a Source_Inventory that maps every Source_Item to at least one Guide section or an explicit no-unique-content classification.

### Requirement 2: Audience Progression and Concept Teaching

**User Story:** As a reader new to data-engineering system design, I want concepts introduced progressively with senior-level depth, so that I can build understanding before evaluating complex trade-offs.

#### Acceptance Criteria

1. THE Guide SHALL organize instruction into foundations, design decisions, reliability and governance, advanced scenarios, and practice sections.
2. WHEN a technical concept is introduced, THE Guide SHALL provide a definition, purpose, operating mechanism, concrete example, Trade_Off, Failure_Mode, and selection rule.
3. WHEN an acronym is introduced, THE Guide SHALL expand the acronym before using the abbreviated form.
4. IF a section depends on a concept explained elsewhere, THEN THE Guide SHALL provide a Cross_Reference to the prerequisite concept.
5. THE Guide SHALL label foundational explanations, senior deep dives, interview guidance, and production guidance with distinct textual markers.
6. WHEN a formula is introduced, THE Guide SHALL define every variable, show units, substitute sample values, and interpret the design consequence.
7. IF a common misconception affects correctness, THEN THE Guide SHALL contrast the misconception with the corrected interpretation.

### Requirement 3: End-to-End Design Workflow

**User Story:** As a system designer, I want a reusable sequence for approaching ambiguous prompts, so that I can produce complete and justified designs.

#### Acceptance Criteria

1. THE Guide SHALL present a Design_Workflow ordered as clarify Consumers and outputs, state Assumptions, estimate capacity, define Invariants, draw data flow, deep-dive into state and models, design recovery, add operations and governance, test tenfold growth, and summarize decisions.
2. WHEN the Guide explains a Design_Workflow step, THE Guide SHALL identify the questions, output artifact, completion check, and common Failure_Mode for the step.
3. WHEN an Assumption changes, THE Guide SHALL show how to revisit affected Capacity_Estimates, architecture decisions, Data_Models, and service objectives.
4. THE Guide SHALL show an end-to-end reference flow from sources through ingestion, processing, storage, Serving_Layers, and Consumers.
5. THE Guide SHALL show security, Data_Lineage, Data_Quality, Observability, cost, and delivery controls as cross-cutting concerns rather than terminal workflow steps.
6. THE Guide SHALL define an Interview_Cadence that allocates time to clarification, estimation, high-level flow, deep dive, reliability, and final Trade_Off review within 45 minutes.
7. THE Guide SHALL provide an Interview_Narration pattern ordered as requirement, constraint, decision, Trade_Off, risk, and Mitigation.

### Requirement 4: Requirements, Invariants, and Service Objectives

**User Story:** As a system designer, I want to translate business language into measurable engineering targets, so that architecture choices can be tested against explicit outcomes.

#### Acceptance Criteria

1. THE Guide SHALL provide a requirements canvas covering Consumers, outputs, Access_Patterns, freshness, Data_Finality, correctness, availability, retention, Replay, security, budget, and team operating constraints.
2. THE Guide SHALL distinguish functional outcomes from Non_Functional_Requirements through paired examples.
3. WHEN a scenario uses a vague term such as real time, large scale, accurate, or reliable, THE Guide SHALL convert the vague term into a measurable SLI and SLO.
4. THE Guide SHALL distinguish SLI, SLO, contractual service commitment, Error_Budget, Data_Finality, RPO, and RTO.
5. WHEN an SLO is defined, THE Guide SHALL identify the measurement boundary, percentile or aggregation rule, time window, owner, alert, and Runbook.
6. WHEN a business rule must remain true across retries or corrections, THE Guide SHALL express the business rule as an Invariant with a verification method.
7. WHERE stale output is permitted, THE Guide SHALL define the maximum staleness, visible timestamp, Consumer label, and fallback behavior.

### Requirement 5: Capacity Estimation and Constraint Translation

**User Story:** As a system designer, I want repeatable capacity calculations, so that scale and cost claims produce concrete design constraints.

#### Acceptance Criteria

1. THE Guide SHALL provide formulas for average record rate, peak record rate, uncompressed bytes per day, retained storage, State_Size, partition demand, and Backlog_Drain throughput.
2. WHEN retained storage is estimated, THE Guide SHALL account separately for compression, replication, metadata, checkpoints, Quarantine, and derived data layers.
3. WHEN peak capacity is estimated, THE Guide SHALL account for Peak_Factor, Headroom, burst duration, key skew, and concurrent Backlog_Drain.
4. THE Guide SHALL include at least two fully worked Capacity_Estimates with explicit inputs, arithmetic, units, rounded outputs, and stated Assumptions.
5. THE Guide SHALL include a worked calculation for 500 million one-kilobyte events per day with a fivefold Peak_Factor.
6. WHEN a Capacity_Estimate is completed, THE Guide SHALL map the estimate to a design implication and a measurement that requires later validation.
7. WHEN tenfold growth is evaluated, THE Guide SHALL identify the first expected bottleneck, the evidence needed to confirm the bottleneck, and an evolution path.

### Requirement 6: Processing and Architecture Decisions

**User Story:** As a system designer, I want capability-based architecture comparisons, so that I can select the simplest processing model that meets the stated requirements.

#### Acceptance Criteria

1. THE Guide SHALL compare Batch_Processing, Stream_Processing, and Hybrid_Processing by latency, Data_Finality, cost profile, state, operational complexity, and recovery model.
2. WHEN Batch_Processing satisfies the SLO, THE Guide SHALL explain why Batch_Processing is the default starting point.
3. WHEN Stream_Processing is selected, THE Guide SHALL tie Stream_Processing to a named Consumer need that cannot meet the SLO through Batch_Processing.
4. THE Guide SHALL compare Lambda_Architecture, Kappa_Architecture, and Lakehouse_Centered_Architecture by durable truth, replay path, logic duplication, state complexity, and team operations.
5. WHEN a technology product is named, THE Guide SHALL first state the capability and required property that the product illustrates.
6. WHEN the Guide recommends an architecture alternative, THE Guide SHALL include at least one rejected alternative and a measurable Switch_Condition.
7. THE Guide SHALL compare managed and self-operated services by staffing, control, cost, service limits, lock-in, and Disaster_Recovery responsibility.
8. THE Guide SHALL explain Orchestration through schedules, dependencies, retry policy, parameterized reruns, concurrency controls, ownership, and Backfill coordination.

### Requirement 7: Event Ingestion and Change Data Capture

**User Story:** As a data-platform designer, I want event and CDC guidance that preserves identity, order, and replayability, so that downstream outputs remain correct during normal processing and recovery.

#### Acceptance Criteria

1. THE Guide SHALL define an event envelope containing Stable_Identity, tenant, aggregate key, event type, Event_Time, production time, source position, schema version, and trace identity.
2. WHEN an Ordering_Scope is required, THE Guide SHALL select the narrowest business boundary that preserves required correctness.
3. WHEN a Partition_Key is evaluated, THE Guide SHALL assess ordering, peak distribution, Cardinality, skew, hot-key behavior, and future repartitioning cost.
4. WHEN event-backbone capacity is estimated, THE Guide SHALL derive partition demand from measured record rate, byte rate, Consumer throughput, Backlog_Drain target, retention, and Headroom rather than a universal partition rate.
5. IF a poison record cannot be processed, THEN THE Guide SHALL route the record to Quarantine with payload reference, rejection reason, and Data_Lineage.
6. WHEN a CDC source is bootstrapped, THE Guide SHALL tie a consistent source snapshot to the exact source position from which incremental changes begin.
7. THE Guide SHALL explain CDC handling for inserts, updates, deletes, transaction order, schema change, append-only history, and current-state reconstruction.
8. IF a CDC source position expires before recovery, THEN THE Guide SHALL describe detection, impact containment, controlled resnapshot, and Reconciliation.
9. WHEN CDC progress is committed, THE Guide SHALL require target output commitment before durable source progress advances.
10. THE Guide SHALL compare event submission, CDC, scheduled file delivery, and external service polling by delivery model, ordering, Replay, request quotas, schema behavior, and source failure recovery.

### Requirement 8: Data Progression and Analytical Modeling

**User Story:** As a data modeler, I want explicit layer and grain guidance, so that analytical outputs remain reusable, auditable, and mathematically correct.

#### Acceptance Criteria

1. THE Guide SHALL define distinct contracts, allowed transformations, failure policies, and Consumer boundaries for Bronze_Layer, Silver_Layer, and Gold_Layer.
2. THE Guide SHALL present the modeling sequence as business process, Data_Grain, Dimensions, Facts, measures, keys, time semantics, late-arrival behavior, and SCD strategy.
3. WHEN multiple business processes have different Data_Grains, THE Guide SHALL model the processes as separate Facts before defining cross-process analysis.
4. IF a Fact-to-Fact join can multiply rows, THEN THE Guide SHALL demonstrate the incorrect result and a grain-preserving alternative.
5. THE Guide SHALL compare star schema, snowflake schema, one-big-table models, and Data Vault models by Consumer usability, governance, change tolerance, query behavior, and modeling cost.
6. THE Guide SHALL compare SCD Type 1, Type 2, and Type 3 behavior with a selection example for each type.
7. WHEN SCD Type 2 is used, THE Guide SHALL define non-overlapping effective intervals, one current version per business key, retry-safe updates, and Event_Time-based Fact lookup.
8. WHEN a late-arriving Fact or Dimension correction occurs, THE Guide SHALL explain inferred members, temporal lookup, interval repair, and downstream correction choices.
9. WHEN financial or global data uses currency, THE Guide SHALL preserve amount, currency, rate identity, rate effective time, and conversion version.
10. WHERE historical belief and historical business effect must both be reproduced, THE Guide SHALL explain Bitemporal_Data and Point_In_Time_Correctness.

### Requirement 9: Storage Formats, Physical Layout, and Serving

**User Story:** As a platform designer, I want storage and serving choices tied to Access_Patterns, so that performance improvements do not compromise correctness or maintainability.

#### Acceptance Criteria

1. THE Guide SHALL distinguish Serialization_Format, File_Format, and Table_Format by the problem solved at each layer.
2. THE Guide SHALL compare text formats, Avro or Protobuf, Parquet or ORC, and Delta Lake or Apache Iceberg using schema behavior, write pattern, analytical scan efficiency, transactions, ecosystem compatibility, and maintenance burden.
3. WHEN a physical layout is designed, THE Guide SHALL evaluate Partitioning, Clustering, sorting, Data_Skipping, Compaction, statistics, snapshot retention, and metadata growth.
4. IF a proposed partition field has unbounded or high Cardinality, THEN THE Guide SHALL compare a lower-cardinality partition with Clustering or indexing alternatives.
5. THE Guide SHALL explain the analytical read path from filter evaluation through partition pruning, Data_Skipping, column pruning, and decompression.
6. THE Guide SHALL compare Serving_Layers for business intelligence, operational dashboards, application interfaces, machine learning, and AI_ERP by Access_Pattern, latency, concurrency, update behavior, and consistency.
7. WHEN a serving copy is introduced, THE Guide SHALL define refresh, correction, authorization, freshness labeling, Data_Finality labeling, and fallback behavior.
8. WHEN a new Serving_Layer is proposed, THE Guide SHALL justify the synchronization cost with a measured latency, concurrency, or Access_Pattern requirement.

### Requirement 10: Correctness, Time Semantics, and Reprocessing

**User Story:** As a reliability engineer, I want explicit correctness and recovery boundaries, so that retries, duplicates, late data, and historical repairs produce controlled outcomes.

#### Acceptance Criteria

1. THE Guide SHALL define Delivery_Semantics separately for transport, processing state, target commit, and business outcome boundaries.
2. THE Guide SHALL explain an idempotent business outcome through Stable_Identity, Deduplication, deterministic transformation, atomic target writes, and committed progress.
3. WHEN Deduplication is designed, THE Guide SHALL specify the Data_Grain, identity, retention horizon, collision behavior, and State_Size consequence.
4. WHEN Stream_Processing uses windows, THE Guide SHALL distinguish Event_Time, Processing_Time, Watermark, allowed lateness, provisional output, final output, and correction behavior.
5. IF Late_Data arrives beyond the allowed lateness boundary, THEN THE Guide SHALL route Late_Data to a defined correction or recomputation path.
6. THE Guide SHALL explain failure outcomes before a write, during a write, after a write, and after a commit but before acknowledgement.
7. WHEN a Backfill is planned, THE Guide SHALL define a manifest containing scope, immutable input version, code version, dependencies, owner, status, and expected output.
8. WHEN a Backfill publishes corrected data, THE Guide SHALL require isolated capacity, resumable chunks, Idempotency, Reconciliation, Atomic_Publication, and rollback metadata.
9. IF one logical operation produces side effects in multiple systems, THEN THE Guide SHALL describe an idempotent coordination or compensation strategy without claiming one checkpoint creates a cross-system transaction.

### Requirement 11: Data Contracts, Quality, Observability, and Incidents

**User Story:** As a data-product owner, I want preventive and diagnostic controls, so that the platform can detect, explain, contain, and repair data failures.

#### Acceptance Criteria

1. THE Guide SHALL define a Data_Contract containing schema, nullability, keys, semantics, units, SLOs, ownership, compatibility, and change policy.
2. WHEN a schema change is proposed, THE Guide SHALL classify the change as compatible or breaking and describe the corresponding Consumer migration path.
3. WHEN a breaking contract change is released, THE Guide SHALL describe versioned publication, dual-run compatibility, Consumer adoption measurement, rollback, and controlled retirement.
4. THE Guide SHALL define Bronze_Layer checks for parsing, envelope fields, source counts, checksums, duplicate rates, and Quarantine.
5. THE Guide SHALL define Silver_Layer checks for Data_Grain uniqueness, types, domains, references, completeness, freshness, and distributions.
6. THE Guide SHALL define Gold_Layer checks for business Invariants, governed metrics, source Reconciliation, and Consumer contracts.
7. WHEN a Data_Quality rule is specified, THE Guide SHALL assign an owner, threshold, severity, action, and recovery verification.
8. THE Guide SHALL organize Observability signals into data, pipeline, platform, and business-impact categories.
9. WHEN an alert is described, THE Guide SHALL connect the alert to affected Consumers, Data_Lineage, recent changes, scope, owner, and Runbook.
10. IF a critical correctness or Tenant_Isolation check fails, THEN THE Guide SHALL describe publication containment, last-valid output handling, impact analysis, repair, Reconciliation, and communication.

### Requirement 12: Security, Governance, Privacy, and Multi-Tenancy

**User Story:** As a platform owner, I want security and governance embedded throughout the design, so that shared data systems preserve authorization, privacy, and tenant boundaries.

#### Acceptance Criteria

1. THE Guide SHALL trace authenticated identity and authorization context through ingestion, storage, processing, Serving_Layers, caches, indexes, logs, and support tooling.
2. THE Guide SHALL explain RBAC, Least_Privilege, Encryption in transit and at rest, key ownership, Audit_Trail, PII classification, and secret handling as design controls.
3. WHEN PII is retained, THE Guide SHALL define purpose, retention period, deletion workflow, backup behavior, and verification evidence.
4. WHEN Data_Residency applies, THE Guide SHALL identify permitted storage locations, processing locations, replication paths, and recovery regions.
5. THE Guide SHALL compare shared-table, namespace or database, and dedicated-stack Tenant_Isolation models by risk, cost, operational burden, and migration path.
6. WHEN tenants share compute, THE Guide SHALL define Workload_Isolation through quotas, scheduling, rate limits, admission control, and per-tenant Observability.
7. WHEN tenant-scoped data enters a cache, search index, vector index, checkpoint, or object path, THE Guide SHALL include tenant identity and authorization in the isolation design.
8. IF an authorization or tenant-boundary test fails, THEN THE Guide SHALL fail the affected publication or request path closed and preserve audit evidence.

### Requirement 13: Scale, Cost, Operations, and Disaster Recovery

**User Story:** As a platform operator, I want growth, cost, and recovery guidance, so that the design remains operable beyond the happy path.

#### Acceptance Criteria

1. WHEN workload grows tenfold, THE Guide SHALL evaluate growth in records, bytes, tenants, keys, concurrency, retention, state, and model complexity separately.
2. WHEN a bottleneck is diagnosed, THE Guide SHALL connect the constrained resource to a targeted scaling action rather than prescribe uniform scaling.
3. THE Guide SHALL compare horizontal scaling, vertical scaling, hot-key mitigation, pre-aggregation, caching, incremental processing, and Workload_Isolation with associated Trade_Offs.
4. THE Guide SHALL provide a cost model covering ingestion, compute, storage, data transfer, serving, metadata operations, retention, Replay, and support labor.
5. WHEN a cost optimization is recommended, THE Guide SHALL state the affected cost driver, expected performance or reliability impact, and rollback threshold.
6. THE Guide SHALL explain Cost_Attribution by Data_Product, workload, or tenant through measurable usage dimensions.
7. WHEN Disaster_Recovery is designed, THE Guide SHALL classify assets as authoritative, control-plane critical, or rebuildable and assign RPO and RTO by class.
8. THE Guide SHALL cover process, cluster, zone, region, operator, credential, and logical-corruption Failure_Modes.
9. WHEN recovery is exercised, THE Guide SHALL verify identity and policy, metadata, source progress, target versions, Consumer reconnection, data loss, elapsed time, and Reconciliation.
10. THE Guide SHALL distinguish regional failover from recovery through Replay, snapshots, or Backfill after logical corruption.

### Requirement 14: AI-Native ERP and Financial System Design

**User Story:** As a senior data engineer, I want a realistic AI_ERP case study, so that I can apply general platform principles to multi-tenant, financially sensitive systems.

#### Acceptance Criteria

1. THE Guide SHALL include an AI_ERP architecture spanning ordered CDC, immutable history, canonical ERP entities, low-latency provisional analytics, reconciled reporting, and governed Serving_Layers.
2. THE Guide SHALL define Financial_Invariants for balanced journals, valid entities and accounts, open posting periods, document totals, currency, and source control totals.
3. WHEN provisional financial data is served, THE Guide SHALL expose freshness, Data_Finality, source cutoff, metric version, and Data_Lineage.
4. WHEN a financial period is corrected after publication, THE Guide SHALL preserve the prior close, create an auditable adjustment or reversal, and publish a versioned restatement.
5. THE Guide SHALL explain multi-entity and multi-currency consolidation through effective-dated ownership, account mapping, rate identity, elimination entries, and versioned close snapshots.
6. WHEN an AI_Gateway answers a question, THE Guide SHALL require authorization before retrieval, Grounding in governed evidence, citations, freshness metadata, and abstention behavior.
7. WHEN AI proposes an ERP action, THE Guide SHALL convert the proposal into a Typed_Command with policy validation, Financial_Invariant validation, risk-tiered Human_Approval, Idempotency, Audit_Trail, and reversal behavior.
8. IF AI evidence is insufficient or unauthorized, THEN THE Guide SHALL abstain from generating a factual financial answer or executable action.
9. WHEN customer-specific ERP behavior is required, THE Guide SHALL use typed, versioned, testable configuration with preview, tenant-scoped rollout, rollback, and output-to-configuration Data_Lineage.
10. WHEN an AI_ERP migration is explained, THE Guide SHALL use bounded vertical slices, parallel comparison, tenant canaries, automated Reconciliation gates, feature flags, and rollback criteria.

### Requirement 15: Worked Examples, Decision Aids, Interviews, and Projects

**User Story:** As a practitioner and interview candidate, I want examples and reusable decision aids, so that I can apply the concepts under realistic constraints.

#### Acceptance Criteria

1. THE Guide SHALL include at least three Worked_Examples covering high-volume event analytics, operational-database CDC into a lakehouse, and multi-tenant AI_ERP financial intelligence.
2. WHEN a Worked_Example is presented, THE Guide SHALL apply a consistent template containing requirements, Assumptions, Capacity_Estimates, Invariants, data flow, Data_Model, failure recovery, security, cost, alternatives, and Switch_Conditions.
3. WHEN a Decision_Framework is presented, THE Guide SHALL compare at least two viable alternatives using requirements, Trade_Offs, Failure_Modes, operating burden, cost, and Switch_Conditions.
4. THE Guide SHALL include Decision_Matrices for processing mode, Architecture_Pattern, Data_Model, storage format, physical layout, Serving_Layer, Tenant_Isolation, and Disaster_Recovery.
5. THE Guide SHALL include an interview evaluation rubric covering requirements, scale, architecture, Data_Grain, correctness, recovery, operations, security, cost, Trade_Offs, and communication.
6. THE Guide SHALL include a final interview checklist that verifies the design from Consumer need through tenfold-growth and cost analysis.
7. THE Guide SHALL include at least five practice prompts that vary latency, scale, source type, correctness, tenancy, and recovery constraints.
8. THE Guide SHALL include a real-project checklist covering discovery, ownership, service objectives, architecture records, contracts, testing, rollout, operation, recovery, and decommissioning.
9. WHEN an interview Assumption replaces missing production evidence, THE Guide SHALL label the Assumption and name the production measurement required to validate the Assumption.
10. WHERE Organization_Specific_Context is retained for Campfire, THE Guide SHALL place the context in a labeled appendix containing freshness caveats, value-to-evidence mappings, outcome-story prompts, and questions for interviewers.

### Requirement 16: Markdown Structure, Navigation, and Reviewability

**User Story:** As a reader using the guide for study or reference, I want a navigable and accessible Markdown document, so that I can locate concepts and verify completion without external files.

#### Acceptance Criteria

1. THE Guide SHALL use one level-one title followed by a consistent nested heading hierarchy.
2. THE Guide SHALL include a linked table of contents for every level-two section.
3. THE Guide SHALL resolve every internal Cross_Reference to an existing heading, table, example, or glossary entry.
4. THE Guide SHALL include a searchable glossary for every acronym and specialized term used in more than one section.
5. WHEN a diagram is included, THE Guide SHALL provide a Markdown-renderable diagram or text diagram and an adjacent prose description of the same data flow.
6. WHEN a table contains a recommendation, THE Guide SHALL introduce the decision context before the table and summarize the selection rule after the table.
7. THE Guide SHALL end each major instructional section with key takeaways, a self-check, and the next relevant Cross_Reference.
8. THE Guide SHALL distinguish commands, formulas, schemas, and pseudocode through fenced blocks with language or content labels.
9. THE Guide SHALL include a final two-minute design-summary template using requirement, decision, benefit, risk, and Mitigation.
10. THE Guide SHALL contain the definitions, examples, formulas, and decision criteria required by each instructional sequence without requiring a Source_Item to complete the sequence.
