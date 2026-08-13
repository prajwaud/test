# Test log - what is actually proven

Written 2026-08-13. Read this before redoing any of it. Several of these findings cost
real time to establish and are not obvious from documentation.

Epistemic tags: [Certain] = directly observed. [Likely] = strong inference.
[Unknown] = genuinely untested, do not assume.

---

## Test C - can Claude Code reach the governed M365 connector

**Result: green, with a caveat about which surface was tested.**

[Certain] A Claude Code Remote (cloud) session reached the WCP Microsoft 365 connector as
praj@waudcapital.com. `get_me` returned the correct identity and `outlook_calendar_search`
returned live events.

[Certain] The connector was already attached to the session rather than added via
`claude mcp add`. The local-CLI bootstrap path described in the original Test C doc
(`claude mcp add` then `/mcp` browser OAuth) was never exercised. If someone needs to know
whether a fresh local terminal can bootstrap the connector, that is still untested.

---

## Test D - can a scheduled unattended run hold auth and send

**Result: red on send. The blocker is a permission gate, not OAuth.**

This took several wrong turns. The findings in order of how much time they save:

### 1. [Certain] The send call requires a human to click Approve

`mcp__Microsoft_365__outlook_send_mail` surfaces an interactive permission prompt
("Allow Claude to use Outlook send mail?"). Confirmed twice, and confirmed by the user
directly: "yes it needed a human click."

This is the actual blocker for unattended delivery. It is not an OAuth failure, not a 401,
and not a connector provisioning gap. Diagnosing it as any of those wastes time.

### 2. [Certain] Read tools do not prompt; write tools do

`get_me`, `outlook_calendar_search`, and `outlook_email_search` all passed through with no
prompt in an unattended scheduled run. Only the send was gated.

### 3. [Certain] `create_trigger` cannot attach connectors for this org

Passing `connectors: ["Microsoft 365"]` to the Claude Code Remote `create_trigger` MCP tool
returns a hard error: *"the connectors parameter is not available for this organization."*

Consequence: a trigger created with `create_new_session_on_fire: true` fires a session with
**no** `mcp__<server>__*` tools at all. Such a trigger cannot read M365, so it fails in a way
that superficially resembles an auth failure but is not.

### 4. [Certain] Self-bind triggers DO retain connector access

A trigger created without `create_new_session_on_fire` binds to the calling session
(`persist_session: true`). When it fired, the resumed session still had working M365 tools
and returned live data.

Note: the API emits a warning on creation claiming "this trigger stores no MCP connectors,
so the sessions it fires will run without connector tools." For self-bind triggers that
warning is **misleading** - the resumed session kept its connectors. Do not abandon the
self-bind approach on the strength of that warning alone.

### 5. [Unknown] Token refresh across a long idle gap

Never cleanly tested. A 90-minute probe was scheduled but the outcome was not recorded
before the architecture changed to app-only auth, which makes the question moot: client
credentials mint a fresh token per run, so there is no refresh token to expire.

If anyone revives the MCP-connector approach, this remains the open risk.

### 6. [Certain] Admin Auto-Allow settings in the routines UI did not remove the prompt

Prithvi (who is the admin) enabled Auto-Allow for `Outlook send mail` and several other
write tools in the routines connector configuration. The prompt still appeared in a
Claude Code Remote session. Those are separate permission layers. Changing the routines-UI
setting does not silence the Claude Code session-level prompt.

[Unknown] Whether the routines-UI Auto-Allow setting works for routines actually created
*through that UI*. It was never tested, because the routine was never created there.

---

## Mailbox specifics worth knowing

[Certain] The mailbox timezone is **Central** (`Central Standard Time` in Graph responses),
not Eastern. The calendar API returns wall-clock strings in the mailbox timezone. Do not
reinterpret them as UTC.

[Unknown] Whether Prithvi wants the brief displayed in Central or Eastern. He specified ET
twice, but WCP is Chicago-based and the mailbox is Central, so this may have been a
copy-through rather than a deliberate choice. The current implementation uses a
`BRIEF_DISPLAY_TIMEZONE` env var so it can be changed in one place. **Confirm before
trusting the times.**

[Certain] `outlook_email_search` has no unread filter parameter. Unread must be filtered
client-side on the `isRead` field. The Graph API used in this repo filters server-side with
`$filter=isRead eq false`, which is cleaner.

---

## Things that were built and then abandoned

- A probe routine created via `create_trigger` with `connectors` - deleted before it fired,
  because with no connector tools it would have emailed a false "Auth FAILED" and looked
  like an OAuth problem.
- A Cowork build spec - written but never executed. Cowork remains an untested alternative
  surface if app-only auth is ever refused.
- A self-bind daily trigger at 09:00 UTC (`trig_01XsaSHKqiFikep7brbeMA6D`) and a 90-minute
  probe (`trig_01WgSrXHzdXTymsfq8g9u3JS`). **Both should be deleted** once this repo's
  scheduled runner is live, or they will keep firing and stalling on the send prompt.
