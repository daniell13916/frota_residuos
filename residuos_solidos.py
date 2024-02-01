import session_info
import streamlit as st
import math


def calcular_numero_rotas(J, L, Vc, Dg, Dd, Vt, Q, C):
    try:
        Ns = math.ceil((1 / J) * ((L / Vc) + 2 * (Dg / Vt) + 2 * ((Dd / Vt) * (Q / C))))
        # Arredonda para cima e aplica o ajuste de 15%
        Ns2= math.ceil(Ns + (Ns * 0.15))
        return Ns2
    except ZeroDivisionError:
        st.error("Erro: Certifique-se de que a duração útil da jornada de trabalho (J) não seja zero.")
        return None

# Função para calcular a quantidade total de lixo a ser coletada (Q) com base em informações de habitantes, produção per capita e % de resíduo coletado
def calcular_quantidade_total_lixo(habitantes, producao_per_capita, percentual_residuo_coletado):
    return (habitantes * producao_per_capita * percentual_residuo_coletado) / 100


# Função para calcular a capacidade dos veículos de coleta (C) com base em informações de peso específico, volume da caçamba e percentual utilizado na caçamba
def calcular_capacidade_veiculos(peso_especifico, volume_cacamba, percentual_utilizado):
    return (peso_especifico * volume_cacamba * percentual_utilizado) / 100


# Interface Streamlit
st.title("Calculadora de Número de Rotas de Veículos")

# Entrada de dados do usuário para múltiplos setores
num_setores = st.number_input("Número de setores:", min_value=1, value=1, step=1, key="num_setores")

# Inicializa uma lista para armazenar os resultados de cada setor
resultados_setores = []
quantidades_lixo_setores = []

