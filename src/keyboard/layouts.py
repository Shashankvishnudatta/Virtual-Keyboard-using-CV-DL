from src.keyboard.virtual_keys import VirtualKey

def get_qwerty_layout(start_x=220, start_y=320, key_w=65, key_h=65, gap=12):
    keys = []
    
    # 1. The 3 Predictive AI Action Buttons (Floating at the top)
    pred_y = start_y - (key_h + 30) # 30px gap above the main keyboard
    pred_width = int(key_w * 3.5)   # Make them wide to fit whole words
    
    keys.append(VirtualKey("PRED_0", start_x, pred_y, pred_width, key_h))
    keys.append(VirtualKey("PRED_1", start_x + pred_width + gap, pred_y, pred_width, key_h))
    keys.append(VirtualKey("PRED_2", start_x + (pred_width * 2) + (gap * 2), pred_y, pred_width, key_h))

    # 2. The Main QWERTY Layout
    keyboard_rows = [
        ["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M", "DEL"] 
    ]
    
    for i, row in enumerate(keyboard_rows):
        for j, label in enumerate(row):
            indent = i * 25 
            x = start_x + j * (key_w + gap) + indent
            y = start_y + i * (key_h + gap)
            
            width = int(key_w * 1.5) if label == "DEL" else key_w
            keys.append(VirtualKey(label, x, y, width, key_h))
            
    row_4_y = start_y + 3 * (key_h + gap)
    keys.append(VirtualKey("SPACE", start_x + 145, row_4_y, (key_w * 6), key_h))
    keys.append(VirtualKey("CLR", start_x + 630, row_4_y, int(key_w * 2), key_h))
            
    return keys