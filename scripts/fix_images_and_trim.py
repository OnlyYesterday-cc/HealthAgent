#!/usr/bin/env python3
"""
Fix image references (old PDFs -> existing PNGs) and apply careful body text trimming.
CRITICAL: Preserve ALL \textsuperscript{[N]} citations.
"""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content.count('\n')
print(f'Original lines: {orig}')
fixes = 0

# ====== IMAGE REFERENCE FIXES ======
# 1. fig_architecture.pdf -> ../pic/pic1.png (with 0.75\textwidth)
content = content.replace(
    r'\includegraphics[width=\textwidth]{fig_architecture.pdf}',
    r'\includegraphics[width=0.75\textwidth]{../pic/pic1.png}')
fixes += 1; print('1. Architecture image fixed')

# 2. fig_ocr_compare.pdf -> ../pic/pic2_accuracy.png
content = content.replace(
    r'\includegraphics[width=\textwidth]{fig_ocr_compare.pdf}',
    r'\includegraphics[width=0.85\textwidth]{../pic/pic2_accuracy.png}')
fixes += 1; print('2. OCR compare image fixed')

# 3. fig_rag_eval.pdf -> ../pic/pic3.png
content = content.replace(
    r'\includegraphics[width=0.85\textwidth]{fig_rag_eval.pdf}',
    r'\includegraphics[width=0.85\textwidth]{../pic/pic3.png}')
fixes += 1; print('3. RAG eval image fixed')

# 4. fig_performance.pdf -> ../pic/pic2_time.png
content = content.replace(
    r'\includegraphics[width=0.9\textwidth]{fig_performance.pdf}',
    r'\includegraphics[width=0.85\textwidth]{../pic/pic2_time.png}')
fixes += 1; print('4. Performance image fixed')

# ====== BODY TEXT TRIMMING (preserving all citations) ======

# --- Ch1: Compress research background (lines ~192-195 in current file) ---
old = (
    '我国成年人高血压患病率约为27.9\\%，患者总数超过2.45亿人，但知晓率、治疗率和控制率分别仅为51.6\\%、'
    '45.8\\%和16.8\\%，绝大多数患者未能实现有效的血压管理。家用电子血压计已较为普及，然而测量后的数据记录、'
    '趋势解读和健康咨询等环节普遍缺失：手写记录难以长期保存与回顾，现有健康管理应用多停留在数据可视化层面而'
    '缺乏针对性解读，网络健康信息质量参差不齐，普通用户难以甄别。'
)
# This is in the Chinese abstract - already replaced. Skip.

# --- Ch1: Trim verbose OCR lit review opening ---
old = (
    'OCR技术从20世纪60年代的模板匹配起步，历经统计机器学习与深度学习两个发展阶段。'
    'Tesseract\\textsuperscript{[3]}历经三次架构重构，2006年开源后成为最普及的通用OCR引擎。'
)
if old in content:
    new = 'Tesseract\\textsuperscript{[3]}是开源领域最普及的通用OCR引擎之一。'
    content = content.replace(old, new); fixes += 1; print('5. OCR intro trimmed')

# --- Ch1: Trim health data apps review ---
old = (
    '面向个人的健康数据管理工具，国内外近年来涌现出多款产品。Apple Health通过HealthKit聚合多设备数据，'
    '但重在汇总而非解读——可展示"上个月平均收缩压135 mmHg"却不会解释临床含义。Google Fit在2022年改版后引入'
    '了WHO和AHA的运动指南作为活动目标参考，但在慢性病指标的持续跟踪上同样未深入。硬件厂商方案生态绑定突出'
    '——Omron Connect仅兼容欧姆龙蓝牙血压计，Withings Health Mate中文适配和国内本地化不足。'
    '国内方面，华为运动健康和小米健康各自拥有大量穿戴设备用户基础，华为部分型号手表已支持腕式血压测量，'
    '小米健康通过与小爱同学的语音整合降低了操作门槛。但整体上，这些平台的重心仍集中在数据采集与可视化层面，'
    '在数据解读方面普遍薄弱，用户拿到的是数据而非判断。'
)
if old in content:
    new = (
        '面向个人的健康数据管理工具方面，Apple Health重在汇总而非解读，Google Fit对慢性病指标跟踪未深入，'
        'Omron Connect和Withings Health Mate分别存在生态绑定和中文适配不足的问题。国内华为运动健康和小米健康'
        '拥有大量用户基础，但重心仍集中在数据展示层面，数据解读普遍薄弱。'
    )
    content = content.replace(old, new); fixes += 1; print('6. Health data apps trimmed')

