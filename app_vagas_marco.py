import streamlit as st
import urllib.parse
import time

def gerar_links_vagas(cargo, localizacao, modalidade):
    cargo_formatado = urllib.parse.quote_plus(cargo)
    local_formatado = urllib.parse.quote_plus(localizacao)

    links = {}

    links["Catho"] = f"https://www.catho.com.br/vagas/?q={cargo_formatado}&where={local_formatado}"
    links["Gupy"] = f"https://www.gupy.io/vagas?jobTitle={cargo_formatado}&location={local_formatado}"
    links["Indeed"] = f"https://br.indeed.com/empregos?q={cargo_formatado}&l={local_formatado}"
    links["InfoJobs"] = f"https://www.infojobs.com.br/empregos.aspx?Palabra={cargo_formatado}&Lugar={local_formatado}"

    if modalidade != "Indiferente":
        links = {nome: f"{url}&modalidade={modalidade.lower()}" for nome, url in links.items()}

    return links

def tela_inicial():
    st.image(
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
        caption="Cresça profissionalmente com as oportunidades certas!",
        use_column_width=True
    )

    st.title("🔍 Buscador de Vagas - Marco Antônio")
    st.markdown("""
    Bem-vindo ao seu aplicativo pessoal de busca de vagas!  
    Aqui você encontra oportunidades em **Catho**, **Gupy**, **Indeed** e **InfoJobs**.

    Clique no botão abaixo para iniciar sua busca por crescimento profissional. 🚀
    """)

    if st.button("🚀 Iniciar Busca"):
        with st.spinner("Preparando ferramentas..."):
            for percent in range(0, 101, 10):
                st.progress(percent)
                time.sleep(0.1)
        st.success("Tudo pronto! Vamos começar.")
        time.sleep(0.5)
        st.session_state["pagina"] = "busca"

def tela_busca():
    st.title("🎯 Encontre as melhores oportunidades")
    st.markdown("""
    Preencha os campos abaixo e clique em **Buscar Vagas**.  
    Vamos buscar para você as melhores vagas em **Catho, Gupy, Indeed e InfoJobs**!
    """)

    with st.form("form_busca_vagas"):
        cargo = st.text_input("🔎 Cargo / Área de Interesse", placeholder="Ex: Gerente de Projetos")
        local = st.text_input("📍 Localização", placeholder="Ex: São Bernardo do Campo - SP")
        modalidade = st.selectbox("🏢 Modalidade", ["Indiferente", "Presencial", "Remoto", "Híbrido"])
        buscar = st.form_submit_button("🔍 Buscar Vagas")

    if buscar:
        if not cargo or not local:
            st.warning("⚠️ Por favor, preencha todos os campos antes de buscar.")
            return

        st.success("Buscando nas plataformas...")

        links = gerar_links_vagas(cargo, local, modalidade)
        st.session_state["resultado_links"] = links
        st.session_state["contador_buscas"] += 1
        st.session_state["pagina"] = "resultados"

def tela_resultados():
    st.title("📄 Resultados da Busca")
    st.markdown("Veja abaixo os links para as plataformas com os filtros que você aplicou:")

    for nome, url in st.session_state.get("resultado_links", {}).items():
        st.markdown(f"- [{nome}]({url})")

    st.success("🎯 Busca concluída! Esperamos que encontre a vaga perfeita. Boa sorte, Marco Antônio! 🍀")
    st.info(f"🔄 Número de buscas nesta sessão: {st.session_state['contador_buscas']}")

def main():
    st.set_page_config(page_title="Buscador de Vagas", page_icon="🔍")

    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "inicial"
        st.session_state["contador_buscas"] = 0

    if st.session_state["pagina"] == "inicial":
        tela_inicial()
    elif st.session_state["pagina"] == "busca":
        tela_busca()
    elif st.session_state["pagina"] == "resultados":
        tela_resultados()

if __name__ == "__main__":
    main()
