/**
 * Páginas com grade de vídeos a partir de JSON (playlist / uploads).
 * Marque o <article> com data-youtube-playlist-grid-page e use os data-* internos.
 *
 * Modo curso linear: data-yt-linear-lessons + data-yt-show-lesson-index + bloco [data-yt-seq-nav].
 */
(function () {
  var EMBED_BASE = "https://www.youtube-nocookie.com/embed/";

  function setLoading(grid, loading) {
    if (!grid) return;
    if (loading) {
      grid.innerHTML =
        '<p class="yt-video-grid__loading" role="status"><i class="fas fa-spinner fa-spin" aria-hidden="true"></i> Carregando lista de vídeos…</p>';
      return;
    }
    var hint = grid.querySelector(".yt-video-grid__loading");
    if (hint) hint.remove();
  }

  function formatIsoDatePt(iso) {
    if (!iso || typeof iso !== "string") return "";
    try {
      var d = new Date(iso);
      if (Number.isNaN(d.getTime())) return "";
      return d.toLocaleString("pt-BR", {
        dateStyle: "short",
        timeStyle: "short",
      });
    } catch (_) {
      return "";
    }
  }

  function selectVideo(iframe, cards, videoId) {
    if (!iframe || !videoId) return;
    iframe.src = EMBED_BASE + videoId + "?rel=0";
    cards.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.dataset.videoId === videoId);
    });
    try {
      iframe.focus({ preventScroll: true });
    } catch (_) {}
  }

  function buildCard(video, index, opts) {
    opts = opts || {};
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className =
      "yt-video-card" + (opts.showLessonIndex ? " yt-video-card--numbered" : "");
    btn.dataset.videoId = video.videoId;
    btn.setAttribute(
      "aria-label",
      (opts.showLessonIndex ? "Aula " + (index + 1) + ": " : "Reproduzir: ") +
        video.title,
    );

    var thumbWrap = document.createElement("span");
    thumbWrap.className = "yt-video-card__thumb-wrap";

    if (opts.showLessonIndex) {
      var badge = document.createElement("span");
      badge.className = "yt-video-card__lesson-index";
      badge.textContent = String(index + 1);
      thumbWrap.appendChild(badge);
    }

    var img = document.createElement("img");
    img.src = video.thumbnail;
    img.alt = "";
    img.width = 480;
    img.height = 360;
    img.loading = "lazy";
    img.decoding = "async";

    thumbWrap.appendChild(img);

    var title = document.createElement("span");
    title.className = "yt-video-card__title";
    title.textContent = video.title;

    btn.appendChild(thumbWrap);
    btn.appendChild(title);
    return btn;
  }

  function initYoutubePlaylistGridRoot(root) {
    var iframe = root.querySelector("[data-yt-grid-iframe]");
    var grid = root.querySelector("[data-yt-grid-root]");
    var metaEl = root.querySelector("[data-yt-grid-meta]");
    var filterInput = root.querySelector("[data-yt-grid-filter]");
    var seqNav = root.querySelector("[data-yt-seq-nav]");
    var seqPrev = seqNav ? seqNav.querySelector("[data-yt-prev]") : null;
    var seqNext = seqNav ? seqNav.querySelector("[data-yt-next]") : null;
    var seqLabel = seqNav ? seqNav.querySelector("[data-yt-seq-label]") : null;

    var jsonUrl =
      root.getAttribute("data-videos-src") || "assets/data/devfast-channel-videos.json";
    var linear = root.hasAttribute("data-yt-linear-lessons");
    var showLessonIndex = root.hasAttribute("data-yt-show-lesson-index");

    var emptyMsg =
      root.getAttribute("data-yt-empty-hint") ||
      "Nenhum vídeo encontrado no arquivo de dados. Rode o script de sincronização na raiz do projeto.";

    if (!iframe || !grid) return Promise.resolve();

    setLoading(grid, true);

    var videosRef = [];
    var currentIndex = 0;

    function updateSeqNav() {
      if (!seqNav || !linear) return;
      seqNav.hidden = videosRef.length === 0;
      if (seqPrev) seqPrev.disabled = currentIndex <= 0;
      if (seqNext) seqNext.disabled = currentIndex >= videosRef.length - 1;
      if (seqLabel && videosRef.length) {
        seqLabel.textContent =
          "Aula " + (currentIndex + 1) + " de " + videosRef.length;
      }
    }

    function selectByIndex(i, cards, iframeEl) {
      if (i < 0 || i >= videosRef.length) return;
      currentIndex = i;
      selectVideo(iframeEl, cards, videosRef[i].videoId);
      updateSeqNav();
    }

    return fetch(jsonUrl)
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then(function (data) {
        var videos = data.videos || [];
        videosRef = videos;
        setLoading(grid, false);
        grid.innerHTML = "";

        if (metaEl) {
          var parts = [];
          if (data.title) parts.push(data.title);
          if (data.videoCount != null) {
            var unit = linear ? "aulas" : "vídeos";
            parts.push(String(data.videoCount) + " " + unit + " na lista");
          }
          var gen = formatIsoDatePt(data.generatedAt);
          if (gen) parts.push("lista atualizada em " + gen);
          if (data.note) parts.push(data.note);
          metaEl.textContent = parts.join(" · ");
        }

        if (!videos.length) {
          grid.innerHTML =
            '<p class="yt-video-grid__empty">' + emptyMsg + "</p>";
          return;
        }

        var frag = document.createDocumentFragment();
        var cards = [];
        videos.forEach(function (v, i) {
          var card = buildCard(v, i, { showLessonIndex: showLessonIndex });
          cards.push(card);
          frag.appendChild(card);
        });
        grid.appendChild(frag);

        cards.forEach(function (card, i) {
          card.addEventListener("click", function () {
            selectByIndex(i, cards, iframe);
          });
        });

        if (linear && seqPrev) {
          seqPrev.addEventListener("click", function () {
            selectByIndex(currentIndex - 1, cards, iframe);
          });
        }
        if (linear && seqNext) {
          seqNext.addEventListener("click", function () {
            selectByIndex(currentIndex + 1, cards, iframe);
          });
        }

        selectByIndex(0, cards, iframe);

        if (filterInput) {
          filterInput.addEventListener("input", function () {
            var q = (filterInput.value || "").trim().toLowerCase();
            cards.forEach(function (card, i) {
              var t = (videos[i] && videos[i].title) || "";
              var match = !q || t.toLowerCase().indexOf(q) !== -1;
              card.hidden = !match;
            });
          });
        }
      })
      .catch(function () {
        setLoading(grid, false);
        grid.innerHTML =
          '<p class="yt-video-grid__error">Não foi possível carregar a lista de vídeos. Confira o arquivo JSON em <code>assets/data/</code> e se você está abrindo a apostila via servidor HTTP (não <code>file://</code>).</p>';
      });
  }

  function setupYoutubePlaylistGridPages(container) {
    var roots = container.querySelectorAll("[data-youtube-playlist-grid-page]");
    if (!roots.length) return Promise.resolve();
    var tasks = [];
    roots.forEach(function (root) {
      tasks.push(initYoutubePlaylistGridRoot(root));
    });
    return Promise.all(tasks);
  }

  window.setupYoutubePlaylistGridPages = setupYoutubePlaylistGridPages;
  window.setupDevfastCanalPage = setupYoutubePlaylistGridPages;
})();
