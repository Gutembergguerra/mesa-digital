const fs=require('fs'),assert=require('assert');
const src=fs.readFileSync('app-body.html','utf8');
const pure=src.match(/\/\*PURE-START\*\/([\s\S]*?)\/\*PURE-END\*\//)[1];
const A=new Function(pure+';return {analyzePitch,scaleMask,nearestAllowed,planCorrection,tuneChannels,pBlend}')();
const sr=44100;
function voice(segs,total){
  const x=new Float32Array(Math.floor(total*sr));
  segs.forEach(sg=>{
    const s0=Math.floor(sg.t0*sr),s1=Math.floor(sg.t1*sr);let ph=0;
    for(let i=s0;i<s1&&i<x.length;i++){
      const t=(i-s0)/sr;
      const cents=sg.cents+(sg.vib?sg.vib*Math.sin(2*Math.PI*5.5*t):0);
      const f=sg.f*Math.pow(2,cents/1200);
      ph+=2*Math.PI*f/sr;
      let v=0;for(let h=1;h<=14;h++)v+=Math.sin(h*ph)/h*(h<6?1:.6);
      const env=Math.min(1,t*30)*Math.min(1,(sg.t1-sg.t0-t)*30);
      x[i]=.25*v*env;
    }
  });
  return x;
}
const centsOf=(f,ref)=>1200*Math.log2(f/ref);
async function medianCents(x,t0,t1,ref){
  const an=await A.analyzePitch(x,sr);
  const vals=[];
  for(let f=0;f<an.f0.length;f++){
    const t=(an.c0+f*an.hopS)/sr;
    if(t>=t0&&t<=t1&&an.f0[f])vals.push(centsOf(an.f0[f],ref));
  }
  vals.sort((a,b)=>a-b);
  return {med:vals[vals.length>>1],n:vals.length,max:Math.max(...vals),min:Math.min(...vals)};
}
(async()=>{
  // duas notas desafinadas: A4 +35 cents (440) e A3 -40 cents (220), com silencio no meio
  const x=voice([{t0:.1,t1:1.1,f:440,cents:35},{t0:1.5,t1:2.6,f:220,cents:-40}],3);
  const t0=Date.now();
  const r=await A.tuneChannels([x],sr,{mask:A.scaleMask('cromatica',0),strength:1,smooth:.02},null);
  console.log('tempo para 3 s de audio:',Date.now()-t0,'ms');
  assert(r.out,'sem saida');
  const y=r.out[0];
  assert.equal(y.length,x.length);
  let nan=0,mx=0,mxx=0;for(let i=0;i<y.length;i++){if(!isFinite(y[i]))nan++;mx=Math.max(mx,Math.abs(y[i]));mxx=Math.max(mxx,Math.abs(x[i]))}
  assert.equal(nan,0);assert(mx<mxx*1.5,'amplitude '+mx+' vs '+mxx);
  const b1=await medianCents(x,.3,1.0,440),a1=await medianCents(y,.3,1.0,440);
  const b2=await medianCents(x,1.7,2.5,220),a2=await medianCents(y,1.7,2.5,220);
  console.log('nota1 antes',b1.med.toFixed(1),'depois',a1.med.toFixed(1),'| nota2 antes',b2.med.toFixed(1),'depois',a2.med.toFixed(1));
  assert(Math.abs(b1.med-35)<4&&Math.abs(b2.med+40)<4,'analise antes');
  assert(Math.abs(a1.med)<8,'nota1 depois '+a1.med);
  assert(Math.abs(a2.med)<8,'nota2 depois '+a2.med);
  // silencio permanece silencio
  let sil=0;for(let i=Math.floor(1.2*sr);i<Math.floor(1.4*sr);i++)sil=Math.max(sil,Math.abs(y[i]));
  assert(sil<1e-4,'silencio '+sil);
  console.log('meia correcao media (cents):',r.plan.meanCents.toFixed(1),'voz em',(r.plan.voiced/r.plan.total*100).toFixed(0)+'%');
  // afinada: quase nao muda
  const x2=voice([{t0:.1,t1:1.1,f:440,cents:0}],1.3);
  const r2=await A.tuneChannels([x2],sr,{mask:A.scaleMask('cromatica',0),strength:1,smooth:.02},null);
  if(r2.out){let d=0;for(let i=0;i<x2.length;i++)d=Math.max(d,Math.abs(r2.out[0][i]-x2[i]));console.log('afinada, dif max',d.toFixed(4));assert(d<.12)}else console.log('afinada: nada a fazer (ok)');
  // forca 50% corrige a metade
  const r3=await A.tuneChannels([x],sr,{mask:A.scaleMask('cromatica',0),strength:.5,smooth:.02},null);
  const a3=await medianCents(r3.out[0],.3,1.0,440);
  console.log('forca 50%: nota1',a3.med.toFixed(1),'(esperado ~17)');
  assert(Math.abs(a3.med-17.5)<7);
  // escala de Do maior: nota 70 (Lá#) +20 cents vai para Si (71)
  const f70=440*Math.pow(2,(70-69)/12);
  const x4=voice([{t0:.1,t1:1.1,f:f70,cents:20}],1.3);
  const r4=await A.tuneChannels([x4],sr,{mask:A.scaleMask('maior',0),strength:1,smooth:.02},null);
  const f71=440*Math.pow(2,2/12);
  const a4=await medianCents(r4.out[0],.3,1.0,f71);
  console.log('Do maior: nota final vs Si (cents)',a4.med.toFixed(1));
  assert(Math.abs(a4.med)<10);
  // vibrato +-30 cents ao redor de 330Hz+0, forca 100% rapida; deve ficar dentro de +-35 de uma nota
  const x5=voice([{t0:.1,t1:1.6,f:330,cents:-25,vib:25}],1.8);
  const r5=await A.tuneChannels([x5],sr,{mask:A.scaleMask('cromatica',0),strength:1,smooth:.02},null);
  const a5=await medianCents(r5.out[0],.4,1.4,330);
  console.log('vibrato: mediana',a5.med.toFixed(1),'faixa',a5.min.toFixed(0),'a',a5.max.toFixed(0));
  assert(Math.abs(a5.med)<15);
  // selecao com blend
  const bl=A.pBlend([x],[y.slice(0,Math.floor(1.2*sr))],0,sr);
  assert.equal(bl[0].length,x.length);
  // estereo
  const r6=await A.tuneChannels([x,x.map(v=>v*.5)],sr,{mask:A.scaleMask('cromatica',0),strength:1,smooth:.02},null);
  assert.equal(r6.out.length,2);
  // 10 s de audio: tempo
  const big=voice([{t0:.1,t1:9.9,f:330,cents:30,vib:15}],10);
  const t1=Date.now();await A.tuneChannels([big],sr,{mask:A.scaleMask('cromatica',0),strength:1,smooth:.05},null);
  console.log('tempo para 10 s:',Date.now()-t1,'ms  (3 min ~',((Date.now()-t1)*18/1000).toFixed(0),'s)');
  console.log('TUNE TESTS OK');
})().catch(e=>{console.error('FALHOU',e.message);process.exit(1)});
