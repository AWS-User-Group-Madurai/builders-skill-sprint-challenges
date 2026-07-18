# Builders Skill Sprint — June 2026

## AWS Blocks Workshop: Three Apps, Three Levels

Choose the one level that matches your experience and build that application with AWS Blocks. The levels are independent: you do not need to complete Level 1 before Level 2 or Level 3. If none of the prescribed apps fits your interests, use the Open Project track and propose an app with equivalent complexity.

**The complete required workshop runs locally with `npm run dev`. No AWS account, credentials, or deployment is needed for any level.** AWS sandbox and deployment work is optional extension material only.

There is no score. Every track has a concrete local definition of done and ends with something working and demoable.

## Tracks at a glance

| Track | Application | Best for | Main Blocks | Required environment |
|---|---|---|---|---|
| [Level 1](level-1-personal-bookmark-manager/README.md) | Personal Bookmark Manager | First AWS Blocks app and private CRUD | `AuthBasic`, `DistributedTable` | Local mocks |
| [Level 2](level-2-live-polls/README.md) | Live Polls | Multi-user state, concurrency, and realtime | `AuthBasic`, `DistributedTable`, `Realtime`, `CronJob` or `AsyncJob` | Local mocks |
| [Level 3](level-3-ai-help-desk/README.md) | AI Help Desk | AI, role authorization, uploads, and operations | `AuthCognito`, `DistributedTable`, `FileBucket`, `KnowledgeBase`, `Agent`, `Realtime`, observability | Local mocks |
| [Open Project](open-project/README.md) | Your own idea | A self-directed app at one of the three complexity bands | Match the selected band | Local mocks |

