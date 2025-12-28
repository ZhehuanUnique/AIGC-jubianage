#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理 Git 历史中的大文件（poster 文件夹）
"""
import sys
import subprocess
from pathlib import Path

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def run_command(cmd, check=True):
    """执行命令并返回结果"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
    if check and result.returncode != 0:
        print(f"错误: {result.stderr}")
        return False
    if result.stdout:
        print(result.stdout)
    return True

def main():
    print("=" * 60)
    print("清理 Git 历史中的 poster 文件夹")
    print("=" * 60)
    
    # 检查是否在 Git 仓库中
    if not Path(".git").exists():
        print("❌ 错误: 当前目录不是 Git 仓库")
        return False
    
    print("\n⚠️  警告: 此操作将重写 Git 历史，需要 force push")
    print("建议先备份仓库或创建新分支")
    
    # 1. 使用 git filter-branch 删除 poster 相关文件
    print("\n步骤 1: 从 Git 历史中删除 poster 文件夹...")
    
    # 删除根目录的 poster/
    cmd1 = 'git filter-branch --force --index-filter "git rm -rf --cached --ignore-unmatch poster" --prune-empty --tag-name-filter cat -- --all'
    if not run_command(cmd1, check=False):
        print("⚠️  filter-branch 可能已执行过，继续下一步...")
    
    # 删除 frontend-nuxt/public/poster/
    cmd2 = 'git filter-branch --force --index-filter "git rm -rf --cached --ignore-unmatch frontend-nuxt/public/poster" --prune-empty --tag-name-filter cat -- --all'
    if not run_command(cmd2, check=False):
        print("⚠️  filter-branch 可能已执行过，继续下一步...")
    
    # 2. 清理引用
    print("\n步骤 2: 清理 Git 引用...")
    run_command("git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin", check=False)
    run_command("git reflog expire --expire=now --all", check=False)
    
    # 3. 垃圾回收
    print("\n步骤 3: 执行垃圾回收...")
    run_command("git gc --prune=now --aggressive")
    
    # 4. 检查仓库大小
    print("\n步骤 4: 检查清理后的仓库大小...")
    run_command("git count-objects -vH")
    
    print("\n" + "=" * 60)
    print("✅ Git 历史清理完成！")
    print("\n下一步操作:")
    print("1. 检查仓库大小是否已减小")
    print("2. 如果满意，执行: git push origin main --force")
    print("   ⚠️  注意: force push 会覆盖远程历史，请确保团队成员已同步")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)

