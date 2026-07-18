# Level 2 — Live Polls

- **Difficulty:** Intermediate
- **Target time:** 60–90 minutes
- **Target environment:** Local AWS Blocks mocks; no AWS account required

This track is independent. Start from a fresh facilitator scaffold; the bookmark app is not a prerequisite.

## Mission

Build a multi-user polling app entirely on your machine. A signed-in user creates a poll, people vote once, every connected screen receives updated results in realtime, and the selected background path completes under `npm run dev`.

## Blocks and primitives

| Item | Why you need it |
|---|---|
| `AuthBasic` | Identifies poll creators and voters |
| `DistributedTable` | Stores polls and immutable per-user votes |
| `Realtime` | Pushes result snapshots to connected local clients |
| `CronJob` | Option A: periodically closes polls whose deadline has passed |
| `AsyncJob` | Option B: computes a result summary after an explicit close |
| `Scope`, `ApiNamespace` | Composes the backend and exports typed methods |

Choose `CronJob` **or** `AsyncJob`; you do not need both for the core challenge. Both have local implementations.

## Read before building

```text
node_modules/@aws-blocks/blocks/docs/core.md
node_modules/@aws-blocks/blocks/docs/bb-auth-basic.md
node_modules/@aws-blocks/blocks/docs/bb-distributed-table.md
node_modules/@aws-blocks/blocks/docs/bb-realtime.md
node_modules/@aws-blocks/blocks/docs/bb-cron-job.md
node_modules/@aws-blocks/blocks/docs/bb-async-job.md
```

Pay particular attention to conditional writes, Realtime channel scoping, and the local behavior of your chosen background Block.

## Required user experience

A signed-in user can create a poll with a question, at least two options, and a close time. Signed-in users can open the poll, vote once, and watch counts update without refreshing. A closed poll rejects new votes.

## Suggested data design

Use two `DistributedTable` instances so each access pattern is explicit.

### Poll record

| Field | Purpose |
|---|---|
| `pollId` | Poll identity and partition key |
| `ownerId` | Server-derived creator |
| `question` | Poll prompt |
| `options` | Stable option IDs and labels |
| `status` | `open` or `closed` |
| `closesAt` | Configured deadline timestamp |
| `closedAt` | Effective close timestamp once closed |
| `createdAt` | Creation timestamp |
| `revision` | Required monotonic value for concurrency and result ordering |
| `summary` | Optional final result from the background path |

Define an index such as `byStatusAndClose` with `status` as its partition key and `closesAt` as its sort key. The Cron path can then query `status = open` with a deadline up to the current time instead of scanning the table.

### Vote record

| Field | Purpose |
|---|---|
| `pollId` | Vote partition key |
| `userId` | Authenticated voter and sort key |
| `optionId` | Selected option |
| `votedAt` | Server-generated vote acceptance timestamp |

The `{ pollId, userId }` key makes one vote per user representable as one record.

## Build milestones

### 1. Add auth and poll creation

- Configure and export `AuthBasic` plus its frontend API.
- Create a protected method that accepts question, options, and close time.
- Validate at least two non-empty, uniquely identified options.
- Derive `ownerId` on the backend.
- Initialize `revision` on the backend and return a server-generated `pollId`.

### 2. Implement one vote per user

Your vote method must perform this order:

1. authenticate the caller and capture a server-side `votedAt`;
2. load the poll and reject missing, closed, or expired polls;
3. validate that `optionId` belongs to the poll;
4. reserve the vote with `{ ifNotExists: true }`;
5. translate a conditional-write failure into a useful "already voted" response;
6. re-read the poll after the reservation; if it closed at or before `votedAt`, conditionally delete that exact reservation and reject the vote;
7. increment the poll `revision` with `{ ifFieldEquals: { revision: previousRevision } }`, retrying bounded concurrency conflicts; and
8. calculate and publish a canonical tally tagged with the successful revision.

A read such as "does a vote exist?" followed by an unconditional write is not sufficient; two concurrent requests can both pass the read. The conditional reservation enforces one vote per user. The post-reservation poll check coordinates an in-flight vote with closure: a vote linearized before `closedAt` is included, while a later one is removed and rejected.

### 3. Produce an ordered, recoverable tally

For a workshop-sized poll, query the vote partition and count option IDs. If the poll is closed, exclude any record whose server timestamp is not earlier than `closedAt`. Publish a full result snapshot rather than an increment so reconnecting clients and retries cannot double-apply a delta.

A result snapshot should contain at least the poll ID, counts by option, total votes, status, `revision`, and update time. Clients apply only snapshots with a revision greater than the last applied revision, so an older concurrent publish cannot overwrite newer state.

