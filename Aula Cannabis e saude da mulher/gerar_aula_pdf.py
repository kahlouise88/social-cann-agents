from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Cores ─────────────────────────────────────────────────────────────────────
VERDE_ESCURO   = colors.HexColor("#1B4332")
VERDE_MEDIO    = colors.HexColor("#2D6A4F")
VERDE_CLARO    = colors.HexColor("#52B788")
VERDE_PASTEL   = colors.HexColor("#D8F3DC")
DOURADO        = colors.HexColor("#B5985A")
BRANCO         = colors.white
CINZA_TEXTO    = colors.HexColor("#2D3748")
CINZA_CLARO    = colors.HexColor("#F7F7F7")
PRETO          = colors.black

# ── Caminho de saída ──────────────────────────────────────────────────────────
OUTPUT = r"C:\Users\User\Desktop\Social Cann\Katharine Louise\Aula Cannabis e saude da mulher\Aula_Cannabis_Saude_da_Mulher_Enfermagem.pdf"


# ── Estilos ───────────────────────────────────────────────────────────────────
def criar_estilos():
    base = getSampleStyleSheet()

    estilos = {
        "titulo_capa": ParagraphStyle(
            "titulo_capa",
            fontSize=38,
            leading=46,
            textColor=BRANCO,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            spaceAfter=10,
        ),
        "subtitulo_capa": ParagraphStyle(
            "subtitulo_capa",
            fontSize=16,
            leading=22,
            textColor=VERDE_CLARO,
            alignment=TA_CENTER,
            fontName="Helvetica",
            spaceAfter=6,
        ),
        "autora_capa": ParagraphStyle(
            "autora_capa",
            fontSize=13,
            leading=18,
            textColor=DOURADO,
            alignment=TA_CENTER,
            fontName="Helvetica-BoldOblique",
        ),
        "titulo_secao": ParagraphStyle(
            "titulo_secao",
            fontSize=22,
            leading=28,
            textColor=BRANCO,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            spaceAfter=4,
        ),
        "titulo_topico": ParagraphStyle(
            "titulo_topico",
            fontSize=16,
            leading=22,
            textColor=VERDE_ESCURO,
            alignment=TA_LEFT,
            fontName="Helvetica-Bold",
            spaceBefore=14,
            spaceAfter=6,
        ),
        "subtitulo": ParagraphStyle(
            "subtitulo",
            fontSize=13,
            leading=18,
            textColor=VERDE_MEDIO,
            alignment=TA_LEFT,
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=4,
        ),
        "corpo": ParagraphStyle(
            "corpo",
            fontSize=11,
            leading=17,
            textColor=CINZA_TEXTO,
            alignment=TA_JUSTIFY,
            fontName="Helvetica",
            spaceAfter=8,
        ),
        "destaque": ParagraphStyle(
            "destaque",
            fontSize=11,
            leading=17,
            textColor=VERDE_ESCURO,
            alignment=TA_JUSTIFY,
            fontName="Helvetica-Bold",
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontSize=11,
            leading=17,
            textColor=CINZA_TEXTO,
            alignment=TA_LEFT,
            fontName="Helvetica",
            leftIndent=16,
            spaceAfter=4,
            bulletIndent=4,
        ),
        "citacao": ParagraphStyle(
            "citacao",
            fontSize=12,
            leading=19,
            textColor=VERDE_ESCURO,
            alignment=TA_CENTER,
            fontName="Helvetica-BoldOblique",
            spaceAfter=8,
            spaceBefore=8,
        ),
        "rodape_secao": ParagraphStyle(
            "rodape_secao",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#888888"),
            alignment=TA_CENTER,
            fontName="Helvetica-Oblique",
        ),
        "enfermagem_destaque": ParagraphStyle(
            "enfermagem_destaque",
            fontSize=12,
            leading=18,
            textColor=BRANCO,
            alignment=TA_JUSTIFY,
            fontName="Helvetica-Bold",
            spaceAfter=6,
        ),
    }
    return estilos


# ── Helpers visuais ───────────────────────────────────────────────────────────
def caixa_colorida(texto, estilo, cor_fundo, padding_v=8, padding_h=14):
    tabela = Table(
        [[Paragraph(texto, estilo)]],
        colWidths=[15.5 * cm],
    )
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), cor_fundo),
        ("TOPPADDING",    (0, 0), (-1, -1), padding_v),
        ("BOTTOMPADDING", (0, 0), (-1, -1), padding_v),
        ("LEFTPADDING",   (0, 0), (-1, -1), padding_h),
        ("RIGHTPADDING",  (0, 0), (-1, -1), padding_h),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return tabela


def linha_verde():
    return HRFlowable(width="100%", thickness=2, color=VERDE_CLARO, spaceAfter=10, spaceBefore=4)


def linha_dourada():
    return HRFlowable(width="100%", thickness=1, color=DOURADO, spaceAfter=8, spaceBefore=4)


def cabecalho_secao(titulo, estilos):
    bloco = Table(
        [[Paragraph(titulo, estilos["titulo_secao"])]],
        colWidths=[17.5 * cm],
    )
    bloco.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE_ESCURO),
        ("TOPPADDING",    (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
    ]))
    return bloco


def caixa_dois_col(col1_titulo, col1_corpo, col2_titulo, col2_corpo, estilos):
    """Cria uma tabela de duas colunas."""
    c1 = [Paragraph(col1_titulo, estilos["subtitulo"]),
          Paragraph(col1_corpo,  estilos["corpo"])]
    c2 = [Paragraph(col2_titulo, estilos["subtitulo"]),
          Paragraph(col2_corpo,  estilos["corpo"])]
    t = Table([[c1, c2]], colWidths=[8.5 * cm, 8.5 * cm])
    t.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND",    (0, 0), (0, 0), VERDE_PASTEL),
        ("BACKGROUND",    (1, 0), (1, 0), colors.HexColor("#EAF4E8")),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t


