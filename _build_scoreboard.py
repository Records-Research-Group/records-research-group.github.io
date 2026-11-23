#!/usr/bin/env python3
# provenance: author=devin-session; created=2026-11-23; source=hand-written;
# purpose=regenerate accessibility_scoreboard.csv + scoreboard.html from the
# RRG request ledger (ai-hub/Artifacts/records_requests.csv); intent=build-tool
"""Build accessibility_scoreboard.csv + scoreboard.html from the RRG
request ledger. The CSV is the published artifact; this script is kept
for regeneration on each update."""
import csv, json, re, sys
from pathlib import Path

AI_HUB = Path(r"C:\Users\jesse\Documents\PythonDev\ai-hub")
SITE = Path(r"C:\Users\jesse\Documents\PythonDev\records-research\records-research-group.github.io")
LEDGER = AI_HUB / "Artifacts" / "records_requests.csv"
AGENCIES = json.loads((AI_HUB / "Artifacts" / "data" / "records_agencies.json").read_text(encoding="utf-8"))["agencies"]
AS_OF = "2026_11_23"
AS_OF_HUMAN = "2026-11-23"

SUBJECT = {
    "vendor_payments": "Vendor payments", "sweep_vendor_payments": "Vendor payments (FY2024–FY2025 + FYTD)",
    "sweep_vendor_payments_foia": "Vendor payments (FOIA)", "checkbook": "Check register / vendor payments",
    "payroll": "Employee payroll register", "provider_activation": "Provider activation records",
    "contract_docs": "Contract documents", "investigation_files": "Investigation files",
    "policy_docs": "Policy documents", "quarterly_reports": "Quarterly reports",
    "program_stats": "Program statistics", "voter_deceased_review": "Voter-registration record review (deceased registrant)",
    "jail_census_reconcile": "Jail census + bookings/releases",
    "school_tech_inventory": "Technology inventory / SBITA schedule",
    "payroll_salary_surveys": "Salary surveys + payroll registers",
    "jail_incustody_deaths": "In-custody death records",
    "procurement_file": "ESS Navigation Center procurement file",
    "millrace_dam": "Millrace diversion dam records",
    "epd_theft_casefile": "EPD copper-theft case file",
    "clcc_carrier_outage": "CLCC 911 carrier outage records",
    "fcc_outage_report": "FCC outage filings", "eweb_storm_outage": "EWEB storm outage records",
    "oha_adhd_claims_agg": "OHA ADHD claims aggregates",
    "oha_bhrn_lane_detail": "OHA BHRN Lane County grant detail",
    "oha_provider_enrollment": "OHA BH provider enrollment",
    "4j_medicaid_sped": "4J Medicaid/SPED claiming",
}
TICKET_PAGES = {
    "26-974": "lane-county-clerk-26-974.html", "26-975": "lane-county-clerk-26-975.html",
    "26-968": "lane-county-26-968.html", "26-971": "lane-county-26-971.html",
    "26-1042": "lane-county-26-1042.html", "26-1032": "lane-county-26-1032.html",
    "26-1055": "lane-county-26-1055.html", "26-1083": "lane-county-26-1083.html",
    "PRR-2026-896": "eugene-prr-2026-896.html", "PRR-2026-926": "eugene-prr-2026-926.html",
    "PRR-2026-948": "eugene-prr-2026-948.html",
}

def agency_name(slug):
    n = AGENCIES.get(slug, {}).get("name") or slug.replace("_", " ").title()
    return n.split(" — ")[0].split(" (")[0].strip()

def resp_dates(notes):
    # exclude bounce entries — a delivery failure is not a substantive response
    ds = []
    for m in re.finditer(r"resp=[^\[;]+?\[([^\]]+)\]\s*(20\d\d-\d\d-\d\d)", notes):
        if m.group(1).strip().lower().startswith("bounce"):
            continue
        ds.append(m.group(2))
    return min(ds) if ds else ""

def last_outcome(notes):
    # resp tag may cover multiple files: resp=a.eml + b.eml [tag]
    tags = re.findall(r"resp=[^\[;]+?\[([^\]]+)\]", notes)
    return tags[-1] if tags else ""

def fee(notes):
    m = re.search(r"(?:fee-quote|invoice|estimate|fee-flex|INV-?\d)[^\n$;]*\$([\d,]+\.?\d*)", notes)
    if m:
        return m.group(1)
    m = re.search(r"(?:fee-quote|invoice|estimate|fee-flex|INV-?\d)[^\n;]*?~?([\d,]+\.?\d*)\s*USD", notes)
    return m.group(1) if m else ""

