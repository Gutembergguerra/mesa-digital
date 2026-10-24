import sys,runpy
from playwright.async_api import Page
og=Page.goto
async def g(self,*a,**k):
    r=await og(self,*a,**k)
    try:
        for _ in range(6): await self.click('#btnAddCh',timeout=2000)
    except Exception as e: print('addch fail',e)
    return r
Page.goto=g
runpy.run_path(sys.argv[1],run_name='__main__')
