import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

def load_from_exel(file): #* podzieliłem na żeby wczytanie było osobno 
    filename = Path(file).stem
    invoice_nr, date = filename.split("-")
    df = pd.read_excel(file, sheet_name="Sheet 1")
    return invoice_nr,date,df

def make_pdf(invoice_nr,date,df): #* tutaj jest tylko praktycznie tworzenie pdf
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)

    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=50, h=8, txt=f"Date:{date}", ln=1)

    # Add a header
    columns = df.columns
    columns = [item.replace("_", " ").title() for item in columns]
    pdf.set_font(family="Times", size=10, style="B")
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt=columns[0], border=1)
    pdf.cell(w=70, h=8, txt=columns[1], border=1)
    pdf.cell(w=30, h=8, txt=columns[2], border=1)
    pdf.cell(w=30, h=8, txt=columns[3], border=1)
    pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

    # Add rows to the table
    for _, row in df.iterrows():     #! tutaj Ci zmieniłem jak nie używasz indexu to jak dasz _ to jest jako zmienna której nie planujesz używać
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
        pdf.cell(w=70, h=8, txt=str(row["product_name"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["amount_purchased"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

    total_sum = df["total_price"].sum()
    pdf.set_font(family="Times", size=10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=70, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt="", border=1)
    pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

    # Add total sum sentence
    pdf.set_font(family="Times", size=10, style="B")
    pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)

    # Add company name and logo
    pdf.set_font(family="Times", size=14, style="B")
    pdf.cell(w=25, h=8, txt=f"PythonHow")
    pdf.image("pythonhow.png", w=10)
    filename=invoice_nr+"-"+date
    pdf.output(f"PDFs/{filename}.pdf")


if __name__ == "__main__": # to jest tylko takie zabezpieczenie, żeby jakbyś zaimportował ten plik to się nie odpali bezpośrednio bo nie jest to główna funkcja 
    files = glob.glob("invoices/*.xlsx")
    #* starałem się trzymać w tym jak to robiłeś ty ale zmieniłem sposób żeby było bardziej czytelnie (jak będziesz miał duże ilości kodu to chcesz mieć elementy, które możesz używać wiele razy)
    for file in files:
        invoice_nr,date,df=load_from_exel(file)
        make_pdf(invoice_nr,date,df)
