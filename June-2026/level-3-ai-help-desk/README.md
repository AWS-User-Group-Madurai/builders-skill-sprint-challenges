# Level 3 — AI Help Desk

- **Difficulty:** Advanced
- **Target time:** 90+ minutes
- **Target environment:** Local AWS Blocks mocks; no AWS account required

This track is independent. Start from a fresh facilitator scaffold; the other apps are not prerequisites.

## Mission

Build a support portal entirely on your machine. Customers ask questions, a locally running Agent retrieves answers from help documentation and can create tickets, and human support agents see new tickets through local Realtime. Add local role authorization, protected file handling, rate limiting, logs, and metric-emission evidence.

## Important implementation notes

### Use the local `AuthCognito` mock for the agent role

This level uses `AuthCognito`, not `AuthBasic`. The current `AuthBasic` API provides username/password sessions but not native user groups. Configure one `agent` group and treat every authenticated user as a customer by default. Customer-owned methods use `requireAuth` plus ownership checks; support methods use `requireRole(context, 'agent')`.

Declaring a group does not assign users to it, and the application-facing auth API must not expose role administration. The facilitator scaffold must include a tested local fixture with:

- one confirmed customer identity; and
- one confirmed identity assigned to the local `agent` group.

Use the fixture or mock-state procedure documented for the installed `bb-auth-cognito` version. Participants must not build a public `makeMeAgent` method or edit mock state from application code. The fixture is workshop setup, not application persistence.

**Facilitator readiness gate:** Level 3 is not ready until both identities can sign in locally and the customer is denied from a `requireRole(context, 'agent')` method. Do not use an AWS deployment as a fallback for a missing local role fixture.

### `FileBucket` and `KnowledgeBase` are separate local concerns

Uploading a file to the local `FileBucket` does not automatically re-index a `KnowledgeBase`. The required workshop flow keeps the responsibilities explicit:

- an agent uploads help documents into a protected local `FileBucket` staging prefix; and
- the searchable corpus lives in a project folder such as `knowledge/`, which is the local `KnowledgeBase` source.

Use the same small document set for both demonstrations: upload it to staging, and include its reviewed copy in `knowledge/`. The staging upload proves protected file storage; the project source proves retrieval. Dynamically promoting uploaded objects into an AWS Knowledge Base is an optional cloud extension.

Customer ticket attachments are optional stretch work, not part of the core upload flow.

### Choose a tested local Agent path

The raw canned provider needs no model service and is useful for basic plumbing, but it synthesizes placeholder string arguments for tools. By itself, it does not prove that the customer's actual question reached `searchHelpDocs`.

The facilitator must provide and test one of these fully local paths before the workshop:

1. **Tool-capable local model:** Ollama or another supported local endpoint with a model that reliably calls both workshop tools.
2. **Deterministic canned-provider adapter:** a scaffold adapter that carries the authenticated original customer message into `searchHelpDocs.query` instead of accepting the canned placeholder. The adapter must have a focused local test proving the exact query reaches `KnowledgeBase.retrieve`.

Either path must display the retrieved fact and source for the customer's real question. Raw canned behavior may still be used to exercise generic tool plumbing, but it does not satisfy the grounded-answer check by itself.

## Blocks and primitives

| Item | Why you need it |
|---|---|
| `AuthCognito` | Local authenticated customers plus an agent group for support-only operations |
| `DistributedTable` | Local durable tickets and rate-limit windows |
| `FileBucket` | Local agent-only help-document staging uploads |
| `KnowledgeBase` | Local retrieval over the reviewed help corpus |
| `Agent` | Tested local-model or deterministic-adapter responses and tool execution |
| `Realtime` | Live ticket updates between local browser contexts |
| `Logger` | Structured console evidence |
| `Metrics` | Application metric calls; paired with safe Logger markers because the local implementation has no CloudWatch view |
| `Scope`, `ApiNamespace` | Backend composition and typed frontend methods |

There is intentionally no built-in rate-limit Block. Compose the limiter from a `DistributedTable` and conditional writes.

## Read before building

```text
node_modules/@aws-blocks/blocks/docs/core.md
node_modules/@aws-blocks/blocks/docs/auth-common.md
node_modules/@aws-blocks/blocks/docs/bb-auth-cognito.md
node_modules/@aws-blocks/blocks/docs/bb-distributed-table.md
node_modules/@aws-blocks/blocks/docs/bb-file-bucket.md
node_modules/@aws-blocks/blocks/docs/bb-knowledge-base.md
node_modules/@aws-blocks/blocks/docs/bb-agent.md
node_modules/@aws-blocks/blocks/docs/bb-realtime.md
node_modules/@aws-blocks/blocks/docs/bb-logger.md
node_modules/@aws-blocks/blocks/docs/bb-metrics.md
```

