# 可选：本地中文向量检索

默认配置已改用云端 DashScope，仓库不再附带本地模型文件。仅在需要恢复离线向量检索时，手动下载 `BAAI/bge-small-zh-v1.5` 到 `backend/models/bge-small-zh-v1.5/`。
来源：https://huggingface.co/BAAI/bge-small-zh-v1.5
自行下载时请保留来源、版本和模型许可说明。

推理使用 CPU，加载本地 Safetensors 权重，不会自动联网下载模型或调用向量 API。
使用 CLS 向量及 L2 归一化；检索问题添加 BGE 中文查询前缀，文档不添加。
向量维度为 512，单段最大长度为 512 token。

在 backend 目录中安装依赖：

```bash
uv pip install --python .venv/bin/python --cache-dir ../.dependency-cache/uv -e '.[dev,local-embedding]'
```

本地 `.env` 配置：

```env
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL_PATH=models/bge-small-zh-v1.5
DASHSCOPE_EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5
DASHSCOPE_EMBEDDING_DIM=512
RAG_KB_DB_PATH=storage/kb-bge-small-zh-v1.5.sqlite
```

生成知识库索引及查看数量：

```bash
.venv/bin/python -m app.cli.kb ingest data/kb
.venv/bin/python -m app.cli.kb stats
```

旧的 `storage/kb.sqlite` 保留，新模型使用独立索引。
更换向量模型时必须使用新索引路径并重新入库，不能混用其他模型的向量。
模型目录已被 Git 忽略；克隆仓库不会获得模型权重和分词器，需要自行下载。
索引和下载缓存不提交到 Git，首次运行按上面的命令生成索引。
问诊回答和 OCR 仍调用 `.env` 配置的云端 Qwen 模型。
