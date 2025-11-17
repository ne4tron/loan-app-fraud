# Loan API CTF (full package)
Files included:
- app.py: Flask backend with basic and hard stages, admin panel, and a simulated leak file in /backup/admin_token.bak
- client.html: vulnerable client
- admin.html: admin panel UI that calls admin endpoints
- requirements.txt, Dockerfile, docker-compose.yml
- ctfd_submit.py: helper to submit flags to an external scoreboard (configure URL)
- local_grader.py: polls the local app to display solves
- static/admin_token.bak: simulated accidental backup containing ADMIN_TOKEN

How to run locally:
1. python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. export CTF_FLAG="CTF{your_flag_here}"
   export CTF_FLAG_HARD="CTF{your_hard_flag_here}"
   export ADMIN_TOKEN="some_secret_token"
4. python app.py
5. Visit http://localhost:5000 to use the client, /admin for admin panel, and /backup/admin_token.bak to find the token (intentionally exposed for the challenge).
6. Use local_grader.py to watch solves.

Challenge design:
- Basic stage: exploit API logic manipulation by sending approved=true in /apply then access /flag?username=alice
- Hard stage: must create a loan with amount >= 1000000 and interest_rate 0, then get it approved by admin (requires ADMIN_TOKEN). The simulated accidental backup at /backup/admin_token.bak leaks the token.
- Score integration: use ctfd_submit.py to POST flags to your scoreboard; or run local_grader.py to see solves locally.

Note: This package intentionally includes vulnerabilities for educational CTF use only.
