# 陆京超第二批交付

负责范围：TC-001至TC-015、D01、D03根因和UTC方案、报告第1、2、4章及整合。源码修复已在2026-09-14提交2cda8a1中包含，本批补齐对应材料与实际验证证据。

## 运行

在仓库根目录的PowerShell运行：

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -e './backend[dev]'
backend/.venv/Scripts/python.exe 模块一作业交付包/第二批_陆京超/run_checks.py all
```

macOS/Linux将解释器路径替换为backend/.venv/bin/python。无需启动服务，也不调用OCR或大模型接口。

all分别运行functional（本批15条）、defects（共享3条专项）、module1（整合30条）和security（安全模块6条）。本批15条已包含在整合30条中，不累加为45条。可用任一套件名替换all，或通过--output-dir指定证据目录。任一套件失败，脚本退出码非零。

每次运行保存UTF-8日志、JUnit XML、环境版本和Git基线信息。既有第一批失败记录和9月12日历史证据保留。

## 内容

- 测试用例_TC001-015.md：输入、方法、预期和测试函数映射。
- 报告补充_第二批.md：当前版本范围、D01/D03根因、实现和整合结论。
- 执行结果：本次验证证据，functional与defects分别计数。

AI协助核对代码、整理材料与运行验证；原30条功能测试沿用工程。成员分工归属不表示这些代码或材料全部由成员独立原创。签署确认、视频录制、课程平台提交仍由成员完成。
