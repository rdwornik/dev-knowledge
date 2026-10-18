Read-only task. Do not edit any file. Read these three files in this repository checkout:
1. scripts/claim.py
2. templates/batch-common-rules-template.md
3. tasks/1572-dispatch-py-queue-skips-an-already-launched-lane-and-fires-the-eligible-ones-instead-of-ha.md

Answer these six questions. Each answer must be backed by the exact line quoted from the file and its file:line.
Q1. In scripts/claim.py, what integer value is the constant for the "claim refused because another session holds it" outcome (IN_FLIGHT)?
Q2. In scripts/claim.py, how many seconds is the claim lock timeout constant (_LOCK_TIMEOUT_S)?
Q3. In scripts/claim.py, what string is the marker infix constant (_MARKER_INFIX)?
Q4. In templates/batch-common-rules-template.md, what is the exact name a lane's session file must have?
Q5. In templates/batch-common-rules-template.md, what does the template say about cron and scheduled wake-ups?
Q6. In the [#1572] task row, on which commit sha must the RED test fail?

Your final message must be ONLY a JSON array, one object per question, no prose and no code fence:
[{"q": 1, "answer": "...", "file": "path", "line": 123, "quote": "the exact line text, trimmed"}, ...]
