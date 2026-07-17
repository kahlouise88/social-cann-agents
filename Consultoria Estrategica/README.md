# Consultoria Estratégica — Modelo Fixo

Este é o padrão oficial para o produto **Consultoria Estratégica** (linha Zen Moderna
Business): "auditoria digital do expert, material de 30+ páginas e reunião de devolutiva".

Sempre que Katharine pedir uma **Consultoria Estratégica** e enviar as informações de um
novo cliente, o diagnóstico deve ser gerado a partir deste modelo.

## Origem do modelo

- **Estrutura de conteúdo** (Partes I–III): `referencias/Diagnostico_Estrategico_Dra_Vanessa_Campos.pdf`
- **Identidade visual** (cores, tipografia, componentes): `referencias/Zen_Moderna_Playbook_Comercial.pdf`
- **Partes IV–IX**: criadas para completar a entrega de 30+ páginas prometida no produto,
  seguindo a mesma lógica diagnóstico → plano de ação.

## Estrutura do documento

1. Capa
2. Apresentação do Documento (teses centrais)
3. Parte I — Perfil da Analisada
4. Parte II — [Canal Principal]: A Primeira Fratura (normalmente a bio do Instagram)
5. Parte III — A Fratura Central (o problema mais caro identificado) + gráfico comparativo + framework de solução
6. Parte IV — Análise de Conteúdo
7. Parte V — Público & Concorrência
8. Parte VI — Funil & Monetização
9. Parte VII — Arquitetura de Oferta & Precificação
10. Parte VIII — Plano de Ação em 90 Dias
11. Parte IX — Indicadores de Sucesso
12. Fechamento — sempre aponta para a reunião de devolutiva (nunca uma oferta fixa; a
    proposta de continuidade é desenhada sob medida em conversa — "regra de ouro" do
    playbook Zen Moderna: nenhuma entrega termina sem apontar o próximo passo).

## Como gerar um diagnóstico novo

1. Copiar `modelo/template_diagnostico_estrategico.html` para
   `clientes/<nome-do-cliente>/diagnostico.html`.
2. Preencher os campos `{{TOKEN}}` e os blocos marcados com
   `<!-- INSTRUÇÃO: ... -->` usando **somente** as informações enviadas pela Katharine
   (prints, métricas, entrevista, texto livre — o formato de entrada varia por cliente).
3. **Nunca inventar número, dado ou resultado.** Quando uma informação não foi enviada:
   - Ou a linha da tabela é removida, ou
   - É escrito explicitamente "não informado" / "a validar na devolutiva" (mesmo padrão
     usado no documento da Dra. Vanessa para os pilares técnicos do método).
4. As Três Teses Centrais (Apresentação) e a Fratura Central (Parte III) são o
   coração do diagnóstico — exigem leitura crítica de verdade, não preenchimento
   genérico. É aqui que mora o valor de "clareza" que o cliente está comprando.
5. Tom de voz: direto, sem elogio decorativo, sem rodeio. Nomeia o problema com
   precisão. Sempre mostra o caminho (não só o diagnóstico).
6. Exportar o HTML final para PDF (ver abaixo) e entregar.

## Tom e princípios (extraídos do documento de referência)

- "Clareza custa caro porque é rara" — o relatório vende clareza, não elogio.
- O trabalho estratégico é **revelar** o que já existe no cliente, não inventar uma
  persona nova.
- Sempre que o cliente já tiver um método/diferencial próprio não comunicado, esse é
  candidato natural a virar a Fratura Central.
- Todo achado crítico vem acompanhado de uma recomendação imediata e acionável —
  nunca só o problema.

## Identidade visual (tokens em `modelo/template_diagnostico_estrategico.html`)

| Uso | Cor |
|---|---|
| Fundo principal | `#F7F1E7` (creme) |
| Cards claros | `#EFE3D1` |
| Painel escuro | `#35251A` (espresso) |
| Acento principal | `#BE5C2E` (terracota) |
| Acento secundário / dourado | `#C9A24B` |
| Status "ok" | `#7C8B6F` (sálvia) |

Tipografia serifada (Georgia) nos títulos, sans-serif nos rótulos/corpo — mesmo padrão
do playbook Zen Moderna (rótulos em caixa alta espaçada, título grande serifado, rodapé
com nome da marca + numeração).

## Exportar para PDF

O ambiente tem o binário do Chromium pré-instalado; falta apenas o pacote Python do
Playwright (`pip3 install playwright` — rápido, não baixa navegador de novo). Gerar o
PDF com impressão headless, mantendo cada `.page` como uma página A4:

```bash
pip3 install --quiet playwright

python3 - <<'EOF'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
        args=["--no-sandbox"],
    )
    page = browser.new_page()
    page.goto("file:///caminho/para/diagnostico.html")
    page.pdf(path="diagnostico.pdf", format="A4", print_background=True,
              margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    browser.close()
EOF
```

(O nome da pasta `chromium-1194` pode mudar em outra máquina — conferir com
`ls /opt/pw-browsers/`.)

## Pasta `clientes/`

Cada cliente atendida por este produto ganha uma subpasta própria com o HTML
preenchido e o PDF final, preservando o histórico de diagnósticos entregues.
