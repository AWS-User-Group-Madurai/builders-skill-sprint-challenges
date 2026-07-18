# Open Project — Build Your Own AWS Blocks App

Use this track when you have an idea that fits the workshop but not one of the three prescribed applications. Your project is independent and starts from a fresh facilitator scaffold.

There is no score. Agree on a complexity band and a local definition of done with a facilitator before writing code. Every band must be fully demonstrable with `npm run dev`; AWS deployment is optional.

## 1. Choose a complexity band

| Band | Target time | Minimum composition | Required runtime | Example ideas |
|---|---:|---|---|---|
| Level 1 equivalent | 45–60 min | Auth, one data Block, `ApiNamespace` | Local mocks | Habit tracker, private reading list, personal inventory |
| Level 2 equivalent | 60–90 min | Auth, durable data, `Realtime`, plus `CronJob` or `AsyncJob` | Local mocks | Live auction, collaborative queue, multiplayer quiz, incident room |
| Level 3 equivalent | 90+ min | Role authorization, durable data, at least one AI or advanced data capability, realtime/background work, and observability | Local mocks | AI research assistant, document triage desk, operations copilot |

Equivalent complexity matters more than copying the examples. A large UI around one public endpoint is not a Level 3 project.

## 2. Read the catalog

Use the full Block-to-AWS-service table in the [June workshop README](../README.md#aws-blocks-catalog-and-aws-service-mapping), then read the installed documentation for every selected Block:

```text
node_modules/@aws-blocks/blocks/docs/index.md
node_modules/@aws-blocks/blocks/docs/<selected-block>.md
```

Prefer `DistributedTable` unless your access patterns genuinely need SQL joins, broad ad hoc filters, large transactions, foreign keys, triggers, or an existing PostgreSQL database.

## 3. Pitch the project

Fill in this short project brief and show it to a facilitator:

```markdown
# Project brief

## Problem
Who has what problem?

## Demo story
In three to five steps, what will the audience see?

## Complexity band
Level 1 / Level 2 / Level 3 equivalent

## Blocks
| Block | Why it is needed | Local behavior | AWS service mapping |
|---|---|---|---|
| ... | ... | ... | ... |

## Users and authorization
- User types:
- Protected operations:
- Ownership or role checks:

## Data and access patterns
- Records/files:
- Keys and indexes:
- Concurrency rule:

## Typed API
- methodName(input) -> output

## Local definition of done
- [ ] Observable behavior 1
- [ ] Negative/security behavior 2
- [ ] Persistence/realtime/background behavior 3

## Local runtime and reset
- Required command: npm run dev
- Test identities or fixtures:
- Data reset strategy:

## Optional cloud extension
- Not required / planned service to validate:
```

A facilitator should be able to answer these questions from the brief:

- Why does each Block exist?
- Which backend methods are protected?
- How is identity derived?
- What proves data is durable locally?
- What race or failure case matters?
- What will be shown in the final local demo?

## 4. Follow the workshop ground rules

1. The frontend calls only typed exports imported from `aws-blocks`.
2. Application persistence uses data and storage Blocks, never direct files, arrays, or a local database.
3. Protected API methods call `requireAuth` or `requireRole` on the backend.
4. User identity, ownership, and roles come from the authenticated session, not browser input.
5. Persistent records and tool inputs use schemas.
6. Every frontend-used API namespace is exported from `aws-blocks/index.ts`.
7. Block IDs remain stable so local state remains attached to the same resources.
8. Every required check passes locally; cloud deployment cannot replace missing local behavior.

## 5. Build one vertical slice at a time

Recommended order:

1. **Walking skeleton:** render the frontend and call one typed API method.
2. **Identity:** sign in and prove one protected method rejects a signed-out caller.
3. **Persistence:** write and read one real record through a local Block implementation.
4. **Core workflow:** complete the smallest useful end-to-end user action.
5. **Complexity feature:** add the local realtime, background, AI, file, or SQL behavior required by your band.
6. **Failure path:** test duplicate, concurrent, unauthorized, expired, or invalid behavior.
7. **Restart/reconnect:** prove the app recovers from a page refresh, local server restart, or Realtime reconnect as appropriate.
8. **Demo:** reset to a known local state and rehearse a three-minute flow.

## Definition of done — all projects

- [ ] The project brief names a user problem and a short demo story.
- [ ] The selected Blocks match the agreed complexity band.
- [ ] The complete application runs locally with `npm run dev` and no AWS credentials.
- [ ] The frontend uses typed `aws-blocks` imports with no manual transport code.
- [ ] All protected methods enforce authentication or roles in the backend.
- [ ] Persistent state goes through a Block and survives the required local restart test.
- [ ] At least one negative path is demonstrated, not only the happy path.
- [ ] The final local behavior matches the project's written definition of done.
- [ ] A local reset strategy is documented and tested.

## Additional proof by band

### Level 1 equivalent

- [ ] Two users cannot cross an ownership boundary.
- [ ] Data remains after a page refresh and local server restart.

### Level 2 equivalent

- [ ] Two local clients observe the same realtime state.
- [ ] A concurrency invariant uses a conditional write or equivalent server-side mechanism.
- [ ] Scheduled or asynchronous behavior completes in the local process.
- [ ] A reconnect reloads canonical state from a durable Block.

### Level 3 equivalent

- [ ] A local auth fixture proves role-restricted behavior is denied to the wrong role.
- [ ] Local AI/data/file capabilities are authorized and grounded in durable state. If AI must preserve user text in tool arguments, use a tested local model or deterministic adapter rather than raw canned placeholders.
- [ ] Abuse or expensive work has a bounded control such as a table-backed rate limiter.
- [ ] Structured logs are visible, and local metric-emission evidence is shown without requiring CloudWatch.
- [ ] The complete advanced demo works with local Block implementations.

## Demo evidence

Prepare a three-minute local demonstration containing:

1. the user problem;
2. one complete happy path;
3. one denied or failure path;
4. the local feature that establishes the selected complexity band; and
5. persistence, background, or reconnect evidence appropriate to the app.

End by naming both the local implementations used and the AWS services those Blocks would map to if deployed later.

## Common scope traps

- Selecting many Blocks without completing one usable flow.
- Spending most of the session on visual styling.
- Choosing SQL before writing down access patterns.
- Calling an Agent without grounding, authorization, a bounded control, or a useful action.
- Treating a hidden button as security.
- Adding realtime deltas that cannot recover after a reconnect.
- Depending on an AWS-only behavior for the required demo.
- Expecting local `Metrics`, `Tracer`, or `Dashboard` to provide a cloud console; design local evidence instead.

## If you finish early

Improve reliability rather than adding random features:

- add an idempotency or optimistic-concurrency rule;
- make realtime updates reconnect-safe;
- add a background notification;
- add structured local operational evidence;
- write one focused end-to-end test; or
- optionally validate the unchanged backend with `npm run sandbox` and clean it up afterward.
