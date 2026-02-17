with open('decrypted.txt', 'r') as f:
    content = f.read()
result = []
for line in content.strip().split('\n'):
    parts = line.split()
    if not parts:
        continue
   
    # Skip the address (first field)
    for word in parts[1:]:
        try:
            val = int(word, 8) # Convert from octal to integer
           
            # od outputs 16-bit little-endian words
            b1 = val & 0xFF # Low byte
            b2 = (val >> 8) & 0xFF # High byte
           
            if b1:
                result.append(chr(b1))
            if b2:
                result.append(chr(b2))
        except:
            pass
text = ''.join(result)
print(text)
# Extract the flag
import re
flags = re.findall(r'[A-Z0-9]+\{[^}]+\}', text)
if flags:
    print("\n" + "="*60)
    print("FLAG FOUND:")
    print("="*60)
    for flag in flags:
        print(flag)
