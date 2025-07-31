# bbs/core.py

import os, sys, subprocess, json, base64
from dataclasses import dataclass
from typing import List

# ─── Data models ─────────────────────────────────────────────────────────────

@dataclass
class GroupPK:
    g1: bytes; g2: bytes; h: bytes
    u: bytes;  v: bytes;  w: bytes

    @property
    def b64_dict(self):
        return {
            k: base64.urlsafe_b64encode(getattr(self, k)).decode().rstrip('=')
            for k in ('g1','g2','h','u','v','w')
        }

@dataclass
class ManagerSK:
    xi1: bytes; xi2: bytes

    @property
    def b64_dict(self):
        return {
            'xi1': base64.urlsafe_b64encode(self.xi1).decode().rstrip('='),
            'xi2': base64.urlsafe_b64encode(self.xi2).decode().rstrip('=')
        }

@dataclass
class MemberSK:
    A:   bytes
    x:   bytes
    kid: str

    @property
    def b64_dict(self):
        return {
            'A':   base64.urlsafe_b64encode(self.A).decode().rstrip('='),
            'x':   base64.urlsafe_b64encode(self.x).decode().rstrip('='),
            'kid': self.kid
        }

@dataclass
class GroupBundle:
    group_pk:   GroupPK
    manager_sk: ManagerSK
    members:    List[MemberSK]

@dataclass
class BbsSignature:
    T1: bytes; T2: bytes; T3: bytes
    c:  int;    s1: int;    s2: int
    s3: int;    s4: int;    s5: int

    def to_bytes(self) -> bytes:
        parts = [self.T1, self.T2, self.T3]
        L = len(self.T1)
        for s in (self.c, self.s1, self.s2, self.s3, self.s4, self.s5):
            parts.append(s.to_bytes(L, 'big'))
        return b''.join(parts)

    def to_base64(self) -> str:
        return base64.urlsafe_b64encode(self.to_bytes()).rstrip(b'=').decode()

# ─── Key Generation ──────────────────────────────────────────────────────────

def generate_group_keys(n_members: int = 1) -> GroupBundle:
    sage_dir = os.path.join(os.path.dirname(__file__), 'sage')
    sage_cmd = (
      "import sys; "
      f"sys.path.insert(0, r'{sage_dir}'); "
      "load('keygen.sage')"
    )
    proc = subprocess.run(
      ['sage', '-c', sage_cmd],
      cwd=sage_dir, capture_output=True, text=True
    )
    if proc.returncode:
        raise RuntimeError(f"Key-gen failed:\n{proc.stderr}")

    outf = os.path.join(sage_dir, 'output.txt')
    if not os.path.exists(outf):
        raise RuntimeError("keygen.sage finished but no output.txt found")
    kv = {}
    with open(outf) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            label, val = line.split()
            kv[label] = val
    os.remove(outf)

    def ub64(s: str) -> bytes:
        pad = '=' * (-len(s) % 4)
        return base64.urlsafe_b64decode(s + pad)

    gpk = GroupPK(
      g1=ub64(kv['g1']), g2=ub64(kv['g2']),
      h =ub64(kv['h']),  u =ub64(kv['u']),
      v =ub64(kv['v']),  w =ub64(kv['w'])
    )
    msk = ManagerSK(
      xi1=ub64(kv['xi1']),
      xi2=ub64(kv['xi2'])
    )
    members = []
    for i in range(1, n_members+1):
        idx = f"member{i:02d}"
        members.append(MemberSK(
          A  = ub64(kv[f"{idx}_A"]),
          x  = ub64(kv[f"{idx}_x"]),
          kid= f"m{i:02d}"
        ))
    return GroupBundle(group_pk=gpk, manager_sk=msk, members=members)

# ─── CLI Invocation Helpers ─────────────────────────────────────────────────

def _run_cli(script_name: str, payload: dict) -> dict:
    sage_dir = os.path.join(os.path.dirname(__file__), 'sage')
    cli_path = os.path.join(sage_dir, script_name)
    proc = subprocess.run(
        ['sage', '-python', cli_path],
        cwd=sage_dir,
        input=json.dumps(payload),
        capture_output=True, text=True
    )
    if proc.returncode:
        raise RuntimeError(f"{script_name} failed:\n{proc.stderr}")
    return json.loads(proc.stdout)

# ─── Sign & Verify ──────────────────────────────────────────────────────────

def sign(msg: bytes, member: MemberSK, group: GroupPK) -> BbsSignature:
    payload = {
        'gpk': group.b64_dict,
        'gsk': member.b64_dict,
        'msg': base64.urlsafe_b64encode(msg).decode().rstrip('=')
    }
    out = _run_cli('sign_cli.py', payload)
    def dpt(f):  return base64.urlsafe_b64decode(out[f] + '==')
    def dint(f): return int.from_bytes(base64.urlsafe_b64decode(out[f]+'=='), 'big')
    return BbsSignature(
        T1=dpt('T1'), T2=dpt('T2'), T3=dpt('T3'),
        c=dint('c'), s1=dint('s1'), s2=dint('s2'),
        s3=dint('s3'), s4=dint('s4'), s5=dint('s5')
    )

def verify(msg: bytes, sig: BbsSignature, group: GroupPK) -> bool:
    payload = {
        'gpk': group.b64_dict,
        'msg': base64.urlsafe_b64encode(msg).decode().rstrip('='),
        'sig': {
            **{f: base64.urlsafe_b64encode(getattr(sig, f)).decode().rstrip('=')
               for f in ('T1','T2','T3')},
            **{f: base64.urlsafe_b64encode(
                   getattr(sig,f).to_bytes(len(sig.T1),'big')
               ).decode().rstrip('=')
               for f in ('c','s1','s2','s3','s4','s5')}
        }
    }
    return _run_cli('verify_cli.py', payload).get('valid', False)

def open_signature(sig: BbsSignature, manager: ManagerSK, group: GroupPK) -> str:
    raise NotImplementedError("BBS open() not implemented yet")
