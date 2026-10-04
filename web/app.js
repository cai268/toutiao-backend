const API_BASE = window.location.protocol === "file:" ? "http://127.0.0.1:8000" : "";
const REQUEST_TIMEOUT_MS = 60_000;

const FALLBACK_IMAGE = "https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&fit=crop&w=900&q=82";

const DEMO_CATEGORIES = [
  { id: 1, name: "热点" },
  { id: 2, name: "科技" },
  { id: 3, name: "财经" },
  { id: 4, name: "体育" },
  { id: 5, name: "文化" },
];

const DEMO_NEWS = [
  {
    id: 1001,
    category_id: 2,
    category_name: "科技",
    title: "端侧大模型进入实用阶段，设备协同成为新一轮竞争焦点",
    description: "模型压缩、内存调度与跨设备推理正在加速成熟，手机、电脑和车载终端开始共享同一套智能能力。",
    content: "新一轮端侧模型竞赛正在从参数规模转向真实场景体验。\n\n多家厂商在新系统中加入本地推理能力，用户可以在不联网的情况下完成摘要、翻译和内容整理。端云协同成为主要路径：敏感数据优先在本机处理，复杂任务再按需交给云端模型。\n\n业内认为，下一阶段的差异不只在模型本身，还取决于设备间的上下文同步、权限体系和能耗表现。",
    image: "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=82",
    author: "科技前线",
    views: 12840,
    publish_time: new Date(Date.now() - 42 * 60 * 1000).toISOString(),
  },
  {
    id: 1002,
    category_id: 1,
    category_name: "热点",
    title: "城市公共空间改造提速，小微更新更强调日常体验",
    description: "从街角公园到社区商业，城市更新开始关注步行可达、停留舒适与长期运营。",
    content: "公共空间更新正在从大拆大建转向更精细的日常改善。\n\n越来越多项目把有限的预算投入到遮阳、座椅、照明和步行路径等基础体验上，并通过社区共建机制延长空间活力。\n\n专家表示，更新项目的衡量标准正在变化：不只看建成效果，也看居民是否愿意反复使用。",
    image: "https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1200&q=82",
    author: "城市观察",
    views: 8620,
    publish_time: new Date(Date.now() - 2.2 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 1003,
    category_id: 3,
    category_name: "财经",
    title: "消费市场结构持续调整，服务类需求保持增长",
    description: "文旅、健康和效率工具成为重要增长点，消费者对价格与体验的平衡更加敏感。",
    content: "最新市场数据表明，服务消费继续保持韧性。\n\n与此同时，消费者更愿意为明确的价值付费，品牌溢价正在被产品体验和服务质量重新定义。企业开始缩短决策链路，通过小规模测试快速验证新供给。",
    image: "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1200&q=82",
    author: "商业新知",
    views: 6410,
    publish_time: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 1004,
    category_id: 4,
    category_name: "体育",
    title: "联赛进入密集赛程，轮换深度将决定争冠走势",
    description: "连续客场和伤病压力叠加，多支球队开始扩大年轻球员出场时间。",
    content: "随着赛程进入关键阶段，阵容轮换成为决定成绩的重要变量。\n\n数据团队开始将疲劳指数、跑动负荷和恢复周期纳入出场决策，教练组也在训练安排上做出更细颗粒度的调整。",
    image: "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1200&q=82",
    author: "赛场内外",
    views: 15230,
    publish_time: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 1005,
    category_id: 5,
    category_name: "文化",
    title: "博物馆夜间开放常态化，公共文化服务寻找新表达",
    description: "夜游、讲座和沉浸式展陈让观众拥有更灵活的参观时间，也对运营提出新要求。",
    content: "夜间开放不再只是节假日的临时活动。\n\n一些博物馆通过控制客流、增加定时讲解和轻量演出，在保护展品的同时改善参观体验。数字化导览也让更多背景信息触手可及。",
    image: "https://images.unsplash.com/photo-1564399579883-451a5d44ec08?auto=format&fit=crop&w=1200&q=82",
    author: "文化周刊",
    views: 4310,
    publish_time: new Date(Date.now() - 9 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 1006,
    category_id: 2,
    category_name: "科技",
    title: "开源工具链降低多智能体应用门槛，评测体系仍待完善",
    description: "开发者更容易搭建协作型应用，但任务边界、可观测性和成本控制仍是落地难点。",
    content: "多智能体开发框架正在迅速成熟。\n\n当前工具链已经覆盖任务规划、工具调用、记忆和追踪，但不同模型在实际任务中的稳定性差异明显。行业需要更统一的评测方式，避免只看演示效果。",
    image: "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=1200&q=82",
    author: "开发者社区",
    views: 9720,
    publish_time: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
  },
];

const state = {
  view: "news",
  categories: [],
  activeCategory: null,
  articles: [],
  query: "",
  density: "comfortable",
  token: localStorage.getItem("toutiao_token") || "",
  user: readStorage("toutiao_user", {
    id: null,
    username: "guest",
    nickname: "访客用户",
    avatar: createAvatar("访客用户"),
    gender: "unknown",
    bio: "登录后可同步收藏、历史记录与 AI 对话记忆。",
  }),
  memories: [],
  activeDialogId: "",
  messages: [],
  favoriteIds: new Set(),
  activeArticle: null,
  mode: "auto",
  authMode: "login",
  loadingChat: false,
};

const elements = {
  navItems: document.querySelectorAll(".nav-item"),
  viewPanels: document.querySelectorAll("[data-view-panel]"),
  currentDate: document.querySelector("#currentDate"),
  refreshNews: document.querySelector("#refreshNews"),
  newsSearch: document.querySelector("#newsSearch"),
  searchNews: document.querySelector("#searchNews"),
  categoryRow: document.querySelector("#categoryRow"),
  newsList: document.querySelector("#newsList"),
  newsListTitle: document.querySelector("#newsListTitle"),
  newsListMeta: document.querySelector("#newsListMeta"),
  densityButtons: document.querySelectorAll("[data-density]"),
  sidebarUser: document.querySelector("#sidebarUser"),
  sidebarAvatar: document.querySelector("#sidebarAvatar"),
  sidebarName: document.querySelector("#sidebarName"),
  sidebarStatus: document.querySelector("#sidebarStatus"),
  aiConnectionText: document.querySelector("#aiConnectionText"),
  memoryCount: document.querySelector("#memoryCount"),
  memorySearch: document.querySelector("#memorySearch"),
  memoryList: document.querySelector("#memoryList"),
  newConversation: document.querySelector("#newConversation"),
  activeConversationTitle: document.querySelector("#activeConversationTitle"),
  modeSwitch: document.querySelector("#modeSwitch"),
  chatMessages: document.querySelector("#chatMessages"),
  promptSuggestions: document.querySelector("#promptSuggestions"),
  chatForm: document.querySelector("#chatForm"),
  chatInput: document.querySelector("#chatInput"),
  authAction: document.querySelector("#authAction"),
  profileAvatar: document.querySelector("#profileAvatar"),
  profileDisplayName: document.querySelector("#profileDisplayName"),
  profileUsername: document.querySelector("#profileUsername"),
  profileBio: document.querySelector("#profileBio"),
  favoriteCount: document.querySelector("#favoriteCount"),
  historyCount: document.querySelector("#historyCount"),
  memoryStatCount: document.querySelector("#memoryStatCount"),
  profileForm: document.querySelector("#profileForm"),
  profileModeText: document.querySelector("#profileModeText"),
  accountBadge: document.querySelector("#accountBadge"),
  nicknameInput: document.querySelector("#nicknameInput"),
  genderInput: document.querySelector("#genderInput"),
  avatarInput: document.querySelector("#avatarInput"),
  bioInput: document.querySelector("#bioInput"),
  bioCounter: document.querySelector("#bioCounter"),
  resetProfile: document.querySelector("#resetProfile"),
  refreshFavorites: document.querySelector("#refreshFavorites"),
  favoritesMeta: document.querySelector("#favoritesMeta"),
  favoritesList: document.querySelector("#favoritesList"),
  articleDialog: document.querySelector("#articleDialog"),
  articleDialogBody: document.querySelector("#articleDialogBody"),
  closeArticle: document.querySelector("#closeArticle"),
  authDialog: document.querySelector("#authDialog"),
  closeAuth: document.querySelector("#closeAuth"),
  authTitle: document.querySelector("#authTitle"),
  authTabs: document.querySelectorAll("[data-auth-mode]"),
  authForm: document.querySelector("#authForm"),
  authUsername: document.querySelector("#authUsername"),
  authPassword: document.querySelector("#authPassword"),
  authMessage: document.querySelector("#authMessage"),
  authSubmitText: document.querySelector("#authSubmitText"),
  toastRegion: document.querySelector("#toastRegion"),
};

function readStorage(key, fallback) {
  try {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : fallback;
  } catch {
    return fallback;
  }
}

function writeStorage(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function createAvatar(name = "用户") {
  const initial = (name.trim()[0] || "用").toUpperCase();
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120"><rect width="100%" height="100%" rx="24" fill="#1e7567"/><text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" font-family="Arial,sans-serif" font-size="46" font-weight="700" fill="white">${initial}</text></svg>`;
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function normalizeImage(url) {
  if (!url) return FALLBACK_IMAGE;
  if (/^https?:\/\//i.test(url) || url.startsWith("data:")) return url;
  return `${API_BASE}/${url.replace(/^\/+/, "")}`;
}

function formatRelativeTime(value) {
  if (!value) return "刚刚";
  const time = new Date(value).getTime();
  if (Number.isNaN(time)) return value;
  const diff = Math.max(0, Date.now() - time);
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return "刚刚";
  if (minutes < 60) return `${minutes} 分钟前`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} 小时前`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days} 天前`;
  return new Intl.DateTimeFormat("zh-CN", {
    month: "short",
    day: "numeric",
  }).format(new Date(value));
}

function formatCount(value) {
  const count = Number(value) || 0;
  if (count >= 10000) return `${(count / 10000).toFixed(1)}万`;
  return count.toLocaleString("zh-CN");
}

function getErrorMessage(payload, status) {
  const validationDetail = Array.isArray(payload?.detail)
    ? payload.detail
        .map((item) => item?.msg || String(item))
        .filter(Boolean)
        .join("；")
    : "";
  if (validationDetail) return validationDetail;

  if (typeof payload?.detail === "string") return payload.detail;
  if (typeof payload?.message === "string") return payload.message;
  if (typeof payload?.data?.detail === "string") return payload.data.detail;

  if (payload?.detail && typeof payload.detail === "object") {
    return payload.detail.message || JSON.stringify(payload.detail);
  }
  if (payload?.data?.detail && typeof payload.data.detail === "object") {
    return payload.data.detail.message || JSON.stringify(payload.data.detail);
  }
  return `请求失败 (${status})`;
}

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (options.body && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  if (state.token) {
    headers.set("Authorization", `Bearer ${state.token}`);
  }

  const controller = new AbortController();
  const timeoutId = window.setTimeout(
    () => controller.abort(),
    REQUEST_TIMEOUT_MS,
  );
  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers,
      signal: controller.signal,
    });
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("后端响应超时");
    }
    throw new Error(`无法连接后端：${error.message}`);
  } finally {
    window.clearTimeout(timeoutId);
  }

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(getErrorMessage(payload, response.status));
  }
  return payload;
}

