import os
import glob
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

def convert_txt_to_pdf():
    os.makedirs("outbound", exist_ok=True)
    txt_files = sorted(set(glob.glob("inbound/**/*.txt", recursive=True) + glob.glob("inbound/*.txt")))
    for txt in txt_files:
        base = os.path.splitext(os.path.basename(txt))[0]
        out = os.path.join("outbound", base + ".pdf")
        with open(txt, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [ln.rstrip('\n') for ln in f]
        c = canvas.Canvas(out, pagesize=LETTER)
        width, height = LETTER
        margin_x = 72
        margin_top = 72
        line_height = 12
        max_lines = int((height - margin_top*2) / line_height)
        y = height - margin_top
        line_count = 0
        for line in lines:
            if line_count >= max_lines:
                c.showPage()
                y = height - margin_top
                line_count = 0
            if len(line) == 0:
                c.drawString(margin_x, y - line_count*line_height, "")
                line_count += 1
                continue
            for i in range(0, len(line), 90):
                segment = line[i:i+90]
                c.drawString(margin_x, y - line_count*line_height, segment)
                line_count += 1
                if line_count >= max_lines:
                    break
        c.save()
        print("Wrote", out)

if __name__ == "__main__":
    convert_txt_to_pdf()
