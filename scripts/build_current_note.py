"""Build the current Markdown note as standalone LaTeX and PDF.

Requires pandoc and XeLaTeX; no network or bibliography service is used.
The dated August PDF is not read or modified. Output is excluded from Git.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'build'/'current-note')
    args = parser.parse_args()
    for executable in ('pandoc','xelatex'):
        if not shutil.which(executable):
            parser.error(f'{executable} is required to build the technical PDF')
    output=args.output.resolve(); output.mkdir(parents=True,exist_ok=True)
    text=(ROOT/'docs'/'CURRENT_TECHNICAL_NOTE.md').read_text(encoding='utf-8')
    lines=text.splitlines()
    title=lines[0].removeprefix('# ')
    body='\n'.join(lines[4:])+'\n' # Title, blank, author/date/version, blank.
    # Keep short equation introductions and the small frontier table together.
    for anchor in ('With $F_N', 'For $N=2$, the ideal confidence frontier is:'):
        body=body.replace(anchor, r'\needspace{12\baselineskip}'+'\n\n'+anchor, 1)
    body=body.replace('## References', r'\clearpage'+'\n\n## References', 1)
    md=output/'current_technical_note.md';md.write_text(body,encoding='utf-8')
    stem='DCP-current-technical-note'
    tex=output/f'{stem}.tex'
    subprocess.run(['pandoc',str(md),'-f','markdown+tex_math_dollars',
        '--standalone','--toc','--toc-depth=1','--shift-heading-level-by=-1',
        '-M',f'title={title}','-M','author=Ruge Lin',
        '-M','date=7 September 2026 | Version 1.2.1',
        '-V','documentclass=article','-V','fontsize=11pt',
        '-V','geometry=a4paper,margin=23mm',
        '-H',str(ROOT/'docs'/'note_header.tex'),'-o',str(tex)],check=True)
    env=os.environ.copy()
    env.setdefault('SOURCE_DATE_EPOCH','1788739200')
    env.setdefault('FORCE_SOURCE_DATE','1')
    for pass_number in range(3):
        done=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',
            '-no-shell-escape',tex.name],cwd=output,env=env,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,text=True)
        (output/f'build-pass-{pass_number+1}.log').write_text(done.stdout,encoding='utf-8')
        if done.returncode:
            print(done.stdout[-8000:],file=sys.stderr)
            raise SystemExit(done.returncode)
    log=(output/f'{stem}.log').read_text(encoding='utf-8')
    for marker in ('Missing character:', 'Undefined control sequence', 'Overfull \\hbox', 'Overfull \\vbox'):
        if marker in log:
            raise RuntimeError(f'PDF preflight failed: {marker}; inspect {output}')
    print(output/f'{stem}.pdf')

if __name__=='__main__': main()