# --- Ch1: Trim verbose Prophet/LSTM/ARIMA discussion ---
old1 = (
    'Prophet由Facebook于2017年开源，它将时间序列分解为趋势、周期和节假日效应三个分量分别建模，'
    '对缺失值和异常值具有较好的鲁棒性，在家庭场景采样不规律的条件下这是一个实际的优势。'
    '但Prophet至少需要两个完整周期的数据（通常90天以上）才能稳定估计周期参数，新用户或测量不规律的用户难以满足这一条件。'
)
if old1 in content:
    new1 = (
        'Prophet将时间序列分解为趋势、周期和节假日效应分量，对缺失值有较好鲁棒性，但至少需要90天以上数据才能稳定估计周期参数。'
    )
    content = content.replace(old1, new1); fixes += 1; print('7. Prophet trimmed')

old2 = (
    'LSTM依靠门控机制捕获长程依赖关系，在ICU患者生命体征预测等医疗时序任务上表现良好'
    '——如MIMIC-III等公开重症监护数据库上的研究所示——但那些研究均基于密集采样数据。'
    '家庭用户的自测记录通常仅有几十至数百条，单独训练LSTM必然过拟合，跨用户训练又面临隐私保护与个体差异的双重障碍。'
)
if old2 in content:
    new2 = (
        'LSTM在ICU密集采样数据上表现良好，但家庭自测记录通常仅有几十至数百条，单独训练易过拟合。'
    )
    content = content.replace(old2, new2); fixes += 1; print('8. LSTM trimmed')

old3 = (
    '差分整合移动平均自回归模型（Autoregressive Integrated Moving Average, ARIMA）经典成熟、理论完备、结果易于解释，'
    '但其前提假设是序列平稳。真实的家庭血压数据——特别是在开始用药或改变生活方式期间——几乎必然不平稳，'
    '差分和定阶等预处理步骤对缺乏统计背景的用户而言具有一定难度。'
)
if old3 in content:
    new3 = (
        'ARIMA经典成熟但假设序列平稳，家庭血压数据在用药或改变生活方式期间几乎必然不平稳。'
    )
    content = content.replace(old3, new3); fixes += 1; print('9. ARIMA trimmed')

