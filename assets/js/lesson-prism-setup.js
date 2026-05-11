/**
 * Garante que todo <pre><code> da aula tenha linguagem Prism antes do highlight:
 * Prism.highlightAll só enxerga code[class*="language-"].
 */
(function () {
  function inferLanguageClass(codeEl) {
    const rawFull = codeEl.textContent || "";
    const raw = rawFull.trim();
    if (!raw) return "language-javascript";

    const head = raw.slice(0, 500);
    const firstLine = raw.split(/\r?\n/)[0].trim();

    // JS / JSX (prioridade — trechos típicos da apostila)
    if (
      /\b(?:const|let|var|function|class|extends|implements|await|async|import\s|export\s)\b/.test(
        head,
      ) ||
      /=&gt;/.test(head) ||
      /['"]use (?:strict|client)['"]/.test(head) ||
      /\b(?:console|document|window|navigator|fetch|alert|prompt|confirm|debugger)\s*[.(]/.test(
        head,
      ) ||
      /\bdocument\s*\.\s*\w+/m.test(head) ||
      /\b(?:localStorage|sessionStorage)\b/.test(head) ||
      /\bJSON\.(?:parse|stringify)/.test(head)
    ) {
      return "language-javascript";
    }

    // HTML escapado (&lt;div…) — sempre markup (aula em HTML textual)
    if (/^&lt;/.test(raw) || /^&lt;!DOCTYPE\b/i.test(raw)) {
      return "language-markup";
    }
    // Marcação literal: JSX (className / { dentro de tags) ou HTML puro
    if (/^<[a-z!/?]/i.test(raw)) {
      const slice = raw.slice(0, 800);
      if (
        /\bclassName\s*=/.test(slice) ||
        />\s*\{/.test(slice) ||
        /\{[^{}]{0,200}\}/.test(slice)
      )
        return "language-jsx";
      return "language-markup";
    }

    // Shell (shebang, comentários #, comandos habituais)
    if (/^#!\//.test(firstLine)) return "language-bash";
    if (
      /^#/.test(firstLine) &&
      !/\b(?:const|let|function|class|interface|type)\b/.test(firstLine.slice(1, 120))
    ) {
      return "language-bash";
    }
    if (/\n#\s+[A-Za-zÀ-ú0-9]/.test(raw)) return "language-bash";
    if (
      /^(sudo|curl|wget|scp|ssh|kubectl|yarn|pnpm|docker)\s/im.test(head) ||
      /^(npm|npx|git|cd|mkdir|rm|rmdir|chmod|chown|export|source|brew|apt|dnf|pacman)\s/im.test(head)
    )
      return "language-bash";
    if (/^export\s+\w+=/im.test(head) || /^source\s+/im.test(head)) {
      return "language-bash";
    }

    // CSS
    if (
      /^@\w+/m.test(firstLine) &&
      /@(?:media|import|keyframes|font-face|supports|charset|layer)\b/i.test(firstLine)
    ) {
      return "language-css";
    }
    if (
      /^[#.:*\[\]?@][^;{]{0,80}\{/.test(firstLine) ||
      /^[a-z*][.\w*-]*(?:\([^)]*\))?\s*\{/i.test(firstLine)
    )
      return "language-css";

    // JSON (chaves com aspas duplas)
    if (/^\s*[{[]/.test(raw) && /"[^"\n]+"\s*:\s*/.test(head)) {
      if (!/\bfunction\b/.test(head)) return "language-json";
    }

    return "language-javascript";
  }

  function syncPreLanguage(pre, langFull) {
    if (!pre || pre.tagName !== "PRE" || !langFull) return;
    const slug = /^language-([\w-]+)$/i.exec(langFull);
    if (!slug) return;
    [...pre.classList]
      .filter((c) => /^language-/i.test(c))
      .forEach((c) => pre.classList.remove(c));
    pre.classList.add("language-" + slug[1]);
  }

  window.normalizeLessonSyntax = function normalizeLessonSyntax(rootEl) {
    if (!rootEl) return;

    rootEl.querySelectorAll("pre > code").forEach((code) => {
      const langs = [...code.classList].filter((c) => /^language-/i.test(c));
      const discardPlain = langs.some((c) =>
        /^language-(plaintext|text)$/i.test(c),
      );

      if (langs.length === 0 || discardPlain) {
        langs.forEach((c) => code.classList.remove(c));
        code.classList.add(inferLanguageClass(code));
      }

      let finalLang = [...code.classList].find((c) => /^language-/i.test(c));
      if (!finalLang) {
        finalLang = inferLanguageClass(code);
        code.classList.add(finalLang);
      }

      syncPreLanguage(code.parentElement, finalLang);
    });
  };
})();