# ── Página de capa ────────────────────────────────────────────────────────────
def pagina_capa(estilos):
    story = []

    fundo = Table(
        [[Paragraph("CANNABIS &amp;<br/>SAÚDE DA MULHER", estilos["titulo_capa"])]],
        colWidths=[17.5 * cm],
    )
    fundo.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), VERDE_ESCURO),
        ("TOPPADDING",    (0, 0), (-1, -1), 60),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 60),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
    ]))
    story.append(fundo)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(
        "Aula para Acadêmicos de Enfermagem",
        estilos["subtitulo_capa"]
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(linha_dourada())
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Katharine Louise", estilos["autora_capa"]))
    story.append(Paragraph("Cannabis &amp; Health Coach", estilos["autora_capa"]))
    story.append(Spacer(1, 1 * cm))

    sumario_data = [
        ["SUMÁRIO"],
        ["1. Breve História do Cannabis"],
        ["2. O Sistema Endocanabinoide (SEC)"],
        ["3. Fitocanabinoides"],
        ["4. Saúde da Mulher e Cannabis"],
        ["5. Cannabis na Gravidez, Parto e Amamentação"],
        ["6. Saúde Integrativa"],
        ["7. A Importância da Medicina Canabinoide para a Enfermagem"],
    ]
    t = Table(sumario_data, colWidths=[17.5 * cm])
    t_style = [
        ("BACKGROUND",    (0, 0), (-1, 0), VERDE_MEDIO),
        ("TEXTCOLOR",     (0, 0), (-1, 0), BRANCO),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 13),
        ("BACKGROUND",    (0, 1), (-1, -1), VERDE_PASTEL),
        ("TEXTCOLOR",     (0, 1), (-1, -1), VERDE_ESCURO),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 11),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 16),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [VERDE_PASTEL, colors.HexColor("#EAF4E8")]),
    ]
    t.setStyle(TableStyle(t_style))
    story.append(t)
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Material educativo — Uso exclusivo acadêmico",
        estilos["rodape_secao"]
    ))
    story.append(PageBreak())
    return story


