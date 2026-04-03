from fpdf import FPDF
from datetime import datetime
THEMES = {
    "light": {"bg": (255, 255, 255), "table_bg": (245, 245, 245)},
    "dark": {"bg": (30, 30, 30), "table_bg": (50, 50, 50)}
}


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    pair1 = int(hex_color[0:2], 16)
    pair2 = int(hex_color[2:4], 16)
    pair3 = int(hex_color[4:6], 16)

    return pair1, pair2, pair3

def generate_invoice(brand_name, client, items, invoice_no, font_color, accent_color, font_family, theme, brand_style, logo = None, brand_font_size = 26):
    colors = THEMES.get(theme, THEMES["light"])
    fc = hex_to_rgb(font_color)
    ac = hex_to_rgb(accent_color)
    if not invoice_no:
        invoice_no = "001"
    bg = colors["bg"]
    table_bg = colors["table_bg"]
    font_map = {
    "Inter": "DejaVu",
    "Roboto": "DejaVu",
    "Montserrat": "DejaVu",
    "Playfair Display": "DejaVu",
    "Merriweather": "DejaVu",
    "Courier New": "DejaVu",
    "DejaVu": "DejaVu"
    } 
    pdf_font = font_map.get(font_family, "DejaVu")
    pdf = FPDF()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVu', 'I', 'DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVu', 'BI', 'DejaVuSans.ttf', uni=True)
    pdf.add_page()
    pdf.set_fill_color(*bg)
    pdf.rect(0,0, 210, 297, "F")
    pdf.set_font(pdf_font, brand_style, brand_font_size)
    pdf.set_text_color(*ac)
    pdf.cell(w=0,h=14,text=brand_name,border=0,ln=1,align="R",fill=False)
    pdf.set_draw_color(*ac)
    pdf.set_line_width(0.8)
    y = pdf.get_y()
    pdf.line(10, y, 200, y)
    pdf.ln(4)
    pdf.set_font(pdf_font, brand_style, 12)
    pdf.set_text_color(*fc)
    pdf.cell(w=0, h=8, text=f"Billed To: {client['name']}  |  {client['email']}", border=0, ln=1, align="L")
    pdf.cell(w=0, h=8, text=f"Invoice No: {invoice_no}", border=0, ln=1, align="L")
    pdf.cell(w=0, h=8, text=f"Date: {datetime.today().strftime('%B %d, %Y')}", border=0, ln=1, align="L")
    pdf.ln(8)
    pdf.set_fill_color(*ac)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font(pdf_font, "B", 10)
    pdf.cell(w=90, h=9, text=f"Description", border=0, align="L", fill= True)
    pdf.cell(w=30, h=9, text=f"Quantity", border=0, align="C", fill = True)
    pdf.cell(w=35, h=9, text=f"Unit Price", border=0, align="C", fill = True)
    pdf.cell(w=35, h=9, text=f"Total", border=0, align="C", fill = True, ln= 1)
    pdf.set_text_color(*fc)
    pdf.set_font(pdf_font, "", 10)
    grand_total = 0
    for i, item in enumerate(items):
        if i % 2 == 0:
            pdf.set_fill_color(*bg)
        else:
            pdf.set_fill_color(*table_bg) 
        total = item["qty"] * item["price"]
        grand_total += total
        pdf.cell(w=90, h=9, text=f"{item['description']}", border=0, align="L", fill = True)
        pdf.cell(w=30, h=9, text=f"{item['qty']}", border=0, align="C", fill = True)
        pdf.cell(w=35, h=9, text=f"₦{item['price']:.2f}", border=0, align="C", fill = True)
        pdf.cell(w=35, h=9, text=f"₦{total:.2f}", border=0, align="C", fill = True, ln= 1)
    pdf.ln(4)
    pdf.set_font(pdf_font, "B", 12)
    pdf.set_fill_color(*ac)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(w=155, h=9, text="Grand Total", border=0, align="R", fill=False)
    pdf.cell(w=35, h=9, text=f"₦{grand_total:.2f}", border=0, align="C", fill=True)

    return bytes(pdf.output())








    
    

