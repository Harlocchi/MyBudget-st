import streamlit as st
import pandas as pd
from datetime import date

st.title("Orçamento - Itens do Serviço")

foto = st.file_uploader("Foto (Logo ou Banner) da sua empresa", type=["jpg", "jpeg", "png"])

# Inicializa a lista de itens na sessão
if "itens" not in st.session_state:
    st.session_state.itens = []

cliente = st.text_input("Nome do Cliente")
descricao = st.text_area("Descrição do Serviço")
data_orcamento = st.date_input("Data do Orçamento", value=date.today())



# Formulário de entrada dos itens
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
        a = st.text(" ")
        adicionar = st.form_submit_button("➕ Adicionar")

    if adicionar and descricao.strip() != "":
        total = valor_unitario * quantidade
        st.session_state.itens.append({
            "Descrição": descricao,
            "Valor Unitário (R$)": valor_unitario,
            "Quantidade": quantidade,
            "Valor Total (R$)": total
        })

# Exibe a lista de itens adicionados
if st.session_state.itens:
    st.markdown("## Lista de Itens")

    for i, item in enumerate(st.session_state.itens):
        cols = st.columns([4, 2, 2, 2, 2])
        cols[0].markdown(f"**{item['Descrição']}**")
        cols[1].markdown(f"R$ {item['Valor Unitário (R$)']:.2f}")
        cols[2].markdown(f"{item['Quantidade']}")
        cols[3].markdown(f"**R$ {item['Valor Total (R$)']:.2f}**")
        if cols[4].button("🗑️", key=f"apagar_{i}"):
            st.session_state.itens.pop(i)
            st.rerun()

    total_geral = sum(item["Valor Total (R$)"] for item in st.session_state.itens)
    st.markdown(f"### **Total Geral: R$ {total_geral:,.2f}**")