def waiver_out(notes):
    n = notes.lower()
    if "waiver" not in n and "192.324(5)" not in notes:
        return ("n", "n/a")
    if re.search(r"waiver[ -]?(granted|approved)", n) or "fee waiver granted" in n or "waiver granted" in n:
        return ("y", "granted")
    if "waiver denied" in n or "waiver-denied" in n or "denial upheld" in n:
        d = re.search(r"(?:waiver[ -]denied|denial upheld)[^\d]*(20\d\d-\d\d-\d\d)?", n)
        return ("y", "denied" + (f" {d.group(1)}" if d and d.group(1) else ""))
    if "waiver moot" in n or "fee waiver moot" in n:
        return ("y", "moot")
    return ("y", "pending")

TAG_LABEL = [
    ("no-responsive-records", "No responsive records (per desk)"),
    ("no-records", "No responsive records (per desk)"),
    ("production-redirect", "Produced via transparency link"),
    ("production", "Produced"), ("delivery", "Produced"), ("completed", "Completed"),
    ("portal-redirect", "Portal redirect"), ("portal-steer", "Channel-switch letter"),
    ("redirect", "Redirected"), ("fee-quote", "Fee estimate issued"),
    ("invoice", "Fee estimate issued"), ("waiver-denied", "Fee waiver denied"),
    ("waiver-granted", "Fee waiver granted"), ("denial", "Denied"),
    ("bounce", "Bounced"), ("misrouted", "Misrouted"),
    ("not-custodian", "Not custodian"), ("questionnaire", "Responded (questionnaire)"),
    ("info-flex", "Responded"), ("fee-flex", "Responded"),
    ("delay", "Acknowledged — delayed"), ("ack", "Acknowledged"),
    ("responded", "Acknowledged/responded"), ("clarification", "Clarification received"),
]

def clean_tag(tag):
    if not tag:
        return ""
    head, _, tail = tag.partition(":")
    head_l = head.strip().lower()
    for prefix, label in TAG_LABEL:
        if head_l.startswith(prefix):
            t = tail.strip()
            return f"{label} — {t[:80]}" if t else label
    return tag.strip()[:90]

def status_of(row, notes):
    n = notes
    st = row["status"]
    tag = last_outcome(n)
    resends = {"32": "66", "47": "65", "25": "20"}  # bounced row re-sent; not an independent desk
    if row["id"] in resends:
        return f"Bounced — re-sent as RRG-{resends[row['id']]}", tag
    if "nonresponse-finding" in n:
        if "delivery unverified" in n:
            return "No response on file (send-desk delivery unverified)", tag
        if "petition_L" in n:
            return "Nonresponse past ORS 192.324 ack window — DA/AG petition filed", tag
        return "Nonresponse past ORS 192.324 ack window — logged", tag
    if "SUPERSEDED" in n or st == "dropped":
        return "Withdrawn (superseded by duplicate filing)", tag
    if st in ("drafted", "scheduled"):
        return f"{st.capitalize()} — not yet sent", tag
    produced = re.search(r"\[production|\[delivery|\[completed|production-complete|production-attachment|_released\.eml|PRODUCTION|\[produced", n)
    lead = ""
    if produced:
        lead = "Produced"
    elif "fee-quote" in n or "invoice" in n or "estimate" in n:
        lead = "Fee estimate issued"
    else:
        lead = clean_tag(tag)
    parts = [lead] if lead else []
    if "petition_L" in n:
        parts.append("petition to DA/AG filed")
    if "BOUNCE" in n and "re-route" in n and "RE-SEND" not in n and not produced:
        parts.append("bounced — re-route pending")
    if not parts:
        parts.append("Sent — awaiting response")
    s = "; ".join(dict.fromkeys(parts))
    return (s[:150].rsplit(" ", 1)[0] if len(s) > 150 else s), tag

