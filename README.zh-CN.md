# skills

[English](./README.md)

一个用于集中管理 Codex skills 的小型仓库。每个 skill 独立放在自己的目录中，便于安装、维护和后续扩展。

这个仓库的目标不是做成大而全的平台，而是沉淀一组真正可复用、可检查、可持续维护的实用 skill。

## 特性

- 一个仓库管理多个 skill
- 每个 skill 一个目录，结构清晰
- 需要稳定行为时可配套脚本
- 偏向真实工作流，而不是堆砌复杂框架

## 当前包含

- `web-fetcher`：把 URL 抓取为可读的 markdown 或文本，供后续总结、抽取、分析使用

## 仓库结构

```text
skills/
├── README.md
├── README.zh-CN.md
├── CONTRIBUTING.md
└── web-fetcher/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── scripts/
        └── fetch.py
```

每个 skill 通常包含：

- `SKILL.md`：skill 的定义和工作说明
- `agents/openai.yaml`：展示名称、默认提示词等元信息
- `scripts/`、`references/`、`assets/`：按需提供脚本、参考资料和资源文件

## `web-fetcher`

`web-fetcher` 适合用于“先把网页变成可读文本，再做后续处理”的场景。

典型使用场景：

- 文章页面
- 文档页面
- 博客页面
- X 状态页
- 需要先转成 markdown 或纯文本再分析的页面

它的行为特点：

- 按顺序尝试多种抓取策略
- 优先使用 markdown 友好的镜像
- 拒绝明显的错误页和登录墙
- HTTP 4xx / 5xx 直接视为失败
- 最后一层才回退到原始 HTML，并尽量提取成可读文本

当前回退顺序：

1. `r.jina.ai`
2. `defuddle.md`
3. `markdown.new`
4. 原始 HTML 转文本

## 安装

如果你的 Codex 环境支持从 GitHub 仓库路径安装，可以使用：

仓库：

```text
huanghuiqiang/skills
```

skill 路径：

```text
web-fetcher
```

也就是说，安装时指向这个仓库中的 `web-fetcher` 目录即可。

## 本地运行

直接输出到终端：

```bash
python3 web-fetcher/scripts/fetch.py https://example.com/article
```

保存到文件：

```bash
python3 web-fetcher/scripts/fetch.py https://example.com/article -o output.md
```

如果 URL 没写协议，脚本会自动补成 `https://`：

```bash
python3 web-fetcher/scripts/fetch.py example.com/article
```

## 成功与失败判定

成功的基本条件：

- 返回内容不能过短
- 不能只有元数据而没有正文
- 不能明显像登录墙或通用错误页

脚本会尽量把失败区分为：

- 镜像不可用
- 返回的是登录页或错误页
- 当前页面类型不受支持
- 没提取到足够可信的可读内容

## 已知限制

- 各镜像服务的可用性可能随时间变化
- 有些站点会主动拦截自动抓取
- `x.com/i/article/...` 这类页面目前仍然不稳定
- 原始 HTML 的回退提取是 best-effort，不是完整的 readability 引擎
- 这个仓库暂时没有覆盖镜像行为的自动化测试

## 贡献建议

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

简要原则：

- 一个 skill 只解决一个边界清晰的问题
- `SKILL.md` 保持精炼
- 复杂逻辑放进脚本或 references
- 不要在 skill 目录里堆无关文档

## License

目前仓库还没有添加许可证文件。若你准备对外开源并允许他人复用，建议明确补上 `LICENSE`。

## 状态

这个仓库会刻意保持小而清晰，重点是让每个 skill 都足够直接、可检查、可维护。
