#!/usr/bin/env python3
"""urltools - Parse, build, encode/decode URLs. Zero deps."""
import sys, json
from urllib.parse import urlparse, urlencode, parse_qs, quote, unquote, urlunparse, urljoin

def cmd_parse(args):
    if not args: print("Usage: urltools parse <url>"); sys.exit(1)
    url = args[0]
    p = urlparse(url)
    params = parse_qs(p.query)
    
    if "--json" in args:
        print(json.dumps({"scheme":p.scheme,"host":p.hostname or "","port":p.port,
            "path":p.path,"query":dict(params),"fragment":p.fragment,"username":p.username,"password":p.password}, indent=2))
    else:
        print(f"  Scheme:   {p.scheme}")
        print(f"  Host:     {p.hostname or ''}")
        if p.port: print(f"  Port:     {p.port}")
        print(f"  Path:     {p.path}")
        if params:
            print(f"  Query:")
            for k, v in params.items():
                print(f"    {k} = {v[0] if len(v)==1 else v}")
        if p.fragment: print(f"  Fragment: {p.fragment}")
        if p.username: print(f"  User:     {p.username}")

def cmd_build(args):
    scheme = "https"; host = ""; path = "/"; query = {}; fragment = ""
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--scheme" and i+1<len(args): scheme = args[i+1]; i+=2
        elif a == "--host" and i+1<len(args): host = args[i+1]; i+=2
        elif a == "--path" and i+1<len(args): path = args[i+1]; i+=2
        elif a == "--query" and i+1<len(args):
            k,v = args[i+1].split("=",1); query[k]=v; i+=2
        elif a == "--fragment" and i+1<len(args): fragment = args[i+1]; i+=2
        else: i+=1
    qs = urlencode(query)
    print(urlunparse((scheme, host, path, "", qs, fragment)))

def cmd_encode(args):
    if not args: text = sys.stdin.read().strip()
    else: text = " ".join(args)
    print(quote(text, safe=""))

def cmd_decode(args):
    if not args: text = sys.stdin.read().strip()
    else: text = " ".join(args)
    print(unquote(text))

def cmd_join(args):
    if len(args) < 2: print("Usage: urltools join <base> <path>"); sys.exit(1)
    print(urljoin(args[0], args[1]))

def cmd_extract(args):
    """Extract specific part of URL."""
    if len(args) < 2: print("Usage: urltools extract <url> <part>"); sys.exit(1)
    url, part = args[0], args[1]
    p = urlparse(url)
    parts = {"scheme":p.scheme,"host":p.hostname,"port":str(p.port or ""),
             "path":p.path,"query":p.query,"fragment":p.fragment,
             "domain":p.hostname,"netloc":p.netloc}
    if part in parts:
        print(parts[part])
    else:
        print(f"❌ Unknown part: {part}. Available: {', '.join(parts)}"); sys.exit(1)

CMDS = {"parse":cmd_parse,"p":cmd_parse,"build":cmd_build,"b":cmd_build,
        "encode":cmd_encode,"enc":cmd_encode,"decode":cmd_decode,"dec":cmd_decode,
        "join":cmd_join,"j":cmd_join,"extract":cmd_extract,"x":cmd_extract}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h","--help"):
        print("urltools - URL parser and builder")
        print("Commands: parse, build, encode, decode, join, extract")
        sys.exit(0)
    cmd = args[0]
    if cmd not in CMDS: print(f"Unknown: {cmd}"); sys.exit(1)
    CMDS[cmd](args[1:])
