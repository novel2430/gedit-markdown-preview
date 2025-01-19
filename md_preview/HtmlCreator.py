import os
import json

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path) + "/deps"
font_directory = os.path.dirname(current_file_path) + "/fonts"
noto_sans = "{}/NotoSans.ttf".format(font_directory)
noto_sans_sc = "{}/NotoSansSC.ttf".format(font_directory)
noto_sans_tc = "{}/NotoSansTC.ttf".format(font_directory)

class HtmlCreator:
    def __init__(self) -> None:
        self.start_page = json.dumps("""
            # Markdown Preview!
            - ☕ Open a markdown file ...
            - 🍺 Wish u have a good day!
            - 🚀 Repo : https://github.com/novel2430/gedit-markdown-preview
            - 👋 Author : Novel2430
            """)
        self.font_faces = f"""
            @font-face {{
              font-family: 'Noto Sans';
              src: url('{noto_sans}') format('truetype');
              font-weight: normal;
              font-style: normal;
            }}
            @font-face {{
              font-family: 'Noto Sans SC';
              src: url('{noto_sans_sc}') format('truetype');
              font-weight: normal;
              font-style: normal;
            }}
            @font-face {{
              font-family: 'Noto Sans TC';
              src: url('{noto_sans_tc}') format('truetype');
              font-weight: normal;
              font-style: normal;
            }}
        """
        self.html_style = f"""
        <style>
            {self.font_faces}
            body {{
              font-family: "Noto Sans TC","Noto Sans SC","Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji";
              margin: 0px;
              transition: background-color 0.3s, color 0.3s;
            }}
            .preview.markdown-body {{
              font-family: "Noto Sans TC","Noto Sans SC","Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji";
            }}
            .preview {{
              padding: 20px;
              transition: background-color 0.3s, color 0.3s, border-color 0.3s;
            }}
            .preview pre {{
              padding: 10px;
              overflow: auto;
              border: 1px solid #ccc;
              border-radius: 5px;
              margin: 10px 0;
              position: relative;
            }}
            .copy-btn {{
              position: absolute;
              top: 10px;
              right: 10px;
              background: #8c8c8c;
              color: white;
              border: none;
              padding: 5px 10px;
              border-radius: 3px;
              cursor: pointer;
              font-size: 12px;
            }}
            .copy-btn:hover {{
              background: #585859;
            }}
        </style>
        """

    def build_html(self, font_path=None, css_path=None, font_type=None, is_dark=True):
        # Font
        set_font_code = ""
        if font_type and font_type:
            set_font_code = f"""
                window.updateFont({font_path}, {font_type})
            """
        # CSS
        set_css_code = ""
        if css_path:
            set_css_code = f"""
                window.updateCSS({css_path})
            """
        # Dark
        set_dark_code = ""
        if is_dark == True:
            set_dark_code = f"""
                window.setDarkMode(true)
            """
        html_body = f"""
        <body>
            <div id="preview" class="preview markdown-body"></div>
            <script src="file://{current_directory}/markdown-it.min.js"></script>
            <script src="file://{current_directory}/highlight.min.js"></script>

            <script>
                const md = window.markdownit({{
                  html:         true,
                }});
                md.core.ruler.after('block', 'add_line_numbers', (state) => {{
                  state.tokens.forEach((token) => {{
                    if (token.map) {{
                      const [startLine, endLine] = token.map;
                      token.attrSet('data-line-start', startLine);
                      token.attrSet('data-line-end', endLine);
                      }}
                    }});
                }});
                md.renderer.rules.fence = (tokens, idx, options, env, self) => {{
                  const token = tokens[idx];
                  const lang = token.info ? token.info.trim() : '';
                  const highlighted = lang && hljs.getLanguage(lang)
                    ? hljs.highlight(token.content, {{ language: lang }}).value
                    : md.utils.escapeHtml(token.content);

                  const lineStart = token.map ? token.map[0] : 0;
                  const codeLines = highlighted.split('\\n');

                  const final = codeLines
                    .map((line, i) => {{
                      if (i < codeLines.length - 1) {{
                        const currentLine = lineStart + i + 1;
                        return `<span data-line-start="${{currentLine}}" data-line-end="${{currentLine+1}}">${{line}}</span>`;
                      }}
                      else {{
                        return '';
                      }}
                    }})
                    .join('\\n');
                    
                  return `<pre><code class="hljs">${{final}}</code></pre>`;
                }};
                md.renderer.rules.html_block = (tokens, idx) => {{
                    const token = tokens[idx];
                    const lineStart = token.attrGet('data-line-start') || '';
                    const lineEnd = token.attrGet('data-line-end') || '';
                    return `<div data-line-start="${{lineStart}}" data-line-end="${{lineEnd}}">${{token.content}}</div>`;
                }};


                const preview = document.getElementById('preview');
                const hljsStyle = document.getElementById('hljs-style');
                const themeStylesheet = document.getElementById('theme-stylesheet');
                let lightCss = "file://{current_directory}/github-markdown-light.css";
                let darkCss = "file://{current_directory}/github-markdown-dark.css";
                let isDefault = true;

                window.renderCopyBtn = function() {{
                  const codeBlocks = preview.querySelectorAll('pre');

                  codeBlocks.forEach((block) => {{
                    const container = document.createElement('div');
                    container.classList.add('code-block');

                    const copyBtn = document.createElement('button');
                    copyBtn.classList.add('copy-btn');
                    copyBtn.textContent = 'Copy';

                    copyBtn.addEventListener('click', () => {{
                      const code = block.querySelector('code');
                      if (code) {{
                        navigator.clipboard.writeText(code.textContent).then(() => {{
                          copyBtn.textContent = 'Copied!';
                          setTimeout(() => (copyBtn.textContent = 'Copy'), 2000);
                        }});
                      }}
                    }});

                    block.style.position = "relative";
                    block.appendChild(copyBtn);
                  }});
                }};

                window.renderMarkdown = function (markdown) {{
                  const html = md.render(markdown);
                  console.log(md.parse(markdown))
                  preview.innerHTML = html;
                }};
                window.updateContent = function (markdown) {{
                    window.renderMarkdown(markdown);
                    window.renderCopyBtn();
                }};
                window.setDarkMode = function (isDarkMode) {{
                  if (isDarkMode) {{
                    hljsStyle.href = 'file://{current_directory}/github-dark.min.css';
                    if (isDefault) {{
                        themeStylesheet.href = "file://{current_directory}/github-markdown-dark.css";
                    }}
                    preview.classList.add('dark-mode');
                    document.body.classList.add('dark-mode');
                  }} else {{
                    hljsStyle.href = 'file://{current_directory}/github.min.css';
                    if (isDefault) {{
                        themeStylesheet.href = "file://{current_directory}/github-markdown-light.css";
                    }}
                    preview.classList.remove('dark-mode');
                    document.body.classList.remove('dark-mode');
                  }}
                }};

                window.synCursor = function (line_number) {{
                    const lineNumber = line_number;

                    const targetElements = Array.from(document.querySelectorAll('[data-line-start]'))
                    .filter(el => {{
                        const start = Number(el.getAttribute('data-line-start'));
                        const end = Number(el.getAttribute('data-line-end') || start);
                        return lineNumber >= start && lineNumber < end;
                    }});
                    const targetElement = targetElements.pop();

                    if (targetElement) {{
                        console.log(targetElement)
                        targetElement.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    }}
                }};

                window.enableMineStyles = function (enable) {{
                    const link = document.getElementById("basic-theme-stylesheet");
                    link.disabled = !enable;
                }};


                window.updateCSS = function (path) {{
                    isDefault = false;
                    themeStylesheet.href = path;
                    window.enableMineStyles(false)
                }};

                window.setCSSDefault = function () {{
                    isDefault = true;
                    if (preview.classList.contains('dark-mode')) {{
                        themeStylesheet.href = "file://{current_directory}/github-markdown-dark.css";
                    }} else {{
                        themeStylesheet.href = "file://{current_directory}/github-markdown-light.css";
                    }}
                    window.enableMineStyles(true)
                }};

                window.updateFont = function (path, type) {{
                    const style = document.createElement('style');
                    style.type = 'text/css';
                    style.textContent = `
                        @font-face {{
                          font-family: 'Custom Font';
                          src: url("${{path}}") format("${{type}}");
                          font-weight: normal;
                          font-style: normal;
                        }}
                        body {{
                          font-family: "Custom Font","Noto Sans TC","Noto Sans SC","Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji";
                        }}
                        .preview.markdown-body {{
                          font-family: "Custom Font","Noto Sans TC","Noto Sans SC","Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji";
                        }}
                    `;
                    document.head.appendChild(style);
                }};

                window.setFontDefault = function () {{
                    const style = document.createElement('style');
                    style.type = 'text/css';
                    style.textContent = `
                        body {{
                          font-family: "Noto Sans TC","Noto Sans SC","Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji";
                        }}
                        .preview.markdown-body {{
                          font-family: "Noto Sans TC","Noto Sans SC","Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji";
                        }}
                    `;
                    document.head.appendChild(style);
                }};

                {set_font_code}
                {set_css_code}
                {set_dark_code}

                window.renderMarkdown({start_page});
          </script>
        </body>
        """
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Markdown Preview</title>
                <link id="theme-stylesheet" rel="stylesheet" href="file://{current_directory}/github-markdown-light.css">
                <link id="basic-theme-stylesheet" rel="stylesheet" href="file://{current_directory}/basic.css">
                <link rel="stylesheet" href="file://{current_directory}/github.min.css" id="hljs-style">
            </head>
            {self.html_style}
            {html_body}
            </html>
        """
