import pandas as pd
import plotly.express as px
import streamlit as st
import curso_sudeste as csu 


print("comecando")

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Tabela IBGE - Escolaridade Sudeste",
    page_icon="📊",
    layout="wide",
)
df_bruto = csu.carregar_dados_brutos()
if not df_bruto.empty:
    df_percentual = csu.filtrar_tabela(df_bruto, ['Estado', 'Porcentagem', 'Nivel_Instrucao', 'Ano'])
    print(df_bruto)
else:
    st.warning("Dataframe Bruto Vazio")

if not df_percentual.empty:
    print('Não tá vazio')
    print(df_percentual)
else:
    print('Dataframe filtrado tá vazio em!')
    st.warning("Dataframe filtrado Vazio")

# Título Principal
st.title("📊 Evolução da Escolaridade no Sudeste (IBGE)")
st.markdown(
    "Visualização da evolução histórica da taxa de ensino superior baseada na API SIDRA (Pesquisa PNAD Contínua)."
)

if not df_percentual.empty:
    df_percentual["Nivel_Instrucao"] = df_percentual["Nivel_Instrucao"].astype(str).str.strip()
    df_superior = df_percentual[df_percentual["Nivel_Instrucao"].str.contains("Superior completo", case=False, na=False)]
    df_superior = df_superior.sort_values(by="Ano")

    st.sidebar.header("Filtros do Painel")
    lista_estados = df_superior["Estado"].unique().tolist()
    estados_selecionados = st.sidebar.multiselect(
        "Selecione os Estados/Regiões:",
        options=lista_estados,
        default=lista_estados
    )

    lista_anos = sorted(df_superior["Ano"].unique().tolist())
    ano_min, ano_max = st.sidebar.select_slider(
        "Intervalo de Anos:",
        options=lista_anos,
        value=(lista_anos[0], lista_anos[-1])
    )

    df_filtrado = df_superior[
        (df_superior["Estado"].isin(estados_selecionados)) &
        (df_superior["Ano"].astype(int).between(int(ano_min), int(ano_max)))
    ]

    fig_porcentagem = px.line(
        df_filtrado,    
        x="Ano",
        y="Porcentagem",
        color="Estado",
        title="Porcentagem de pessoas com Superior Completo ao longo dos anos",
        labels={"Porcentagem": "Taxa (%)", "Ano": "Ano de Referência"},
        markers=True,  # Coloca pontos nos nós de cada ano
        height=500,
    )

    fig_porcentagem.update_layout(yaxis={"ticksuffix": "%"})
    st.plotly_chart(fig_porcentagem, width='stretch')
    st.markdown("---")
    st.subheader("📰 Insights de Mercado: Fuga de Cérebros e Escassez de TI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Alerta de Escassez: Profissionais de Exatas e TI**")
        st.write(
            "O mercado de tecnologia no Sudeste enfrenta um déficit crescente de profissionais qualificados. "
            "A taxa de formados em cursos de Exatas não acompanha a demanda acelerada de inovação das empresas e hubs tecnológicos da região."
        )
        st.image(
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=1200&auto=format&fit=crop",
            caption="Análise de Dados e Inovação Tecnológica",
            use_container_width=True
        )
    
    with col2:
        st.warning("**O Fenômeno da 'Fuga de Cérebros'**")
        st.write(
            "Talentos de alta qualificação acadêmica formados em universidades públicas e privadas do Sudeste "
            "estão migrando para oportunidades internacionais ou centros remotos globais, exigindo políticas públicas atrativas locais."
        )
        st.image(
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=1200&auto=format&fit=crop",
            caption="Profissionais qualificados e o cenário de mercado",
            use_container_width=True
        )
else:
    st.warning("Não foi possível renderizar a tabela devido à falta de dados.")

