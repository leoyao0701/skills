# 可选的文件生成与检查工具

只在需要实际生成文件且当前环境可执行代码时读取。不能执行脚本的模型仍按其他参考规则完成研究、正文与源码输出。脚本属于辅助实现，不代替原文核查或学术判断。

## 最短可运行示例

以下命令从技能目录 `literature-to-presentation/` 中运行，使用 Python 3.9+。HTML、讲稿和来源记录仅使用 Python 标准库。

```sh
python3 scripts/build_presentation.py examples/demo.json --out demo-output
```

得到 `index.html`、`notes.html`（原文在左、讲稿在右）、`notes.md`、`sources.json` 和 `checks.json`。从浏览器打开 `index.html`，可翻页、按稳定 ID 定位、连续阅读或跳转讲稿。不要把示例的虚构材料当作真实文献。

需要 PPTX 时，先安装可选依赖，再增加 `--pptx`：

```sh
python3 -m pip install -r scripts/requirements-pptx.txt
python3 scripts/build_presentation.py examples/demo.json --out demo-output --pptx
```

得到可编辑的文本框和原生表格，讲稿与来源写入备注。可用 `--font "已安装的字体名称"` 指定字体；不随包提供字体。默认字体名称为 Noto Sans CJK SC，实际显示取决于本机安装情况。

## 内容数据约定

参考 `examples/demo.json`，不要另外维护相互矛盾的 HTML/PPTX 文本。

- 顶层：`title`、可选 `language`、`sources` 列表、非空 `slides` 列表。
- 来源：唯一 `id`、`citation`、`locator`、`scope`、已核对的 `quote`。工具不会替你核实这些字段。
- 页面：唯一 `id`（英文字母开头，之后可用字母、数字、下划线、连字符）、`title`、`layout`、`body`、`sources`（来源 ID 列表）、`notes`（详细讲稿）。文本字段使用字符串。
- 可选 `quote_source`：必须属于本页 `sources`，且该来源有非空 `quote`；在页内展示对应来源的引文。
- `text` 为正文/引文；`parallel`、`comparison` 为平级栏；`timeline` 为带时间标签的行；`argument` 为分层说明区。后四种使用 `items: [{"title":"...","text":"..."}]`。
- `matrix` 使用 `matrix: {"columns":[...], "rows":[[...], ...]}`，列名和单元格均用字符串，每一行长度与列数相同；PPTX 中是真实表格。
- 除 `text` 外填写 `relation`，用面向听众的句子说明关系。工具只检查该字段存在，不判断因果或分类是否成立。

六种版式是可修改的基础组件。内容较多时应拆页或调整组件；不通过删去限定、压缩历史事实或任意缩小字号强行适配。此初版不包含图片编排、图表生成或任意 HTML 到 PPTX 的自动转换。

## PDF 与 OCR

以下固定版本的 PDF 依赖要求 Python 3.10+（其中 Pillow 的版本要求）。仅生成 HTML 不需要这些依赖。

```sh
python3 -m pip install -r scripts/requirements-pdf.txt
python3 scripts/extract_pdf.py book.pdf --out extracted.json
```

输出逐页文本、从 1 开始的 PDF 页号和 `not_verified` 状态；印刷页码留空待核对，不假定固定偏移量。扫描件可另装 Tesseract 及所需语言数据，再使用 `--ocr-pages 1,3-5 --language chi_sim+eng`。OCR 页图保存在输出旁边，供回看原页。程序不会自动安装系统软件或下载语言数据。

## 检查范围

- `build_presentation.py` 检查结构、字段类型、来源 ID、矩阵列数与密度提示；PPTX 按换行和字符宽度估算空间，过密时提示拆页，导出后重新读取并检查形状边界与备注一致性。空间估算不等于实际字体排版检查。导出失败时以 `checks.json` 和退出状态为准，不把目录中的旧 PPTX 当作本轮成品。
- 需要浏览器检查时安装 `scripts/requirements-check.txt`，并运行 `python3 -m playwright install chromium`；已有兼容浏览器也可通过 `--browser-executable` 指定。

```sh
python3 scripts/check_render.py demo-output/index.html --out render-check
```

浏览器检查保存逐页截图、溢出与脚本错误记录。自动检查不能覆盖所有重叠、阅读体验、PowerPoint 字体替换或来源真实性；最终文件仍需人工阅读和视觉检查。HTML 的结果不能证明 PPTX 的排版已经验证。

依赖许可见技能目录中的 `THIRD_PARTY_NOTICES.md`；脚本和组件适用随附 `LICENSE`。不要从本机系统目录补拷专有软件来让工具运行。

## 工具回归测试

```sh
python3 -m unittest discover -s tests -v
```

标准库测试覆盖输入类型、引用关系、HTML 转义与讲稿同步；安装相应依赖后会增加 PDF 和 PPTX 测试。浏览器用例默认跳过，安装 Playwright 后可通过环境变量 `LTP_BROWSER_EXECUTABLE` 指向已有兼容浏览器再运行。跳过的测试不是通过；回归测试不证明学术结论正确。
