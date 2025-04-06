import streamlit as st
import pandas as pd
from datetime import date
from fpdf import FPDF
import tempfile
import os
import imghdr
from datetime import datetime
import streamlit.components.v1 as components


n_budget = 1

# Deixa a página mais larga
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        .main .block-container {
            max-width: 95%;
            padding-left: 3rem;
            padding-right: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

htmlfile = open("adsense.html", "r", encoding="utf-8")
source_code = htmlfile.read()
print(source_code)
components.html(source_code, height=150)



st.title("Orçamento - Itens do Serviço")

# Upload da imagem (logo/banner)
foto = st.file_uploader("Foto (Logo ou Banner) da sua empresa", type=["jpg", "jpeg", "png"])
if foto:
    st.image(foto, width=150)

# Inicializa a lista de itens
if "itens" not in st.session_state:
    st.session_state.itens = []

# Dados gerais
company_cnpj = st.text_input("CNPJ da empresa")
company_fone = st.text_input("Telefone da empresa")
cliente = st.text_input("Nome do Cliente")
descricao_servico = st.text_area("Descrição do Serviço")
data_orcamento = st.date_input("Data do Orçamento", value=date.today())

# Formulário de itens
st.title("Lista de Materiais")
with st.form("form_itens"):
    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])

    with col1:
        descricao = st.text_input("Descrição do Item")
    with col2:
        valor_unitario = st.number_input("Valor Unitário (R$)", min_value=0.0, step=0.01)
    with col3:
        quantidade = st.number_input("Quantidade", min_value=1, step=1, value=1)
    with col4:
        st.markdown("")
        st.text(" ")
        adicionar = st.form_submit_button("➕ Adicionar")

    if adicionar and descricao.strip() != "":
        total = valor_unitario * quantidade
        st.session_state.itens.append({
            "Descrição": descricao.strip(),
            "Valor Unitário (R$)": valor_unitario,
            "Quantidade": quantidade,
            "Valor Total (R$)": total
        })

# Exibição da tabela
if st.session_state.itens:
    st.markdown("## Lista de Itens")

    # Cabeçalho
    header = st.columns([4, 2, 2, 2, 1])
    header[0].markdown("**Descrição**")
    header[1].markdown("**Valor Unitário (R$)**")
    header[2].markdown("**Quantidade**")
    header[3].markdown("**Valor Total (R$)**")
    header[4].markdown("**Remover**")

    # Linhas
    for i, item in enumerate(st.session_state.itens):
        cols = st.columns([4, 2, 2, 2, 1])
        cols[0].write(item["Descrição"])
        cols[1].write(f"R$ {item['Valor Unitário (R$)']:.2f}")
        cols[2].write(item["Quantidade"])
        cols[3].write(f"R$ {item['Valor Total (R$)']:.2f}")
        if cols[4].button("🗑️", key=f"remover_{i}"):
            st.session_state.itens.pop(i)
            st.rerun()

    total_geral = sum(item["Valor Total (R$)"] for item in st.session_state.itens)
    st.markdown(f"### **Total Geral: R$ {total_geral:,.2f}**")

# Classe PDF
class PDF(FPDF):
    def __init__(self, logo_path=None):
        super().__init__()
        self.logo_path = logo_path

    def header(self):
        # Logo centralizado no topo
        if self.logo_path:
            self.image(self.logo_path, x=10, y=10, w=60)

        # Bloco com dados da empresa (em "caixinha" à direita)
        self.set_xy(130, 10)
        self.set_font("Arial", "", 10)



        # Caixa 1: Criado em
        self.set_xy(130, 28)
        self.cell(30, 8, "Criado em:", border=1)
        self.cell(30, 8, f"{datetime.now().strftime('%d/%m/%Y')}", border=1, ln=1)


        # Caixa 2: Orçamento nº
        self.set_xy(130, 36)
        self.cell(30, 8, "Orçamento nº :", border=1)
        self.cell(30, 8, n_budget, border=1, ln=1)

        self.set_xy(130, 44)
        self.cell(30, 8, "Telefone:", border=1)
        self.cell(30, 8, f"{company_fone}", border=1, ln=1)


    

        # Título centralizado
        self.set_xy(10, 60)
        self.set_font("Arial", "B", 16)
        self.cell(190, 30, "ORÇAMENTO DE SERVIÇO", ln=True, align="C")
        self.ln(5)

# Geração do PDF
if st.button("📄 Gerar PDF"):
    logo_temp_path = None
    if foto:
        image_bytes = foto.read()
        image_type = imghdr.what(None, image_bytes)
        
        if image_type not in ["jpeg", "png"]:
            st.error("❌ Tipo de imagem inválido. Envie um arquivo JPG ou PNG.")
        else:
            # Cria um arquivo temporário com a extensão correta
            temp_logo = tempfile.NamedTemporaryFile(delete=False, suffix=f".{image_type}")
            temp_logo.write(image_bytes)
            temp_logo.close()
            logo_temp_path = temp_logo.name
    else:
        logo_temp_path = None
    

    pdf = PDF(logo_path=logo_temp_path)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Dados do orçamento
    pdf.cell(0, 10, f"Cliente: {cliente}", ln=True)
    pdf.cell(0, 10, f"CNPJ: {company_cnpj}", ln=True)
    pdf.cell(0, 10, f"Telefone: {company_fone}", ln=True)
    pdf.cell(0, 10, f"Data: {data_orcamento.strftime('%d/%m/%Y')}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Descrição do Serviço:\n{descricao_servico}")
    pdf.ln(5)

    # Cabeçalho da tabela
    pdf.set_font("Arial", "B", 12)
    pdf.cell(80, 10, "Descrição", border=1)
    pdf.cell(30, 10, "Unitário (R$)", border=1)
    pdf.cell(30, 10, "Quantidade", border=1)
    pdf.cell(40, 10, "Total (R$)", border=1, ln=True)

    pdf.set_font("Arial", "", 12)
    for item in st.session_state.itens:
        desc = item["Descrição"]
        # Garante que a descrição não ultrapasse o limite
        desc = (desc[:40] + '...') if len(desc) > 43 else desc
        pdf.cell(80, 10, desc, border=1)
        pdf.cell(30, 10, f"{item['Valor Unitário (R$)']:.2f}", border=1)
        pdf.cell(30, 10, str(item["Quantidade"]), border=1)
        pdf.cell(40, 10, f"{item['Valor Total (R$)']:.2f}", border=1, ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(140, 10, "Total Geral", border=1)
    pdf.cell(40, 10, f"R$ {total_geral:.2f}", border=1, ln=True)

    # Salvar o PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        pdf.output(f.name)
        st.success("✅ PDF gerado com sucesso!")
        st.download_button("📥 Baixar PDF", data=open(f.name, "rb"), file_name=f"orcamento-{cliente}.pdf")

    # Limpeza da imagem temporária
    if logo_temp_path and os.path.exists(logo_temp_path):
        os.remove(logo_temp_path)
    n_budget+=1