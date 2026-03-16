# urltools

URL parser, builder, and encoder. Zero dependencies.

## Commands

```bash
urltools parse "https://example.com/path?q=1" [--json]
urltools build --host example.com --path /api --query "key=val"
urltools encode "hello world"
urltools decode "hello%20world"
urltools join "https://example.com" "/api/v2"
urltools extract "https://example.com:8080/path" host
```

## Requirements

- Python 3.6+ (stdlib only)
