import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';
import { toggleTheme } from './themeManager.js';

// 初始化 Markdown-it 并配置代码高亮
const md = new MarkdownIt({
  highlight: (str, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value;
      } catch (__) {}
    }
    return ''; // 默认转义
  },
});

// 示例 Markdown 内容
const markdownContent = `
# Hello Markdown and Code Highlighting!

Here is a **Markdown** example with syntax highlighting:

\`\`\`javascript
console.log('Hello, world!');
\`\`\`
`;

// 渲染 Markdown 并插入到页面
const htmlContent = md.render(markdownContent);
document.getElementById('app').innerHTML = htmlContent;
const preview = document.getElementById('app');

// 默认加载浅色模式
toggleTheme(false);

// 切换主题按钮逻辑
document.getElementById('toggle-theme').addEventListener('click', () => {
  const isDarkMode = document.body.classList.toggle('dark-mode');
  preview.classList.toggle('dark-mode');
  toggleTheme(isDarkMode);
});