Local parity notes for this challenge:

- `KnowledgeBase` performs local document retrieval rather than calling Bedrock embeddings. Verify source-aware retrieval, not cloud ranking quality.
- A tested local model or deterministic adapter is required for query-faithful Agent retrieval; the raw canned provider alone generates placeholder tool arguments.
- `FileBucket`, `DistributedTable`, and auth state persist beneath `.bb-data/`.
- `Realtime` uses the local WebSocket bridge and is ephemeral, so reconnect from durable ticket data.
- `Logger` prints locally; `Metrics` has no local CloudWatch dashboard.

## Authorization classes

| Class | How it is identified | Allowed actions |
|---|---|---|
| Customer | Any authenticated local user | Ask the assistant; create and view tickets owned by their session identity |
| Agent | Authenticated local user in the `agent` group | List/update relevant tickets, subscribe to the support channel, and stage help-document uploads |

Agent membership adds support capabilities; it does not replace normal authentication. Enforce every permission in backend methods. A hidden navigation link is not a role check.

## Suggested ticket design

A ticket record should include at least:

| Field | Purpose |
|---|---|
| `ticketId` | Unique ticket identity |
| `customerId` | Server-derived owner |
| `subject` | Short description |
| `description` | Customer-provided detail |
| `status` | For example `open`, `inProgress`, or `resolved` |
| `priority` | Validated severity |
| `source` | `portal` or `assistant` |
| `createdAt`, `updatedAt` | Ordering and audit timestamps |
| `version` | Optimistic-concurrency value |

Design keys and indexes for two access patterns: a customer lists only their tickets, while an agent lists open tickets across customers. Do not solve either path with an unbounded scan.

## Build milestones

### 1. Configure local authentication and the agent group

- Configure `AuthCognito` with `groups: ['agent'] as const` and a stable Block ID.
- Export the authentication API used by the frontend.
- Use the facilitator's confirmed customer and agent identities.
- Use `requireAuth` plus server-derived ownership for customer methods.
- Use `requireRole(context, 'agent')` for every support-only method.
- In two browser contexts, prove the agent can call one support method and the customer receives a denial.

Never add a public role-assignment endpoint.

### 2. Build protected ticket APIs

Implement typed methods for:

- creating a customer ticket;
- listing the current customer's tickets;
- listing all relevant tickets for agents;
- changing ticket status as an agent; and
- obtaining access to the agent Realtime channel.

A customer lookup must use the authenticated customer key. For an agent update, validate status and use optimistic concurrency if two agents can edit simultaneously.

### 3. Push tickets to the local agent screen

- Define a typed `Realtime` namespace for ticket events.
- Publish a complete ticket snapshot after creation or update.
- Grant channel access only after `requireRole(context, 'agent')`.
- Load an initial agent ticket list, then merge live snapshots by `ticketId` so reconnects and duplicate messages are safe.
- Disconnect and reconnect the agent screen to prove it reloads canonical tickets from `DistributedTable`.

When the Agent tool creates a ticket later, use the same ticket service and publish path rather than duplicating persistence logic.

### 4. Add the required local help-document staging upload

- Create a `FileBucket` with a stable Block ID.
- Protect list, upload-handle, finalize, download, and delete methods with `requireRole(context, 'agent')`.
- Generate object keys on the server under a prefix such as `help-staging/{generatedId}/{safeName}`.
- Allow only the workshop's small `.md` and `.txt` files in the core path.
- Prefer the typed upload handle described by the installed docs; if using a local presigned URL, keep it short-lived and bind its content type.
- After upload, require an agent-only finalize call. Read the object through `FileBucket`, enforce the workshop byte limit, validate that it is acceptable text, and delete or quarantine failures before listing the file as ready.

Browser-supplied filename, MIME type, and size are hints, not security checks. A presigned upload URL does not by itself enforce a maximum byte count or inspect content. Production systems should add malware scanning and a quarantine workflow.

The staging bucket is not the Knowledge Base source in the core challenge. Do not present an uploaded object as searchable merely because finalization succeeded.

### 5. Add and verify the local knowledge corpus

Place the reviewed copy of the workshop corpus under a project-relative folder such as:

```text
knowledge/
├── account-access.md
├── billing.md
└── service-limits.md
```