Realtime delivery is best-effort. Load a canonical snapshot from the durable tables on first render and after reconnect; do not use the WebSocket stream as the system of record.

### 4. Add local realtime results

- Define a schema for revisioned result messages.
- Use one channel per `pollId` in a results namespace.
- Protect the API method that grants or returns channel access.
- Subscribe and wait for the local connection before relying on incoming updates.
- Publish after a successful vote and after a poll changes to closed.
- Load one durable initial snapshot and refresh it after a disconnect.

### 5. Add one local background path

#### Option A — scheduled close with `CronJob`

Run a recurring sweep, such as once per minute. The local Cron implementation runs its schedule in the development process. Query the `byStatusAndClose` index for due, open polls. Close each poll with an optimistic condition on its current status/revision, set `closedAt` to its configured deadline, increment the revision, and publish a canonical final snapshot. Make the handler idempotent because scheduled work can run more than once.

#### Option B — result summary with `AsyncJob`

Allow the poll owner to close the poll through an authenticated, ownership-checked method. Conditionally change the open poll to closed, set `closedAt` from the server clock, and increment its revision. After that write succeeds, submit a local background job that calculates and stores a final summary, then publishes it. The request should not perform the summary work inline.

`AsyncJob` is programmatic, not a delayed scheduler. Do not claim that it automatically waits until `closesAt`; use `CronJob` if deadline-driven automatic closure is part of your demo.

### 6. Build the frontend

Provide:

- an authenticated create-poll form;
- a poll view with disabled states for closed polls and completed votes;
- visible errors for duplicate or late votes;
- a live tally view; and
- a clear connection/loading state.

All calls and channel acquisition go through typed exports from `aws-blocks`.

### 7. Validate the complete app locally

Run only:

```bash
npm run dev
```

Use two browser contexts. If both voters need different identities, use an incognito window or a separate browser profile.

| Check | Expected result |
|---|---|
| User A creates a poll | A valid poll opens |
| User A and User B view it | Both receive an initial tally |
| User A votes | Both screens update in about one second |
| User A submits another vote, including concurrently | Conditional write rejects it; tally does not change |
| User B votes | Both screens update once |
| Chosen local close/summary path runs | Poll state and final snapshot update |
| Anyone votes after closure | Vote is rejected |
| One client disconnects and reconnects | It reloads the canonical durable snapshot |
| Local server restarts | Poll and vote records remain under `.bb-data/` |

## Definition of done

- [ ] The complete app and background path run under `npm run dev` without AWS credentials.
- [ ] Only authenticated users can create polls or vote.
- [ ] Polls and votes live in local `DistributedTable` records.
- [ ] The vote record uses a conditional `ifNotExists` write.
- [ ] A duplicate or concurrent second vote is rejected without changing counts.
- [ ] Two local browser contexts receive the same result snapshot within about one second.
- [ ] Realtime channel access is scoped and granted through a protected API method.
- [ ] A local `CronJob` closes due polls, or a local `AsyncJob` computes the final summary after an authorized close.
- [ ] Revision checks prevent stale snapshots from replacing newer state.
- [ ] Closed polls reject votes.
- [ ] Reconnects recover from durable data, and local records survive a server restart.
- [ ] The frontend uses only typed `aws-blocks` exports.

## Demo evidence

Show the facilitator:

1. two local browser contexts;
2. one vote updating both screens;
3. a rejected second vote by the same user;
4. the chosen local background path completing;
5. a disconnect/reconnect loading the canonical snapshot; and
6. persisted poll state after a local server restart.

Be ready to point to the conditional write and explain why it prevents a race.

## Local cleanup

Stop the local development process when finished. Keep `.bb-data/` to resume later, or delete it only when you intentionally want to reset the workshop app. No AWS cleanup is required.

## Optional AWS extension — not required

After the local definition of done is complete, you may validate the unchanged backend with:

```bash
npm run sandbox
```

A sandbox uses real AWS backend services but normally leaves the frontend local. A hosted frontend requires the scaffold's full deploy path. If you choose either extension, destroy its resources afterward with the corresponding generated cleanup script.

## If you have time

- Add typed presence showing how many people are viewing a poll.
- Email the owner a final summary with `EmailClient`; locally, inspect the captured/console output.
- Add an end-to-end test in `test/e2e.test.ts` for the conditional vote rule.
- Add a shareable poll list while keeping create and vote protected.
- Try the optional AWS sandbox only after every local check passes.

## Hints

- Do not publish a tally when the conditional vote write fails.
- Publish snapshots, not `+1` messages.
- Channel credentials are scoped; do not reuse one poll's access for another poll.
- Keep option IDs stable even if labels are edited.
- Test the duplicate vote using simultaneous requests, not only two slow button clicks.
