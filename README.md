CyberNeutron Loan Fraud CTF


A multi-stage web exploitation challenge focused on real-world loan fraud abuse techniques.

CyberNeutron Loan Fraud CTF is a fully interactive, progressive web security challenge where players exploit a fictional loan application system.
The CTF is designed for training beginners–intermediate cybersecurity learners using realistic attack vectors, browser analysis, and Burp Suite interception.

🚀 Overview

Players must exploit vulnerabilities in a loan application platform used by a fictional fintech service.
Each stage introduces a more advanced security flaw—building a full exploitation chain in the final stage.

The CTF includes:

✔️ Multi-stage progression
✔️ Visual progress tracker
✔️ Real-time validation
✔️ Flag system
✔️ 3-level hint system per stage
✔️ Professional cyber-themed UI

🧩 Stages Breakdown
🔹 Stage 1 — Client-Side Manipulation

Players inspect and modify front-end code to bypass strict client-side validation.
They learn about:

Weak JavaScript-only security

Manipulating DOM elements

Browser dev tools exploitation

Goal: Submit an application with invalid/ineligible values.
Skill: Basic client-side tampering.

🔹 Stage 2 — Hidden API Key Discovery

Participants explore browser console logs, network panel, and front-end JS files to recover an exposed API key.

They learn:

Why embedding keys in the front-end is insecure

How front-end frameworks leak sensitive info

Using dev tools to extract API logic

Goal: Obtain access to protected API routes.
Skill: Client-side reconnaissance.

🔹 Stage 3 — Checksum Bypass

The platform includes a fake “security checksum” used to validate critical requests.
Players reverse-engineer or bypass the client-side checksum algorithm.

They learn:

How checksums work

Why client-side cryptography is weak

Reverse engineering obfuscated JS

Goal: Submit an altered payload accepted by backend.
Skill: Understanding client-side pseudo security.

🔹 Stage 4 — Full Exploit Chain

The final stage requires players to combine:

Form manipulation

API key abuse

Checksum forgery

Backend logic exploitation

Goal: Completely compromise the loan approval mechanism and extract the final flag.
Skill: Multi-step exploit chaining.

🛠️ Technical Features
Frontend

Dynamic progress tracker

Animated UI elements

Real-time failure and success feedback

Progressive hints (3 per stage)

Flag popup system

Educational console messages

Backend

Stage-by-stage validation

Intentional vulnerabilities

Admin panel functionality

Score tracking

Secure flag issuing system

Interception Ready

The challenge is designed for use with:

Burp Suite

OWASP ZAP

HTTP Replay Tools

Players will analyze and exploit requests in real time.

🎯 Learning Objectives

By the end of the CTF, participants will understand:

✔️ Why client-side security cannot be trusted
✔️ API enumeration and key exposure
✔️ How weak “checksums” and “tokens” can be manipulated
✔️ How chained vulnerabilities can compromise a real system
✔️ Safe design patterns in fintech security models
📦 How to Play

Visit the CyberNeutron Loan Fraud CTF website.

Create or choose a username.

Start at Stage 1; progress in order.

Use browser dev tools + Burp Suite for analysis.

Read hints when needed (three per stage).

Capture flags and unlock the final badge.

🌐 Deployment (Recommended)
Frontend (Netlify)

Upload these files:

client.html
admin.html
assets/
scripts/

Backend (Render)

Deploy with:

uvicorn app:app --host 0.0.0.0 --port 10000


Then update frontend API path:

const API = "https://your-api.onrender.com";

🏁 Flags

Each stage awards a unique flag:

FLAG{stage_1_bypassed}
FLAG{stage_2_api_key_exposed}
FLAG{stage_3_checksum_defeated}
FLAG{stage_4_system_compromised}


Final chain completion unlocks:

FLAG{cyberneutron_master_of_loan_fraud_ctf}

📚 Notes for Instructors / Event Hosts

Recommended for students learning web exploitation

Difficulty: Beginner → Intermediate

Meets requirements for cybersecurity club workshops

Designed to be solvable without prior scripting knowledge

Ideal for teaching client-side vs server-side security

👤 Credits

CyberNeutron Loan Fraud CTF
Developed for educational and ethical cybersecurity training.
All vulnerabilities are intentional and safe for classroom or competition environments.
