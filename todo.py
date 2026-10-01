import json
import os
import sys

TASKS_FILE = "tasks.json"


def load_tasks():
    """读取 tasks.json，返回任务列表；文件不存在时报错退出。"""
    if not os.path.exists(TASKS_FILE):
        print("路径下无任务文件，请将tasks.json文件放入和python脚本文件的同目录下")
        sys.exit(1)
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    """把任务列表写回 tasks.json。"""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def print_usage():
    print("用法: python todo.py <指令> [参数]")
    print()
    print("指令:")
    print('  add "任务内容"       添加新任务')
    print("  list [--done|--pending]  列出任务（可筛选已完成/未完成）")
    print("  done <任务编号>      标记任务为已完成")
    print("  delete <任务编号>     删除任务")


def add_task(content):
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": new_id, "content": content, "done": False})
    save_tasks(tasks)
    print(f"已添加任务 #{new_id}: {content}")


def list_tasks(status=None):
    tasks = load_tasks()
    if status == "done":
        tasks = [t for t in tasks if t["done"]]
        empty_msg = "没有已完成的任务"
    elif status == "pending":
        tasks = [t for t in tasks if not t["done"]]
        empty_msg = "没有未完成的任务"
    else:
        empty_msg = "暂无任务"
    if not tasks:
        print(empty_msg)
        return
    for t in tasks:
        status = "[x]" if t["done"] else "[ ]"
        print(f"{t['id']}. {status} {t['content']}")


def done_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"任务 #{task_id} 已完成")
            return
    print(f"找不到任务 #{task_id}")


def delete_task(task_id):
    tasks = load_tasks()
    remaining = [t for t in tasks if t["id"] != task_id]
    if len(remaining) == len(tasks):
        print(f"找不到任务 #{task_id}")
        return
    save_tasks(remaining)
    print(f"已删除任务 #{task_id}")


def main():
    # 统一用 UTF-8 输出，避免在 Git Bash 等 UTF-8 终端里出现中文乱码
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print("错误：缺少指令")
        print_usage()
        return

    cmd = sys.argv[1]

    if cmd == "add":
        if len(sys.argv) < 3:
            print("错误：缺少任务内容")
            print('用法: python todo.py add "任务内容"')
            return
        content = " ".join(sys.argv[2:])
        add_task(content)
    elif cmd == "list":
        status = None
        if len(sys.argv) >= 3:
            flag = sys.argv[2]
            if flag == "--done":
                status = "done"
            elif flag == "--pending":
                status = "pending"
            else:
                print(f"错误：未知参数 '{flag}'")
                print("用法: python todo.py list [--done|--pending]")
                return
        list_tasks(status)
    elif cmd == "done":
        if len(sys.argv) < 3:
            print("错误：缺少任务编号")
            print("用法: python todo.py done <任务编号>")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print(f"找不到任务 #{sys.argv[2]}")
            return
        done_task(task_id)
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("错误：缺少任务编号")
            print("用法: python todo.py delete <任务编号>")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print(f"找不到任务 #{sys.argv[2]}")
            return
        delete_task(task_id)
    else:
        print(f"错误：未知指令 '{cmd}'")
        print_usage()


if __name__ == "__main__":
    main()
