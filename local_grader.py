# local_grader.py
# Lightweight local grader: polls the app's /_solves endpoint and prints new solves.
import time, requests, argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--url', default='http://localhost:5000/_solves')
    p.add_argument('--interval', type=int, default=5)
    args = p.parse_args()
    seen = set()
    while True:
        try:
            r = requests.get(args.url, timeout=5)
            j = r.json()
            for s in j.get('solves', []):
                key = (s['username'], s['flag'], s['stage'])
                if key not in seen:
                    seen.add(key)
                    print('NEW SOLVE:', s)
        except Exception as e:
            print('error:', e)
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