function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast${type === "error" ? " error" : ""}`;
  toast.textContent = message;
  elements.toastRegion.append(toast);
  window.setTimeout(() => toast.remove(), 3200);
}

function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons({
      attrs: {
        "aria-hidden": "true",
      },
    });
  }
}

function focusChatInput() {
  const isCoarsePointer = window.matchMedia?.("(pointer: coarse)").matches;
  if (isCoarsePointer) return;
  elements.chatInput.focus({ preventScroll: true });
}

function syncViewportHeight() {
  const viewportHeight = window.visualViewport?.height || window.innerHeight;
  document.documentElement.style.setProperty(
    "--app-viewport-height",
    `${viewportHeight}px`,
  );
}

function setView(view, syncHash = true) {
  if (!["news", "assistant", "profile"].includes(view)) return;
  state.view = view;
  const assistantActive = view === "assistant";
  document.documentElement.classList.toggle("assistant-active", assistantActive);
  document.body.classList.toggle("assistant-active", assistantActive);
  elements.navItems.forEach((item) => {
    item.classList.toggle("is-active", item.dataset.view === view);
  });
  elements.viewPanels.forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.viewPanel === view);
  });
  if (view === "profile") {
    loadFavorites();
  }
  if (view === "assistant") {
    window.setTimeout(focusChatInput, 120);
  }
  if (syncHash) {
    history.replaceState(null, "", `#${view}`);
  }
  refreshIcons();
}

