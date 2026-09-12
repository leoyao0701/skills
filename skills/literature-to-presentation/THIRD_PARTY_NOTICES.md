# 第三方依赖与来源说明

本目录中的工作流、页面组件、脚本和虚构示例由本项目编写，以随附 MIT 许可证发布。实现沿用原报告中“同一内容数据生成多种交付物”和“先判断关系再选组件”的方法；原报告的专用环境路径、书籍原文、历史图片、字体文件及专有软件没有纳入。

下表是可选外部依赖，不是随本项目分发的软件副本。本项目的 MIT 许可证不改变它们及其传递依赖的许可证。安装或再分发完整环境时，应以所用版本附带的许可、声明与二进制组件为准。

| 外部项目 | 用途 | 许可及官方来源 |
|---|---|---|
| python-pptx | 可编辑 PPTX 导出与重新读取 | [MIT](https://github.com/scanny/python-pptx/blob/master/LICENSE) |
| pypdf | PDF 原生文本提取 | [BSD-3-Clause](https://github.com/py-pdf/pypdf/blob/main/LICENSE) |
| pypdfium2 | OCR 前的 PDF 页图渲染 | [Apache-2.0 / BSD-3-Clause 等分项说明](https://pypdfium2.readthedocs.io/en/stable/readme.html#licensing)；PDFium 及其构建依赖另有许可，分发二进制时需保留完整声明 |
| Pillow | 保存 PDF 页图 | [许可说明](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |
| Tesseract | 可选 OCR 命令行程序，需另装语言数据 | [Apache-2.0](https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE)；语言数据及其他组件按各自版本许可处理 |
| Playwright Python | 可选 HTML 浏览器检查 | [Apache-2.0](https://github.com/microsoft/playwright-python/blob/main/LICENSE)；所用浏览器另有许可，本包不包含浏览器 |

`@oai/artifact-tool`、系统 presentations skill 及其辅助程序没有被复制、修改或打包进本项目。本次 PPTX 导出器使用 python-pptx 公开接口重新实现。提及原工具只说明制作历史，不代表获得再分发授权，也不代表相关机构为本项目背书。

HTML 样式只列字体名称，不附带字体文件。模型生成的真实报告、用户研究材料和用户后来添加的素材，其权利范围不由本许可证自动覆盖。
