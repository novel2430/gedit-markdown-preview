// 从 npm 包中导入样式

export function toggleTheme(isDarkMode) {
  const hljsLink = document.getElementById('hljs-style');
  const markdownLink = document.getElementById('theme-stylesheet');

  if (!hljsLink || !markdownLink) {
    console.error('Required <link> elements are missing!');
    return;
  }

  if (isDarkMode) {
    console.log(isDarkMode)
    hljsLink.href = "/github-dark.min.css";
    markdownLink.href = "/github-markdown-dark.css";
  } else {
    console.log(isDarkMode)
    hljsLink.href = "/github.min.css";
    markdownLink.href = "/github-markdown-light.css";
  }
}

