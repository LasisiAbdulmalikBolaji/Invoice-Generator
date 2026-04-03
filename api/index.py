from flask import Flask, request, send_file, render_template
import os
import io
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from invoice_engine import generate_invoice



app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods= ["POST"])
def generate():
    data = request.get_json()
    pdf_bytes= generate_invoice(data['brandName'], data['client'], data['items'], data['invoiceNo'], data['fontColor'], data['accentColor'], data['fontFamily'], data['theme'], data['brandStyle'], data.get('logo', None), data.get('brandFontSize', 26))
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True, download_name=f"{data['invoiceNo']}.pdf")


# only start the server if the file is being run on the pc not on vercel
if __name__ =="__main__":
    app.run(debug=True)

