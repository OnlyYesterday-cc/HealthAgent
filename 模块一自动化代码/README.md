# 模块一自动化代码

从源项目提取的测试代码副本，原项目内的测试保留。

- `tests/`：认证、个人信息、血压记录共30条功能测试，含公共夹具。
- `defects/`：D01、D02、D03共3条缺陷专项。
- `run_tests.py`：调用源项目后端代码和虚拟环境；支持放在仓库根目录或课程目录。

先按源项目README安装后端依赖，再在本目录运行：

```bash
python3 run_tests.py module1
python3 run_tests.py defects
```

Windows可用`python`替代`python3`。两组结果分别统计，专项不计入30条功能用例。此目录不包含应用源码、依赖或历史执行日志，不能脱离源项目独立运行。