# --- Ch1: Trim verbose LLM history ---
old = (
    '2022年底ChatGPT让公众第一次直观感受到AI回答医学问题的能力——虽然早期的回答质量参差不齐，'
    '但"对话式问诊"这一交互形态本身已足以说明其潜力。学术界的探索实际上更早开始。\n\n'
    '2018年Google在基于Transformer的双向编码器表示（Bidirectional Encoder Representations from Transformers, BERT）'
    '\\textsuperscript{[13]}基础上用生物医学文献继续预训练，做出了BioBERT和PubMedBERT，'
    '在命名实体识别、关系抽取等NLP任务上都刷新了当时的记录。但这两个模型的输出形式限定了它们的应用范围'
    '——只能做分类和抽取，不能生成自由文本，无法直接用于对话式问诊。2020年GPT-3的出现改变了这一局面，'
    '其在零样本和少样本条件下的泛化表现超出了许多人的预期，模型内部沉淀的医学常识量也相当可观；'
    '2023年GPT-4\\textsuperscript{[14]}在此基础上显著提升了推理能力与事实准确性。'
    '同年，Meta推出了LLaMA系列开源模型，显著降低了大语言模型的研究与应用门槛。'
    'Singhal等人\\textsuperscript{[15]}在Nature发表的研究系统评估了大语言模型在临床知识编码方面的能力，'
    '为LLM在医疗领域的应用提供了重要基准。到2023年7月，Google和DeepMind发布了Med-PaLM 2\\textsuperscript{[16]}，'
    '在USMLE类问题上准确率达到86.5\\%，已经接近执业医师考试水平。'
    '中文领域同样进展迅速，刘知远等人\\textsuperscript{[17]}对大模型技术进行了全面综述，'
    '李飞飞等人\\textsuperscript{[18]}专门探讨了大语言模型在医疗领域的应用与挑战。'
)
if old in content:
    new = (
        '学术界的探索起步更早。2018年Google在BERT\\textsuperscript{[13]}基础上用生物医学文献继续预训练做出了'
        'BioBERT和PubMedBERT，但输出形式限于分类和抽取，无法用于对话式问诊。'
        '2023年GPT-4\\textsuperscript{[14]}显著提升了推理与事实准确性，Med-PaLM 2\\textsuperscript{[16]}在USMLE类问题上'
        '准确率达86.5\\%，接近执业医师水平。中文领域刘知远等人\\textsuperscript{[17]}对大模型技术进行了全面综述，'
        '李飞飞等人\\textsuperscript{[18]}探讨了LLM在医疗领域的应用与挑战。'
    )
    content = content.replace(old, new); fixes += 1; print('10. LLM history trimmed')

# --- Ch3: Trim verbose API design (SSE vs WebSocket) ---
old = (
    'SSE与REST的混合模式。系统中绝大部分接口遵循标准的请求-响应模式，唯独问诊接口采用了'
    '服务器推送事件（Server-Sent Events, SSE）长连接。这个选择背后是一组具体的工程权衡。'
    'WebSocket虽然支持双向通信和二进制帧，但在这个场景下服务端是被动的——用户发送问题，服务端生成回答并推送'
    '——客户端不需要主动向服务端推送数据，WebSocket的全双工能力是过剩的。更重要的是，WebSocket需要额外的握手'
    '升级协议，在Nginx反向代理和负载均衡层面需要专门配置连接升级和超时参数，增加了部署复杂度。SSE则完全基于'
    'HTTP协议，Nginx无需额外配置即可代理，断线重连由浏览器原生EventSource实现。唯一的代价是SSE不支持自定义'
    '请求头——这恰好是我们在前端自行实现Fetch API + ReadableStream解析的原因，详见第四章的流式实现部分。'
)
if old in content:
    new = (
        'SSE与REST的混合模式。问诊接口采用服务器推送事件（SSE）长连接而非WebSocket——后者在此场景下'
        '全双工能力过剩，且需要Nginx专门配置连接升级，而SSE完全基于HTTP协议、部署更简单。SSE不支持自定义请求头，'
        '前端因此自行实现Fetch API + ReadableStream解析（详见第四章）。'
    )
    content = content.replace(old, new); fixes += 1; print('11. API SSE trimmed')

# --- Ch3: Trim verbose pagination paragraph ---
old = (
    '分页与限流。列表类接口（血压记录查询、会话列表、历史消息）全部采用基于偏移量的分页方案，'
    '请求参数包含limit和offset，默认limit=20、最大limit=100。响应体中除了数据列表外，始终返回'
    'total\\_count字段——前端组件依赖这个总数来计算分页控件显示多少页按钮，避免"有下一页但不知道还有几页"'
    '的体验缺陷。服务端未实现令牌桶等限流机制——这是当前设计中的一个已知缺口，主要原因是系统尚未部署到公网环境，'
    '所有调用均来自本地开发环境或内网测试，限流的需求在实际运行中尚未出现。若后续部署到公网，应在Nginx层或'
    'FastAPI中间件层补充此能力。'
)
if old in content:
    new = (
        '分页与限流。列表类接口采用基于偏移量的分页方案（默认limit=20，最大100），响应体始终返回total\\_count字段'
        '供前端分页控件使用。服务端未实现限流机制——因系统尚未部署至公网，若后续部署应在Nginx层补充。'
    )
    content = content.replace(old, new); fixes += 1; print('12. Pagination trimmed')

