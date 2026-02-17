# C2C 2026 CTF - Challenge Scripts

> **Qualifier Rank: #94**

Scripts and payloads used during the C2C 2026 CTF competition.

## Repository Structure

```
.
├── Blockchain
│   ├── convergence_exploit.sh       # Constraint mismatch → transcend()
│   ├── nexus_exploit.sh             # Vault inflation attack
│   └── tge_solve.py                 # Check-after-effect bug in upgrade()
├── Forensics
│   ├── log_email_extractor.py       # Extract email from blind SQLi logs
│   ├── tattletale_decode_keylog.py  # Decode raw Linux input_event keylog
│   └── tattletale_decode_od.py      # Decode octal dump to plaintext
├── Misc
│   └── jinjail_payload.txt          # Jinja2 SSTI WAF bypass payload
├── Reverse
│   └── bunaken_aes_bruteforce.py    # AES-128-CBC key bruteforce (Bun.js)
└── Web
    ├── clicker_exploit.py           # JKU Injection + SSRF (curl brace expansion)
    ├── corp_mail_jwt_note.txt        # SSTI → JWT secret leak notes
    └── rick_ssti_payload.txt         # Go SSTI payload (%#v private field)
```

## Challenges Solved

| Category   | Challenge               | Vulnerability                          |
|------------|-------------------------|----------------------------------------|
| Misc       | JinJail                 | Jinja2 SSTI WAF Bypass via numpy.f2py  |
| Web        | Corp-mail               | Python SSTI → JWT Secret Leak          |
| Web        | Clicker                 | JKU Injection + SSRF (curl globbing)   |
| Web        | The Soldier of God Rick | Go SSTI via `%#v` private field leak   |
| Forensics  | Log                     | SQLi Log Analysis                      |
| Forensics  | Tattletale              | Linux Keylogger Forensics              |
| Reverse    | Bunaken                 | AES-128-CBC Key Bruteforce (Bun.js)    |
| Blockchain | TGE                     | Check-After-Effect Bug                 |
| Blockchain | Nexus                   | Vault Inflation Attack                 |
| Blockchain | Convergence             | Constraint Mismatch                    |
Note: Welcome challenge is not included here as the flag appears directly on the index page — no script needed.
## Requirements

```bash
# Python scripts
pip install pycryptodome web3 requests PyJWT cryptography

# Blockchain scripts
curl -L https://foundry.paradigm.xyz | bash && foundryup

# Web clicker exploit (requires ngrok)
ngrok http 9000
```

## Disclaimer

Scripts were written for educational purposes during a CTF competition.
AI tools (Claude Sonnet 4.5, ChatGPT) were used to assist with script
generation and code analysis.

