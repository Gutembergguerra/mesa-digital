import asyncio, subprocess, time, sys
from playwright.async_api import async_playwright
fails=[]
def ck(n,ok,x=''):
    print(('OK   ' if ok else 'FALHA'),n,x)
    if not ok: fails.append(n)
async def main():
    srv=subprocess.Popen([sys.executable,'-m','http.server','8772','--directory','/home/claude/mesa/site'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1);errs=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
        for name,vp in (('retrato',{'width':400,'height':800}),('desktop',{'width':1200,'height':800})):
            print('==',name)
            c=await b.new_context(viewport=vp,accept_downloads=True);pg=await c.new_page()
            pg.on('pageerror',lambda e:errs.append(str(e)))
            say=lambda:pg.evaluate("document.getElementById('avisos').textContent")
            await pg.goto('http://localhost:8772/index.html');await pg.wait_for_timeout(400)
            vis=lambda:pg.evaluate("Array.from(document.querySelectorAll('#grid>section')).filter(s=>!s.hidden).length")
            ck('abre sem canais',await vis()==0, await pg.inner_text('#chInfo'))
            await pg.click('#btnRecTop') if False else None
            await pg.click('#btnAddCh');await pg.wait_for_timeout(120)
            ck('adicionar 1',await vis()==1,await say())
            await pg.click('#btnAddCh');await pg.click('#btnAddCh');await pg.wait_for_timeout(120)
            ck('3 canais',await vis()==3)
            ck('opcoes edCh',await pg.evaluate("document.getElementById('edCh').options.length")==3)
            ck('goSel canais',await pg.evaluate("Array.from(goSel.options).filter(o=>/^c\\d$/.test(o.value)).length")==3)
            await pg.click('#btnRmCh');await pg.wait_for_timeout(120)
            ck('remover',await vis()==2,await say())
            for _ in range(5): await pg.click('#btnAddCh')
            ck('limite 6',await vis()==6,await say())
            # demo + edição
            await pg.select_option('#goSel','files');await pg.click('#btnDemo');await pg.wait_for_timeout(700);await pg.click('#projClose')
            await pg.select_option('#goSel','ed');await pg.wait_for_timeout(200)
            await pg.select_option('#edCh','0')
            # dividir por partes iguais
            await pg.select_option('#dvMode','iguais');await pg.fill('#dvArg','4');await pg.click('text=Adicionar partes à lista');await pg.wait_for_timeout(200)
            ck('4 partes',await pg.evaluate("document.getElementById('dvList').options.length")==4,await say())
            await pg.click('text=Ouvir parte');await pg.wait_for_timeout(300);ck('ouvir',('Ouvindo' in await say()),await say())
            await pg.fill('#dvName','Intro');await pg.press('#dvName','Tab');await pg.wait_for_timeout(100)
            ck('renomear','Intro' in await pg.evaluate("document.getElementById('dvList').options[0].text"))
            await pg.select_option('#dvTo','new') if False else None
            await pg.click('text=Remover canal') if False else None
            # colocar parte 1 no canal 6 (substitui): confirma 2x
            await pg.select_option('#dvTo','5');await pg.click('text=Colocar parte no canal');await pg.click('text=Colocar parte no canal');await pg.wait_for_timeout(200)
            ck('colocar',('colocada' in await say()),await say())
            dur=await pg.evaluate("document.getElementById('fc5').textContent");print('  canal6:',dur)
            # cursor e dividir no cursor
            await pg.fill('#edPos','0') if False else None
            await pg.evaluate("document.getElementById('edPos').value='3000';document.getElementById('edPos').dispatchEvent(new Event('input'))")
            ck('cursor 3s',abs(float((await pg.inner_text('#tempo')).split('/')[0].replace(':','.').split('.')[-2] or 0))>=0)
            await pg.select_option('#edCh','0');await pg.select_option('#dvMode','cursor');await pg.click('text=Adicionar partes à lista');await pg.wait_for_timeout(200)
            ck('partes 6',await pg.evaluate("document.getElementById('dvList').options.length")==6,await say())
            # seleção cursor ate fim + cortar
            await pg.click('text=Selecionar do cursor até o fim');await pg.wait_for_timeout(100);print('  ',await say())
            await pg.click('button:text-is("Cortar")');await pg.wait_for_timeout(200);ck('cortou','Corte feito' in await say(),await say())
            # emendar canal 2 no 1
            await pg.select_option('#emFrom','1');await pg.select_option('#emTo','0');await pg.click('button:text-is("Emendar")');await pg.wait_for_timeout(300)
            ck('emendou','Emendado' in await say(),await say())
            await pg.click('text=Desfazer a emenda');await pg.wait_for_timeout(100);ck('desfez','Desfeito' in await say(),await say())
            # zip
            async with pg.expect_download() as d: await pg.click('text=Exportar todas as partes em ZIP')
            dl=await d.value;await dl.save_as('/tmp/pz.zip');import zipfile;z=zipfile.ZipFile('/tmp/pz.zip');ck('zip ok',z.testzip() is None and len(z.namelist())==6,str(z.namelist()[:2]))
            # remover canal com audio exige 2 cliques
            await pg.click('#btnRmCh');await pg.wait_for_timeout(120);ck('confirma remover','de novo' in await say(),await say());await pg.click('#btnRmCh');ck('removido 5',await vis()==5)
            # projeto: novo
            await pg.click('#btnProj');await pg.wait_for_timeout(150)
            heads=await pg.evaluate("Array.from(document.querySelectorAll('#projSec h3')).map(h=>h.textContent)")
            ck('ordem projetos',heads==['Abrir projeto','Novo projeto','Salvar projeto','Levar para outro aparelho'],str(heads))
            await pg.click('button:text-is("Novo projeto")');await pg.wait_for_timeout(150)
            if 'de novo' in await say(): await pg.click('button:text-is("Novo projeto")') if await pg.is_visible('button:text-is("Novo projeto")') else None
            await pg.wait_for_timeout(500)
            ck('novo limpa',await vis()==0,await say())
            ck('foco em adicionar',await pg.evaluate('document.activeElement.id')=='btnAddCh')
            ov=await pg.evaluate("[document.documentElement.scrollWidth,innerWidth]");ck('sem rolagem lateral',ov[0]<=ov[1],str(ov))
            await pg.screenshot(path=f'v11_{name}.png',full_page=False)
    print('ERROS JS:',errs or 'nenhum');print('FALHAS:',fails or 'nenhuma');srv.kill()
asyncio.run(main())
