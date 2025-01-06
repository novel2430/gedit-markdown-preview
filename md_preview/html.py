import os
import json

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path) + "/deps"
font_directory = os.path.dirname(current_file_path) + "/fonts"
noto_sans = "{}/NotoSans.ttf".format(font_directory)
noto_sans_sc = "{}/NotoSansSC.ttf".format(font_directory)
noto_sans_tc = "{}/NotoSansTC.ttf".format(font_directory)

start_page = json.dumps("""
# Markdown Preview!
- ☕ Open a markdown file ...
- 🍺 Wish u have a good day!
- 🚀 Repo : https://github.com/novel2430/gedit-markdown-preview
- 👋 Author : Novel2430
""")

font_faces = f"""
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

html_style = f"""
<style>
    {font_faces}
    body {{
      font-family: "Noto Sans TC","Noto Sans SC","Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji";
      margin: 0px;
      transition: background-color 0.3s, color 0.3s;
    }}
    .dark-mode {{
      background-color: #1e1e1e;
    }}
    .preview.markdown-body {{
      font-family: "Noto Sans TC","Noto Sans SC","Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji";
    }}
    .preview {{
      padding: 20px;
      background-color: white;
      color: black;
      transition: background-color 0.3s, color 0.3s, border-color 0.3s;
    }}
    .preview.dark-mode {{
      background-color: #1e1e1e;
      color: #c9d1d9;
      border-color: #444;
    }}
    .preview.dark-mode pre {{
      background-color: #2d2d2d;
      border-color: #555;
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
            
          return `<pre><code class="hljs ${{lang}}">${{final}}</code></pre>`;
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
        window.toggleDark = function () {{
          const isDarkMode = preview.classList.toggle('dark-mode');
          document.body.classList.toggle('dark-mode');
          if (isDarkMode) {{
            hljsStyle.href = 'file://{current_directory}/github-dark.min.css';
            themeStylesheet.href = "file://{current_directory}/github-markdown-dark.css";
          }} else {{
            hljsStyle.href = 'file://{current_directory}/github.min.css';
            themeStylesheet.href = "file://{current_directory}/github-markdown-light.css";
          }}
        }};

        window.renderMarkdown({start_page});

  </script>
</body>

"""

html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Markdown Preview</title>
    <link id="theme-stylesheet" rel="stylesheet" href="file://{current_directory}/github-markdown-light.css">
</head>
{html_style}
{html_body}
</html>
"""
