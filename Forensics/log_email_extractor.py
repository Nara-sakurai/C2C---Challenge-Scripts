import re, urllib.parse
email_chars = {}
with open('access.log') as f:
    for line in f:
        if '%21%3D' not in line: continue
        m = re.search(r'GET ([^ ]+) HTTP', line)
        if not m: continue
        url = urllib.parse.unquote(m.group(1))
        ne = re.search(r'\),(\d+),1\)\)!=(\d+),', url)
        if ne and 'user_email' in url:
            email_chars[int(ne.group(1))] = chr(int(ne.group(2)))
email = ''.join(email_chars.get(i,'?') for i in range(1, max(email_chars)+1))
print(f"Email: {email}")
