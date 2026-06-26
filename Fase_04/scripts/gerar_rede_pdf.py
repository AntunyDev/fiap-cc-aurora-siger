"""Gera o arquivo rede_colonia.pdf sem bibliotecas externas."""

from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
SAIDA = BASE / "rede_colonia.pdf"


def escapar(texto):
    return texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def criar_pdf(caminho, paginas):
    objetos = []
    kids = []

    objetos.append("<< /Type /Catalog /Pages 2 0 R >>")
    objetos.append("<< /Type /Pages /Kids [] /Count 0 >>")
    objetos.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objetos.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    for linhas in paginas:
        conteudo = ["BT", "/F2 17 Tf", "46 800 Td"]
        primeira = True
        for linha in linhas:
            if primeira:
                conteudo.append(f"({escapar(linha)}) Tj")
                conteudo.append("/F1 9 Tf")
                conteudo.append("0 -24 Td")
                primeira = False
                continue
            if linha.startswith("# "):
                conteudo.append("/F2 12 Tf")
                conteudo.append(f"({escapar(linha[2:])}) Tj")
                conteudo.append("/F1 9 Tf")
            else:
                conteudo.append(f"({escapar(linha)}) Tj")
            conteudo.append("0 -13 Td")
        conteudo.append("ET")

        stream = "\n".join(conteudo)
        pagina_id = len(objetos) + 1
        conteudo_id = len(objetos) + 2
        kids.append(f"{pagina_id} 0 R")
        objetos.append(
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            "/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            f"/Contents {conteudo_id} 0 R >>"
        )
        objetos.append(f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream")

    objetos[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>"

    saida = "%PDF-1.4\n"
    offsets = [0]
    for indice, objeto in enumerate(objetos, start=1):
        offsets.append(len(saida.encode("latin-1")))
        saida += f"{indice} 0 obj\n{objeto}\nendobj\n"

    xref = len(saida.encode("latin-1"))
    saida += f"xref\n0 {len(objetos) + 1}\n"
    saida += "0000000000 65535 f \n"
    for offset in offsets[1:]:
        saida += f"{offset:010d} 00000 n \n"
    saida += f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\n"
    saida += f"startxref\n{xref}\n%%EOF\n"

    caminho.write_bytes(saida.encode("latin-1"))


PAGINAS = [
    [
        "Rede da Colonia Aurora Siger - SIGIC",
        "# Visao geral",
        "Sistema Inteligente de Gerenciamento da Infraestrutura da Colonia.",
        "Representacao da rede em grafo nao direcionado e ponderado.",
        "Vertices: modulos da colonia. Arestas: conexoes energeticas/operacionais.",
        "Pesos: distancia em km e perda energetica percentual.",
        "",
        "# Modulos",
        "HAB - Habitacao | consumo 42 u/h | prioridade 10 | status ativo",
        "CTL - Centro de Controle | consumo 36 u/h | prioridade 10 | status ativo",
        "ENE - Armazenamento de Energia | consumo 14 u/h | prioridade 9 | status ativo",
        "AGR - Agricultura | consumo 48 u/h | prioridade 7 | status ativo",
        "LAB - Laboratorio Cientifico | consumo 32 u/h | prioridade 5 | status manutencao",
        "COM - Comunicacao | consumo 28 u/h | prioridade 8 | status ativo",
        "MED - Suporte Medico | consumo 30 u/h | prioridade 9 | status alerta",
        "OXI - Producao de Oxigenio | consumo 52 u/h | prioridade 10 | status ativo",
        "",
        "# Diagrama logico",
        "                 CTL -------- COM -------- LAB",
        "                  |           |",
        "                  |           |",
        "HAB ----------- ENE -------- OXI -------- AGR",
        " |                         /   |",
        " |                        /    |",
        "MED ---------------------      ",
        "",
        "ENE atua como hub energetico. CTL coordena a operacao. OXI, HAB e MED",
        "ficam proximos por serem sistemas criticos de sobrevivencia.",
    ],
    [
        "Rede da Colonia Aurora Siger - Tabela de Conexoes",
        "# Arestas ponderadas",
        "Origem  Destino  Distancia  Perda energetica  Classificacao",
        "ENE     CTL      2.0 km     3.0%              Critica",
        "ENE     HAB      2.5 km     4.0%              Critica",
        "ENE     OXI      1.8 km     2.5%              Critica",
        "CTL     COM      1.2 km     1.5%              Normal",
        "CTL     LAB      2.4 km     3.8%              Normal",
        "HAB     MED      0.9 km     1.0%              Critica",
        "HAB     AGR      3.1 km     5.2%              Normal",
        "AGR     OXI      2.2 km     3.5%              Normal",
        "LAB     COM      1.7 km     2.2%              Normal",
        "MED     OXI      1.6 km     2.0%              Normal",
        "COM     OXI      2.9 km     4.8%              Normal",
        "",
        "# Justificativa da topologia",
        "- ENE, CTL e OXI ficam mais centrais por serem sistemas criticos.",
        "- HAB se conecta diretamente a MED para reduzir tempo de resposta medica.",
        "- AGR se conecta a HAB e OXI por depender de suporte humano e ciclo de ar.",
        "- COM possui redundancia com CTL, LAB e OXI para manter comunicacao em falhas.",
        "",
        "# Indicadores da rede",
        "Vertices: 8 modulos.",
        "Arestas: 11 conexoes.",
        "Consumo total: 282 u/h.",
        "Capacidade total de armazenamento: 485 unidades.",
        "Perda media das conexoes: aproximadamente 3.05%.",
    ],
]


if __name__ == "__main__":
    criar_pdf(SAIDA, PAGINAS)
    print(f"PDF gerado em: {SAIDA}")

