# HealthAgent 模块二测试作业

方案2：用AI辅助测试认证、个人信息和血压记录。计划新增20条用例，陆京超、袁立沛各负责10条及相应材料，计划工作量各50%。陆京超的10条测试及M2-D01修复已完成，Office材料尚待整理，袁立沛部分尚未代做。

## 主要文件

参照模块一，根目录放小组说明；陆京超所有个人用例、缺陷、AI记录与执行结果集中在第一批_陆京超。文件夹不随Git提交批次增加。测试源码仍按原工程结构位于backend/tests/module2。

```text
模块二作业交付包/
├── README.md
├── 成员分工_拟定.md
├── 提交说明.md
├── 成果汇报纲要与演示视频脚本.md
├── run_module2_tests.py
└── 第一批_陆京超/
    ├── README.md
    ├── run_checks.py
    ├── 测试用例_M2-TC001-010.md
    ├── AI实践记录_第一批.md
    ├── 缺陷证据/
    │   └── 缺陷记录_M2-D01.md
    └── 执行结果/
        └── 按执行时间归档的日志、XML和环境信息
```

详见[成员分工](成员分工_拟定.md)、[陆京超材料](第一批_陆京超/README.md)、[提交说明](提交说明.md)。

## 怎么运行

沿用backend/.venv，在仓库根目录PowerShell运行：

```powershell
backend/.venv/Scripts/python.exe 模块二作业交付包/第一批_陆京超/run_checks.py
backend/.venv/Scripts/python.exe 模块二作业交付包/第一批_陆京超/run_checks.py regression
```

第一条运行陆京超10条模块二测试；第二条执行模块一30条功能、6条安全及3条专项回归，合计39条，不能算作模块二新增用例。根目录run_module2_tests.py转发到同一入口。macOS/Linux换用backend/.venv/bin/python。

首次安装：python -m venv backend/.venv，然后用虚拟环境Python执行pip install -e './backend[dev]'。测试采用SQLite内存库和测试签名密钥，不调用外部AI接口；每次结果保存到第一批_陆京超/执行结果，支持--output-dir指定目录，失败返回非零。

## 当前状态

2026-09-14扩展10条修复前为5通过5失败，修复后10通过；模块一回归39通过。原首批5条的2通过3失败记录原样保留，不能当作当前修复版本结果。M2-D01已修复，待本人复核与关闭签署。

作业仍需至少15条新增用例、有效缺陷报告及最终Excel、Word、PPT和视频。陆京超后续个人材料仍放第一批文件夹；当前Markdown不替代Office交付件。附录4章节、关键对话截图及人工修正记录要求继续适用。PDF载明9月25日展示、当晚23:00提交，最终以课堂通知为准。