function renderDate() {
  elements.currentDate.textContent = new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "short",
  }).format(new Date());
}

function renderCategories() {
  elements.categoryRow.innerHTML = "";

  const allButton = document.createElement("button");
  allButton.type = "button";
  allButton.className = `category-chip${state.activeCategory === null ? " is-active" : ""}`;
  allButton.dataset.categoryId = "";
  allButton.textContent = "全部";
  elements.categoryRow.append(allButton);

  state.categories.forEach((category) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `category-chip${Number(state.activeCategory) === Number(category.id) ? " is-active" : ""}`;
    button.dataset.categoryId = category.id;
    button.textContent = category.name;
    elements.categoryRow.append(button);
  });
}

function renderNewsSkeleton() {
  elements.newsList.innerHTML = Array.from({ length: 4 }, () => `
    <div class="skeleton-item">
      <div class="skeleton-lines">
        <div class="skeleton-line title"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-line short"></div>
      </div>
      <div class="skeleton-image"></div>
    </div>
  `).join("");
}

function getFilteredArticles() {
  const keyword = state.query.trim().toLowerCase();
  if (!keyword) return state.articles;
  return state.articles.filter((article) => {
    return [article.title, article.description, article.author, article.category_name]
      .filter(Boolean)
      .some((value) => String(value).toLowerCase().includes(keyword));
  });
}

function renderNews() {
  const articles = getFilteredArticles();
  const category = state.categories.find((item) => Number(item.id) === Number(state.activeCategory));
  const categoryName = category?.name || "全部新闻";

  elements.newsListTitle.textContent = state.query ? `“${state.query}”的搜索结果` : categoryName;
  elements.newsListMeta.textContent = state.query
    ? `找到 ${articles.length} 条内容`
    : `共 ${state.articles.length} 条内容 · 按发布时间排序`;

  if (!articles.length) {
    elements.newsList.innerHTML = `
      <div class="empty-state">
        <div>
          <i data-lucide="search-x"></i>
          <h3>没有找到匹配内容</h3>
          <p>尝试调整关键词或切换新闻分类。</p>
        </div>
      </div>
    `;
    refreshIcons();
    return;
  }

  elements.newsList.innerHTML = articles.map((article) => {
    const categoryLabel = article.category_name
      || state.categories.find((item) => Number(item.id) === Number(article.category_id))?.name
      || "新闻";
    return `
      <article class="news-item" data-article-id="${article.id}" tabindex="0">
        <div class="news-copy">
          <div class="news-kicker">
            <span>${escapeHtml(categoryLabel)}</span>
            <span>${escapeHtml(formatRelativeTime(article.publish_time))}</span>
          </div>
          <h3>${escapeHtml(article.title)}</h3>
          <p class="news-description">${escapeHtml(article.description || "暂无摘要")}</p>
          <footer class="news-footer">
            <span><i data-lucide="pen-line"></i>${escapeHtml(article.author || "头条简报")}</span>
            <span><i data-lucide="eye"></i>${formatCount(article.views)}</span>
            <span><i data-lucide="clock-3"></i>${escapeHtml(formatRelativeTime(article.publish_time))}</span>
          </footer>
        </div>
        <div class="news-thumb">
          <img src="${escapeHtml(normalizeImage(article.image))}" alt="${escapeHtml(article.title)}" loading="lazy">
        </div>
      </article>
    `;
  }).join("");

  elements.newsList.querySelectorAll("img").forEach((image) => {
    image.addEventListener("error", () => {
      if (image.src !== FALLBACK_IMAGE) {
        image.src = FALLBACK_IMAGE;
      } else {
        image.parentElement.classList.add("image-error");
        image.remove();
      }
    });
  });

  refreshIcons();
}

async function loadNews() {
  const showInitialFallback = state.categories.length === 0 && state.articles.length === 0;
  if (showInitialFallback) {
    state.categories = DEMO_CATEGORIES;
    state.activeCategory = Number(DEMO_CATEGORIES[0].id);
    state.articles = DEMO_NEWS;
    renderCategories();
    renderNews();
  }

  renderNewsSkeleton();
  let usedFallback = false;

  try {
    const categoryPayload = await request("/api/news/categories?skip=0&limit=100");
    const categories = Array.isArray(categoryPayload.data) ? categoryPayload.data : [];
    state.categories = categories.length ? categories : DEMO_CATEGORIES;
    if (categories.length === 0) usedFallback = true;
  } catch {
    state.categories = DEMO_CATEGORIES;
    usedFallback = true;
  }

  const activeCategoryExists = state.categories.some((item) => {
    return Number(item.id) === Number(state.activeCategory);
  });
  if ((!state.activeCategory || !activeCategoryExists) && state.categories.length) {
    state.activeCategory = Number(state.categories[0].id);
  }
  renderCategories();

  if (usedFallback) {
    state.articles = DEMO_NEWS;
    renderNews();
    return;
  }

  try {
    const params = new URLSearchParams({
      page: "1",
      page_size: "100",
    });
    if (state.activeCategory !== null) {
      params.set("category_id", String(state.activeCategory));
    }
    const payload = await request(`/api/news/list?${params.toString()}`);
    const first = Array.isArray(payload.data) ? payload.data[0] : payload.data;
    const list = Array.isArray(first?.list) ? first.list : [];
    state.articles = list.map((article) => ({
      ...article,
      category_name: state.categories.find((item) => Number(item.id) === Number(article.category_id))?.name,
    }));
    renderNews();
  } catch {
    state.articles = DEMO_NEWS.filter((article) => {
      return state.activeCategory === null || Number(article.category_id) === Number(state.activeCategory);
    });
    if (!state.articles.length) state.articles = DEMO_NEWS;
    renderNews();
    showToast("新闻接口暂不可用，已显示演示内容", "error");
  }
}

function selectCategory(categoryId) {
  state.activeCategory = categoryId === "" ? null : Number(categoryId);
  state.query = "";
  elements.newsSearch.value = "";
  renderCategories();
  loadNews();
}

