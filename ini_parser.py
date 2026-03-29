#!/usr/bin/env python3
"""ini_parser - INI config file parser with nested sections."""
import sys, json, re

class IniParser:
    def __init__(self): self.data = {}
    def parse(self, text):
        self.data = {}; current = self.data
        for line in text.split("\n"):
            line = line.strip()
            if not line or line.startswith(("#", ";")): continue
            m = re.match(r'\[([^\]]+)\]', line)
            if m:
                parts = m.group(1).split("."); current = self.data
                for p in parts: current.setdefault(p, {}); current = current[p]
                continue
            if "=" in line:
                k, v = line.split("=", 1); k = k.strip(); v = v.strip()
                if v.lower() in ("true","yes"): v = True
                elif v.lower() in ("false","no"): v = False
                else:
                    try: v = int(v)
                    except:
                        try: v = float(v)
                        except: v = v.strip('"')
                current[k] = v
        return self.data
    def get(self, path, default=None):
        cur = self.data
        for p in path.split("."):
            if isinstance(cur, dict) and p in cur: cur = cur[p]
            else: return default
        return cur

def main():
    cfg = "[database]\nhost = localhost\nport = 5432\nssl = true\n\n[database.pool]\nmin = 5\nmax = 20\n\n[server]\nport = 8080\ndebug = false"
    p = IniParser(); data = p.parse(cfg)
    print("INI parser demo\n")
    print(json.dumps(data, indent=2))
    print(f"\n  database.host = {p.get('database.host')}")
    print(f"  database.pool.max = {p.get('database.pool.max')}")

if __name__ == "__main__":
    main()
