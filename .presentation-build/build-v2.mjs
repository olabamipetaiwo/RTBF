import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import { resolvePresentationFont, finalizePresentation } from '/Users/taiwoolabamipe/.codex/plugins/cache/openai-primary-runtime/presentations/26.921.10847/skills/presentations/container_tools/artifact_tool_utils.mjs';
const workspaceDir = '/Users/taiwoolabamipe/Downloads/UCF/RTBF';
const skillDir = '/Users/taiwoolabamipe/.codex/plugins/cache/openai-primary-runtime/presentations/26.921.10847/skills/presentations';
const buildDir = path.join(workspaceDir, '.presentation-build');
const font = resolvePresentationFont({fontFamily:'Arial'});
const presentation = Presentation.create({slideSize:{width:1600,height:900}});
function text(slide, content, left, top, width, height, size=30, bold=false, color='#222222') {
  const shape = slide.shapes.add({geometry:'textbox',position:{left,top,width,height},fill:'none',line:{fill:'none',width:0}});
  shape.text=content;
  shape.text.style={typeface:font,fontSize:size,bold,color,autoFit:'none'};
  return shape;
}
function base(title, index) {
  const slide = presentation.slides.add();
  slide.background.fill='#FFFFFF';
  text(slide,title,80,55,1440,95,52,true);
  text(slide,String(index).padStart(2,'0'),1450,840,70,30,20,false,'#777777');
  return slide;
}
function clean(value) { return value.replace(/\*\*/g,'').trim(); }
const markdown=await fs.readFile(path.join(workspaceDir,'result-meeting.md'),'utf8');
const sections=markdown.split(/^## /m).slice(1).map(section=>{
  const [title,...rest]=section.split('\n');
  const [body,notes='']=rest.join('\n').split('*Notes:*');
  const rows=body.split('\n').filter(line=>/^(- |\d+\. )/.test(line)).map(line=>{
    const match=line.match(/^(?:- |\d+\. )\*\*(.+?):?\*\*:?\s*(.*)$/);
    if (!match) throw new Error(`Unrecognized row: ${line}`);
    return {label:match[1].replace(/:$/,''),body:clean(match[2])};
  });
  return {title,rows,notes:notes.trim()};
});
const cover=presentation.slides.add();
cover.background.fill='#191919';
text(cover,'Results',90,265,1400,140,104,true,'#FFFFFF');
text(cover,'Chatbot data deletion',95,435,1350,70,42,false,'#DDDDDD');
text(cover,'Behavioral audit and user expectations',95,520,1350,60,30,false,'#BBBBBB');
cover.speakerNotes.textFrame.setText('Results meeting. The findings and discussion points follow the supplied outline.');
function addContent(section,index) {
  const slide=base(section.title,index+1);
  const isAcross=section.title==='Across platforms';
  const isDiscussion=section.title==='How we use these results';
  let top=isDiscussion?225:175;
  if(isDiscussion) text(slide,'PROPOSED FOR DISCUSSION · Main-result sentence still to be decided',80,158,1430,50,25,true,'#666666');
  const available=(isAcross?590:620)-(isDiscussion?45:0);
  const dense = section.rows.length > 6;
  const bodySize = dense ? 28 : 30;
  const lineHeight = dense ? 34 : 37;
  const weights=section.rows.map(row=>Math.max(2,Math.ceil(row.body.length/81)));
  const extra=Math.max(8,(available-weights.reduce((sum,n)=>sum+n*lineHeight,0))/section.rows.length);
  section.rows.forEach((row,rowIndex)=>{
    const height=weights[rowIndex]*lineHeight+extra;
    text(slide,row.label,80,top,310,height-10,27,true,'#555555');
    text(slide,row.body,415,top,1105,height-8,bodySize);
    top+=height;
  });
  if(isAcross) text(slide,'Provisional findings. The 14 of 33 figure still needs checking against its source.',80,795,1400,38,23,false,'#666666');
  slide.speakerNotes.textFrame.setText(section.notes);
}
sections.forEach(addContent);
const candidatePath=path.join(buildDir,'candidate-v2.pptx');
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
console.log('Exported',presentation.slides.items.length,'slides');
await finalizePresentation({workspaceDir,candidatePath,finalPath:path.join(workspaceDir,'output/result-meeting-v2.pptx'),pythonExecutable:'/Users/taiwoolabamipe/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3.12',integrityValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit'],explicitTotalSlideCount:13,fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(buildDir,'validation-v2.json')});
console.log('Finalized');