function renderArticleDialog(article) {
  state.activeArticle = article;
  const categoryLabel = article.category_name
    || state.categories.find((item) => Number(item.id) === Number(article.category_id))?.name
    || "新闻";
  const isFavorite = state.favoriteIds.has(Number(article.id));
  elements.articleDialogBody.innerHTML = `
    <img class="article-dialog-image" src="${escapeHtml(normalizeImage(article.image))}" alt="${escapeHtml(article.title)}">
    <div class="article-dialog-content">
      <div class="news-kicker">
        <span>${escapeHtml(categoryLabel)}</span>
        <span>${escapeHtml(formatRelativeTime(article.publish_time))}</span>
      </div>
      <h2>${escapeHtml(article.title)}</h2>
      ${article.description ? `<p class="article-dialog-description">${escapeHtml(article.description)}</p>` : ""}
      <div class="article-byline">
        <span>${escapeHtml(article.author || "头条简报")}</span>
        <span>${formatCount(article.views)} 次阅读</span>
        <span>${escapeHtml(formatRelativeTime(article.publish_time))}</span>
        <button class="article-favorite${isFavorite ? " is-active" : ""}" id="articleFavoriteButton" type="button" data-news-id="${article.id}">
          <i data-lucide="bookmark" aria-hidden="true"></i>
          <span>${isFavorite ? "已收藏" : "收藏"}</span>
        </button>
      </div>
      <div class="article-content">${escapeHtml(article.content || article.description || "暂无正文")}</div>
    </div>
  `;
  const dialogImage = elements.articleDialogBody.querySelector("img");
  dialogImage?.addEventListener("error", () => {
    if (dialogImage.src !== FALLBACK_IMAGE) dialogImage.src = FALLBACK_IMAGE;
  });
  refreshIcons();
}

function updateArticleFavoriteButton() {
  const button = document.querySelector("#articleFavoriteButton");
  if (!button || !state.activeArticle) return;
  const isFavorite = state.favoriteIds.has(Number(state.activeArticle.id));
  button.classList.toggle("is-active", isFavorite);
  button.querySelector("span").textContent = isFavorite ? "已收藏" : "收藏";
  button.querySelector("i")?.setAttribute("data-lucide", isFavorite ? "bookmark-check" : "bookmark");
  refreshIcons();
}

async function loadFavoriteStatus(newsId) {
  if (!state.token) return;
  try {
    const payload = await request(`/api/favority/check?news_id=${encodeURIComponent(newsId)}`);
    const isFavorite = Boolean(payload.data?.is_favorited);
    if (isFavorite) state.favoriteIds.add(Number(newsId));
    else state.favoriteIds.delete(Number(newsId));
    updateArticleFavoriteButton();
  } catch {
    // Keep the current local state when the favorite status cannot be loaded.
  }
}

async function toggleFavorite(newsId) {
  if (!state.token) {
    showToast("请先登录后收藏新闻");
    openAuthDialog();
    return;
  }

  const numericNewsId = Number(newsId);
  const isFavorite = state.favoriteIds.has(numericNewsId);
  const action = isFavorite ? "remove" : "add";
  try {
    await request(`/api/favority/${action}`, {
      method: "POST",
      body: JSON.stringify({ news_id: numericNewsId }),
    });
    if (isFavorite) state.favoriteIds.delete(numericNewsId);
    else state.favoriteIds.add(numericNewsId);
    updateArticleFavoriteButton();
    await Promise.all([loadFavorites(), loadProfileStats()]);
    showToast(isFavorite ? "已取消收藏" : "已加入收藏");
  } catch (error) {
    showToast(error.message, "error");
  }
}

async function openArticle(articleId) {
  let article = state.articles.find((item) => Number(item.id) === Number(articleId));

  if (article) {
    renderArticleDialog(article);
    elements.articleDialog.showModal();
  }

  try {
    const payload = await request(`/api/news/detail?ID=${encodeURIComponent(articleId)}`);
    if (payload.data) {
      article = payload.data;
      renderArticleDialog(article);
      if (!elements.articleDialog.open) elements.articleDialog.showModal();
    }
  } catch {
    if (!article) showToast("暂时无法读取新闻详情", "error");
  }
  await loadFavoriteStatus(articleId);
}

function updateProfileUI() {
  const user = state.user;
  const displayName = user.nickname || user.username || "访客用户";
  const avatar = normalizeImage(user.avatar || createAvatar(displayName));
  const editableAvatar = String(user.avatar || "").startsWith("data:") ? "" : user.avatar || "";

  elements.sidebarAvatar.src = avatar;
  elements.sidebarName.textContent = displayName;
  elements.sidebarStatus.textContent = state.token ? "已同步账号" : "本地模式";
  elements.profileAvatar.src = avatar;
  elements.profileDisplayName.textContent = displayName;
  elements.profileUsername.textContent = `@${user.username || "guest"}`;
  elements.profileBio.textContent = user.bio || "还没有填写个人简介。";
  elements.nicknameInput.value = user.nickname || "";
  elements.genderInput.value = user.gender || "unknown";
  elements.avatarInput.value = editableAvatar;
  elements.bioInput.value = user.bio || "";
  elements.bioCounter.textContent = String((user.bio || "").length);
  elements.profileModeText.textContent = state.token
    ? "账号资料已连接服务器"
    : "当前为本地访客资料";
  elements.accountBadge.textContent = state.token ? "ONLINE" : "GUEST";
  elements.accountBadge.style.color = state.token ? "var(--green)" : "var(--amber)";
  elements.accountBadge.style.background = state.token ? "var(--green-soft)" : "#fff4df";
  elements.authAction.querySelector("span").textContent = state.token ? "退出登录" : "登录 / 注册";

  const authIcon = elements.authAction.querySelector("svg");
  if (authIcon && window.lucide) {
    authIcon.outerHTML = `<i data-lucide="${state.token ? "log-out" : "log-in"}"></i>`;
  }
  refreshIcons();
}