rows = list(csv.DictReader(LEDGER.open(encoding="utf-8")))
out, petitions, produced_n, fee_total, fee_n, waivers = [], set(), 0, 0.0, 0, {"req": 0, "granted": 0, "denied": 0}
first_resp_n = nonresp_n = bounce_n = 0
for r in rows:
    notes = r.get("notes") or ""
    rid, agency, tmpl = r["id"], r["agency"], r["template"]
    sent = r.get("sent") or ""
    if not sent and r["status"] in ("drafted", "scheduled", "dropped"):
        pass  # include for completeness
    ticket = ""
    for pat, fmt in [(r"ticket=([^\s;,]+)", "{0}"),
                     (r"ticket_26[ _-](\d{3,4})[ _]", "26-{0}"),
                     (r"ticket_PRR_(\d+)_(\d+)[ _]", "PRR-{0}-{1}"),
                     (r"ticket_PRR-(\d+-\d+)", "PRR-{0}")]:
        m = re.search(pat, notes)
        if m:
            ticket = fmt.format(*m.groups()).rstrip(";,.")
            break
    fr = resp_dates(notes)
    if fr: first_resp_n += 1
    status, tag = status_of(r, notes)
    if produced := re.search(r"\bProduced\b", status): produced_n += 1
    if "Nonresponse past" in status: nonresp_n += 1
    if "Bounced" in status: bounce_n += 1
    fee_amt = fee(notes)
    if fee_amt:
        fee_n += 1
        fee_total += float(fee_amt.replace(",", ""))
    w_req, w_out = waiver_out(notes)
    if w_out == "pending" and ("Produced" in status or "produced" in tag.lower() or "delivery" in tag.lower()):
        w_out = "moot"
    if w_req == "y":
        waivers["req"] += 1
        if w_out.startswith("granted"): waivers["granted"] += 1
        elif w_out.startswith("denied"): waivers["denied"] += 1
    for p in re.findall(r"petition_(L\d+)", notes):
        petitions.add(p)
    note_short = ""
    if "millrace" in tmpl.lower(): note_short = "Millrace dam thread"
    out.append({
        "ref": f"RRG-{int(rid):02d}" if rid.isdigit() and int(rid) < 100 else f"RRG-{rid}",
        "agency": agency_name(agency), "portal_ticket": ticket,
        "subject": SUBJECT.get(tmpl, tmpl), "filed": sent[:10],
        "first_response": fr, "status": status,
        "fee_quoted_usd": fee_amt, "fee_paid_usd": "0",
        "waiver_requested": w_req, "waiver_outcome": w_out, "notes": note_short})

# ---- CSV ----
fields = ["ref","agency","portal_ticket","subject","filed","first_response",
          f"status_as_of_{AS_OF}","fee_quoted_usd","fee_paid_usd",
          "waiver_requested","waiver_outcome","notes"]
