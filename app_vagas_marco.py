
import streamlit as st
import streamlit.components.v1 as components
import fitz  # PyMuPDF para ler PDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import tempfile

# Função para extrair texto do PDF
def extrair_texto_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    doc = fitz.open(tmp_path)
    texto = ""
    for page in doc:
        texto += page.get_text()
    return texto.lower()

# Palavras-chave
PALAVRAS_CERTAS = ["projetos", "scrum", "sap", "erp", "cloud", "power bi", "jira"]
PALAVRAS_AMPLAS = ["administração", "negócio", "gestão", "análise de sistemas", "cloud computing"]

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Busca no LinkedIn
def buscar_linkedin(keywords):
    driver = iniciar_driver()
    driver.get("https://www.linkedin.com/jobs/search/?keywords=gerente%20de%20projetos&location=São%20Paulo")
    time.sleep(5)
    vagas = driver.find_elements(By.CLASS_NAME, "base-search-card__title")
    resultados = []
    for vaga in vagas:
        titulo = vaga.text.lower()
        if any(k in titulo for k in keywords):
            link = vaga.find_element(By.XPATH, "..").get_attribute("href")
            resultados.append((vaga.text, link))
    driver.quit()
    return resultados

# Busca na Gupy
def buscar_gupy(keywords):
    driver = iniciar_driver()
    driver.get("https://portal.gupy.io/job-search/gerente%20de%20projetos")
    time.sleep(5)
    resultados = []
    try:
        vagas = driver.find_elements(By.CLASS_NAME, "sc-oqQ8jv.gBRbFA")
        for vaga in vagas:
            try:
                titulo = vaga.find_element(By.CLASS_NAME, "sc-iBPTik.jFkljf").text.lower()
                link = vaga.find_element(By.TAG_NAME, "a").get_attribute("href")
                if any(k in titulo for k in keywords):
                    resultados.append((titulo.title(), link))
            except:
                continue
    except:
        pass
    driver.quit()
    return resultados

# Interface principal
def main():
    st.title("🔍 Buscador de Vagas Marco Antônio")
    uploaded_file = st.file_uploader("Envie seu currículo (PDF)", type=["pdf"])
    
    if uploaded_file:
        texto_cv = extrair_texto_pdf(uploaded_file)
        st.success("Currículo carregado com sucesso!")

        opcao = st.radio("Qual tipo de busca você deseja?", ("Busca Certeira", "Busca Abrangente"))
        if opcao == "Busca Certeira":
            palavras = PALAVRAS_CERTAS
        else:
            palavras = PALAVRAS_CERTAS + PALAVRAS_AMPLAS

        if st.button("🔍 Buscar Vagas Agora"):
            st.info("Buscando no LinkedIn...")
            resultados_linkedin = buscar_linkedin(palavras)

            st.info("Buscando na Gupy...")
            resultados_gupy = buscar_gupy(palavras)

            st.subheader("📄 Vagas no LinkedIn:")
            if resultados_linkedin:
                for idx, (titulo, link) in enumerate(resultados_linkedin):
                    components.html(f'<a href="{link}" target="_blank" style="font-size:20px;text-decoration:none;">🔗 {titulo}</a><br>', height=40)
            else:
                st.write("Nenhuma vaga encontrada.")

            st.subheader("📄 Vagas na Gupy:")
            if resultados_gupy:
                for idx, (titulo, link) in enumerate(resultados_gupy):
                    components.html(f'<a href="{link}" target="_blank" style="font-size:20px;text-decoration:none;">🔗 {titulo}</a><br>', height=40)
            else:
                st.write("Nenhuma vaga encontrada.")

if __name__ == "__main__":
    main()