function renderFavorites(items, total) {
  elements.favoritesMeta.textContent = state.token
    ? `共 ${total} 条收藏`
    : "登录后可查看收藏的新闻";

  if (!state.token) {
    elements.favoritesList.innerHTML = `
      <div class="favorites-empty">
        <i data-lucide="bookmark" aria-hidden="true"></i>
        <p>登录后在这里查看和管理收藏内容</p>
      </div>
    `;
    refreshIcons();
    return;
  }

  if (!items.length) {
    elements.favoritesList.innerHTML = `
      <div class="favorites-empty">
        <i data-lucide="bookmark-x" aria-hidden="true"></i>
        <p>还没有收藏新闻</p>
      </div>
    `;
    refreshIcons();
    return;
  }

  elements.favoritesList.innerHTML = items.map((article) => {
    const categoryLabel = state.categories.find((item) => {
      return Number(item.id) === Number(article.category_id);
    })?.name || "新闻";
    return `
      <article class="favorite-news-item" data-favorite-news-id="${article.id}" tabindex="0">
        <div class="favorite-news-thumb">
          <img src="${escapeHtml(normalizeImage(article.image))}" alt="${escapeHtml(article.title)}" loading="lazy">
        </div>
        <div class="favorite-news-copy">
          <div class="favorite-news-kicker">
            <span>${escapeHtml(categoryLabel)}</span>
            <span>${escapeHtml(formatRelativeTime(article.favorite_time || article.publish_time))}</span>
          </div>
          <h3>${escapeHtml(article.title)}</h3>
          <p>${escapeHtml(article.description || "暂无摘要")}</p>
        </div>
        <button class="favorite-remove" type="button" data-remove-favorite-id="${article.id}" title="取消收藏" aria-label="取消收藏">
          <i data-lucide="trash-2" aria-hidden="true"></i>
        </button>
      </article>
    `;
  }).join("");

  elements.favoritesList.querySelectorAll("img").forEach((image) => {
    image.addEventListener("error", () => {
      if (image.src !== FALLBACK_IMAGE) image.src = FALLBACK_IMAGE;
    });
  });
  refreshIcons();
}

async function loadFavorites() {
  if (!state.token) {
    state.favoriteIds = new Set();
    renderFavorites([], 0);
    return;
  }

  elements.favoritesMeta.textContent = "正在读取收藏";
  try {
    const payload = await request("/api/favority/list?page=1&page_size=100");
    const items = Array.isArray(payload.data?.list) ? payload.data.list : [];
    const total = Number(payload.data?.total) || items.length;
    state.favoriteIds = new Set(items.map((article) => Number(article.id)));
    renderFavorites(items, total);
    updateArticleFavoriteButton();
  } catch (error) {
    elements.favoritesList.innerHTML = `
      <div class="favorites-empty">
        <i data-lucide="circle-alert" aria-hidden="true"></i>
        <p>${escapeHtml(error.message)}</p>
      </div>
    `;
    elements.favoritesMeta.textContent = "收藏加载失败";
    refreshIcons();
  }
}

async function loadProfileStats() {
  if (!state.token) {
    elements.favoriteCount.textContent = "0";
    elements.historyCount.textContent = "0";
    elements.memoryStatCount.textContent = String(state.memories.length);
    return;
  }

  const results = await Promise.allSettled([
    request("/api/favority/list?page=1&page_size=1"),
    request("/api/history/list?page=1&page_size=1"),
  ]);

  const favoritePayload = results[0].status === "fulfilled" ? results[0].value : null;
  const historyPayload = results[1].status === "fulfilled" ? results[1].value : null;
  elements.favoriteCount.textContent = String(favoritePayload?.data?.total || 0);
  elements.historyCount.textContent = String(historyPayload?.data?.total || 0);
  elements.memoryStatCount.textContent = String(state.memories.length);
}

async function saveProfile(event) {
  event.preventDefault();
  const nextProfile = {
    ...state.user,
    nickname: elements.nicknameInput.value.trim(),
    gender: elements.genderInput.value,
    avatar: elements.avatarInput.value.trim(),
    bio: elements.bioInput.value.trim(),
  };

  if (!nextProfile.avatar || nextProfile.avatar.startsWith("data:")) {
    nextProfile.avatar = null;
  }

  if (state.token) {
    try {
      const payload = await request("/api/users/update", {
        method: "PUT",
        body: JSON.stringify({
          nickname: nextProfile.nickname || null,
          gender: nextProfile.gender,
          avatar: nextProfile.avatar,
          bio: nextProfile.bio || null,
        }),
      });
      state.user = { ...state.user, ...(payload.data || nextProfile) };
      showToast("个人资料已同步");
    } catch (error) {
      showToast(error.message, "error");
      return;
    }
  } else {
    state.user = nextProfile;
    showToast("访客资料已保存在本机");
  }

  writeStorage("toutiao_user", state.user);
  updateProfileUI();
}

function resetProfileForm() {
  updateProfileUI();
}

function openAuthDialog() {
  if (state.token) {
    state.token = "";
    localStorage.removeItem("toutiao_token");
    state.user = {
      id: null,
      username: "guest",
      nickname: "访客用户",
      avatar: createAvatar("访客用户"),
      gender: "unknown",
      bio: "登录后可同步收藏、历史记录与 AI 对话记忆。",
    };
    state.favoriteIds = new Set();
    writeStorage("toutiao_user", state.user);
    updateProfileUI();
    loadFavorites();
    showToast("已退出当前账号");
    return;
  }

  elements.authDialog.showModal();
  window.setTimeout(() => elements.authUsername.focus(), 80);
}

function setAuthMode(mode) {
  state.authMode = mode;
  elements.authTabs.forEach((tab) => {
    tab.classList.toggle("is-active", tab.dataset.authMode === mode);
  });
  elements.authTitle.textContent = mode === "login" ? "登录账号" : "创建账号";
  elements.authSubmitText.textContent = mode === "login" ? "登录" : "注册";
  elements.authMessage.textContent = "";
  elements.authPassword.autocomplete = mode === "login" ? "current-password" : "new-password";
}