Include distinctive, workshop-specific facts so retrieval can be proven. Configure `KnowledgeBase` with this folder and implement a protected retrieval method or Agent tool. Under `npm run dev`, verify that a query returns the expected source and fact.

Do not claim a newly staged `FileBucket` object is searchable. The local Knowledge Base watches its configured project source, not the staging bucket.

### 6. Add the local support Agent and tools

Give the Agent a focused support system prompt and at least two tools:

1. `searchHelpDocs` — validates a query, calls `KnowledgeBase.retrieve`, and returns source-aware results.
2. `createTicket` — validates ticket fields, uses the authenticated customer identity supplied by your trusted API layer, writes through the shared ticket service, and publishes to the agent channel.

Use the facilitator-tested local path for the required proof:

- With a **local model**, ask a natural corpus-specific question and verify that the model calls `searchHelpDocs` with that question, then invokes `createTicket` when asked to escalate.
- With the **deterministic adapter**, verify that the adapter passes the authenticated original message—not the canned placeholder—into `searchHelpDocs.query`. Keep a focused local test for this exact handoff. The canned provider may still trigger the tool-selection plumbing around the adapter.

Render the retrieved fact, source, and ticket confirmation. A tool call that searches for a generated placeholder such as `sample` does not count as grounded retrieval.

Protect every chat/conversation API method. Derive the user ID from the session, and verify conversation ownership before returning conversation history. A hard-to-guess conversation ID is not authorization.

If streaming, establish the subscription before sending the message so early chunks are not lost.

### 7. Compose a local rate limiter

Apply a per-user fixed-window limit to the Agent send-message endpoint. Use a composite table key: `subject` as the partition key and `windowStart` as the sort key.

| Field | Purpose |
|---|---|
| `subject` | Authenticated user ID plus operation name |
| `windowStart` | Current fixed-window boundary and sort key |
| `count` | Requests accepted in this window |
| `version` | Optimistic-concurrency value |
| `expiresAt` | TTL for eventual cleanup |

Required behavior:

1. derive `subject` from the authenticated session and calculate the current `windowStart` on the server;
2. address exactly the `{ subject, windowStart }` record;
3. create a missing window at count 1 with `{ ifNotExists: true }`;
4. when the record exists, reject at the limit or replace it with an incremented count/version using `{ ifFieldEquals: { version } }`;
5. retry a small bounded number of conditional conflicts;
6. reject before invoking the Agent when the limit is reached; and
7. log and count the rejection without logging the customer's prompt.

Each new time window has a new sort key, so delayed TTL deletion cannot keep a user stuck in the previous window. TTL is cleanup, not rollover logic. A process-local counter is not accepted because it would not preserve the intended distributed design.

### 8. Add locally visible observability

Use `Logger` for structured events such as:

- ticket created or status changed;
- help-document staging accepted or rejected;
- knowledge retrieval completed with result count and duration;
- Agent invocation succeeded or failed; and
- rate limit rejected a request.

Use `Metrics` for a small operational set, for example:

- `TicketsCreated`;
- `HelpDocsStaged`;
- `AgentRequests` and `AgentErrors`;
- `RateLimitRejected`; and
- `KnowledgeRetrievalLatency`.

The local `Metrics` implementation does not provide a CloudWatch view. For every metric call in this workshop, emit a separate safe structured `Logger` event such as `metric_emitted` with only the metric name, unit, and value. The facilitator verifies both the `Metrics` call in code and its corresponding console marker.

Do not log prompts, document content, tokens, passwords, upload handles, presigned URLs, or other sensitive values. Include correlation, user, ticket, and conversation identifiers only where appropriate.

### 9. Build two local frontend views

**Customer view**

- authenticated chat with streamed state;
- source-aware tool results;
- clear ticket escalation confirmation; and
- own-ticket list.

**Agent view**

- role-protected ticket queue;
- live insert/update behavior;
- status controls; and
- help-document staging upload, validation status, and list.

The frontend imports typed APIs from `aws-blocks`; it does not call hidden transport routes directly.

### 10. Complete the local verification

Run only:

```bash
npm run dev
```

Then:

1. open separate customer and agent browser contexts using the facilitator identities;
2. prove the customer is denied from an agent-only operation;
3. ask a distinctive corpus question through the tested local model or deterministic adapter and display the retrieved fact and source;
4. invoke the ticket tool and watch the local agent screen update;
5. stage and finalize one valid help document, then reject one invalid document;
6. exceed the rate limit and wait for a successful new-window rollover;
7. inspect structured console logs and `metric_emitted` markers; and
8. restart the local server, sign back in, and prove tickets and staged files remain.

