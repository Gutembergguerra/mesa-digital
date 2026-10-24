import asyncio, subprocess, time, sys
from playwright.async_api import async_playwright

async def main():
    srv = subprocess.Popen([sys.executable,'-m','http.server','8765','--directory','/home/claude/mesa/site'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(1)
    errs=[]
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
            ctx = await b.new_context(accept_downloads=True, viewport={'width':400,'height':800})
            page = await ctx.new_page()
            page.on('pageerror', lambda e: errs.append('pageerror: '+str(e)))
            page.on('console', lambda m: errs.append('console.'+m.type+': '+m.text) if m.type=='error' else None)
            await page.add_init_script("localStorage.setItem('mesa-view2','compacto')")
            await page.goto('http://localhost:8765/index.html')
            await page.evaluate("document.querySelectorAll('.acc-body').forEach(b=>b.hidden=false);document.getElementById('fileSec').hidden=false;document.getElementById('projSec').hidden=false")
            await page.wait_for_timeout(500)
            say = lambda: page.evaluate("document.getElementById('avisos').textContent")
            print('canais:', await page.locator('#grid section.card').count())
            # exemplo + tocar + pausar
            await page.click('#btnDemo'); await page.wait_for_timeout(300); print('demo:', await say())
            await page.click('#btnPlay'); await page.wait_for_timeout(1200)
            print('botao tocando:', await page.inner_text('#btnPlay'), '| tempo:', await page.inner_text('#tempo'))
            await page.click('#btnPlay'); await page.wait_for_timeout(200)
            print('botao pausado:', await page.inner_text('#btnPlay'), '|', await say())
            # ajustes para testar restauracao
            await page.fill('#pjName','Teste um')
            await page.click('#muc2'); await page.click('#soc3')
            await page.evaluate("""()=>{const e=document.getElementById('vc0');e.value=-12;e.dispatchEvent(new Event('input',{bubbles:true}))}""")
            await page.select_option('#mcomp','forte')
            await page.click('#mrevb')
            print('vc0 antes:', await page.get_attribute('#vc0','aria-valuetext'))
            await page.click('text=Salvar projeto no aparelho'); await page.wait_for_timeout(1200)
            print('salvar:', await say())
            print('lista:', await page.inner_text('#pjList'))
            # mudar tudo e reabrir
            await page.click('#muc2'); await page.click('#soc3')
            await page.evaluate("""()=>{const e=document.getElementById('vc0');e.value=0;e.dispatchEvent(new Event('input',{bubbles:true}))}""")
            await page.select_option('#mcomp','suave')
            await page.click('#mrevb')
            await page.click('text=Abrir projeto selecionado'); await page.wait_for_timeout(300)
            print('abrir 1:', await say())
            await page.click('text=Abrir projeto selecionado'); await page.wait_for_timeout(1500)
            print('abrir 2:', await say())
            print('vc0 depois:', await page.get_attribute('#vc0','aria-valuetext'))
            print('mute c2:', await page.get_attribute('#muc2','aria-pressed'), '| solo c3:', await page.get_attribute('#soc3','aria-pressed'),
                  '| comp:', await page.input_value('#mcomp'), '| reverb:', await page.get_attribute('#mrevb','aria-pressed'))
            print('arquivo canal1:', await page.inner_text('#fc0'))
            # exportar arquivo e importar de volta
            async with page.expect_download() as dl:
                await page.click('text=Exportar projeto em arquivo')
            d = await dl.value
            path='/tmp/claude-0/-home-claude/4129777c-0cf8-5d04-a000-871a28639019/scratchpad/smoke/'+d.suggested_filename
            await d.save_as(path)
            import os; print('exportado:', d.suggested_filename, os.path.getsize(path),'bytes')
            await page.click('#muc2')
            await page.set_input_files('#pjImp', path); await page.wait_for_timeout(300)
            print('importar:', await say())
            await page.wait_for_timeout(1200)
            print('importar fim:', await say(), '| mute c2:', await page.get_attribute('#muc2','aria-pressed'))
            # apagar
            await page.click('text=Apagar projeto selecionado'); await page.wait_for_timeout(200)
            print('apagar 1:', await say())
            await page.click('text=Apagar projeto selecionado'); await page.wait_for_timeout(600)
            print('apagar 2:', await say(), '|', await page.inner_text('#pjList'))
            # overflow horizontal no celular
            print('scrollWidth/innerWidth:', await page.evaluate("[document.documentElement.scrollWidth, innerWidth]"))
            # exportar mixagem WAV
            async with page.expect_download(timeout=60000) as dl2:
                await page.click('text=Exportar mixagem em WAV')
            d2 = await dl2.value; p2='/tmp/claude-0/-home-claude/4129777c-0cf8-5d04-a000-871a28639019/scratchpad/smoke/mix.wav'
            await d2.save_as(p2); print('wav:', d2.suggested_filename, os.path.getsize(p2),'bytes')
            await b.close()
    finally:
        srv.terminate()
    print('ERROS:', '\n'.join(errs) if errs else 'nenhum')
asyncio.run(main())