async function submitAuth(event) {
  event.preventDefault();
  elements.authMessage.textContent = "";
  const username = elements.authUsername.value.trim();
  const password = elements.authPassword.value;

  try {
    const payload = await request(`/api/users/${state.authMode}`, {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    state.token = payload.data?.token || "";
    state.user = payload.data?.userinfo || payload.data?.userInfo || state.user;
    localStorage.setItem("toutiao_token", state.token);
    writeStorage("toutiao_user", state.user);
    elements.authDialog.close();
    elements.authForm.reset();
    updateProfileUI();
    await Promise.all([loadMemories(), loadFavorites(), loadProfileStats()]);
    showToast(state.authMode === "login" ? "登录成功" : "注册成功");
  } catch (error) {
    elements.authMessage.textContent = error.message;
  }
}

function localMemories() {
  const stored = readStorage("toutiao_memories", []);
  const now = new Date().toISOString();
  return [
    {
      dialog_id: "daily-news",
      title: "今日新闻速览",
      updated_at: now,
      message_count: 4,
      local: true,
    },
    {
      dialog_id: "tech-research",
      title: "端侧 AI 技术对比",
      updated_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
      message_count: 8,
      local: true,
    },
    ...stored,
  ];
}

async function loadMemories() {
  if (state.token) {
    try {
      state.memories = await request("/api/memory");
      elements.aiConnectionText.textContent = "服务已连接";
    } catch {
      state.memories = localMemories();
      elements.aiConnectionText.textContent = "本地会话模式";
    }
  } else {
    state.memories = localMemories();
    elements.aiConnectionText.textContent = "本地会话模式";
  }

  if (!state.activeDialogId && state.memories.length) {
    state.activeDialogId = state.memories[0].dialog_id;
  }
  renderMemories();
  elements.memoryStatCount.textContent = String(state.memories.length);
}

function ensureActiveConversation() {
  if (!state.activeDialogId) {
    startNewConversation();
  }
  return state.activeDialogId;
}

function renderMemories() {
  const keyword = elements.memorySearch.value.trim().toLowerCase();
  const memories = state.memories.filter((memory) => {
    return !keyword || String(memory.title || "").toLowerCase().includes(keyword);
  });

  elements.memoryCount.textContent = `${state.memories.length} 个会话`;
  if (!memories.length) {
    elements.memoryList.innerHTML = `
      <div class="empty-state" style="min-height:180px;border:0;color:#7f858e">
        <div><p>没有匹配的会话</p></div>
      </div>
    `;
    return;
  }

  elements.memoryList.innerHTML = memories.map((memory) => `
    <div class="memory-item${memory.dialog_id === state.activeDialogId ? " is-active" : ""}" data-dialog-id="${escapeHtml(memory.dialog_id)}" role="button" tabindex="0">
      <i data-lucide="message-square-text"></i>
      <span class="memory-item-copy">
        <strong>${escapeHtml(memory.title || "未命名对话")}</strong>
        <small>${memory.message_count || 0} 条消息 · ${escapeHtml(formatRelativeTime(memory.updated_at))}</small>
      </span>
      <button class="memory-delete" type="button" data-delete-dialog-id="${escapeHtml(memory.dialog_id)}" title="删除记忆" aria-label="删除记忆">
        <i data-lucide="trash-2" aria-hidden="true"></i>
      </button>
    </div>
  `).join("");
  refreshIcons();
}

async function selectMemory(dialogId) {
  if (!dialogId) {
    startNewConversation();
    return;
  }

  state.activeDialogId = dialogId;
  const memory = state.memories.find((item) => item.dialog_id === dialogId);
  elements.activeConversationTitle.textContent = memory?.title || "新对话";
  renderMemories();

  if (!state.token) {
    const stored = readStorage(`toutiao_messages_${dialogId}`, []);
    state.messages = stored.length ? stored : defaultMessages(dialogId);
    renderMessages();
    return;
  }

  try {
    const payload = await request(`/api/memory/${encodeURIComponent(dialogId)}/messages`);
    state.messages = payload.messages || [];
    renderMessages();
  } catch {
    state.messages = defaultMessages(dialogId);
    renderMessages();
  }
}

async function deleteMemory(dialogId) {
  const memory = state.memories.find((item) => item.dialog_id === dialogId);
  if (!memory) return;
  if (!window.confirm(`删除“${memory.title || "未命名对话"}”的记忆？`)) return;

  try {
    if (state.token && !memory.local) {
      await request(`/api/memory/${encodeURIComponent(dialogId)}`, {
        method: "DELETE",
      });
    }

    localStorage.removeItem(`toutiao_messages_${dialogId}`);
    state.memories = state.memories.filter((item) => item.dialog_id !== dialogId);
    elements.memoryStatCount.textContent = String(state.memories.length);

    if (state.activeDialogId === dialogId) {
      state.activeDialogId = "";
      state.messages = [];
      if (state.memories.length) {
        await selectMemory(state.memories[0].dialog_id);
      } else {
        startNewConversation();
      }
    } else {
      renderMemories();
    }
    showToast("对话记忆已删除");
  } catch (error) {
    showToast(error.message, "error");
  }
}

function defaultMessages(dialogId) {
  if (dialogId === "daily-news") {
    return [
      {
        role: "assistant",
        content: "上午好。我已经准备好整理今天的新闻，你可以指定领域、时间范围或信息来源。",
      },
      {
        role: "user",
        content: "帮我总结一下今天值得关注的科技进展。",
      },
      {
        role: "assistant",
        content: "今天值得关注的方向主要有三个：端侧大模型开始强调跨设备协同；多智能体工具链继续降低开发门槛；行业评测正在从能力演示转向稳定性与成本。\n\n如果你需要，我可以继续按公司或技术方向拆分。",
      },
    ];
  }

  return [
    {
      role: "assistant",
      content: "这是新会话。告诉我你想了解的问题，我会根据当前检索方式整理答案。",
    },
  ];
}

function renderMessages() {
  const messages = state.messages.length
    ? state.messages
    : [{ role: "assistant", content: "告诉我你想了解的问题。" }];

  elements.chatMessages.innerHTML = messages.map((message) => {
    const isUser = message.role === "user";
    const roleName = isUser ? "你" : "AI助手";
    const icon = isUser ? "user-round" : "bot";
    return `
      <div class="message ${isUser ? "user" : "assistant"}">
        <span class="message-avatar"><i data-lucide="${icon}"></i></span>
        <div class="message-content">
          <div class="message-meta">
            <strong>${roleName}</strong>
            <span>${isUser ? "刚刚" : state.mode.toUpperCase()}</span>
          </div>
          <div class="message-bubble">${escapeHtml(message.content)}</div>
        </div>
      </div>
    `;
  }).join("");
  refreshIcons();
  elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function startNewConversation() {
  const id = `dialog-${Date.now().toString(36)}`;
  state.activeDialogId = id;
  state.messages = defaultMessages(id);
  const memory = {
    dialog_id: id,
    title: "新对话",
    updated_at: new Date().toISOString(),
    message_count: state.messages.length,
    local: true,
  };
  state.memories = [memory, ...state.memories.filter((item) => item.dialog_id !== id)];
  elements.activeConversationTitle.textContent = memory.title;
  renderMemories();
  renderMessages();
  focusChatInput();
}

function setMode(mode) {
  state.mode = mode;
  elements.modeSwitch.querySelectorAll("button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.mode === mode);
  });
}

function appendMessage(role, content, extra = {}) {
  state.messages.push({ role, content, ...extra });
  renderMessages();
  if (!state.token) {
    writeStorage(`toutiao_messages_${state.activeDialogId}`, state.messages);
  }
  return state.messages.length - 1;
}

function appendLoadingMessage() {
  const wrapper = document.createElement("div");
  wrapper.className = "message assistant";
  wrapper.id = "chatLoadingMessage";
  wrapper.innerHTML = `
    <span class="message-avatar"><i data-lucide="bot"></i></span>
    <div class="message-content">
      <div class="message-meta"><strong>AI助手</strong><span>${state.mode.toUpperCase()}</span></div>
      <div class="message-bubble"><span class="message-loading"><span></span><span></span><span></span></span></div>
    </div>
  `;
  elements.chatMessages.append(wrapper);
  refreshIcons();
  elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function removeLoadingMessage() {
  document.querySelector("#chatLoadingMessage")?.remove();
}

function updateLoadingStatus(message) {
  const bubble = document.querySelector("#chatLoadingMessage .message-bubble");
  if (bubble) bubble.textContent = message;
}

function updateStreamingAssistantMessage(content) {
  const message = state.messages.at(-1);
  if (!message || message.role !== "assistant") return;
  message.content = content;

  const bubbles = elements.chatMessages.querySelectorAll(".message.assistant .message-bubble");
  const bubble = bubbles[bubbles.length - 1];
  if (bubble) bubble.textContent = content;
  else renderMessages();
  elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

async function streamChat(message, handlers = {}) {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(
    () => controller.abort(),
    REQUEST_TIMEOUT_MS,
  );
  let response;

  try {
    response = await fetch(`${API_BASE}/api/chat/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(state.token ? { Authorization: `Bearer ${state.token}` } : {}),
      },
      body: JSON.stringify({
        message,
        dialog_id: state.activeDialogId,
        mode: state.mode,
      }),
      signal: controller.signal,
    });
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("建立流式连接超时");
    }
    throw new Error(`无法连接后端：${error.message}`);
  } finally {
    window.clearTimeout(timeoutId);
  }

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(getErrorMessage(payload, response.status));
  }
  if (!response.body) {
    throw new Error("浏览器不支持流式响应");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let doneData = null;

  const handleBlock = (block) => {
    let eventName = "message";
    const dataLines = [];

    block.split(/\r?\n/).forEach((line) => {
      if (line.startsWith("event:")) eventName = line.slice(6).trim();
      if (line.startsWith("data:")) dataLines.push(line.slice(5).trimStart());
    });

    if (!dataLines.length) return;
    const data = JSON.parse(dataLines.join("\n"));

    if (eventName === "status") handlers.onStatus?.(data.message);
    if (eventName === "meta") handlers.onMeta?.(data);
    if (eventName === "token") handlers.onToken?.(data.content || "");
    if (eventName === "done") {
      doneData = data;
      handlers.onDone?.(data);
    }
    if (eventName === "error") {
      throw new Error(data.message || "AI 服务调用失败");
    }
  };

  while (true) {
    const { value, done } = await reader.read();
    buffer += decoder.decode(value || new Uint8Array(), { stream: !done });

    let boundary = buffer.indexOf("\n\n");
    while (boundary !== -1) {
      const block = buffer.slice(0, boundary);
      buffer = buffer.slice(boundary + 2);
      if (block.trim()) handleBlock(block);
      boundary = buffer.indexOf("\n\n");
    }

    if (done) break;
  }

  if (buffer.trim()) handleBlock(buffer);
  return doneData;
}

async function submitChat(event) {
  event.preventDefault();
  const message = elements.chatInput.value.trim();
  if (!message || state.loadingChat) return;

  elements.chatInput.value = "";
  autoResizeChatInput();
  ensureActiveConversation();
  appendMessage("user", message);
  state.loadingChat = true;
  elements.chatForm.querySelector("button").disabled = true;
  appendLoadingMessage();

  try {
    if (state.token) {
      let assistantIndex = -1;
      let answer = "";
      const result = await streamChat(message, {
        onStatus: updateLoadingStatus,
        onToken(token) {
          if (assistantIndex === -1) {
            removeLoadingMessage();
            assistantIndex = appendMessage("assistant", "");
          }
          answer += token;
          updateStreamingAssistantMessage(answer);
        },
      });

      removeLoadingMessage();
      if (assistantIndex === -1) {
        assistantIndex = appendMessage(
          "assistant",
          result?.answer || "助手没有返回内容。",
        );
      }
      if (assistantIndex !== -1) {
        Object.assign(state.messages[assistantIndex], {
          route: result?.route,
          retrieval: result?.retrieval,
          streaming: false,
        });
      }
    } else {
      await new Promise((resolve) => window.setTimeout(resolve, 650));
      removeLoadingMessage();
      appendMessage("assistant", createLocalAnswer(message, state.mode));
    }

    const memory = state.memories.find((item) => item.dialog_id === state.activeDialogId);
    if (memory) {
      if (memory.title === "新对话" || memory.title === "未命名对话") {
        memory.title = message.slice(0, 22);
        elements.activeConversationTitle.textContent = memory.title;
      }
      memory.updated_at = new Date().toISOString();
      memory.message_count = state.messages.length;
      renderMemories();
    }
  } catch (error) {
    removeLoadingMessage();
    appendMessage("assistant", `本次请求失败：${error.message}`);
    showToast(error.message, "error");
  } finally {
    state.loadingChat = false;
    elements.chatForm.querySelector("button").disabled = false;
    focusChatInput();
  }
}

function createLocalAnswer(message, mode) {
  const modeLabel = {
    rag: "知识库检索",
    web: "Web 搜索",
    auto: "自动检索",
  }[mode] || "自动检索";

  const localArticle = state.articles.find((article) => {
    return `${article.title} ${article.description}`.includes(message.slice(0, 8));
  });
  const reference = localArticle ? `\n\n可以参考《${localArticle.title}》。` : "";

  return `已使用${modeLabel}模式处理你的问题。\n\n当前页面处于本地预览状态，尚未连接账号或 AI 后端。登录后，助手会调用项目中的检索流程并返回带来源的答案。${reference}\n\n围绕“${message.slice(0, 40)}${message.length > 40 ? "..." : ""}”，建议先明确目标和时间范围，再从知识库与实时来源中交叉验证。`;
}

function autoResizeChatInput() {
  elements.chatInput.style.height = "auto";
  elements.chatInput.style.height = `${Math.min(elements.chatInput.scrollHeight, 130)}px`;
}

function bindEvents() {
  elements.navItems.forEach((item) => {
    item.addEventListener("click", () => setView(item.dataset.view));
  });

  elements.sidebarUser.addEventListener("click", () => {
    setView("profile");
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  elements.refreshNews.addEventListener("click", loadNews);
  elements.searchNews.addEventListener("click", () => {
    state.query = elements.newsSearch.value.trim();
    renderNews();
  });
  elements.newsSearch.addEventListener("input", () => {
    state.query = elements.newsSearch.value.trim();
    renderNews();
  });
  elements.newsSearch.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      state.query = elements.newsSearch.value.trim();
      renderNews();
    }
  });

  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      setView("news");
      elements.newsSearch.focus();
    }
  });

  elements.categoryRow.addEventListener("click", (event) => {
    const button = event.target.closest("[data-category-id]");
    if (button) selectCategory(button.dataset.categoryId);
  });

  elements.newsList.addEventListener("click", (event) => {
    const item = event.target.closest("[data-article-id]");
    if (item) openArticle(item.dataset.articleId);
  });
  elements.newsList.addEventListener("keydown", (event) => {
    const item = event.target.closest("[data-article-id]");
    if (item && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      openArticle(item.dataset.articleId);
    }
  });

  elements.densityButtons.forEach((button) => {
    button.addEventListener("click", () => {
      state.density = button.dataset.density;
      elements.densityButtons.forEach((item) => item.classList.toggle("is-active", item === button));
      elements.newsList.classList.toggle("is-compact", state.density === "compact");
    });
  });

  elements.memorySearch.addEventListener("input", renderMemories);
  elements.memoryList.addEventListener("click", (event) => {
    const deleteButton = event.target.closest("[data-delete-dialog-id]");
    if (deleteButton) {
      event.stopPropagation();
      deleteMemory(deleteButton.dataset.deleteDialogId);
      return;
    }
    const button = event.target.closest("[data-dialog-id]");
    if (button) selectMemory(button.dataset.dialogId);
  });
  elements.memoryList.addEventListener("keydown", (event) => {
    const item = event.target.closest("[data-dialog-id]");
    if (item && event.target === item && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      selectMemory(item.dataset.dialogId);
    }
  });
  elements.newConversation.addEventListener("click", startNewConversation);
  elements.modeSwitch.addEventListener("click", (event) => {
    const button = event.target.closest("[data-mode]");
    if (button) setMode(button.dataset.mode);
  });
  elements.promptSuggestions.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    elements.chatInput.value = button.textContent.trim();
    autoResizeChatInput();
    focusChatInput();
  });
  elements.chatInput.addEventListener("input", autoResizeChatInput);
  elements.chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      elements.chatForm.requestSubmit();
    }
  });
  elements.chatForm.addEventListener("submit", submitChat);

  elements.profileForm.addEventListener("submit", saveProfile);
  elements.bioInput.addEventListener("input", () => {
    elements.bioCounter.textContent = String(elements.bioInput.value.length);
  });
  elements.resetProfile.addEventListener("click", resetProfileForm);
  elements.refreshFavorites.addEventListener("click", loadFavorites);
  elements.favoritesList.addEventListener("click", (event) => {
    const removeButton = event.target.closest("[data-remove-favorite-id]");
    if (removeButton) {
      event.stopPropagation();
      toggleFavorite(removeButton.dataset.removeFavoriteId);
      return;
    }
    const item = event.target.closest("[data-favorite-news-id]");
    if (item) openArticle(item.dataset.favoriteNewsId);
  });
  elements.favoritesList.addEventListener("keydown", (event) => {
    const item = event.target.closest("[data-favorite-news-id]");
    if (item && event.target === item && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      openArticle(item.dataset.favoriteNewsId);
    }
  });
  elements.articleDialogBody.addEventListener("click", (event) => {
    const button = event.target.closest("#articleFavoriteButton");
    if (button) toggleFavorite(button.dataset.newsId);
  });
  elements.authAction.addEventListener("click", openAuthDialog);
  elements.closeArticle.addEventListener("click", () => elements.articleDialog.close());
  elements.closeAuth.addEventListener("click", () => elements.authDialog.close());
  elements.authTabs.forEach((tab) => {
    tab.addEventListener("click", () => setAuthMode(tab.dataset.authMode));
  });
  elements.authForm.addEventListener("submit", submitAuth);

  [elements.articleDialog, elements.authDialog].forEach((dialog) => {
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
  });
}

async function init() {
  syncViewportHeight();
  window.addEventListener("resize", syncViewportHeight);
  window.visualViewport?.addEventListener("resize", syncViewportHeight);
  renderDate();
  updateProfileUI();
  bindEvents();
  refreshIcons();
  const initialView = window.location.hash.slice(1);
  if (["news", "assistant", "profile"].includes(initialView)) {
    setView(initialView, false);
  }
  await Promise.all([loadNews(), loadMemories(), loadFavorites()]);
  if (state.activeDialogId) {
    await selectMemory(state.activeDialogId);
  } else {
    startNewConversation();
  }
  loadProfileStats();
}

document.addEventListener("DOMContentLoaded", init);
window.addEventListener("load", refreshIcons);
window.addEventListener("hashchange", () => {
  setView(window.location.hash.slice(1), false);
});