# ── Seção 1 — Bem-vindo ───────────────────────────────────────────────────────
def secao_boas_vindas(estilos):
    story = []
    story.append(cabecalho_secao("BEM-VINDO(A)", estilos))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Sobre Este Material", estilos["titulo_topico"]))
    story.append(Paragraph(
        "Este material foi desenvolvido para apoiar a formação de acadêmicos de enfermagem "
        "no tema Cannabis e Saúde da Mulher. A enfermagem está na linha de frente do cuidado, "
        "e compreender o sistema endocanabinoide e as evidências científicas sobre o uso de "
        "canabinoides é fundamental para uma prática clínica atualizada e humanizada.",
        estilos["corpo"]
    ))
    story.append(Paragraph(
        "Cuidar e nutrir as mulheres é um prazer que tenho, e este treinamento foi pensado e "
        "desenhado para abrir portas para algo mais amplo. Nosso corpo é o lugar onde vivemos, "
        "e tudo o que fazemos tem uma resposta — dos nossos pensamentos ao tipo de alimentação "
        "e estilo de vida que levamos.",
        estilos["corpo"]
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(caixa_colorida(
        "\"A planta que se desenvolveu junto com as mulheres ao longo de milênios.\"",
        estilos["citacao"], VERDE_PASTEL
    ))
    story.append(Spacer(1, 0.5 * cm))
    story.append(linha_verde())
    story.append(Paragraph("O Que Vamos Abordar", estilos["titulo_topico"]))

    topicos = [
        ("1.", "Breve história do cannabis na medicina"),
        ("2.", "O Sistema Endocanabinoide e sua regulação"),
        ("3.", "Fitocanabinoides: CBD, THC, CBG, CBC e outros"),
        ("4.", "A saúde da mulher ao longo do ciclo de vida"),
        ("5.", "Cannabis na gestação, parto e lactação"),
        ("6.", "Saúde Integrativa e as 12 dimensões do bem-estar"),
        ("7.", "O papel da Enfermagem na medicina canabinoide"),
    ]
    for num, texto in topicos:
        story.append(Paragraph(f"<b>{num}</b> {texto}", estilos["bullet"]))

    story.append(PageBreak())
    return story


# ── Seção 2 — História ────────────────────────────────────────────────────────
def secao_historia(estilos):
    story = []
    story.append(cabecalho_secao("1. BREVE HISTÓRIA DO CANNABIS", estilos))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Raízes Milenares", estilos["titulo_topico"]))
    story.append(Paragraph(
        "Por muito tempo, a saúde da mulher foi marginalizada tanto na medicina quanto na pesquisa "
        "sobre cannabis. A maioria dos estudos científicos foi centrada na fisiologia masculina, "
        "deixando lacunas importantes sobre como os canabinoides interagem com a biologia feminina, "
        "os ciclos hormonais e o equilíbrio emocional. Isso está mudando.",
        estilos["corpo"]
    ))
    story.append(Paragraph(
        "O cannabis é conhecido e utilizado para a saúde feminina há milênios, com registros que "
        "remontam a mais de 6.000 a.C.:",
        estilos["corpo"]
    ))

    marcos = [
        ("Egito Antigo", "Primeiro papiro de obstetrícia e ginecologia do mundo faz referência ao uso do cannabis para condições femininas."),
        ("China, Pérsia, África e Índia", "Registros abundantes de uso medicinal, incluindo tratamento de cólicas, dismenorreia e sintomas do parto."),
        ("Reino Unido (Era Moderna)", "Registros botânicos documentam o uso do cannabis no tratamento de cólicas menstruais, dismenorreia, sintomas da menopausa e enxaquecas."),
        ("Era Contemporânea", "O conhecimento sobre o Sistema Endocanabinoide (SEC) explica, com base científica, o que antes era intuitivo e desconhecido."),
    ]
    for titulo, descricao in marcos:
        story.append(KeepTogether([
            Paragraph(titulo, estilos["subtitulo"]),
            Paragraph(descricao, estilos["corpo"]),
        ]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(linha_verde())
    story.append(Paragraph("Aspectos Botânicos", estilos["titulo_topico"]))
    story.append(Paragraph(
        "A Cannabis sativa L. é o nome científico da espécie. Dentro dela, existem <b>quimiovares</b> "
        "— variedades químicas — cultivadas para diferentes finalidades:",
        estilos["corpo"]
    ))

    story.append(caixa_dois_col(
        "Cannabis Hemp (Cânhamo)",
        "• Menos de 0,3% de THC\n• Sem efeitos psicoativos\n• Rica em CBD\n• Antioxidante, neuroprotetora, anticonvulsivante\n• Anti-inflamatória, ansiolítica\n• Planta Sativa cultivada externamente",
        "Maconha (Alto THC)",
        "• 5% a 30% de THC\n• Cultivada pelas flores ricas em resina\n• Analgésica, anti-náusea, anticancerígena\n• Apenas plantas fêmeas cultivadas separadamente\n• Sativa e Indica\n• Efeito psicotrópico considerável",
        estilos
    ))
    story.append(PageBreak())
    return story


# ── Seção 3 — Fitocanabinoides ────────────────────────────────────────────────
def secao_fitocanabinoides(estilos):
    story = []
    story.append(cabecalho_secao("2. FITOCANABINOIDES", estilos))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph(
        "Fitocanabinoides são compostos naturais encontrados na planta Cannabis. Interagem com o SEC "
        "ao se ligar aos receptores canabinoides (CB1 e CB2) ou influenciando outras vias receptoras, "
        "modulando diversos processos fisiológicos. São metabólitos secundários presentes nas folhas "
        "e flores, principalmente na resina.",
        estilos["corpo"]
    ))

    story.append(Paragraph("Efeito Entourage", estilos["titulo_topico"]))
    story.append(caixa_colorida(
        "O \"efeito entourage\" refere-se à interação sinérgica entre os diversos compostos do "
        "cannabis — fitocanabinoides, terpenos e flavonoides. Esta sinergia pode ampliar os efeitos "
        "terapêuticos dos compostos individuais, sugerindo que extratos de planta inteira podem "
        "oferecer benefícios mais significativos do que canabinoides isolados.",
        estilos["corpo"], VERDE_PASTEL
    ))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Principais Fitocanabinoides", estilos["titulo_topico"]))

    canabinoides = [
        ("CBD — Canabidiol", "Não psicoativo. Anti-inflamatório, ansiolítico, neuroprotetor. Eleva indiretamente os níveis de anandamida. Amplamente utilizado para ansiedade, dor crônica, epilepsia e condições autoimunes."),
        ("THC — Tetrahidrocanabinol", "Principal composto psicoativo. Liga-se diretamente ao CB1. Analgésico, antináusea, estimulante do apetite, neuroprotetor. Usado em dor crônica, quimioterapia e espasticidade."),
        ("CBG — Canabigerol", "Chamado de \"canabinoide mãe\" — precursor de outros canabinoides. Anti-inflamatório, antibacteriano, neuroprotetor. Pode apoiar a saúde vesical."),
        ("CBC — Canabicrômeno", "Anti-inflamatório, analgésico. Interage com TRPV1 e TRPA1. Pode promover neurogênese."),
        ("CBN — Canabidinol", "Formado pela degradação do THC. Maior afinidade pelo CB2. Sedativo, auxilia em distúrbios do sono, propriedades antibacterianas."),
        ("THCV — Tetrahidrocanabivarina", "Supressor do apetite em doses baixas. Pode auxiliar no controle da glicemia e no manejo do peso."),
        ("CBDV — Canabivaridiol", "Estrutura similar ao CBD. Propriedades anticonvulsivantes. Potencial no tratamento da epilepsia."),
        ("CBG — Canabigerovarina", "Interage com canais TRP. Anti-inflamatório, analgésico. Pode apoiar a saúde da pele."),
    ]

    for nome, descricao in canabinoides:
        story.append(KeepTogether([
            Paragraph(nome, estilos["subtitulo"]),
            Paragraph(descricao, estilos["corpo"]),
        ]))

    story.append(PageBreak())
    return story


# ── Seção 4 — Sistema Endocanabinoide ─────────────────────────────────────────
def secao_sec(estilos):
    story = []
    story.append(cabecalho_secao("3. SISTEMA ENDOCANABINOIDE (SEC)", estilos))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("O Que É o SEC?", estilos["titulo_topico"]))
    story.append(Paragraph(
        "Imagine um sistema em seu corpo projetado para manter tudo em equilíbrio. Esse é o seu "
        "Sistema Endocanabinoide. Ele é composto por três partes principais:",
        estilos["corpo"]
    ))

    partes = [
        ("Endocanabinoides", "Moléculas naturais produzidas pelo próprio organismo, como a anandamida (AEA) e o 2-AG."),
        ("Receptores Canabinoides", "Principalmente CB1 e CB2, encontrados em todo o corpo."),
        ("Enzimas", "Constroem e degradam endocanabinoides conforme a necessidade."),
    ]
    for titulo, descricao in partes:
        story.append(Paragraph(f"<b>• {titulo}:</b> {descricao}", estilos["corpo"]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(caixa_colorida(
        "O SEC funciona como um termostato interno. Quando algo está muito alto ou muito baixo "
        "— dor, estresse, inflamação — o SEC trabalha para restaurar o equilíbrio. "
        "É um sistema regulatório mestre.",
        estilos["corpo"], VERDE_PASTEL
    ))

    story.append(Paragraph("Funções do SEC", estilos["titulo_topico"]))
    funcoes = [
        "Humor e bem-estar emocional",
        "Apetite e metabolismo",
        "Percepção de dor",
        "Ciclo sono-vigília",
        "Vida e morte celular",
        "Regulação de temperatura",
        "Movimento e coordenação motora",
        "Memória e aprendizagem",
        "Função imunológica",
        "Inflamação sistêmica",
        "Homeostase energética",
    ]
    for f in funcoes:
        story.append(Paragraph(f"• {f}", estilos["bullet"]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(linha_verde())

    story.append(Paragraph("Receptores CB1 e CB2", estilos["titulo_topico"]))
    story.append(caixa_dois_col(
        "Receptor CB1",
        "Encontrado principalmente no cérebro e no sistema nervoso central.\n\n"
        "Envolvido em: humor, memória, percepção de dor, apetite e controle motor.\n\n"
        "Ativado principalmente pela anandamida e pelo THC.\n\n"
        "O THC se liga diretamente ao CB1, criando os efeitos euforizantes (\"barato\").\n\n"
        "Regula as respostas ao estresse e equilíbrio emocional.",
        "Receptor CB2",
        "Encontrado principalmente no sistema imunológico, intestino e órgãos periféricos.\n\n"
        "Regula: inflamação, resposta imunológica e reparo tecidual.\n\n"
        "Ativado principalmente pelo 2-AG (endocanabinoide).\n\n"
        "O CBD não se liga diretamente ao CB2, mas modula o sistema para restaurar o equilíbrio.\n\n"
        "Papel fundamental na dor crônica e condições autoimunes.",
        estilos
    ))

    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Endocanabinoides: O Sistema de Equilíbrio Interno", estilos["titulo_topico"]))

    story.append(Paragraph(
        "<b>Anandamida (AEA):</b> Batizada com a palavra sânscrita para \"êxtase\" (ananda). "
        "Papel-chave no humor, memória, fertilidade e apetite. Degradada pela enzima FAAH.",
        estilos["corpo"]
    ))
    story.append(Paragraph(
        "<b>2-Araquidonoilglicerol (2-AG):</b> Mais abundante que a AEA. "
        "Regula dor, inflamação e respostas imunológicas. Degradado pela enzima MAGL.",
        estilos["corpo"]
    ))

    story.append(Paragraph("Como os Endocanabinoides São Produzidos?", estilos["subtitulo"]))
    story.append(Paragraph(
        "São produzidos \"sob demanda\" nas membranas celulares a partir de ácidos graxos ômega-6. "
        "Quando o corpo detecta estresse, dor ou inflamação, enzimas produzem endocanabinoides "
        "exatamente no local necessário. Após cumprir sua função, são rapidamente degradados.",
        estilos["corpo"]
    ))

    story.append(Paragraph("Como o Estilo de Vida Afeta o Tônus do SEC", estilos["titulo_topico"]))

    story.append(caixa_dois_col(
        "Fatores de Apoio",
        "• Gorduras saudáveis (ômega-3)\n• Exercício físico regular\n• Sono profundo e restaurador\n"
        "• Mindfulness, meditação e prazer\n• Chocolate amargo (compostos tipo anandamida)\n"
        "• CBD (eleva indiretamente os níveis de AEA)\n• Massagem e toque terapêutico\n"
        "• Adaptógenos: ashwagandha e manjericão sagrado",
        "Fatores Disruptivos",
        "• Estresse crônico\n• Alimentos ultraprocessados (alto ômega-6)\n"
        "• Privação de sono\n• Trauma e supressão emocional\n"
        "• Sedentarismo\n• Isolamento social",
        estilos
    ))
    story.append(PageBreak())
    return story


# ── Seção 5 — Saúde da Mulher ─────────────────────────────────────────────────
def secao_saude_mulher(estilos):
    story = []
    story.append(cabecalho_secao("4. SAÚDE DA MULHER E CANNABIS", estilos))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph(
        "Os corpos das mulheres foram por muito tempo mal compreendidos, silenciados e negligenciados "
        "tanto nos sistemas de saúde convencionais quanto alternativos. No contexto do uso do cannabis, "
        "isso é especialmente evidente. Este módulo busca preencher essa lacuna, unindo a ciência do SEC "
        "à natureza cíclica da saúde feminina.",
        estilos["corpo"]
    ))

    story.append(Paragraph("O Ciclo Hormonal e o SEC", estilos["titulo_topico"]))
    story.append(Paragraph(
        "Hormônios e o SEC estão em constante diálogo:",
        estilos["corpo"]
    ))
    pontos = [
        "O <b>estrogênio</b> aumenta a sensibilidade do receptor CB1, potencializando os efeitos do THC durante a ovulação.",
        "A <b>progesterona</b> pode ter efeitos moduladores, frequentemente reduzindo o impacto psicoativo.",
        "Os <b>níveis de endocanabinoides</b> flutuam ao longo do ciclo menstrual.",
    ]
    for p in pontos:
        story.append(Paragraph(f"• {p}", estilos["bullet"]))

    story.append(Paragraph("Aplicações Clínicas por Fase do Ciclo", estilos["titulo_topico"]))

    fases = [
        ("TPM / TDPM", "CBD e THC em doses baixas podem reduzir ansiedade, irritabilidade e cólicas. Canabinoides anti-inflamatórios como THCA ou CBG auxiliam na dor e tensão mamária na fase lútea."),
        ("Fase Ovulatória", "Aumento da sensibilidade do SEC pode alterar os efeitos percebidos. Dosagem consciente é essencial neste período."),
        ("Fase Lútea", "Canabinoides anti-inflamatórios como THCA e CBG podem reduzir dor e sensibilidade mamária."),
        ("Menstruação", "CBD e baixas doses de THC para dor e espasmos uterinos. O SEC tem receptores no tecido uterino."),
    ]
    for fase, desc in fases:
        story.append(KeepTogether([
            Paragraph(fase, estilos["subtitulo"]),
            Paragraph(desc, estilos["corpo"]),
        ]))

    story.append(linha_verde())
    story.append(Paragraph("Saúde Mental e Emocional", estilos["titulo_topico"]))
    story.append(Paragraph(
        "Transtornos de humor estão intimamente ligados aos ciclos hormonais. O SEC modula humor, "
        "resposta ao estresse e neuroplasticidade.",
        estilos["corpo"]
    ))

    aplicacoes = [
        ("Ansiedade", "CBD para modulação de receptores GABA. Potencial para uso diário com monitoramento em diário."),
        ("Depressão", "THC em doses baixas pode ajudar; evitar uso excessivo para não causar desregulação."),
        ("TEPT e Trauma", "Cannabis pode apoiar a reconsolidação de memória e liberação emocional quando integrada à terapia."),
    ]
    for nome, desc in aplicacoes:
        story.append(Paragraph(f"<b>{nome}:</b> {desc}", estilos["corpo"]))

    story.append(linha_verde())
    story.append(Paragraph("Navegando pelas Fases da Vida", estilos["titulo_topico"]))

    fases_vida = [
        ("Puberdade", "O SEC influencia o desenvolvimento cerebral. O uso precoce de cannabis requer educação e limites cuidadosos."),
        ("Fertilidade", "Endocanabinoides estão envolvidos na ovulação, implantação e função espermática. Recomenda-se evitar ou minimizar THC na preconcepção, salvo indicação médica."),
        ("Gestação e Amamentação", "O uso ainda é controverso. Essencial educar sobre dados limitados de segurança e riscos potenciais, especialmente com THC."),
        ("Perimenopausa e Menopausa", "O tônus do SEC diminui com a idade. Cannabis pode aliviar fogachos, insônia, ansiedade e ressecamento vaginal."),
    ]
    for fase, desc in fases_vida:
        story.append(KeepTogether([
            Paragraph(fase, estilos["subtitulo"]),
            Paragraph(desc, estilos["corpo"]),
        ]))

    story.append(linha_verde())
    story.append(Paragraph("Condições Crônicas Comuns em Mulheres", estilos["titulo_topico"]))
    story.append(Paragraph(
        "Muitos transtornos crônicos de dor e inflamação afetam desproporcionalmente as mulheres "
        "e podem estar relacionados à disfunção do SEC:",
        estilos["corpo"]
    ))

    condicoes = [
        ("Fibromialgia", "CBD e CBG podem ajudar a regular a percepção de dor e inflamação."),
        ("Endometriose", "Targeting de CB1/CB2 e GPR55; benefícios com extratos de espectro completo."),
        ("SII (Síndrome do Intestino Irritável)", "Envolvimento do SEC na motilidade intestinal e inflamação; microdosagem de THC ou CBD."),
        ("Enxaqueca", "THC e CBD demonstraram potencial na prevenção e redução da intensidade das crises."),
        ("PCOS (Síndrome dos Ovários Policísticos)", "O SEC regula o eixo reprodutivo e inflamatório. CBD pode auxiliar na modulação hormonal e redução de estresse."),
    ]
    for cond, desc in condicoes:
        story.append(Paragraph(f"<b>• {cond}:</b> {desc}", estilos["bullet"]))

    story.append(Spacer(1, 0.3 * cm))
    story.append(caixa_colorida(
        "Nota Terapêutica: Muitas dessas condições são subdiagnosticadas e frequentemente "
        "desconsideradas pelos sistemas de saúde. A medicina canabinoide pode oferecer "
        "validação científica e alívio real.",
        estilos["corpo"], VERDE_PASTEL
    ))
    story.append(PageBreak())
    return story


# ── Seção 6 — Gravidez ───────────────────────────────────────────────────────
def secao_gravidez(estilos):
    story = []
    story.append(cabecalho_secao("5. CANNABIS NA GRAVIDEZ, PARTO E AMAMENTAÇÃO", estilos))
    story.append(Spacer(1, 0.4 * cm))

    story.append(caixa_colorida(
        "ATENÇÃO: Este é um tema de grande relevância para a enfermagem. "
        "O acolhimento não-julgamental e a educação baseada em evidências são fundamentais.",
        estilos["destaque"], colors.HexColor("#FFF3CD")
    ))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("O SEC no Período Reprodutivo", estilos["titulo_topico"]))
    story.append(Paragraph(
        "O sistema endocanabinoide tem papel central na reprodução humana. Endocanabinoides "
        "estão presentes no líquido folicular, no endométrio e no óvulo fertilizado. "
        "Regulam implantação, desenvolvimento embrionário e modulação imunológica gestacional.",
        estilos["corpo"]
    ))

    story.append(Paragraph("Gestação", estilos["subtitulo"]))
    story.append(Paragraph(
        "O uso de cannabis na gestação é um tema controverso e com dados de segurança limitados. "
        "Estudos associam o uso de THC durante a gestação a:",
        estilos["corpo"]
    ))
    riscos_gest = [
        "Baixo peso ao nascer",
        "Partos prematuros",
        "Impacto no neurodesenvolvimento fetal (o cérebro fetal tem receptores CB1 ativos)",
        "Alterações na atenção, memória e comportamento na infância",
    ]
    for r in riscos_gest:
        story.append(Paragraph(f"• {r}", estilos["bullet"]))

    story.append(Paragraph(
        "O CBD isolado também tem estudos limitados na gestação. A orientação atual é de abstenção "
        "de qualquer forma de cannabis durante a gravidez, salvo indicação médica específica com "
        "avaliação individualizada de risco-benefício.",
        estilos["corpo"]
    ))

    story.append(Paragraph("Amamentação", estilos["subtitulo"]))
    story.append(Paragraph(
        "O THC é lipofílico e passa para o leite materno, podendo ser detectado por semanas. "
        "Evidências sugerem que a exposição ao THC via leite materno pode afetar o neurodesenvolvimento "
        "do lactente. Recomenda-se evitar o uso durante a amamentação.",
        estilos["corpo"]
    ))

    story.append(Paragraph("Papel da Enfermagem neste Contexto", estilos["titulo_topico"]))
    papeis = [
        "Abordagem acolhedora e não-julgamental na anamnese sobre uso de substâncias",
        "Educação baseada em evidências sobre riscos e benefícios",
        "Rastreamento de uso de cannabis no pré-natal",
        "Encaminhamento para acompanhamento multidisciplinar quando necessário",
        "Apoio emocional e escuta ativa — muitas mulheres usam cannabis para náuseas, ansiedade e dor",
    ]
    for p in papeis:
        story.append(Paragraph(f"• {p}", estilos["bullet"]))

    story.append(PageBreak())
    return story


# ── Seção 7 — Saúde Integrativa ──────────────────────────────────────────────
def secao_integrativa(estilos):
    story = []
    story.append(cabecalho_secao("6. SAÚDE INTEGRATIVA", estilos))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("O Que É Saúde Integrativa?", estilos["titulo_topico"]))
    story.append(Paragraph(
        "A Saúde Integrativa combina o conhecimento da saúde convencional com práticas de estilo "
        "de vida baseadas em evidências para criar uma cura que respeite a pessoa como um todo — "
        "corpo, mente e espírito. Não trata apenas doenças: pergunta <i>\"O que está causando "
        "desequilíbrio? O que a cura significa para você?\"</i>",
        estilos["corpo"]
    ))
    story.append(Paragraph(
        "É sobre autoconsciência, bioindividualidade e a compreensão de que nossas escolhas "
        "diárias moldam nossa saúde hormonal, emocional e imunológica.",
        estilos["corpo"]
    ))

    story.append(Paragraph("As 12 Dimensões da Saúde Integrativa", estilos["titulo_topico"]))

    dimensoes = [
        ("1", "Saúde e Bem-estar Físico"),
        ("2", "Nutrição e Relação com a Alimentação"),
        ("3", "Carreira e Propósito de Vida"),
        ("4", "Resiliência Emocional"),
        ("5", "Prática Espiritual"),
        ("6", "Relacionamentos e Suporte Social"),
        ("7", "Alegria e Criatividade"),
        ("8", "Movimento e Descanso"),
        ("9", "Bem-estar Financeiro"),
        ("10", "Ambiente (casa, natureza, espaço de trabalho)"),
        ("11", "Aprendizado e Estimulação Mental"),
        ("12", "Culinária Caseira e Rituais de Nutrição"),
    ]
    dim_data = [[f"{num}. {desc}"] for num, desc in dimensoes]
    t = Table(dim_data, colWidths=[17.5 * cm])
    row_styles = []
    for i in range(len(dim_data)):
        bg = VERDE_PASTEL if i % 2 == 0 else colors.HexColor("#EAF4E8")
        row_styles.append(("BACKGROUND", (0, i), (-1, i), bg))
    t.setStyle(TableStyle([
        ("TEXTCOLOR",     (0, 0), (-1, -1), VERDE_ESCURO),
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 11),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
    ] + row_styles))
    story.append(t)

    story.append(Spacer(1, 0.4 * cm))
    story.append(caixa_colorida(
        "\"Quando uma área está fora de sincronia, as outras sentem. "
        "Quando nutrida, o sistema inteiro floresce.\"",
        estilos["citacao"], VERDE_PASTEL
    ))

    story.append(Paragraph("Por Que Isso Importa para a Saúde da Mulher?", estilos["titulo_topico"]))
    story.append(Paragraph(
        "Os corpos das mulheres são cíclicos e sensíveis ao estresse, inflamação e deficiência "
        "nutricional. A saúde integrativa apoia:",
        estilos["corpo"]
    ))
    apoios = [
        "Equilíbrio hormonal por meio de alimentação, ervas e descanso",
        "Regulação do sistema nervoso via respiração, conexão e limites saudáveis",
        "Liberação emocional por práticas criativas e terapêuticas",
    ]
    for a in apoios:
        story.append(Paragraph(f"• {a}", estilos["bullet"]))

    story.append(Paragraph(
        "Esta abordagem ajuda as mulheres a pararem de \"consertar\" sintomas e a começarem a "
        "entender o que seus corpos estão comunicando.",
        estilos["corpo"]
    ))
    story.append(PageBreak())
    return story


# ── Seção 8 — Enfermagem (NOVA) ───────────────────────────────────────────────
def secao_enfermagem(estilos):
    story = []
    story.append(cabecalho_secao("7. MEDICINA CANABINOIDE E A ENFERMAGEM", estilos))
    story.append(Spacer(1, 0.4 * cm))

    story.append(caixa_colorida(
        "A enfermagem está na vanguarda do cuidado. Compreender a medicina canabinoide "
        "é uma competência emergente e essencial para a prática clínica contemporânea.",
        estilos["destaque"], VERDE_PASTEL
    ))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Por Que a Enfermagem Precisa Conhecer o SEC?", estilos["titulo_topico"]))
    story.append(Paragraph(
        "O Sistema Endocanabinoide é o maior sistema regulatório do organismo humano, envolvido "
        "em virtualmente todos os processos fisiológicos. Profissionais de enfermagem que compreendem "
        "este sistema estão melhor equipados para:",
        estilos["corpo"]
    ))
    razoes = [
        "Avaliar e monitorar pacientes em uso de canabinoides prescritos",
        "Educar pacientes e familiares sobre uso terapêutico e riscos",
        "Identificar interações medicamentosas com canabinoides (especialmente CBD com anticoagulantes, antiepilépticos e imunossupressores)",
        "Oferecer cuidado livre de estigma e baseado em evidências",
        "Participar de equipes multidisciplinares em clínicas de cannabis medicinal",
        "Aplicar o raciocínio clínico sobre a farmacodinâmica dos canabinoides",
    ]
    for r in razoes:
        story.append(Paragraph(f"• {r}", estilos["bullet"]))

    story.append(linha_verde())
    story.append(Paragraph("O Contexto Regulatório no Brasil", estilos["titulo_topico"]))
    story.append(Paragraph(
        "A Agência Nacional de Vigilância Sanitária (ANVISA) regulamentou, por meio da RDC 327/2019 "
        "e da RDC 660/2022, o uso de produtos à base de Cannabis para fins medicinais no Brasil. "
        "Isso representa um marco importante para a enfermagem:",
        estilos["corpo"]
    ))
    regulatorio = [
        "Produtos com CBD e THC podem ser prescritos por médicos para diversas condições",
        "A enfermagem deve estar preparada para acompanhar pacientes em uso dessas terapias",
        "O COFEN (Conselho Federal de Enfermagem) orienta que o enfermeiro pode participar ativamente do cuidado a pacientes em uso de cannabis medicinal",
        "A educação continuada sobre este tema é cada vez mais necessária nos currículos de enfermagem",
    ]
    for r in regulatorio:
        story.append(Paragraph(f"• {r}", estilos["bullet"]))

    story.append(linha_verde())
    story.append(Paragraph("Competências da Enfermagem em Cannabis Medicinal", estilos["titulo_topico"]))

    competencias = [
        (
            "Avaliação Clínica",
            "Anamnese completa incluindo uso de cannabis (recreativo e medicinal). "
            "Avaliação de sintomas-alvo, histórico de uso, dose, via de administração e efeitos adversos. "
            "Monitoramento de desfechos clínicos e qualidade de vida."
        ),
        (
            "Educação em Saúde",
            "Orientar pacientes e familiares sobre vias de administração, titulação de dose e expectativas terapêuticas. "
            "Desmistificar preconceitos sem minimizar riscos reais. "
            "Orientar sobre armazenamento seguro, especialmente em famílias com crianças."
        ),
        (
            "Gestão de Efeitos Adversos",
            "Reconhecer sintomas de intoxicação aguda por THC (taquicardia, ansiedade, desorientação). "
            "Monitorar efeitos como hipotensão ortostática, sonolência excessiva e boca seca. "
            "Identificar sinais de dependência ou uso problemático."
        ),
        (
            "Interações Medicamentosas",
            "CBD inibe enzimas do citocromo P450 (CYP3A4, CYP2D6), podendo alterar metabolismo de diversos fármacos. "
            "Atenção especial com: anticoagulantes (varfarina), antiepilépticos (clobazam), imunossupressores e antidepressivos. "
            "Sempre comunicar ao médico prescritor qualquer uso de canabinoides."
        ),
        (
            "Cuidado Livre de Estigma",
            "Abordagem não-julgamental é fundamental — muitos pacientes têm medo de revelar o uso de cannabis. "
            "A escuta ativa e a abertura ao diálogo criam vínculo terapêutico e melhoram os desfechos. "
            "Reconhecer que o estigma histórico prejudicou o acesso à pesquisa e ao cuidado."
        ),
        (
            "Saúde da Mulher Especificamente",
            "Reconhecer as especificidades da fisiologia feminina em relação ao SEC (ciclo hormonal, fertilidade, gestação). "
            "Abordagem sensível e educativa no pré-natal e puerpério sobre uso de cannabis. "
            "Apoiar mulheres com condições crônicas (endometriose, fibromialgia, TPM grave) que buscam alternativas terapêuticas."
        ),
    ]
    for titulo, desc in competencias:
        story.append(KeepTogether([
            Paragraph(titulo, estilos["subtitulo"]),
            Paragraph(desc, estilos["corpo"]),
            Spacer(1, 0.1 * cm),
        ]))

    story.append(linha_verde())
    story.append(Paragraph("Vias de Administração — O que o Enfermeiro Precisa Saber", estilos["titulo_topico"]))

    vias_data = [
        ["Via", "Início de Ação", "Duração", "Considerações de Enfermagem"],
        ["Inalatória (vaporização)", "1–5 min", "1–3 h", "Evitar combustão. Risco respiratório. Não indicada em doenças pulmonares."],
        ["Sublingual (óleo/tinturas)", "15–45 min", "4–8 h", "Boa biodisponibilidade. Titulação mais previsível. Orientar técnica correta."],
        ["Oral (cápsulas/comestíveis)", "30–120 min", "6–12 h", "Metabolização hepática (THC → 11-OH-THC mais potente). Maior variabilidade."],
        ["Tópica (cremes/géis)", "Local, variável", "Variável", "Efeito local sem absorção sistêmica significativa. Segura para maioria."],
        ["Retal (supositórios)", "15–30 min", "4–8 h", "Bypass do metabolismo de 1ª passagem. Maior biodisponibilidade do THC."],
    ]
    t = Table(vias_data, colWidths=[3.2 * cm, 2.8 * cm, 2.5 * cm, 9 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), VERDE_ESCURO),
        ("TEXTCOLOR",     (0, 0), (-1, 0), BRANCO),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 9),
        ("BACKGROUND",    (0, 1), (-1, -1), CINZA_CLARO),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [CINZA_CLARO, VERDE_PASTEL]),
        ("TEXTCOLOR",     (0, 1), (-1, -1), CINZA_TEXTO),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 9),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("GRID",          (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
    ]))
    story.append(t)

    story.append(Spacer(1, 0.5 * cm))
    story.append(linha_verde())
    story.append(Paragraph("O Futuro da Enfermagem e a Medicina Canabinoide", estilos["titulo_topico"]))
    story.append(Paragraph(
        "O campo da medicina canabinoide está em rápida expansão. Nos próximos anos, a enfermagem "
        "será cada vez mais chamada a:",
        estilos["corpo"]
    ))
    futuro = [
        "Integrar avaliação do uso de cannabis na prática clínica rotineira",
        "Participar de pesquisas clínicas sobre eficácia e segurança de canabinoides",
        "Atuar em clínicas especializadas em cannabis medicinal",
        "Desenvolver protocolos de cuidado para populações vulneráveis (gestantes, idosos, pacientes oncológicos)",
        "Liderar a educação em saúde sobre cannabis para pacientes e comunidades",
        "Contribuir para políticas públicas de saúde relacionadas à regulamentação do cannabis",
    ]
    for f in futuro:
        story.append(Paragraph(f"• {f}", estilos["bullet"]))

    story.append(Spacer(1, 0.4 * cm))
    story.append(caixa_colorida(
        "\"A enfermagem que conhece o Sistema Endocanabinoide cuida com mais ciência, "
        "mais humanidade e mais eficácia. O cuidado integral começa pelo conhecimento integral.\"",
        estilos["citacao"], VERDE_PASTEL
    ))
    story.append(PageBreak())
    return story


