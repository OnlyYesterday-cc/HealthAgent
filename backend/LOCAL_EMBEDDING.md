# 本地中文向量检索

本机使用 `BAAI/bge-small-zh-v1.5`，模型文件位于 `backend/models/bge-small-zh-v1.5/`。
来源：https://huggingface.co/BAAI/bge-small-zh-v1.5
下载版本记录在模型目录的 `source.json` 中，模型说明保存在该目录的 `README.md` 中。

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
模型权重、分词器与来源记录已纳入 Git；克隆仓库即可获得模型文件。
索引和下载缓存不提交到 Git，首次运行按上面的命令生成索引。
问诊回答和 OCR 仍调用 `.env` 配置的云端 Qwen 模型。