Watch our [AWS Blocks session recording](https://www.youtube.com/watch?v=9ch17B2QQqk&t=5487s) for a practical walkthrough and demonstration of building with AWS Blocks.

## Learning outcomes

By the end of your chosen track, you will have:

- shipped a working full-stack application entirely on your machine;
- composed backend capabilities from AWS Blocks instead of wiring infrastructure by hand;
- called backend methods from the frontend through the typed `api` import;
- protected user data at the API boundary;
- persisted application state through local Block implementations;
- exercised applicable auth, realtime, background, file, retrieval, and Agent behavior locally; and
- understood which AWS services the same Blocks map to without needing to deploy them.

## Prerequisites

- Node.js 22 or later and npm 10 or later.
- The starter scaffold supplied by the facilitators.
- A TypeScript-capable editor. **AWS Blocks currently supports TypeScript only.**
- For Level 3, a facilitator-provided local `AuthCognito` fixture with one customer identity and one identity in the `agent` group.
- For Level 3, either a facilitator-tested tool-capable local model or a deterministic local adapter that preserves the customer's original question when invoking `searchHelpDocs`. The raw canned provider alone is not sufficient for grounded-answer evidence.

Check your local versions:

```bash
node --version
npm --version
```

You do **not** need the AWS CLI, an AWS account, AWS credentials, CDK bootstrap, or a cloud budget for the required workshop.

## Optional: AWS Blocks Kiro Power

Kiro users can install the [Custom Kiro Power for AWS Blocks](https://github.com/awsdataarchitect/aws-blocks). It gives Kiro AWS Blocks-specific scaffolding guidance, implementation patterns, type-safe frontend wiring, and troubleshooting so participants can describe an app in plain English and build it with the appropriate Blocks. The Power is optional and does not change this workshop's local-only requirements.

In Kiro, open **Powers → Add Custom Power → Import from GitHub**, then enter `https://github.com/awsdataarchitect/aws-blocks`. See the [Kiro Powers documentation](https://kiro.dev/docs/powers/) for more information.

## Start here

1. Copy the facilitator scaffold into your own working directory.
2. Keep its generated configuration and scripts, but remove the sample application's backend and frontend behavior.
3. From the scaffold directory, install dependencies:

   ```bash
   npm install
   ```

4. Start the complete local development loop:

   ```bash
   npm run dev
   ```

5. Open the URL printed by the scaffold, normally `http://localhost:3000`.
6. Read the documentation for every Block before using it. Start with:

   ```text
   node_modules/@aws-blocks/blocks/docs/index.md
   node_modules/@aws-blocks/blocks/docs/core.md
   node_modules/@aws-blocks/blocks/docs/<block-doc>.md
   ```

The installed package documentation is the source of truth for the API version in your scaffold.

## Ground rules for every track

1. **Use the typed transport.** The frontend calls the backend only through exports imported from `aws-blocks`. Do not write `fetch`, construct JSON-RPC payloads, or curl REST-style routes.
2. **Persist through Blocks.** Application records and files must go through a data or storage Block. Do not write application persistence directly to local files, arrays, or a local database.
3. **Authorize at the endpoint.** Every API method that reads or changes protected data starts with `auth.requireAuth(context)` or `auth.requireRole(context, role)`. API methods are public by default.
4. **Derive identity on the server.** Never accept `userId`, owner, or role from the browser when it can be derived from the authenticated session.
5. **Export the API.** Every API namespace used by the frontend must be exported from `aws-blocks/index.ts`.
6. **Validate data.** Define persistent records and tool inputs with the schema library used by the scaffold, normally Zod.
7. **Keep Block IDs stable.** Stable IDs preserve local data and prevent destructive replacements if the app is deployed later.
8. **Finish locally.** Every required completion check must pass under `npm run dev`; cloud deployment cannot be used as a substitute for a missing local workflow.

## Folder structure

```text
June-2026/
├── README.md
├── level-1-personal-bookmark-manager/
│   └── README.md
├── level-2-live-polls/
│   └── README.md
├── level-3-ai-help-desk/
│   └── README.md
└── open-project/
    └── README.md
```

The challenge folders contain instructions rather than duplicate applications. Start each track from a fresh copy of the same facilitator scaffold.

## AWS Blocks catalog and AWS service mapping

The runtime catalog and primary service mappings below are based on the official [What is AWS Blocks?](https://docs.aws.amazon.com/blocks/latest/devguide/what-is-blocks.html) guide. The current package also documents deployment components and core primitives; always compare this table with `node_modules/@aws-blocks/blocks/docs/index.md` because the installed version may evolve. Content was rephrased for compliance with licensing restrictions.

The AWS service column is a learning reference, not a list of workshop prerequisites.

### Runtime Blocks

| Category | Block | What it provides | Local implementation | Primary AWS service(s) |
|---|---|---|---|---|
| Data and storage | `KVStore` | Key/value reads, writes, deletes, and guarded updates | Disk-backed mock under `.bb-data/` | Amazon DynamoDB |
| Data and storage | `DistributedTable` | Schema-validated records, keys, indexes, and queries | Disk-backed mock under `.bb-data/` | Amazon DynamoDB |
| Data and storage | `Database` | Full PostgreSQL behavior and Kysely queries | PGlite | Amazon Aurora Serverless v2 or an existing PostgreSQL database |
| Data and storage | `DistributedDatabase` | Serverless SQL for workloads that do not need full PostgreSQL features | PGlite | Amazon Aurora DSQL |
| Data and storage | `FileBucket` | File upload, download, deletion, and presigned URLs | Local filesystem behind the Block API | Amazon S3 |
| Authentication | `AuthBasic` | Username/password authentication and signed sessions | Local JWT sessions | Amazon DynamoDB plus signed JWT cookies |
| Authentication | `AuthCognito` | Managed authentication with groups, MFA, and passkeys | Local provider mock | Amazon Cognito |
| Authentication | `AuthOIDC` | Sign-in through an external identity provider | Real configured IdP, or an explicitly selected in-process stub | Amazon DynamoDB and AWS Systems Manager Parameter Store, plus the external OIDC/OAuth provider |
| Compute and background | `AsyncJob` | Programmatically submitted background work | In-process queue/handler | Amazon SQS and AWS Lambda |
| Compute and background | `CronJob` | Recurring or scheduled handlers | In-process timers | Amazon EventBridge Scheduler and AWS Lambda |
| AI | `Agent` | Conversational AI, tools, streaming, and persisted conversations | Canned provider or configured local model | Amazon Bedrock |
| AI | `KnowledgeBase` | Semantic retrieval over a document corpus | Local document parsing and retrieval cache | Amazon Bedrock Knowledge Bases with Amazon S3/S3 Vectors |
| Communication | `Realtime` | Typed WebSocket pub/sub channels | Local WebSocket server | Amazon API Gateway WebSocket APIs and Amazon DynamoDB |
| Communication | `EmailClient` | Transactional email | Console/log capture | Amazon SES |
| Configuration | `AppSetting` | Configuration values and secrets | Disk-backed mock under `.bb-data/settings/` | AWS Systems Manager Parameter Store |
| Observability | `Logger` | Structured, contextual logs | Console output | Amazon CloudWatch Logs |
| Observability | `Metrics` | Custom application metrics | Local no-op; pair with a structured log for workshop-visible proof | Amazon CloudWatch |
| Observability | `Tracer` | Request and operation traces | Local no-op behavior | AWS X-Ray |
| Observability | `Dashboard` | Generated operational dashboard | No local cloud dashboard | Amazon CloudWatch dashboards |

### Deployment components

These are optional deployment-layer components rather than runtime requirements.

| Component | What it provides | Local equivalent | Primary AWS service(s) |
|---|---|---|---|
| `Hosting` | Static, SPA, or SSR frontend hosting | Framework development server | Amazon CloudFront and Amazon S3; AWS Lambda for applicable SSR workloads |
| `Pipeline` | Branch-based, self-updating delivery pipelines | No local runtime equivalent | AWS CodePipeline V2, AWS CodeBuild, and AWS CodeConnections |

`Hosting` is documented in the CDK layer. `Pipeline` is available in current package documentation but may not appear in older versions of the public catalog.

### Core primitives used by every app

| Primitive | Purpose | AWS mapping if deployed later |
|---|---|---|
| `Scope` | Groups Blocks and gives resources stable identities | No standalone service; it defines the application resource boundary |
| `ApiNamespace` | Exposes typed backend methods to the frontend | AWS Lambda behind Amazon API Gateway |

## Required local mode and optional cloud modes

Only the first row is required for this workshop.

| Command | Role in this workshop | AWS account | Frontend |
|---|---|---|---|
| `npm run dev` | **Required:** runs the complete app with local Block implementations | Not required | Local development server |
| `npm run sandbox` | Optional extension: validate the backend against real AWS services | Required | Usually remains local |
| `npm run deploy` | Optional extension: create a hosted cloud deployment | Required | Hosted when `Hosting` is configured |

If you choose an optional cloud extension, use the exact generated scripts from the scaffold and destroy the resources afterward.

## Common mistakes facilitators will check

- An endpoint exposes user data without calling `requireAuth` or `requireRole`.
- The browser sends a `userId` that the backend trusts.
- Application state is kept in an array or written directly to disk instead of using a Block.
- The frontend bypasses the typed import with `fetch` or a hand-built JSON-RPC request.
- An API namespace is created but not exported.
- A vote tally changes before the one-vote conditional write succeeds.
- `Database` is selected even though `DistributedTable` satisfies the access patterns.
- A participant assumes `AuthBasic` supplies groups; use the local `AuthCognito` mock when native roles/groups are required.
- A participant assumes uploading a file to `FileBucket` automatically re-indexes a `KnowledgeBase`.
- A participant expects local `Metrics` to display CloudWatch output; the local workshop pairs each metric call with a safe structured log marker.
- A participant deploys to AWS to avoid completing a required local behavior.
- A Block ID is renamed casually and its local data appears to disappear.

## Local data and cleanup

The required workshop creates no AWS resources and therefore incurs no AWS charges.

- Stop the local development process when finished.
- Local Block state survives restarts under `.bb-data/`.
- Keep `.bb-data/` when you want to resume, or delete it when you intentionally want a clean local reset.
- Do not commit local mock users, uploaded files, or application data.

If you independently choose an optional AWS sandbox or deployment, destroy it with the scaffold's cleanup script and confirm its CloudFormation stack and retained data are gone.

## Resources

- [What is AWS Blocks?](https://docs.aws.amazon.com/blocks/latest/devguide/what-is-blocks.html)
- [AWS Blocks package on npm](https://www.npmjs.com/package/@aws-blocks/blocks)
- Installed reference: `node_modules/@aws-blocks/blocks/docs/index.md`

Pick a track, define your local proof of completion, and start with the smallest working vertical slice.
