# ctfd_submit.py
# Simple flexible submitter that POSTs a flag to a configured endpoint.
# Usage:
#   python ctfd_submit.py --url https://ctfd.example/submit_flag --key YOUR_API_KEY --flag "CTF{...}"
import argparse
import requests
import os

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--url', required=True, help='Full URL to POST the flag to')
    p.add_argument('--key', required=False, help='API key (optional) - will be set in Authorization header as Bearer')
    p.add_argument('--flag', required=True, help='Flag to submit')
    args = p.parse_args()

    headers = {}
    if args.key:
        headers['Authorization'] = f'Bearer {args.key}'
    headers['Content-Type'] = 'application/json'
    payload = {'flag': args.flag}
    r = requests.post(args.url, json=payload, headers=headers, timeout=10)
    print('status', r.status_code)
    try:
        print(r.json())
    except Exception:
        print(r.text)

if __name__ == '__main__':
    main()
