# 陆京超第二批交付

负责范围：TC-001至TC-015、D01、D03根因和UTC方案、报告第1、2、4章及整合。源码修复已在2026-09-14提交2cda8a1中包含。

本目录分批完善。当前批次只完成TC-001至TC-015的清单、运行入口与功能验证；D01/D03专项核验、完整30条整合验证和报告补充留待后续批次。

## 运行

在仓库根目录的PowerShell运行：

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -e './backend[dev]'
backend/.venv/Scripts/python.exe 模块一作业交付包/第二批_陆京超/run_checks.py functional
```

macOS/Linux将解释器路径替换为backend/.venv/bin/python。无需启动服务，也不调用OCR或大模型接口。

省略套件名时默认运行functional（本批15条）。可通过--output-dir指定证据目录。测试失败时脚本退出码非零。

入口另支持defects（共享3条专项）、module1（整合30条）、security（安全模块6条）及all，供后续批次使用，提供入口不表示已经完成验证。本批15条已包含在整合30条中，不累加为45条。

每次运行保存UTF-8日志、JUnit XML、环境版本和Git基线信息。既有第一批失败记录和9月12日历史证据保留。

## 本批验证结果

2026-09-14在Windows、Python 3.10.11、pytest 8.3.3环境运行默认入口，实际收集15条，15条通过，0失败。被测源码基线为201e1c2；本批只修改运行入口与材料。

证据目录：[执行结果/20260914_155941_795601](执行结果/20260914_155941_795601)。functional.log保存完整输出，functional.xml保存逐条结果，environment.json保存环境版本、源码基线和执行命令。

日志包含pytest-asyncio默认fixture事件循环范围未配置的提示，以及Starlette依赖弃用警告。它们未导致本次用例失败，本批未调整公共测试配置或依赖版本。

## 内容

- 测试用例_TC001-015.md：输入、方法、预期和测试函数映射。
- 执行结果：本批functional日志、JUnit XML和环境信息。

报告补充尚未生成；本批不更新共享Office材料和缺陷关闭状态。

AI协助核对代码、整理材料与运行验证；原30条功能测试沿用工程。成员分工归属不表示这些代码或材料全部由成员独立原创。签署确认、视频录制、课程平台提交仍由成员完成。
