(() => {
  const root = document.documentElement;
  const viewStorageKey = "hugo-styles:view";
  const lessonSidebarStorageKey = "hugo-styles:lesson-sidebar-collapsed";
  const lessonTocStorageKey = "hugo-styles:lesson-toc-collapsed";
  const allowedViews = new Set(["learner", "instructor"]);
  const lessonShells = Array.from(document.querySelectorAll("[data-lesson-shell]"));
  const floatingBackToTopButtons = Array.from(document.querySelectorAll("[data-lesson-back-to-top]"));
  const desktopTocMedia = window.matchMedia("(min-width: 1280px)");

  const scrollToTop = () => {
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    window.scroll({
      top: 0,
      left: 0,
      behavior: prefersReducedMotion ? "auto" : "smooth",
    });
  };

  const syncFloatingBackToTop = () => {
    if (floatingBackToTopButtons.length === 0) {
      return;
    }

    const shouldShow = lessonShells.some((shell) => {
      const tocHidden = shell.dataset.tocCollapsed === "true" || !desktopTocMedia.matches;
      return tocHidden && window.scrollY > 300;
    });

    floatingBackToTopButtons.forEach((button) => {
      button.dataset.visible = shouldShow ? "true" : "false";
      button.tabIndex = shouldShow ? 0 : -1;
    });
  };
  const syncViewUrl = (view) => {
    const url = new URL(window.location.href);
    if (view === "learner") {
      url.searchParams.delete("view");
    } else {
      url.searchParams.set("view", view);
    }
    window.history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);
  };

  const applyView = (view) => {
    const next = allowedViews.has(view) ? view : "learner";
    root.dataset.view = next;
    document.querySelectorAll("[data-view-toggle]").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.viewToggle === next));
    });
  };

  const urlParams = new URLSearchParams(window.location.search);
  const fromUrl = urlParams.get("view");
  const fromStorage = window.localStorage.getItem(viewStorageKey);
  applyView(fromUrl || fromStorage || root.dataset.view || "learner");

  document.querySelectorAll("[data-view-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const next = button.dataset.viewToggle || "learner";
      window.localStorage.setItem(viewStorageKey, next);
      applyView(next);
      syncViewUrl(next);
    });
  });

  document.querySelectorAll("[data-expand-solutions]").forEach((button) => {
    button.addEventListener("click", () => {
      const details = document.querySelectorAll("[data-lesson-disclosure='solution'], [data-lesson-disclosure='hint']");
      const shouldOpen = button.dataset.expanded !== "true";
      details.forEach((item) => {
        item.open = shouldOpen;
      });
      button.dataset.expanded = String(shouldOpen);
      button.textContent = shouldOpen ? "Collapse Hints and Solutions" : "Expand Hints and Solutions";
    });
  });

  const applyLessonToggleState = (kind, collapsed) => {
    const next = collapsed ? "true" : "false";
    const pressed = collapsed ? "false" : "true";
    const attribute = kind === "sidebar" ? "sidebarCollapsed" : "tocCollapsed";
    const buttonSelector = kind === "sidebar" ? "[data-lesson-sidebar-toggle]" : "[data-lesson-toc-toggle]";
    const collapsedLabel = kind === "sidebar" ? "Show lesson menu" : "Show on this page panel";
    const expandedLabel = kind === "sidebar" ? "Hide lesson menu" : "Hide on this page panel";
    const collapsedAria = kind === "sidebar" ? "Show lesson menu" : "Show on this page panel";
    const expandedAria = kind === "sidebar" ? "Hide lesson menu" : "Hide on this page panel";

    lessonShells.forEach((shell) => {
      shell.dataset[attribute] = next;
    });

    document.querySelectorAll(buttonSelector).forEach((button) => {
      button.setAttribute("aria-pressed", pressed);
      button.setAttribute("aria-label", collapsed ? collapsedAria : expandedAria);
      button.setAttribute("title", collapsed ? collapsedLabel : expandedLabel);
    });

    syncFloatingBackToTop();
  };

  document.querySelectorAll("[data-aio-search]").forEach((input) => {
    input.addEventListener("input", () => {
      const query = input.value.trim().toLowerCase();
      document.querySelectorAll("[data-aio-episode]").forEach((episode) => {
        const haystack = `${episode.dataset.title || ""} ${episode.textContent || ""}`.toLowerCase();
        episode.style.display = !query || haystack.includes(query) ? "" : "none";
      });
    });
  });

  floatingBackToTopButtons.forEach((button) => {
    button.addEventListener("click", scrollToTop);
  });

  if (lessonShells.length > 0) {
    const sidebarFromStorage = window.localStorage.getItem(lessonSidebarStorageKey);
    const tocFromStorage = window.localStorage.getItem(lessonTocStorageKey);
    applyLessonToggleState("sidebar", sidebarFromStorage === "true");
    applyLessonToggleState("toc", tocFromStorage === "true");

    document.querySelectorAll("[data-lesson-sidebar-toggle]").forEach((button) => {
      button.addEventListener("click", () => {
        const shell = button.closest("[data-lesson-shell]");
        const collapsed = shell?.dataset.sidebarCollapsed !== "true";
        window.localStorage.setItem(lessonSidebarStorageKey, String(collapsed));
        applyLessonToggleState("sidebar", collapsed);
      });
    });

    document.querySelectorAll("[data-lesson-toc-toggle]").forEach((button) => {
      button.addEventListener("click", () => {
        const shell = button.closest("[data-lesson-shell]");
        const collapsed = shell?.dataset.tocCollapsed !== "true";
        window.localStorage.setItem(lessonTocStorageKey, String(collapsed));
        applyLessonToggleState("toc", collapsed);
      });
    });
  }

  document.addEventListener("scroll", syncFloatingBackToTop, { passive: true });
  desktopTocMedia.addEventListener("change", syncFloatingBackToTop);
  syncFloatingBackToTop();
})();
