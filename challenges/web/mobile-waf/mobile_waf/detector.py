import urllib.parse
import re
import json
import base64

def decode_unicode_and_overlong(s):
    if not isinstance(s, str):
        return ""
    # IIS %uXXXX
    s = s.replace('%u2215', '/').replace('%U2215', '/')
    s = s.replace('%u2216', '\\').replace('%U2216', '\\')
    s = re.sub(r'%[uU]00([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), s)
    
    # Overlong UTF-8
    rep = {
        '%c0%af': '/', '%C0%AF': '/',
        '%c1%9c': '\\', '%C1%9C': '\\',
        '%c0%ae': '.', '%C0%AE': '.',
        '%c0%80': '\x00', '%C0%80': '\x00',
    }
    for k, v in rep.items():
        s = s.replace(k, v)
        
    # JSON unicode escape \uXXXX
    s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
    return s

def try_b64decode_string(s):
    if not isinstance(s, str) or len(s) < 8:
        return []
    cand = s.replace('-', '+').replace('_', '/')
    cand += '=' * ((4 - len(cand) % 4) % 4)
    try:
        raw_bytes = base64.b64decode(cand)
        # Check binary signatures like Python pickle or .NET BinaryFormatter or Ruby Marshal
        if raw_bytes.startswith(b'\x04\x08'):
            return ['ruby_marshal_deser']
        if b'posix' in raw_bytes and b'system' in raw_bytes:
            return ['posix_system_pickle']
        if raw_bytes.startswith(b'\x80\x03') or raw_bytes.startswith(b'\x80\x04'):
            if any(term in raw_bytes for term in [b'system', b'popen', b'exec', b'subprocess', b'builtin']):
                return ['python_pickle_rce']
                
        raw = raw_bytes.decode('utf-8')
        if raw and all(32 <= ord(c) < 127 or c in '\r\n\t' for c in raw):
            return [raw]
    except Exception:
        pass
    return []

def extract_b64_from_text(s):
    if not isinstance(s, str):
        return []
    results = []
    
    # 1. data:text/html;base64,....
    data_match = re.search(r'base64,([A-Za-z0-9+/=_\-]+)', s)
    if data_match:
        results.extend(try_b64decode_string(data_match.group(1)))
        
    # 2. Key-value pairs in query or urlencoded strings
    if '=' in s:
        for part in s.split('&'):
            if '=' in part:
                k, v = part.split('=', 1)
                results.extend(try_b64decode_string(v))
                
    # 3. JSON values
    if s.strip().startswith('{') or s.strip().startswith('['):
        try:
            obj = json.loads(s)
            if isinstance(obj, dict):
                for val in obj.values():
                    if isinstance(val, str):
                        results.extend(try_b64decode_string(val))
        except Exception:
            pass
            
    # 4. Regex tokens
    for token in re.findall(r'[A-Za-z0-9+/=_\-]{16,}', s):
        results.extend(try_b64decode_string(token))
        
    return results

def normalize_variants(s):
    if not isinstance(s, str):
        return []
    variants = set()
    variants.add(s)
    
    # Unicode and overlong decoding
    ol = decode_unicode_and_overlong(s)
    if ol != s:
        variants.add(ol)
    
    # Repeated unquote_plus
    curr = s
    for _ in range(5):
        nxt = urllib.parse.unquote_plus(decode_unicode_and_overlong(curr))
        if nxt == curr:
            break
        variants.add(nxt)
        curr = nxt
    variants.add(curr)
    
    # Repeated unquote (without plus)
    curr = s
    for _ in range(5):
        nxt = urllib.parse.unquote(decode_unicode_and_overlong(curr))
        if nxt == curr:
            break
        variants.add(nxt)
        curr = nxt
    variants.add(curr)
    
    # Comment-stripped variants for all existing
    comment_stripped = set()
    for v in list(variants):
        no_comm = re.sub(r'/\*.*?\*/', ' ', v)
        if no_comm != v:
            comment_stripped.add(no_comm)
            comment_stripped.add(urllib.parse.unquote_plus(no_comm))
    variants.update(comment_stripped)
    
    # JSON parsed string extraction
    json_strings = set()
    for v in list(variants):
        vt = v.strip()
        if (vt.startswith('{') and vt.endswith('}')) or (vt.startswith('[') and vt.endswith(']')):
            try:
                obj = json.loads(vt)
                def extract_strings(o):
                    if isinstance(o, str):
                        json_strings.add(o)
                        json_strings.add(urllib.parse.unquote_plus(o))
                    elif isinstance(o, dict):
                        for k, val in o.items():
                            if isinstance(k, str):
                                json_strings.add(k)
                            extract_strings(val)
                    elif isinstance(o, list):
                        for val in o:
                            extract_strings(val)
                extract_strings(obj)
            except Exception:
                pass
    variants.update(json_strings)

    # Base64 decoded variants
    b64_variants = set()
    for v in list(variants):
        for dec in extract_b64_from_text(v):
            b64_variants.add(dec)
            b64_variants.add(urllib.parse.unquote_plus(dec))
    variants.update(b64_variants)
    
    return list(variants)

def check_sqli(text):
    # 1. UNION SELECT
    if re.search(r'\bunion\s+(?:all\s+)?select\b', text, re.I):
        return True
    
    # 2. Quote followed by boolean or comments
    if re.search(r"['\"]\s*(?:or|and)\s+['\"0-9a-z_]+\s*=\s*['\"0-9a-z_]+", text, re.I):
        return True
    if re.search(r"['\"]\s*(?:or|and)\s+\d+\s*=\s*\d+", text, re.I):
        return True
    if re.search(r"['\"]\s*\|\s*\|", text):
        return True
    # Quote followed by comment, e.g. admin'-- or ' or 1=1-- or admin'--&pass=
    if re.search(r"['\"]\s*--(?:\s|\+|--|&|$)", text):
        return True
    if re.search(r"['\"]\s*#(?:[^\w\d]|$) ", text):
        return True
    
    # 3. Stacked queries / DDL / DML
    if re.search(r";\s*(?:drop\s+table|delete\s+from|insert\s+into|update\s+\w+\s+set|select\s+.*from)\b", text, re.I):
        return True

    # 4. Error-based / SQL functions / time-based
    if re.search(r'\b(?:extractvalue|updatexml|benchmark|sleep|pg_sleep|waitfor\s+delay)\s*\(', text, re.I):
        return True
    if re.search(r'\bconvert\s*\(\s*\w+\s*,', text, re.I):
        return True
    if re.search(r'@@version\b', text, re.I):
        return True
    if re.search(r'\bprocedure\s+analyse\b', text, re.I):
        return True
    if re.search(r'\bselect\s+.*from\s+(?:information_schema|sqlite_master|pg_tables|pg_shadow|sys\.)', text, re.I):
        return True
    if re.search(r'order\s+by\s+\d+\s*--', text, re.I) or re.search(r'group\s+by\s+\d+\s*--', text, re.I):
        return True
    # Parenthesized subquery: (SELECT ... FROM ...)
    if re.search(r'\(\s*select\s+.*?from\b', text, re.I):
        return True
    if re.search(r'\bcast\s*\(\s*\(?\s*select\b', text, re.I):
        return True
    if re.search(r'\bselect\s+(?:current_database|current_user|session_user|version)\b', text, re.I):
        return True
    # Blind SQLi: AND (SELECT ...), OR (SELECT ...)
    if re.search(r'\b(?:and|or)\s*\(?\s*select\b', text, re.I):
        return True
    if re.search(r'\b(?:and|or)\s+(?:cast|convert)\s*\(', text, re.I):
        return True
    if re.search(r'\b(?:and|or)\s+.*?\bselect\b.*?\bfrom\b', text, re.I):
        return True
    if re.search(r'\b(?:limit|offset)\s+.*?\bselect\b.*?\bfrom\b', text, re.I):
        return True
    if re.search(r'\bcase\s+when\b.*?\bselect\b.*?\bfrom\b', text, re.I):
        return True
        
    return False

def check_xss(text):
    # 1. HTML tags with scripts or handlers
    if re.search(r'<\s*script\b', text, re.I):
        return True
    if re.search(r'<\s*/\s*script\b', text, re.I):
        return True
    # Any on<event>= handler
    if re.search(r'\bon\w+\s*=\s*[\'"]?[a-z0-9_$\(]', text, re.I):
        return True
    # 2. javascript: pseudoprotocol
    if re.search(r'javascript\s*:', text, re.I):
        return True
    # 3. data:text/html
    if re.search(r'data\s*:\s*text/html', text, re.I):
        return True
    # 4. <iframe, <object, <embed, <svg, <img, <style, etc.
    if re.search(r'<\s*(iframe|object|embed|svg|img|body|input|audio|video|style)\b[^>]*(\bon\w+|javascript:|data:text/html|alert)', text, re.I):
        return True
    if re.search(r'<\s*img\b[^>]*onerror', text, re.I):
        return True
    # 5. Direct JavaScript execution keywords
    if re.search(r'\balert\s*\([^)]*\)', text, re.I):
        return True
    if re.search(r'\b(?:document\.cookie|document\.domain|window\.location)\b', text, re.I):
        return True
    return False

def check_rce(text):
    # Detect executable shell command injection
    if re.search(r'[;&|`]\s*\{[a-z0-9_,-]+\}', text, re.I):
        return True
    if re.search(r'\{[a-z0-9_]+,[^}]+\}', text, re.I):
        return True
    cmd_pattern = r'(powershell|powershell\.exe|cmd|cmd\.exe|certutil|mshta|cscript|wscript|cat|nc|netcat|ncat|bash|sh|dash|zsh|curl|wget|id|whoami|uname|ls|rm|chmod|chown|kill|python|python3|perl|ruby|php|touch|echo|ping|traceroute|sleep)\b'
    # Prefixes: ;, &&, ||, |, `, $(, &
    if re.search(r'(?:[;&|`]|&&|\|\||\$\()\s*' + cmd_pattern, text, re.I):
        return True
    if re.search(r'`\s*' + cmd_pattern, text, re.I):
        return True
    # Pipe to shell
    if re.search(r'\|\s*(sh|bash|dash|zsh|powershell)\b', text, re.I):
        return True
    # /bin/sh or /bin/bash
    if re.search(r'/(?:bin|usr/bin)/(?:sh|bash|dash|zsh)\b', text, re.I):
        return True
    # CLI Argument injection (e.g. -write /.../sh.php, -exec, --checkpoint, -o /..., --output)
    if re.search(r'(?:^|[\s+])--?(?:write|exec|checkpoint|checkpoint-action)\b', text, re.I):
        return True
    if re.search(r'(?:^|[\s+])-(?:o|O|-output)\s*=?\s*/[a-z0-9_.-]+', text, re.I):
        return True
    # Git ext:: protocol RCE
    if re.search(r'\bext::[a-z0-9_-]', text, re.I):
        return True
    return False

def check_lfi(text):
    # Path traversal / LFI / RFI
    if re.search(r'(?:\.\./|\.\.\\|\.\.%2f|\.\.%5c|%2e%2e)', text, re.I):
        return True
    if re.search(r'\b(php|data|expect|input|phar|zip)://', text, re.I):
        return True
    if re.search(r'\bfile:///(?:etc|proc|windows|var|tmp|home|root|sys)', text, re.I):
        return True
    # Remote File Inclusion (RFI)
    if re.search(r'(?:module|file|include|page|template|tpl|load|plugin|doc|src)\s*=\s*https?://', text, re.I):
        return True
        
    sys_paths = r'(?:etc/(?:passwd|shadow|hosts|issue|os-release)|proc/(?:self|version|\d+)|windows/(?:win\.ini|system32))'
    if re.search(r'\b[a-zA-Z]{3,}\s+in\s+/' + sys_paths, text, re.I):
        return False
    if re.search(r'/' + sys_paths + r'\s+[a-zA-Z]{2,}\b', text, re.I):
        return False
        
    if re.search(r'(?:^|[?&=;\'"\\/])/?' + sys_paths, text, re.I):
        return True
    return False

def check_ssrf(text):
    # Dangerous schemes
    if re.search(r'\b(ldap|ldaps|gopher|dict)://', text, re.I):
        return True
    if re.search(r'\bfile:///(?:etc|proc|windows|var|tmp|home|root|sys)', text, re.I):
        return True
    # URLs with private IPs / localhost / metadata (handling credentials like user@ip)
    # e.g. http://127.1:8080 or 0x7f000001 or http://assets.example.com@169.254.169.254/
    if re.search(r'(?:https?|ftp)://(?:[^/@\s]+@)?(?:127\.\d+(?:\.\d+)*(?::\d+)?|0177\.\d+(?:\.\d+)*(?::\d+)?|0x[0-9a-fA-F]+|localhost|0\.0\.0\.0|0(?::\d+)?(?:/|$)|10\.\d+(?:\.\d+)*(?::\d+)?|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|192\.168\.\d+\.\d+|169\.254\.\d+\.\d+|2852039166|2130706433|\[[0-9a-f:]*(?:127\.|169\.254\.|10\.|192\.168\.|1|0)[0-9a-f:.]*\])', text, re.I):
        return True
    if re.search(r'\[::1\]', text) or re.search(r'\[::\]', text):
        return True
    if re.search(r'(?:latest|metadata)/(?:meta-data|instance)', text, re.I):
        return True
    if re.search(r'metadata\.google\.internal|computeMetadata|169\.254\.169\.254', text, re.I):
        return True
    if re.search(r'\b(?:rebind|nip\.io|sslip\.io)\b', text, re.I):
        return True
    if re.search(r'https?://[a-f0-9]{8}\.[a-f0-9]{8}\.', text, re.I):
        return True
    return False

def check_http_abuse_general(text):
    # Prototype pollution
    if re.search(r'__proto__|constructor[\W_]+prototype', text, re.I):
        return True
    # JWT "alg": "none" attack
    if 'eyJhbGciOiJub25l' in text:
        return True
    if re.search(r'"alg"\s*:\s*"none"', text, re.I):
        return True
    # Any URL-encoded CRLF (%0d, %0a) is ALWAYS an attack
    if re.search(r'%0[da]', text, re.I):
        return True
    # Injected HTTP headers with CRLF
    crlf_inject = r'(?:\\r\\n|\\r|\\n|[\r\n])\s*(?:Set-Cookie|Location|Content-Length|X-[\w-]+):\s*'
    if re.search(crlf_inject, text, re.I):
        return True
    # Content-Disposition: attachment injection
    if re.search(r'(?:\\r\\n|\\r|\\n|[\r\n])\s*Content-Disposition:\s*attachment', text, re.I):
        return True
    if re.search(r'(?:%0d%0a|%0d|%0a|\\r\\n|\\r|\\n|[\r\n])\s*HTTP/1\.[01]', text, re.I):
        return True
    # Host / Open Redirect abuse via @ in redirect_uri or next
    if re.search(r'(?:redirect_uri|redirect|next|url|u|to|r|goto|link|return_to)=https?://[^/]+@[^/]+', text, re.I):
        return True
    # Protocol-relative open redirect
    if re.search(r'(?:redirect_uri|redirect|next|url|target|dest|u|to|r|goto|link|return_to)=//[^\s/]+', text, re.I):
        return True
    # Backslash URL bypass: https:/\ or https:\\ or return_to=https:/%5c
    if re.search(r'https?:[/\\]*\\', text, re.I):
        return True
    # Null byte injection
    if '%00' in text or '\x00' in text:
        return True
    # HTTP Request Smuggling in body: method followed by path and HTTP/1.x
    if re.search(r'(?:GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+/[A-Za-z0-9_/.-]*\s+HTTP/1\.[01]', text):
        return True
    return False

def check_http_abuse_params(text):
    if text.strip().startswith('{') or text.strip().startswith('['):
        return False
    if 'Content-Disposition:' in text or 'boundary=' in text:
        return False
    # Check for parameter delimiter injection: %3b, %26, or raw ; followed by param=
    if re.search(r'(?:%3b|%26|;)\s*[a-z0-9_-]+=', text, re.I):
        return True
    return False

def is_ssti_inner(m_text):
    m_text = m_text.strip()
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', m_text):
        if m_text.lower() in ['config', 'self', 'request', 'lipsum', 'cycler', 'joiner', 'namespace']:
            return True
        return False
    return True

def check_ssti(text):
    # 0. Smarty {php} ... {/php}
    if re.search(r'\{php\}', text, re.I):
        return True
    if re.search(r'\{/php\}', text, re.I):
        return True
        
    # 1. {{ ... }}
    for m in re.finditer(r'\{\{(.*?)\}\}', text):
        if is_ssti_inner(m.group(1)):
            return True
            
    # 2. {% ... %}
    if re.search(r'\{%.*?%\}', text):
        return True
        
    # 3. %{ ... }, #{ ... }, *{ ... } (OGNL / Struts / Spring EL)
    if re.search(r'[%#\*]\{[^}]+\}', text):
        return True
        
    # 4. ${ ... }
    for m in re.finditer(r'\$\{(.*?)\}', text):
        if is_ssti_inner(m.group(1)):
            return True
            
    # 5. Apache Velocity / Freemarker
    if re.search(r'#set\s*\(\s*\$', text, re.I):
        return True
    if re.search(r'#(?:include|parse|evaluate|define)\s*\(', text, re.I):
        return True
    if re.search(r'\.class\.forName\(|\.getRuntime\(\)|\.getMethod\(|\.invoke\(', text):
        return True
        
    # 6. Smarty static call: {Class::method(...)}
    if re.search(r'\{[a-zA-Z0-9_]+::[a-zA-Z0-9_]+\s*\(', text):
        return True
            
    return False

def check_xxe_nosql_deser(text):
    # Deserialization signatures (Pickle, Ruby Marshal, etc.)
    if text in ['posix_system_pickle', 'python_pickle_rce', 'ruby_marshal_deser']:
        return True
    if 'BAhv' in text:
        return True
    # .NET BinaryFormatter
    if 'AAEAAAD/////' in text:
        return True
    # SnakeYAML / PyYAML unsafe tags
    if re.search(r'!!(?:javax?|python|ruby)\b', text, re.I):
        return True
    if 'ScriptEngineManager' in text:
        return True
    # NoSQL injection: [$ne], [$gt], [$where], etc.
    if re.search(r'\[\$(ne|gt|gte|lt|lte|in|nin|regex|where|exists|func|function|expr)\]', text, re.I):
        return True
    if re.search(r'"\$(ne|gt|gte|lt|lte|in|nin|regex|where|exists|func|function|expr|accumulator)"\s*:', text, re.I):
        return True
    if re.search(r'function\s*\(\s*\)\s*\{', text):
        return True
    # XXE & XML Entity Expansion (Billion Laughs)
    if re.search(r'<!ENTITY\b', text, re.I):
        return True
    if re.search(r'<!DOCTYPE\s+[^>]*\[', text, re.I):
        return True
    # PHP Deserialization: O:8:"ClassName":...
    if re.search(r'\b[Oa]:\d+:"[^"]+":\d+:', text):
        return True
    # Java Deserialization / Python pickle magic bytes
    if re.search(r'(?:rO0AB[A-Za-z0-9+/=]{4,}|cos\nsystem|c__builtin__\nexec|gASV|gAJ)', text):
        return True
    return False

def predict(req):
    path = req.get("path", "")
    query = req.get("query", "")
    body = req.get("body", "")
    headers = req.get("headers", {})
    
    # 0. Check path for matrix param / path confusion (; in path) or leading double slash
    if ';' in path or '%3b' in path.lower() or path.startswith('//') or '/%2f' in path.lower():
        return "block"
        
    # Check headers for smuggling / rewrite / poisoning / reverse proxy auth spoofing
    poison_headers = {
        'x-host', 'x-forwarded-host', 'x-rewrite-url', 'x-original-url', 'x-http-destination',
        'x-remote-user', 'x-authenticated-groups', 'x-authenticated-user', 'x-forwarded-user',
        'metadata-flavor'
    }
    for hname, hval in headers.items():
        hl = hname.lower()
        if hl == 'transfer-encoding':
            return "block"
        if hl in poison_headers:
            return "block"
            
    # Check query for SQL comments (--+, --&, -- , or trailing --)
    if query and re.search(r'--(?:\+|&|\s|$)', query):
        return "block"
    
    # 1. Parameter-specific checks for raw query and body
    param_sources = [query, body]
    for ps in param_sources:
        if not ps:
            continue
        if check_http_abuse_params(ps):
            return "block"
        
    # Gather raw fields
    raw_sources = [path, query, body]
    for hname, hval in headers.items():
        if isinstance(hval, str):
            raw_sources.append(hval)
            
    # Generate all normalized variants
    all_variants = []
    for s in raw_sources:
        if s:
            all_variants.extend(normalize_variants(s))

    for comp in all_variants:
        if not comp:
            continue
        if check_http_abuse_general(comp):
            return "block"
        if check_lfi(comp):
            return "block"
        if check_sqli(comp):
            return "block"
        if check_xss(comp):
            return "block"
        if check_rce(comp):
            return "block"
        if check_ssrf(comp):
            return "block"
        if check_ssti(comp):
            return "block"
        if check_xxe_nosql_deser(comp):
            return "block"
            
    return "allow"
