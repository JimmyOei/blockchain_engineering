# Lab 2 — Coordinated Group Signing

3 members, 3 rounds, 1 group_id, 10-second budget. Each round must be submitted by a different member.

## Algorithm

Member `i` is the **leader** of round `i + 1`. The leader does everything for that round:

1. Asks the server for the challenge (`ChallengeRequest`).
2. Receives the nonce.
3. Signs it locally, broadcasts the nonce to the other 2 members (`NoncePayload`).
4. Other 2 sign and send their signatures back (`SignaturePayload`).
5. Leader bundles all 3 sigs in registration order and submits (`SubmissionPayload`).
6. On success, leader tells the next leader to start (`StartRoundPayload`).

Round 1 → member 0, round 2 → member 1, round 3 → member 2.

### Bootstrap (one-time)

- Member 0 is the only registrar. Once it has discovered the server **and** both teammates, it sends `RegisterPayload`.
- On `ResponseRegisterPayload`, member 0 broadcasts the `group_id` to the other two via `GroupIdPayload`, then immediately starts round 1.

## Files

| File | Purpose |
|---|---|
| `main.py` | IPv8 boot + overlay setup. Runs forever; Ctrl+C to stop. |
| `lab2_community.py` | All protocol logic. |
| `message_payloads.py` | All message definitions (server-defined 1–6, internal peer-to-peer 7–10). |
| `first_key.txt`, `second_key.txt`, `third_key.txt` | The 3 registered Lab 1 **public** keys (hex). Identical on all laptops. |
| `my_key.pem` | This laptop's **private** key (per-laptop, NOT committed). |

## Run

On each laptop:

```bash
MY_MEMBER_ID=0 python main.py   # laptop 0
MY_MEMBER_ID=1 python main.py   # laptop 1
MY_MEMBER_ID=2 python main.py   # laptop 2
```

Watch for `🎉  All 3 rounds done` (printed by member 2 on round-3 success).
