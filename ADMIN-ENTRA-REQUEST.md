# Entra ID permission request - automated daily brief

**Requested by:** Prithvi Raj (praj@waudcapital.com)
**Purpose:** An automated email that sends Prithvi a summary of his own calendar and unread
mail each weekday morning at 5:00am ET. It reads one mailbox and sends to that same mailbox.
No other user's data is accessed, and nothing is sent to anyone else.

**Why this needs app-only permissions:** the job runs unattended at 5am. Delegated
(user-signed-in) permissions require an interactive browser sign-in and a human to approve
each send, which is not possible on a schedule.

---

## What to create

### 1. App registration

Entra admin center → App registrations → New registration

- **Name:** `WCP Daily Brief`
- **Supported account types:** Accounts in this organizational directory only (single tenant)
- **Redirect URI:** none needed

Record the **Application (client) ID** and **Directory (tenant) ID**.

### 2. API permissions

API permissions → Add a permission → Microsoft Graph → **Application permissions**

| Permission | Why it is needed |
|---|---|
| `Calendars.Read` | Read the day's meetings |
| `Mail.Read` | Read unread inbox mail to triage it |
| `Mail.Send` | Send the assembled brief |

Then click **Grant admin consent**. All three are application permissions, not delegated.

### 3. Client secret

Certificates & secrets → New client secret. 24-month expiry.

Record the secret **value** at creation time - it is not retrievable afterward.

### 4. Scope the app to a single mailbox - please do not skip this

By default, these three application permissions apply to **every mailbox in the tenant**.
That is far more access than this job needs, and an unscoped `Mail.Send` credential can
send as anyone in the firm.

Restrict the app to Prithvi's mailbox only, via Exchange Online PowerShell:

```powershell
Connect-ExchangeOnline

New-ApplicationAccessPolicy `
  -AppId <application-client-id> `
  -PolicyScopeGroupId praj@waudcapital.com `
  -AccessRight RestrictAccess `
  -Description "WCP Daily Brief - restrict to Prithvi's mailbox only"
```

Verify it took effect:

```powershell
Test-ApplicationAccessPolicy -Identity praj@waudcapital.com -AppId <application-client-id>
# Expected: AccessCheckResult = Granted

# And confirm it is denied elsewhere - substitute any other mailbox:
Test-ApplicationAccessPolicy -Identity <someone.else>@waudcapital.com -AppId <application-client-id>
# Expected: AccessCheckResult = Denied
```

Policy changes can take up to 30 minutes to propagate.

---

## What to send back

Four values, ideally through a secrets manager or password vault rather than email:

1. Directory (tenant) ID
2. Application (client) ID
3. Client secret value
4. Confirmation that the Application Access Policy is in place and tested

---

## Security notes

- The three permissions above are the complete ask. No `Mail.ReadWrite`, no
  `Calendars.ReadWrite`, no SharePoint or Teams scopes.
- With the access policy applied, the credential can only touch praj@waudcapital.com.
- The secret will be stored as a GitHub Actions encrypted secret, not in source control.
- Set a calendar reminder for the secret expiry. The job fails silently on an expired
  secret unless monitoring catches it.
- If this credential is ever suspected compromised, delete the client secret in Entra -
  that revokes access immediately without touching the app registration.
