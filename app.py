from datetime import datetime
from io import BytesIO
from flask import Flask, render_template, render_template_string, request, send_file
from docx import Document
import os

app = Flask(__name__, template_folder='.')

CAMINHO_MODELO = os.path.join(os.path.dirname(__file__), 'Procuração Pessoa Física.docx')

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # 1) Captura dos dados do formulário
        dados = {
            "<<NOME>>":            request.form.get("nome_completo", ""),
            "<<ESTADO CIVIL>>":      request.form.get("estado_civil", ""),
            "<<NACIONALIDADE>>":   request.form.get("nacionalidade", ""),
            "<<CPF>>":             request.form.get("cpf", ""),
            "<<DATA NASCIMENTO>>": request.form.get("data_nascimento", ""),
            "<<PROFISSAO>>":       request.form.get("profissao", ""),
            "<<CIDADE NASCIMENTO>>": request.form.get("cidade_nascimento", ""),
            "<<ESTADO NASCIMENTO>>": request.form.get("estado_nascimento", ""),
            "<<RG>>":                request.form.get("numero_rg", ""),
            "<<ORGAO EMISSOR>>":     request.form.get("orgao_emissor", ""),
            "<<ESTADO EMISSOR>>":    request.form.get("estado_emissor", ""),
            "<<NOME PAI>>":          request.form.get("nome_pai", ""),
            "<<NOME MAE>>":          request.form.get("nome_mae", ""),
            "<<CIDADE DOMICILIO>>":  request.form.get("cidade_domicilio", ""),
            "<<ESTADO DOMICILIO>>":  request.form.get("estado_domicilio", ""),
            "<<LOGRADOURO DOMICILIO>>":        request.form.get("logradouro", ""),
            "<<RUA DOMICILIO>>":               request.form.get("rua", ""),
            "<<NUMERO DOMICILIO>>":            request.form.get("numero", ""),
            "<<BAIRRO DOMICILIO>>":            request.form.get("bairro", ""),
            "<<CEP>>":               request.form.get("cep", ""),
        }

        # 2) Captura data e hora de preenchimento
        data_preenchimento = datetime.now().strftime("%d/%m/%Y")
        # Você pode injetar esse valor em um placeholder, por exemplo:
        dados["<<DATA PREENCHIMENTO>>"] = data_preenchimento

        if not os.path.isfile(CAMINHO_MODELO):
            return f"Arquivo modelo não encontrado em: {CAMINHO_MODELO}", 500

        # Abre e preenche o documento
        doc = Document(CAMINHO_MODELO)
        def substituir(p):
            for run in p.runs:
                for ph, val in dados.items():
                    if ph in run.text:
                        run.text = run.text.replace(ph, val)

        for p in doc.paragraphs:
            substituir(p)
        for tbl in doc.tables:
            for row in tbl.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        substituir(p)

        # Gera o nome e salva no servidor
        pasta = os.path.dirname(CAMINHO_MODELO)
        nome_pessoa = request.form.get("nome_completo", "documento").strip().replace(" ", "_")
        nome_saida = f"{nome_pessoa}_Procuração_PF.docx"
        caminho_saida = os.path.join(pasta, nome_saida)
        doc.save(caminho_saida)

        # Retorna página de sucesso mostrando o caminho no servidor
        return render_template_string("""
            <h2>Documento gerado com sucesso!</h2>/
            <p>Arquivo salvo em: {caminho_saida}</p>""")

    # GET: exibe o formulário
    return render_template('form.html')

from flask import send_from_directory

@app.route('/download/<filename>')
def download_file(filename):
    pasta = '/opt/render/project/src'
    return send_from_directory(pasta, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)