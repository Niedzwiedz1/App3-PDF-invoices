import pandas as pd
import glob
import fpdf
from pathlib import Path

filepaths = glob.glob("invoices/*.xlsx")

# Crete pdf files from excel file names
for filepath in filepaths:
    pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    filename = Path(filepath).stem
    invoice_nr, date = filename.split("-")

# Add invoice number
    pdf.set_font(family="Times", style="B", size=12)
    pdf.cell(w=50, h=8, txt=f"Invoice nr: {invoice_nr}", ln=1, align="L")

# Add invoice date
    pdf.set_font(family="Times", style="B", size=12)
    pdf.cell(w=50, h=8, txt=f"Date {date}", ln=1, align="L")

    df = pd.read_excel(filepath, sheet_name="Sheet 1")

# Add name of the table columns
    column_names = list(df.columns)
    column_names = [item.replace("_", " ").title() for item in column_names]

    pdf.set_font(family="Times", style="B", size=10)
    pdf.cell(w=30, h=8, txt=column_names[0], border=1)
    pdf.cell(w=50, h=8, txt=column_names[1], border=1)
    pdf.cell(w=30, h=8, txt=column_names[2], border=1)
    pdf.cell(w=30, h=8, txt=column_names[3], border=1)
    pdf.cell(w=30, h=8, txt=column_names[4], border=1, ln=1)

# Add row to the table
    for index, row in df.iterrows():

        pdf.set_font(family="Times", style="B", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
        pdf.cell(w=50, h=8, txt=str(row["product_name"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

# Add sum of the prices
    total_sum = df["total_price"].sum()
    pdf.set_font(family="Times", style="B", size=10)
    pdf.cell(w=30, h=8, border=1)
    pdf.cell(w=50, h=8, border=1)
    pdf.cell(w=30, h=8, border=1)
    pdf.cell(w=30, h=8, border=1)
    pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

# Add sum sentence
    pdf.set_font(family="Times", style="B", size=12)
    pdf.cell(w=0, h=8, align="L", ln=1, txt=f"The total due amount is {total_sum} Euros")

# Add company name and logo
    pdf.set_font(family="Times", style="B", size=12)
    pdf.cell(w=25, h=8, align="L", txt=f"Python How")
    pdf.image("logo.png", w=8)

    pdf.output(f"pdf/{filename}.pdf")


