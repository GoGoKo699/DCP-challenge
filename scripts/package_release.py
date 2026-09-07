"""Assemble release assets from a clean tracked tree and a built technical PDF."""
from __future__ import annotations
import argparse
from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
VERSION='1.2.1'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'build'/'release-assets')
    parser.add_argument('--note-dir',type=Path,default=ROOT/'build'/'current-note')
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    names=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    names=sorted(n for n in names if n)
    # Release builds must package precisely a committed, clean source tree.
    subprocess.run(['git','diff','--exit-code','HEAD'],cwd=ROOT,check=True)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    with ZipFile(out/f'DCP-challenge-{VERSION}.zip','w',compression=ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            path=ROOT/name
            if not path.is_file() or path.is_symlink():
                raise ValueError(f'unsupported tracked object: {name}')
            info=ZipInfo(f'DCP-challenge-{VERSION}/{name}',(2026,9,7,0,0,0))
            info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644 << 16
            z.writestr(info,path.read_bytes(),compresslevel=9)
    for suffix in ('pdf','tex'):
        shutil.copy2(args.note_dir/f'DCP-current-technical-note.{suffix}',out)
    shutil.copy2(ROOT/'correction'/'author_correction.pdf',out/'author_correction_August_2026.pdf')
    shutil.copy2(ROOT/'audit'/'RELEASE_REVIEW.md',out/'RELEASE_REVIEW.md')
    (out/'RELEASE_COMMIT.txt').write_text(commit+'\n',encoding='utf-8')
    required=['VALIDATION.txt','ENVIRONMENT.txt']
    for name in required:
        if not (out/name).is_file(): raise FileNotFoundError(out/name)
    files=sorted(p for p in out.iterdir() if p.is_file() and p.name!='SHA256SUMS')
    (out/'SHA256SUMS').write_text(''.join(f'{sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in files),encoding='utf-8')
    print(f'{len(files)} release assets hashed at {out}; source commit {commit}')

if __name__=='__main__': main()
