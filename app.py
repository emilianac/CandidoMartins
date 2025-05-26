from datetime import datetime
from io import BytesIO
from flask import Flask, render_template, render_template_string, request, send_file
from docx import Document
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__, template_folder='.')

CAMINHO_MODELO = os.path.join(os.path.dirname(__file__), 'Procuração Pessoa Física.docx')

def enviar_email_com_anexo(destino, assunto, corpo, arquivo_bytes, nome_arquivo):
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = 'seuemail@gmail.com'  # seu email Gmail
    msg['To'] = destino
    msg.set_content(corpo)
    msg.add_attachment(arquivo_bytes,
                       maintype='application',
                       subtype='vnd.openxmlformats-officedocument.wordprocessingml.document',
                       filename=nome_arquivo)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('emilianacandsilva@gmail.com', 'tumb gwsq dcba jvdl')
        smtp.send_message(msg)

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
        nome_pessoa = request.form.get("nome_completo", "documento").strip().replace(" ", "_")
        nome_saida = f"{nome_pessoa}_Procuração_PF.docx"

        file_stream = BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        arquivo_bytes = file_stream.read()

        # Envia email automático pra você
        enviar_email_com_anexo(
            destino='emilianacand@gmail.com',
            assunto='Novo documento gerado',
            corpo='Segue em anexo o documento gerado pelo formulário.',
            arquivo_bytes=arquivo_bytes,
            nome_arquivo=nome_saida
        )
      
    return render_template('form.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)