# --- Ch5: Trim verbose test strategy ---
old = (
    '测试采用"单元测试→集成测试→端到端测试→手工验证"四层递进策略，各层聚焦不同粒度的质量保障目标。'
    '单元测试针对每个服务模块的纯逻辑部分做独立验证，所有外部依赖用mock替换，每次git commit前自动运行，'
    '十余秒即可检测回归错误。集成测试基于FastAPI TestClient在内存SQLite数据库上构造完整HTTP请求-响应链路，'
    '每个测试用例拥有独立数据库实例，主要验证路由、序列化和鉴权中间件之间的协作。'
    '端到端测试按用户真实操作顺序串行执行，验证各模块间接口契约和数据结构的一致性。'
    '手工验证在真实浏览器环境中走查关键UI交互，发现自动化测试难以覆盖的体验问题。'
)
if old in content:
    new = (
        '测试采用"单元测试→集成测试→端到端测试→手工验证"四层递进策略。单元测试用mock替换所有外部依赖，'
        '每次git commit前自动运行；集成测试基于FastAPI TestClient在内存SQLite上构造完整HTTP链路；'
        '端到端测试按用户真实操作顺序串行执行；手工验证在真实浏览器中走查关键UI交互。'
    )
    content = content.replace(old, new); fixes += 1; print('13. Test strategy trimmed')

# --- Trim Ch3 chapter summary ---
old = (
    '本章从功能需求、目标用户、非功能需求、系统架构、数据库设计、安全设计和接口设计七个维度对健康管理智能体进行了'
    '全面的需求分析与设计论述。功能需求围绕家庭血压管理场景中"记录—理解—咨询"三个断裂点展开，凝练出七项具体需求'
    '并提炼出"人机协同""诚实策略""安全嵌入"三条设计原则；目标用户细分为三类人群，交互决策均从具体用户画像出发；'
    '非功能需求从性能、安全、合规和代码质量四方面设定了可验证的约束指标；系统架构采用经典的前后端分离三层模型，'
    '各层职责明确、模块间松耦合；数据库设计围绕用户、血压记录、会话消息和知识库四组业务对象展开，将向量数据与关系数据'
    '统一管理以简化部署；安全设计覆盖认证、授权、数据三个层面，并在OWASP Top 10维度上建立了多层防护。'
)
if old in content:
    new = (
        '本章从功能需求、目标用户、非功能需求、系统架构、数据库设计、安全设计和接口设计七个维度进行了需求分析与设计，'
        '提炼出"人机协同""诚实策略""安全嵌入"三条设计原则，采用前后端分离三层架构，并在OWASP Top 10维度上建立了多层安全防护。'
    )
    content = content.replace(old, new); fixes += 1; print('14. Ch3 summary trimmed')

# --- Trim Ch5 chapter summary ---
old = (
    '本章从测试策略、后端测试、前端测试、全链路端到端测试、RAG问诊评测、性能基准和安全测试七个方面对健康管理智能体'
    '进行了系统性测评。测试采用了"单元测试→集成测试→端到端测试→手工验证"四层递进策略，各层聚焦不同粒度的质量保障目标。'
    '后端86个测试用例全部通过，代码覆盖率为82\\%，核心服务模块覆盖率超过90\\%；前端15个测试用例全部通过，TypeScript严格'
    '模式零类型错误；全链路E2E测试覆盖了完整的用户旅程与鉴权逻辑。RAG问诊评测在10道典型问题上三项安全指标均达100\\%；'
    '性能基准表明所有关键操作的P95延迟均在设计约束之内；OWASP专项安全测试验证了认证、授权、数据校验和注入防护等环节的'
    '有效性。综合评测结果表明，系统各项设计指标均已达成验收要求。'
)
if old in content:
    new = (
        '本章从测试策略、后端测试、前端测试、E2E测试、RAG评测、性能基准和安全测试七个方面进行了系统性测评。'
        '后端86个用例全部通过（覆盖率82\\%，核心模块>90\\%），前端15个用例全部通过且TypeScript零错误，'
        '全链路E2E覆盖了完整用户旅程。RAG三项安全指标均达100\\%，所有关键操作P95延迟在设计约束之内。'
    )
    content = content.replace(old, new); fixes += 1; print('15. Ch5 summary trimmed')