## Verification matrix

| Check | Expected local result |
|---|---|
| Signed-out caller invokes a protected method | Denied |
| Customer invokes an agent-only ticket or upload method | Denied by backend role check |
| Agent stages and finalizes a valid small help document | File appears in the protected local staging list |
| Oversized or invalid staged document is finalized | Object is deleted/quarantined and never marked ready |
| Customer asks a corpus-specific question | Retrieved answer/tool result identifies the local source |
| Newly staged document has no ingestion workflow | App does not falsely present it as searchable |
| Customer asks to escalate | Agent tool creates one owned ticket |
| Local agent ticket screen is open | New tool-created ticket appears live |
| Customer requests another customer's ticket | Not returned |
| Agent endpoint exceeds its configured window | Rejected before Agent invocation |
| Concurrent requests hit the limiter | Conditional updates keep the count bounded |
| The clock enters a new limit window | A new key accepts requests even if the old TTL record remains |
| Operational event occurs | Structured console log and safe metric marker appear |
| Local server restarts | Tickets, auth fixture state, and staged files remain available |

## Definition of done

- [ ] The entire application runs with `npm run dev` and no AWS account or credentials.
- [ ] The facilitator's local customer and agent identities prove both allowed and denied role paths.
- [ ] Customer ownership checks use `requireAuth`; support-only methods use the local `agent` group and `requireRole`.
- [ ] Customers create and list only their own local `DistributedTable` tickets.
- [ ] Agents receive ticket snapshots live and can perform agent-only updates.
- [ ] An agent stages and finalizes a help document through protected local `FileBucket` methods.
- [ ] The app clearly distinguishes staged uploads from the indexed local Knowledge Base corpus.
- [ ] `KnowledgeBase` retrieves a distinctive answer from the reviewed local corpus.
- [ ] The tested local Agent path preserves the customer's real retrieval query, returns a source-grounded result, and has a ticket-creation tool; raw canned placeholder arguments are not accepted as proof.
- [ ] A tool-created ticket appears live in the local agent view.
- [ ] Conversation reads verify authenticated ownership.
- [ ] A composite-key, conditional-write rate limiter rejects excess Agent requests and rolls into a new window correctly.
- [ ] `Logger` output and metric-emission markers are visible without leaking sensitive content.
- [ ] Local tickets and staged files survive a development-server restart.
- [ ] The frontend uses only typed `aws-blocks` exports.

## Demo evidence

Show the facilitator, using only local browser and terminal windows:

1. a customer denied from an agent-only operation;
2. an agent staging and finalizing a help document;
3. a local corpus result with its source;
4. the tested local Agent path creating a ticket through its tool;
5. that ticket appearing live on the local agent screen;
6. a rate-limit rejection and successful rollover;
7. structured console logs and metric-emission markers; and
8. persisted data after a local restart.

Explain why the FileBucket staging path is not automatically a Knowledge Base ingestion path.

## Local cleanup

Stop the local development process when finished. Keep `.bb-data/` to resume later, or delete it only when you intentionally want to reset mock users, tickets, rate windows, and staged files. No AWS cleanup is required.

## Optional extensions — not required

- If the deterministic adapter was used for completion, optionally configure a tool-capable Ollama model and compare its query/tool behavior.
- Add customer ticket attachments with ownership-checked local upload/download/finalize methods.
- Trigger notifications with `AsyncJob` and inspect the local output.
- Add SLA checks with local `CronJob`.
- After every local check passes, optionally try `npm run sandbox` or `npm run deploy` to compare Cognito, Bedrock, S3, WebSocket, and CloudWatch behavior. Destroy any resources immediately afterward.
- Build an explicit S3-to-Knowledge-Base ingestion workflow only as a cloud extension.
- Add `Tracer` and a `Dashboard` for a later deployed environment.
- Move reporting to `DistributedDatabase` or `Database` when joins and ad hoc filtering justify SQL.

## Hints

- Complete one vertical slice—customer creates a ticket and agent sees it—before adding retrieval or Agent behavior.
- Keep ticket creation in one reusable backend service so portal and tool behavior cannot drift.
- Use complete snapshots for Realtime ticket updates.
- Keep upload staging separate from corpus promotion and ingestion.
- Make rate-limit retries bounded; an endless retry loop becomes its own availability problem.
- Do not rely on raw canned string arguments for retrieval. Use the facilitator-tested local model or deterministic query-preserving adapter.
