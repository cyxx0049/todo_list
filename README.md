# 我的第一个Claude code项目
- 用Claude code从零生成一个项目：/init
- 用python写出待办事项脚本
- 实现功能：待办事项的增删查改，具体命令为
1.python todo.py add "..." #项目名称
2.python todo.py delete 1 #项目编号
3.python todo.py list [--done/--pending/(None)]
4.python todo.py done 1 #项目编号
- 使用plan mode规划了数据结构及边界条件等等
- 用json文件持久化
- 在Claude code自动验证时，在bash窗口出现乱码，对此问题进行提问及要求改进，最后在代码运行中加入代码：# 统一用 UTF-8 输出，避免在 Git Bash 等 UTF-8 终端里出现中文乱码
    sys.stdout.reconfigure(encoding="utf-8")
最终解决
- 项目收获：实践了Claude code的plan mode工作流