# Loop para coletar dados de cada setor
for i in range(num_setores):
    st.header(f"Setor {i + 1}")

    J = st.number_input("Duração útil da jornada de trabalho (J) em horas", min_value=0.1, value=8.0, step=0.1,
                        key=f"J_{i}")
    L = st.number_input("Extensão total das vias (L) em km", min_value=0.1, value=10.0, step=0.1, key=f"L_{i}")
    Vc = st.number_input("Velocidade média de coleta (Vc) em km/h", min_value=1.0, value=20.0, step=1.0, key=f"Vc_{i}")
    Dg = st.number_input("Distância entre a garagem e o setor de coleta (Dg) em km", min_value=0.1, value=5.0, step=0.1,
                         key=f"Dg_{i}")
    Dd = st.number_input("Distância entre o setor de coleta e o ponto de descarga (Dd) em km", min_value=0.1, value=2.0,
                         step=0.1, key=f"Dd_{i}")
    Vt = st.number_input("Velocidade média do veículo nos percursos de posicionamento e de transferência (Vt) em km/h",
                         min_value=1.0, value=30.0, step=1.0, key=f"Vt_{i}")

    # Verifica se o usuário já tem a informação da quantidade total de lixo a ser coletada (Q)
    tem_quantidade_total = st.checkbox(f"Você tem a quantidade total de lixo a ser coletada (Q) para o Setor {i + 1}?",
                                       key=f"checkbox_Q_{i}")

    if tem_quantidade_total:
        Q = st.number_input(f"Quantidade total de lixo a ser coletada (Q) para o Setor {i + 1} em toneladas",
                            min_value=0.1, value=50.0, step=0.1, key=f"Q_{i}")
    else:
        # Se não tiver a informação, solicita o número de habitantes, produção per capita e % de resíduo coletado
        habitantes = st.number_input(f"Número de habitantes para o Setor {i + 1}", min_value=1, value=10000, step=1,
                                     key=f"habitantes_{i}")
        producao_per_capita = st.number_input(f"Produção per capita para o Setor {i + 1} em toneladas", min_value=0.01,
                                              value=0.5, step=0.01, key=f"producao_per_capita_{i}")
        percentual_residuo_coletado = st.slider(f"Percentual de resíduo coletado para o Setor {i + 1} (%)", min_value=1,
                                                max_value=100, value=70, step=1, key=f"percentual_residuo_coletado_{i}")

        # Calcula a quantidade total de lixo a ser coletada (Q) com base nas informações fornecidas
        Q = calcular_quantidade_total_lixo(habitantes, producao_per_capita, percentual_residuo_coletado)
        st.info(f"Quantidade total de lixo a ser coletada (Q) para o Setor {i + 1} calculada automaticamente.")

    # Pergunta sobre a presença de lixo comercial
    tem_lixo_comercial = st.checkbox(f"Apresenta lixo comercial para o Setor {i + 1}?",
                                     key=f"checkbox_lixo_comercial_{i}")

    # Se tem lixo comercial, pergunta pela quantidade em toneladas por dia
    if tem_lixo_comercial:
        quantidade_lixo_comercial = st.number_input(
            f"Quantidade de lixo comercial para o Setor {i + 1} em toneladas por dia", min_value=0.0, value=1.0,
            step=0.1, key=f"quantidade_lixo_comercial_{i}")
        Q += quantidade_lixo_comercial

    # Armazena a quantidade total de lixo a ser coletada (Q) para o Setor
    quantidades_lixo_setores.append(Q)

    # Pergunta sobre a frequência da coleta
    frequencia_coleta = st.selectbox(f"Frequência da coleta para o Setor {i + 1}", ["Diária", "Alternada", "Outro"])

    # Pergunta sobre o período de coleta
    periodo_coleta = st.selectbox(f"Período de coleta para o Setor {i + 1}",
                                  ["Manhã", "Tarde", "Noite", "Dois períodos", "Outro"])

    # Ajusta a quantidade total de lixo a ser coletada (Q) com base na frequência e período de coleta
    if frequencia_coleta == "Diária":
        multiplicador_frequencia = 1
    elif frequencia_coleta == "Alternada":
        multiplicador_frequencia = 2
    else:
        multiplicador_frequencia = st.number_input(f"Número de dias entre coletas para o Setor {i + 1}", min_value=1,
                                                   value=7, step=1, key=f"multiplicador_frequencia_{i}")

    if periodo_coleta in ["Manhã", "Tarde", "Noite"]:
        divisor_periodo = 1
    elif periodo_coleta == "Dois períodos":
        divisor_periodo = 2
    else:
        divisor_periodo = 3

    Q_ajustada = Q * multiplicador_frequencia / divisor_periodo

    # Pergunta se o usuário tem a informação da capacidade dos veículos de coleta (C)
    tem_capacidade_veiculos = st.checkbox(
        f"Você tem a informação da capacidade dos veículos de coleta (C) para o Setor {i + 1}?", key=f"checkbox_C_{i}")

    if tem_capacidade_veiculos:
        C = st.number_input(f"Capacidade dos veículos de coleta (C) para o Setor {i + 1} em toneladas", min_value=0.1,
                            value=10.0, step=0.1, key=f"C_{i}")
    else:
        # Se não tiver a informação, solicita o peso específico, volume da caçamba e percentual utilizado na caçamba
        peso_especifico = st.number_input(f"Peso específico do lixo compactado para o Setor {i + 1} (kg/m³)",
                                          min_value=1, value=800, step=1, key=f"peso_especifico_{i}")
        volume_cacamba = st.number_input(f"Volume da Caçamba do Caminhão para o Setor {i + 1} (m³)", min_value=0.1,
                                         value=10.0, step=0.1, key=f"volume_cacamba_{i}")
        percentual_utilizado_cacamba = st.slider(f"Percentual utilizado na caçamba para o Setor {i + 1} (%)",
                                                 min_value=1, max_value=100, value=70, step=1,
                                                 key=f"percentual_utilizado_cacamba_{i}")

        # Calcula a capacidade dos veículos de coleta (C) com base nas informações fornecidas
        C = calcular_capacidade_veiculos(peso_especifico, volume_cacamba, percentual_utilizado_cacamba)
        st.info(f"Capacidade dos veículos de coleta (C) para o Setor {i + 1} calculada automaticamente.")

    # Botão para calcular
    if st.button(f"Calcular Número de Rotas para Setor {i + 1}"):
        # Calcula o número de rotas para o setor atual
        numero_rotas_setor = calcular_numero_rotas(J, L, Vc, Dg, Dd, Vt, Q_ajustada, C)

        # Armazena o resultado para o setor atual
        if numero_rotas_setor is not None:
            resultados_setores.append(numero_rotas_setor)

# Exibe o resultado total se pelo menos um setor foi processado
if resultados_setores:
    resultado_total = sum(resultados_setores)
    st.success(f"O número total de rotas de veículos para todos os setores é: {resultado_total}")

    # Calcula o valor do lixo gerado (soma das quantidades de lixo de cada setor)
    valor_lixo_gerado = sum(quantidades_lixo_setores)
    st.info(f"O valor total de lixo gerado por todos os setores é: {valor_lixo_gerado} Kg.")

    # Calcula o maior Ns ajustado entre os setores
    maior_Ns_ajustado = max(resultados_setores)

    # Determina o período com o maior Ns ajustado
    periodo_maior_Ns = st.selectbox("Selecione o período para determinar o número de caminhões:",
                                    ["Manhã", "Tarde", "Noite"])

#Todas as versões do python e bibliotecas
session_info.show()
