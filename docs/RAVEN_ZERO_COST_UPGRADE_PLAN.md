# Raven Zero-Cost Upgrade Architecture (18 November 2026)

## Non-negotiable rules
No paid credits, AI API tokens, subscriptions, paid trials or surprise usage charges. No autonomous sending, bidding, contacting vendors or investor release. Keep existing sourcing channels and investor-specific buy boxes. Treat all new findings as UNVERIFIED until source and dated evidence are checked.

## Integration priorities
1. Preserve existing app, lead records, investor records and backups. No overwrite or migration without reconciliation.
2. Agent-led sourcing module: raven-agent-sourcing.html (local-first CRM, first-refusal notes, follow-up date, negotiation ceiling, fee calculation). Agent-first is an additional channel, not a replacement for probate, planning, insolvency, public notices, social and portal searches.
3. Standard deal schema: lead ID, source URL, date checked, address, asking price, vendor/agent, tenure, condition, comps with URLs and sold dates, independent valuation status, works, fees, contingency, investor buy box, ceiling offer, negotiation log, approval and release status.
4. Free deterministic maths: sourcing fee max(£3000, 1.5% agreed purchase price), investor profit after all acquisition/holding/refurbishment/selling costs; price sensitivity and counteroffers. Do not assert BMV without independent comparable evidence.
5. Investor matching: explicit filters and rank by suitability; protect investor identities and commercial data. No release without Kevin approval.
6. Research/monitoring: public sources only, respectful access, comply with site terms, no bypassing access controls. Record every source URL and retrieval date. Human review before publication or outreach.
7. Telegram: connect only after token securely provisioned; never commit tokens. Outbound deal alerts require review and approval.
8. External memory: structured canonical records plus changelog and dated evidence; export JSON/CSV; avoid unverified memory-based assertions. Keep sensitive records out of the public GitHub repository.

## Free/open-source candidates, NOT installed or connected
- GitHub: existing repository and version history (connected).
- Cloudflare Pages + Workers + D1: free-tier hosting/database, account connection and deployment still required; usage ceilings must be enforced.
- Playwright / Scrapy / Crawl4AI: public web extraction, local execution subject to target terms and machine resources.
- changedetection.io: monitor public listing changes; self-hosting requires runtime.
- Activepieces Community Edition: self-hosted automation; avoid cloud paid run thresholds.
- SQLite + FTS5: local durable searchable property/investor/agent memory.
- Ollama: optional local AI, only if machine can run it; no external paid model API.
- GitHub Actions: optional scheduled public-only jobs within free allowances; avoid private data in public artifacts/logs.

## Acceptance tests
- Existing lead and investor counts unchanged after integration.
- Duplicate URLs and address variants reconcile without losing history.
- Fee minimum and percentage correct; ceiling accounts for fee switching threshold.
- Missing comparables show 'unverified', never invented valuations.
- Offers, messages and investor releases never fire without explicit approval.
- JSON backup and restore round-trip without data loss.
- Scheduled searches log success, failure, source, timestamp and limitations.
- Zero paid services required for baseline operation.

## Danielle Bell workshop
Only advertised themes are confirmed: agent scripts, first refusal, four unspecified agent strategies and investor-led sourcing. Do not invent the exact four methods; integrate verified training details after 19 November session.