# ── Página final ──────────────────────────────────────────────────────────────
def pagina_final(estilos):
    story = []
    story.append(Spacer(1, 2 * cm))

    bloco = Table(
        [[Paragraph(
            "\"TODO SER HUMANO É<br/>UM, ÚNICO E EXCLUSIVO!<br/>RESPEITE SUA BIO-INDIVIDUALIDADE.\"",
            estilos["titulo_secao"]
        )]],
        colWidths=[17.5 * cm],
    )
    bloco.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), VERDE_ESCURO),
        ("TOPPADDING",    (0, 0), (-1, -1), 40),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 40),
        ("LEFTPADDING",   (0, 0), (-1, -1), 20),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 20),
    ]))
    story.append(bloco)
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("Katharine Louise", estilos["autora_capa"]))
    story.append(Paragraph("Cannabis &amp; Health Coach", estilos["autora_capa"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(linha_dourada())
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "Material educativo elaborado para acadêmicos de enfermagem — Maio 2026.",
        estilos["rodape_secao"]
    ))
    story.append(Paragraph(
        "Este documento tem finalidade estritamente educativa e não substitui orientação médica individualizada.",
        estilos["rodape_secao"]
    ))
    return story


# ── Rodapé de página ──────────────────────────────────────────────────────────
class RodapeCanvas:
    def __init__(self, doc):
        self.doc = doc

    def __call__(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#888888"))
        canvas.drawString(2 * cm, 1.2 * cm, "Cannabis & Saúde da Mulher | Katharine Louise")
        canvas.drawRightString(19.5 * cm, 1.2 * cm, f"Página {doc.page}")
        canvas.setStrokeColor(VERDE_CLARO)
        canvas.setLineWidth(0.5)
        canvas.line(2 * cm, 1.8 * cm, 19.5 * cm, 1.8 * cm)
        canvas.restoreState()


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2.5 * cm,
    )

    estilos = criar_estilos()

    story = []
    story += pagina_capa(estilos)
    story += secao_boas_vindas(estilos)
    story += secao_historia(estilos)
    story += secao_fitocanabinoides(estilos)
    story += secao_sec(estilos)
    story += secao_saude_mulher(estilos)
    story += secao_gravidez(estilos)
    story += secao_integrativa(estilos)
    story += secao_enfermagem(estilos)
    story += pagina_final(estilos)

    rc = RodapeCanvas(doc)
    doc.build(story, onFirstPage=rc, onLaterPages=rc)
    print(f"PDF gerado com sucesso: {OUTPUT}")


if __name__ == "__main__":
    main()
