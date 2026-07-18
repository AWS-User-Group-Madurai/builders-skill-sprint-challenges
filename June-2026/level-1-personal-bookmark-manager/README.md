# Level 1 — Personal Bookmark Manager

- **Difficulty:** Beginner
- **Target time:** 45–60 minutes
- **Target environment:** Local AWS Blocks mocks; no AWS account required

This track is independent. Start from a fresh copy of the facilitator scaffold; no work from another level is required.

## Mission

Build a private bookmark manager where people sign up, sign in, save useful links, list them, and delete them. Every signed-in user sees only their own bookmarks, and the records persist across page refreshes and local server restarts.

## Blocks and primitives

| Item | Why you need it |
|---|---|
| `AuthBasic` | Username/password signup, signin, sessions, and the `Authenticator` UI |
| `DistributedTable` | Schema-validated bookmark records grouped by user |
| `Scope` | Stable application and resource boundary |
| `ApiNamespace` | Typed methods imported directly by the frontend |

## Read before building

Read these files from the installed scaffold:

```text
node_modules/@aws-blocks/blocks/docs/core.md
node_modules/@aws-blocks/blocks/docs/auth-common.md
node_modules/@aws-blocks/blocks/docs/bb-auth-basic.md
node_modules/@aws-blocks/blocks/docs/bb-distributed-table.md
```

Use the signatures in the installed docs rather than copying code for a different package version.

## Required user experience

A visitor can:

1. sign up and sign in;
2. submit a URL, title, and tag;
3. see their saved bookmarks;
4. delete one of their bookmarks; and
5. sign out.

A signed-out visitor cannot read or change bookmark data. Signing in as another user shows a different collection.

## Suggested data design

Define the bookmark record with a schema. It should contain at least:

| Field | Purpose |
|---|---|
| `userId` | Server-derived owner and partition key |
| `bookmarkId` | Server-generated unique sort key |
| `url` | Valid bookmark URL |
| `title` | Human-readable label |
| `tag` | Simple category |
| `createdAt` | Sortable creation timestamp |

Use `userId` as the partition key and `bookmarkId` as the sort key. Never accept `userId` from the frontend.

## Build milestones

### 1. Reset and run the scaffold

Remove the sample application's behavior while preserving its generated configuration, scripts, and import aliases. Run `npm install`, then `npm run dev`, and confirm both frontend and backend start.

### 2. Add authentication

- Create an `AuthBasic` instance with a stable Block ID.
- Export the API returned by `auth.createApi()` so the frontend can use it.
- Render the provider-agnostic `Authenticator` component.
- React to authentication state changes: show the bookmark app only to signed-in users and clear protected UI state on signout.

Hiding a button is not authorization. The backend checks in the next milestone are mandatory.

### 3. Add the bookmark table

- Define a Zod schema for the bookmark record.
- Create a `DistributedTable` with the user partition and bookmark sort key.
- Generate bookmark IDs and timestamps on the backend.

Local table data should be managed by the Block under `.bb-data/`. Do not create your own JSON file.

### 4. Export the typed bookmark API

Expose methods equivalent to:

- `createBookmark(input)`;
- `listBookmarks()`; and
- `deleteBookmark(bookmarkId)`.

At the top of **every** method:

1. call `auth.requireAuth(context)`;
2. derive the owner ID from that returned user; and
3. build every table key or query with that server-derived ID.

For deletion, a bookmark ID alone is not enough. Combine it with the authenticated user's ID so one user cannot delete another user's record.

### 5. Build the frontend

- Import the exported auth API and bookmark API from `aws-blocks`.
- Add a form with URL, title, and tag validation.
- Render loading, empty, success, and error states.
- Refresh the list after a successful create or delete.
- Do not call the backend with `fetch`.

### 6. Prove privacy and persistence

Use a normal browser window and a private/incognito window to create two separate users.

| Check | Expected result |
|---|---|
| Call a bookmark method while signed out | Rejected as unauthenticated |
| User A creates a bookmark | It appears for User A |
| Refresh the page | The bookmark remains |
| Restart the local dev process and sign in again | The bookmark remains in the local Block data |
| Sign in as User B | User A's bookmark is absent |
| User B tries User A's known bookmark ID | Read/delete is not possible |

## Definition of done

- [ ] Signup, signin, signout, and auth-state rendering work.
- [ ] URL, title, and tag are stored as a schema-validated table record.
- [ ] Create, list, and delete run through the typed `aws-blocks` import.
- [ ] Every bookmark API method calls `requireAuth`.
- [ ] The backend derives `userId`; the browser never chooses it.
- [ ] Bookmark data survives a refresh and local server restart.
- [ ] Two test users cannot view or delete each other's bookmarks.
- [ ] No application persistence uses an array, direct file write, or local database.

## Demo evidence

Show the facilitator:

1. the app while signed out;
2. User A's bookmark list;
3. a different list for User B; and
4. the bookmark still present after a restart.

Also point to one API method and explain where authentication and ownership are enforced.

## If you have time

- Add an index that supports listing by tag and creation time.
- Add client-side filtering or sorting by tag.
- Export the signed-in user's bookmarks as downloaded JSON. The export method must still authenticate and query the data Block; do not read `.bb-data/` directly.
- Add edit support with an ownership-safe key.

## Hints

- Exporting the auth API and rendering an `Authenticator` are separate steps; both are needed.
- Prefer `requireAuth` to a nullable user lookup for protected methods.
- Query the user partition instead of scanning the whole table.
- If the frontend import does not expose a method, check that its `ApiNamespace` is exported from `aws-blocks/index.ts`.