with (SITE / "data" / "accessibility_scoreboard.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in out:
        rr = dict(r); rr[f"status_as_of_{AS_OF}"] = rr.pop("status"); w.writerow(rr)

# ---- HTML ----
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
trs = []
for r in out:
    t = r["portal_ticket"]
    tcell = f'<a href="requests/{TICKET_PAGES[t]}">{esc(t)}</a>' if t in TICKET_PAGES else esc(t)
    fee_c = f'${r["fee_quoted_usd"]}' if r["fee_quoted_usd"] else "—"
    wav = r["waiver_outcome"] if r["waiver_requested"] == "y" else "—"
    trs.append(f'<tr id="{r["ref"].lower()}"><td>{r["ref"]}</td><td>{esc(r["agency"])}</td><td>{tcell}</td><td>{esc(r["subject"])}</td>'
               f'<td>{r["filed"]}</td><td>{r["first_response"] or "—"}</td><td>{esc(r["status"])}</td>'
               f'<td class="num">{fee_c}</td><td>{esc(wav)}</td></tr>')

# resend pairs: an earlier bounced row is not an independent desk
sent_n = sum(1 for r in rows if (r.get("sent") or ""))
ag_n = len({r["agency"] for r in rows if (r.get("sent") or "") and r["id"] not in {"32","47","25"}})
canon_n = sum(1 for r in rows if r["template"] == "sweep_vendor_payments" and (r.get("sent") or ""))
canon_nr = sum(1 for r in rows if r["template"] == "sweep_vendor_payments"
               and r["id"] not in {"32","47","25"}
               and "nonresponse-finding" in (r.get("notes") or "")
               and "delivery unverified" not in r["notes"])
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Public-records accessibility scoreboard — Records Research Group</title>
<style>
  body {{ font-family: Georgia, serif; max-width: 68rem; margin: 3rem auto;
         padding: 0 1rem; color: #1a1a1a; line-height: 1.6; }}
  h1 {{ font-size: 1.5rem; }}
  table {{ border-collapse: collapse; width: 100%; font-size: .84rem; }}
  th, td {{ border: 1px solid #bbb; padding: .3rem .45rem; text-align: left;
           vertical-align: top; }}
  th {{ background: #f0f0f0; position: sticky; top: 0; }}
  .stats td:first-child {{ width: 60%; }}
  .num {{ text-align: right; white-space: nowrap; }}
  .note {{ color: #555; font-size: .95rem; }}
</style>
</head>
<body>
<p><a href="index.html">&larr; Records Research Group</a></p>
<h1>Public-records accessibility scoreboard</h1>
<p class="note">As of {AS_OF_HUMAN}. The accessibility record itself —
what was requested, acknowledged, quoted, waived, denied, and produced —
is published here as a dataset. Machine-readable source:
<a href="data/accessibility_scoreboard.csv">accessibility_scoreboard.csv</a>.
Per-finding analysis: <a href="findings/">findings</a>. Study context:
<a href="notes/2026-10-lane-county-study.html">Lane County records
accessibility study</a>.</p>

<h2>Summary</h2>
<table class="stats">
<tr><th>Measure</th><th>Value</th></tr>
<tr><td>Requests filed (Oct–Nov 2026 waves)</td><td class="num">{sent_n}</td></tr>
<tr><td>Distinct agencies (bounce re-sends deduplicated)</td><td class="num">{ag_n}</td></tr>
<tr><td>Requests with a recorded first response (excl. bounces)</td><td class="num">{first_resp_n} of {sent_n}</td></tr>
<tr><td>Canonical state sweep rows (identical vendor-payments ask)</td><td class="num">{canon_n}</td></tr>
<tr><td>Record sets produced</td><td class="num">{produced_n}</td></tr>
<tr><td>Fee estimates issued</td><td class="num">{fee_n} requests — ${fee_total:,.2f} total quoted</td></tr>
<tr><td>Fees paid to date</td><td class="num">$0</td></tr>
<tr><td>Fee waivers requested (ORS 192.324(5))</td><td class="num">{waivers['req']}</td></tr>
<tr><td>&nbsp;&nbsp;— granted (incl. federal FOIA)</td><td class="num">{waivers['granted']}</td></tr>
<tr><td>&nbsp;&nbsp;— denied</td><td class="num">{waivers['denied']}</td></tr>
<tr><td>Nonresponses past ORS ack window — logged or petitioned</td><td class="num">{nonresp_n} ({canon_nr} of {canon_n} canonical rows = {canon_nr/canon_n:.1%})</td></tr>
<tr><td>Petitions for review filed (ORS 192.415 / AG)</td><td class="num">{len(petitions)}</td></tr>
<tr><td>Bounced addresses (dead directory entries)</td><td class="num">{bounce_n}</td></tr>
</table>

<h2>How to read statuses</h2>
<table class="stats">
<tr><th>Status label</th><th>Meaning</th></tr>
<tr><td>Produced / Completed</td><td>Records delivered (any format); resolved</td></tr>
<tr><td>Fee estimate issued</td><td>Priced, unpaid — open while the pay-or-close clock runs</td></tr>
<tr><td>Portal redirect / Channel-switch letter</td><td>Desk demands or steers to a portal channel; request posture preserved</td></tr>
<tr><td>No responsive records (per desk)</td><td>Desk reports a null set — unfalsifiable from outside, logged as stated</td></tr>
<tr><td>Nonresponse past ORS 192.324 ack window — logged</td><td>No acknowledgment inside the statutory window; logged 2026-11-20</td></tr>
<tr><td>Nonresponse past ORS 192.324 ack window — DA/AG petition filed</td><td>As above, escalated under ORS 192.415</td></tr>
<tr><td>petition to DA/AG filed</td><td>Petition for review filed on the thread's denial/fee/refusal</td></tr>
<tr><td>Bounced / No response on file (delivery unverified)</td><td>Send failed or delivery cannot be confirmed — excluded from response-rate interpretations</td></tr>
<tr><td>Sent — awaiting response / Acknowledged</td><td>In flight; inside or at the ack window</td></tr>
<tr><td>Withdrawn / Drafted</td><td>Not in the corpus — superseded duplicates or unsent drafts</td></tr>
</table>
<p class="note">This table is a <b>dated snapshot</b> (as of {AS_OF_HUMAN});
statuses change as correspondence arrives — pending, missing, denied,
and resolved rows are labeled separately above. Errors reported to the
<a href="about.html">corrections address</a> get a dated fix; bodies
named in findings may submit a response for verbatim, dated appending
(see <a href="findings/index.html#subject-response-rights">subject
response rights</a>).</p>

<h2>Per-request ledger</h2>
<table>
<tr><th>Ref</th><th>Agency</th><th>Ticket</th><th>Subject</th><th>Filed</th><th>First response</th><th>Status</th><th>Fee quoted</th><th>Waiver</th></tr>
{chr(10).join(trs)}
</table>

<p class="note">Statuses are abbreviated; full correspondence metadata
(dates, fee breakdowns, petition texts) is maintained in the study's
request ledger. Identical wave-2 state requests use one canonical ask
(vendor payments FY2024–FY2025 + FYTD); federal requests use the FOIA
variant. Fees paid remain $0 — every fee event to date has been met
with waiver pressure or narrowing rather than payment.</p>
</body>
</html>
'''
(SITE / "scoreboard.html").write_text(html, encoding="utf-8")
print(f"rows={len(out)} sent={sent_n} agencies={ag_n} first_resp={first_resp_n} produced={produced_n} "
      f"fees={fee_n}/${fee_total:,.2f} waivers={waivers} petitions={sorted(petitions, key=lambda x:int(x[1:]))} nonresp={nonresp_n} bounces={bounce_n}")
