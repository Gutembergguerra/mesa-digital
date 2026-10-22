# Mesa de Áudio: notas do projeto

Aplicativo web (PWA) de mesa de áudio com 6 canais e Master, feito para funcionar bem com leitor de tela (NVDA no Windows, TalkBack no Android). Autor: Gutemberg Guerra. Todos os direitos reservados.

## Arquivos
- `index.html`: o app inteiro (HTML, CSS e JavaScript num arquivo só).
- `sw.js`: cache para funcionar sem internet. Aumentar o número em `CACHE` a cada publicação.
- `manifest.webmanifest`, `icon-192.png`, `icon-512.png`: instalação como aplicativo.
- Publicado pelo GitHub Pages a partir da branch `main`, pasta raiz.
- Backups: branches `backup-v1-estavel` e `backup-v2-estavel`.

## O que o app tem
Volume, pan, mudo, solo e armar por canal. Efeitos por canal (pré-amplificador, equalizador, delay, chorus), presets de efeitos, copiar e restaurar efeitos, ouvir sem efeitos. Gravação em um ou vários canais armados (entradas separadas com placa de 2 canais), com contagem e metrônomo. Edição (marcar, cortar, copiar, colar, silenciar, desfazer). Afinação de voz. Reverb de voz (cadeia de 4 módulos). Master (equalizador, compressor, reverb leve, limitador). Exportar WAV e MP3. Projetos (salvar, abrir, exportar, importar). Visualizações: Faixas, Compacto, Lista, Lado a lado, Um canal por vez, Mesa vertical. Instruções do aplicativo dentro do app.

## Regras do projeto
- Nunca perder a acessibilidade: controles nativos, valores falados, foco estável.
- Qualquer mudança no app deve atualizar o tutorial "Instruções do aplicativo".
- Um código só para computador e celular.
- Testar com Playwright em celular em pé, deitado e computador.

## Preferências do autor (valem para qualquer conversa nova)
- O autor usa leitor de tela (NVDA e TalkBack) e fala as mensagens por voz, então pode haver erros de digitação. Entenda pelo contexto.
- O que o leitor de tela fala é mais importante do que o que aparece na tela. Nomes de botões claros e curtos, valores falados em português.
- Tela limpa: sem textos de apoio ou frases explicativas soltas. As explicações ficam em "Instruções do aplicativo".
- Pouca rolagem. Opções que não são usadas o tempo todo ficam dentro de um menu fechado (lista, tela própria com botão Fechar), não soltas na tela.
- O botão Gravar fica sempre à vista, no topo, e o foco do leitor fica nele ao gravar e parar. O mesmo vale para o Tocar.
- O gesto de voltar do Android deve fechar só a tela aberta, sem sair do app.
- Botões em ordem lógica, mesma ordem visual e de leitura. Botões relacionados juntos (Voltar e Avançar).
- Presets e escolhas em lista fechada, não em muitos botões.
- Efeitos são por canal. O reverb de voz vale para um canal só de cada vez.
- Respostas curtas e claras, passo a passo quando for explicar. Sem termos em inglês ou técnicos demais.
- Usa a versão gratuita do Claude: juntar vários pedidos numa mudança só, evitar trabalho repetido.
- Avisar sempre que um aplicativo instalado só pega a versão nova ao fechar e abrir de novo.