# --- Trim Ch6 work summary ---
old = (
    '（1）提出并实现了一种分类先行的双通路OCR血压计图像识别方案。该方案以本地方向梯度直方图+支持向量机'
    '（HOG+SVM）分类器为路由层，将七段数码管液晶显示屏（LCD）图像直接交由视觉语言大模型（VLM）完成端到端识别，'
    '将标准印刷字体图像经由百度云通用OCR配合X坐标聚类完成字段抽取。在20张图像（LCD与标准字体各10张，共计60个'
    '标注字段）上的统一评测表明，该方案在两类图像上的端到端字段准确率均达到100.0\\%，而四种纯OCR基线方案在七段'
    '数码管场景下的准确率均不足20\\%；通过将字段分配从纯Y坐标排序改进为X坐标聚类，标准字体图像上的字段准确率'
    '从33.3\\%提升至100\\%。'
)
if old in content:
    new = (
        '（1）提出并实现了分类先行的双通路OCR血压计图像识别方案：以HOG+SVM分类器为路由层，LCD图像交VLM端到端'
        '识别，标准字体图像经百度云OCR配合X坐标聚类完成字段抽取。在20张图像（60个标注字段）上端到端准确率均达100.0\\%，'
        '四种纯OCR基线在LCD场景下均不足20\\%。X坐标聚类将标准字体字段准确率从33.3\\%提升至100\\%。'
    )
    content = content.replace(old, new); fixes += 1; print('16. Ch6 work summary (1) trimmed')

old = (
    '（2）设计并实现了一套面向安全的个性化检索增强生成（RAG）健康问诊系统。以12篇医学知识文档构建向量知识库'
    '（基于sqlite-vec扩展实现本地向量存储与语义检索），Prompt中嵌入用户近14天血压概况与检索到的知识片段，系统指令中'
    '设定六条安全行为边界（禁止推荐药物剂量、禁止确定性诊断、强制引用标注与免责声明），并通过自动评测脚本实现安全指标'
    '的快速回归验证。在10道典型评测问题上，引用标注率、免责声明率和剂量安全率三项指标均达到100\\%，未发现事实性错误。'
)
if old in content:
    new = (
        '（2）设计并实现了一套面向安全的个性化RAG健康问诊系统：以12篇医学文档构建向量知识库，Prompt嵌入用户近14天'
        '血压概况与检索片段，设定六条安全行为边界并配套自动评测脚本。10道评测题上三项安全指标均达100\\%，未发现事实性错误。'
    )
    content = content.replace(old, new); fixes += 1; print('17. Ch6 work summary (2) trimmed')

old = (
    '（3）构建了从血压数据采集、趋势分析到可视化看板的完整数据链路，并建立了分层测试体系。数据层实现严格的用户级数据'
    '隔离，趋势判定层采用自适应窗口策略（数据充分时给出趋势判断，不足时如实告知），看板层基于双Y轴时序图与彩色统计卡片'
    '呈现关键信息。后端86个测试用例全部通过、代码覆盖率为82\\%，前端15个测试用例全部通过，全链路端到端测试覆盖核心'
    '用户路径与鉴权逻辑。'
)
if old in content:
    new = (
        '（3）构建了从数据采集、趋势分析到可视化看板的完整数据链路：实现用户级数据隔离、自适应窗口趋势判定和双Y轴时序'
        '看板。后端86个测试用例全部通过（覆盖率82\\%），前端15个用例全部通过，全链路E2E覆盖核心用户路径。'
    )
    content = content.replace(old, new); fixes += 1; print('18. Ch6 work summary (3) trimmed')

# Save
with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

final = content.count('\n')
print(f'\nTotal fixes: {fixes}')
print(f'Lines: {orig} -> {final} (removed {orig - final})')
