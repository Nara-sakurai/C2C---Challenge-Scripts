import struct
# Linux input event structure
EVENT_FORMAT = 'QQHHi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)
# Linux key code to character mapping
KEY_MAP = {
    2:'1', 3:'2', 4:'3', 5:'4', 6:'5', 7:'6', 8:'7', 9:'8', 10:'9', 11:'0',
    12:'-', 13:'=', 16:'q', 17:'w', 18:'e', 19:'r', 20:'t', 21:'y', 22:'u',
    23:'i', 24:'o', 25:'p', 26:'[', 27:']', 30:'a', 31:'s', 32:'d', 33:'f',
    34:'g', 35:'h', 36:'j', 37:'k', 38:'l', 39:';', 40:"'", 44:'z', 45:'x',
    46:'c', 47:'v', 48:'b', 49:'n', 50:'m', 51:',', 52:'.', 53:'/', 57:' ',
    28:'\n', 14:'<BS>', 42:'<LSHIFT>', 54:'<RSHIFT>', 58:'<CAPS>',
    15:'\t', 1:'<ESC>', 29:'<LCTRL>', 97:'<RCTRL>'
}
# Shift key mappings
SHIFT_MAP = {
    2:'!', 3:'@', 4:'#', 5:'$', 6:'%', 7:'^', 8:'&', 9:'*', 10:'(', 11:')',
    12:'_', 13:'+', 39:':', 40:'"', 51:'<', 52:'>', 53:'?', 26:'{', 27:'}',
    30:'A', 31:'S', 32:'D', 33:'F', 34:'G', 35:'H', 36:'J', 37:'K', 38:'L',
    44:'Z', 45:'X', 46:'C', 47:'V', 48:'B', 49:'N', 50:'M',
    16:'Q', 17:'W', 18:'E', 19:'R', 20:'T', 21:'Y', 22:'U', 23:'I', 24:'O', 25:'P'
}
def decode_keylog(filename):
    with open(filename, 'rb') as f:
        data = f.read()
   
    shift_pressed = False
    caps_lock = False
    captured_text = []
   
    for i in range(0, len(data), EVENT_SIZE):
        if i + EVENT_SIZE > len(data):
            break
       
        event = struct.unpack(EVENT_FORMAT, data[i:i+EVENT_SIZE])
        tv_sec, tv_usec, typ, code, value = event
       
        # Type 1 = key press/release event
        if typ != 1:
            continue
       
        # Handle shift keys
        if code in (42, 54): # Left/Right shift
            shift_pressed = (value in (1, 2))
       
        # Handle caps lock
        elif code == 58 and value == 1:
            caps_lock = not caps_lock
       
        # Handle backspace
        elif code == 14 and value in (1, 2):
            if captured_text:
                captured_text.pop()
       
        # Handle enter
        elif code == 28 and value in (1, 2):
            captured_text.append('\n')
       
        # Handle regular keys (on press only)
        elif value in (1, 2) and code not in (29, 97): # Ignore Ctrl keys
            effective_shift = shift_pressed ^ (caps_lock and code in range(16, 51))
           
            if effective_shift and code in SHIFT_MAP:
                captured_text.append(SHIFT_MAP[code])
            elif code in KEY_MAP:
                captured_text.append(KEY_MAP[code])
   
    return ''.join(captured_text)
if __name__ == '__main__':
    text = decode_keylog('cron.aseng')
    print(text)
