import fitz

doc = fitz.open(r'C:\Users\Harik\.gemini\antigravity-ide\brain\afbc5b5f-e8b4-4374-8052-5dd3fc252dfb\.user_uploaded\media_1789534853550.pdf')
for pno in range(len(doc)):
    page = doc[pno]
    print(f"\n============================== PAGE {pno+1} ==============================")
    for b in page.get_text('dict')['blocks']:
        if 'lines' in b:
            for l in b['lines']:
                line_str = " ".join([s['text'] for s in l['spans']]).strip()
                if line_str:
                    first_span = l['spans'][0]
                    sz = first_span['size']
                    bold = "B" if "Bold" in first_span['font'] else " "
                    # encode to safe ascii
                    safe_line = line_str.encode('ascii', errors='replace').decode('ascii')
                    print(f"[{sz:4.1f}pt {bold}] {safe_line}")
