#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kb_check.py —— 子课题验收关卡（最小可运行版）
用法:
    python scripts/kb_check.py SR-07                # 验收检查
    python scripts/kb_check.py --print-fingerprint  # 打印 GOAL.md 指纹
退出码: 0 = 全绿; 1 = 存在失败项
"""
import hashlib, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DONE_SECTIONS = ("自评表", "产出物清单", "目标贡献", "发现")
def fingerprint():
    g = ROOT / "GOAL.md"
    if not g.is_file():
        sys.exit("FATAL: GOAL.md 不存在")
    return hashlib.sha256(g.read_bytes()).hexdigest()[:8]
def state_field(key):
    txt = (ROOT / "STATE.md").read_text(encoding="utf-8")
    m = re.search(rf"^{re.escape(key)}:\s*(\S+)", txt, re.M)
    return m.group(1) if m else None
def run(sr):
    fails, warns = [], []
    st = ROOT / "subtasks" / sr
    if not st.is_dir():
        print(f"FATAL: {st} 不存在")
        return 1
    # C1 完成报告
    done = st / "DONE.md"
    if not done.is_file():
        fails.append("C1 DONE.md 不存在")
    else:
        txt = done.read_text(encoding="utf-8")
        for sec in DONE_SECTIONS:
            if sec not in txt:
                fails.append(f"C1 DONE.md 缺章节: {sec}")
        m = re.search(r"目标贡献\s*\n+([^\n#]+)", txt)
        if not (m and m.group(1).strip()):
            fails.append("C1 目标贡献栏为空")
        elif "无法表述" in m.group(1):
            warns.append("目标贡献=无法表述，需主会话复核并考虑升级")
    # C2 入库申请（允许空申请，但须提交且含理由）
    apps = sorted((ROOT / "kb" / "inbox").glob(f"{sr}-*.yaml"))
    if not apps:
        fails.append("C2 kb/inbox/ 无本子课题申请单（空申请也须提交）")
    else:
        body = apps[-1].read_text(encoding="utf-8")
        if "type:" not in body:
            fails.append("C2 申请单缺 type 字段")
        if re.search(r"type:\s*empty", body) and "理由" not in body:
            fails.append("C2 空申请缺少理由")
    # C3 git 工作区干净
    r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        fails.append("C3 存在未提交变更:\n    "
                     + r.stdout.strip().replace("\n", "\n    "))
    elif r.returncode != 0:
        warns.append("C3 非 git 仓库，跳过")
    # G1 宪章指纹（防未声明修改）
    if state_field("goal_fingerprint") != fingerprint():
        fails.append("G1 GOAL.md 指纹与 STATE.md 不一致（未声明的宪章修改？）")
    # G2 任务卡宪章版本（防过期任务卡）
    task = st / "TASK.md"
    if not task.is_file():
        fails.append("G2 TASK.md 不存在")
    else:
        m = re.search(r"goal_version:\s*(\S+)",
                      task.read_text(encoding="utf-8"))
        if not m:
            fails.append("G2 TASK.md 缺 goal_version")
        elif m.group(1) != state_field("goal_version"):
            fails.append(f"G2 任务卡宪章版本 {m.group(1)} 已过期，须处置")
    # G3 产出物头部元数据
    out = ROOT / "outputs" / sr
    if out.is_dir():
        for f in out.rglob("*"):
            if not f.is_file() or f.name.endswith(".meta.yaml"):
                continue
            if f.suffix in (".md", ".py"):
                head = "\n".join(f.read_text(encoding="utf-8",
                                             errors="ignore").splitlines()[:6])
                if "goal:" not in head:
                    fails.append(f"G3 缺 goal 头部: {f.relative_to(ROOT)}")
            else:
                meta = Path(str(f) + ".meta.yaml")
                if not (meta.is_file()
                        and "goal:" in meta.read_text(encoding="utf-8")):
                    fails.append(f"G3 缺元数据侧车: {meta.name}")
    else:
        warns.append("outputs/ 无该子课题产物（确认任务是否本就无文件产出）")
    for w in warns:
        print(f"WARN  {w}")
    for x in fails:
        print(f"FAIL  {x}")
    print("====", "验收关卡全绿" if not fails
          else f"验收关卡: {len(fails)} 项失败", "====")
    return 0 if not fails else 1
if __name__ == "__main__":
    if "--print-fingerprint" in sys.argv:
        print(fingerprint())
        sys.exit(0)
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(run(sys.argv[1]))
