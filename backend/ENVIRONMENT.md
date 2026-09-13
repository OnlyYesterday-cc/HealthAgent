# HealthAgent 环境安装

`requirements.txt` 锁定当前已安装的后端依赖版本，包含 FastAPI、OCR 图像处理、本地 BGE 向量推理及 pytest 测试工具。该快照来自 Python 3.12、macOS Apple Silicon 环境，其他平台尚未验证。前端依赖由 `frontend/package.json` 与 `frontend/package-lock.json` 管理。

## 后端

在 `HealthAgent/backend` 目录执行：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

如果使用 uv，可直接安装到虚拟环境：

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

以上创建虚拟环境的步骤用于新环境；当前机器已经安装完成，无需重建。

程序从 backend 目录启动，不要求将项目本身安装为 Python 包：

```bash
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 模型与配置

- 首次配置时从 `.env.example` 复制为 `.env`，设置 JWT 密钥、`DASHSCOPE_CHAT_API_KEY` 和向量服务使用的 `DASHSCOPE_API_KEY`；已有 `.env` 时保留其中配置。
- 默认使用云端 DashScope 向量服务（`EMBEDDING_PROVIDER=dashscope`），无需下载或复制本地 BGE 模型。模型目录不再随仓库提供。
- OCR 使用 Qwen 3.8 Flash，关闭思考；文字问诊使用同一套餐，思考强度 low。
- 本地向量推理仅作为可选功能保留，恢复方法见 `LOCAL_EMBEDDING.md`。切换向量模型后需使用独立索引路径并重新入库。
- 默认 SQLite，无需安装 PostgreSQL 或 Docker。

首次构建本地知识库，在 backend 目录执行：

```bash
.venv/bin/python -m app.cli.kb ingest data/kb
.venv/bin/python -m app.cli.kb stats
```

## 前端

本机使用 Node.js 26.4.0。打开另一个终端，在 `HealthAgent/frontend` 目录执行：

```bash
npm ci
npm run dev -- --host 127.0.0.1 --port 5173
```

访问 http://127.0.0.1:5173 。运行时保持前后端进程开启。

`requirements.txt` 用于复现当前版本；`pyproject.toml` 保留项目直接依赖声明。升级依赖后应同步更新快照，避免写入本机绝对路径或密钥。
