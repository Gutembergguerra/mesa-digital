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
