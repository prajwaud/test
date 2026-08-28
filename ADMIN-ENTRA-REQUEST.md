# Entra ID request - WCP AI Agent mailbox and app-only Graph access

**Requested by:** Prithvi Raj (praj@waudcapital.com)
**Purpose:** Scheduled, unattended emails sent by an automated agent from a dedicated
agent mailbox:

1. A daily brief summarizing Prithvi's own calendar and unread mail, sent to him each
   weekday at 5:00am ET.
2. A weekly market-intelligence digest sent each Friday morning to a fixed internal
   distribution of three: Prithvi Raj, Doug Rassner and Reeve Waud Jr.

All automated mail sends from the agent mailbox, so recipients see it comes from the
agent, not from Prithvi. Reads are limited to Prithvi's own mailbox (for the brief) and
the agent mailbox (for replies to the digest). Recipients are additionally constrained
in code to a version-controlled allowlist of the three names above; adding a recipient
requires a reviewed commit.

**Why this needs app-only permissions:** the jobs run unattended (5:00am weekdays,
Friday mornings). Delegated (user-signed-in) permissions require an interactive browser
sign-in and a human to approve each send, which is not possible on a schedule.

---

## What to create

### 1. Shared mailbox - the agent identity

Exchange admin center → Recipients → Mailboxes → Add a shared mailbox

- **Display name:** `Prithvi WCP AI Agent`
- **Proposed address:** `prithvi-ai-agent@waudcapital.com` (adjust to naming convention)
- No license required for a shared mailbox.
- Grant **Full Access** to praj@waudcapital.com, so Prithvi can read replies that land
  in the agent mailbox.

### 2. Mail-enabled security group - the access-policy scope

The Application Access Policy below scopes by group, so create a mail-enabled security
group (e.g. `WCP AI Agent Scope`) with exactly two members:

- praj@waudcapital.com
- prithvi-ai-agent@waudcapital.com

### 3. App registration

Entra admin center → App registrations → New registration

- **Name:** `WCP AI Agent`
- **Supported account types:** Accounts in this organizational directory only (single tenant)
- **Redirect URI:** none needed

Record the **Application (client) ID** and **Directory (tenant) ID**.

### 4. API permissions

API permissions → Add a permission → Microsoft Graph → **Application permissions**

| Permission | Why it is needed |
|---|---|
| `Calendars.Read` | Read the day's meetings from Prithvi's calendar |
| `Mail.Read` | Read Prithvi's unread inbox (brief) and digest replies (agent mailbox) |
| `Mail.Send` | Send the assembled emails from the agent mailbox |

Then click **Grant admin consent**. All three are application permissions, not delegated.

### 5. Client secret

Certificates & secrets → New client secret. 24-month expiry.

Record the secret **value** at creation time - it is not retrievable afterward.

### 6. Scope the app to the two mailboxes - please do not skip this

By default, these three application permissions apply to **every mailbox in the tenant**.
That is far more access than this needs, and an unscoped `Mail.Send` credential can send
as anyone in the firm.

Restrict the app to the group from step 2, via Exchange Online PowerShell:

```powershell
Connect-ExchangeOnline

New-ApplicationAccessPolicy `
  -AppId <application-client-id> `
  -PolicyScopeGroupId "WCP AI Agent Scope" `
  -AccessRight RestrictAccess `
  -Description "WCP AI Agent - restrict to Prithvi's mailbox and the agent mailbox only"
```

Verify it took effect:

```powershell
Test-ApplicationAccessPolicy -Identity praj@waudcapital.com -AppId <application-client-id>
# Expected: AccessCheckResult = Granted

Test-ApplicationAccessPolicy -Identity prithvi-ai-agent@waudcapital.com -AppId <application-client-id>
# Expected: AccessCheckResult = Granted

# And confirm it is denied elsewhere - substitute any other mailbox:
Test-ApplicationAccessPolicy -Identity <someone.else>@waudcapital.com -AppId <application-client-id>
# Expected: AccessCheckResult = Denied
```

Policy changes can take up to 30 minutes to propagate.

---

## What to send back

Five values, ideally through a secrets manager or password vault rather than email:

1. Directory (tenant) ID
2. Application (client) ID
3. Client secret value
4. The agent mailbox address as created
5. Confirmation that the Application Access Policy is in place and tested

---

## Security notes

- The three permissions above are the complete ask. No `Mail.ReadWrite`, no
  `Calendars.ReadWrite`, no SharePoint or Teams scopes.
- With the access policy applied, the credential can only touch praj@waudcapital.com
  and the agent mailbox.
- The secret will be stored as a GitHub Actions encrypted secret, not in source control.
- Set a calendar reminder for the secret expiry. The job fails silently on an expired
  secret unless monitoring catches it.
- If this credential is ever suspected compromised, delete the client secret in Entra -
  that revokes access immediately without touching the app registration.
