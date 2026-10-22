const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Menú para celulares
const toggle = document.getElementById("nav-toggle");
const nav = document.getElementById("nav");

function closeMenu() {
  nav.classList.remove("is-open");
  toggle.setAttribute("aria-expanded", "false");
  toggle.setAttribute("aria-label", "Abrir menú");
  onScroll();
}

toggle.addEventListener("click", () => {
  const open = nav.classList.toggle("is-open");
  toggle.setAttribute("aria-expanded", String(open));
  toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  onScroll();
});

nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));

// El encabezado pasa de transparente a "vidrio" al bajar (o al abrir el menú)
const header = document.getElementById("header");
const onScroll = () =>
  header.classList.toggle("is-scrolled", window.scrollY > 40 || nav.classList.contains("is-open"));
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

// Año actual en el pie de página
document.getElementById("year").textContent = new Date().getFullYear();

// Pestañas accesibles (carrusel de portada y sectores), con flechas del teclado
function setupTabs(tabs, onSelect) {
  function select(tab) {
    tabs.forEach((t) => {
      const active = t === tab;
      t.classList.toggle("is-active", active);
      t.setAttribute("aria-selected", String(active));
      t.tabIndex = active ? 0 : -1;
    });
    onSelect(tab);
  }

  tabs.forEach((tab, i) => {
    tab.addEventListener("click", () => select(tab));
    tab.addEventListener("keydown", (e) => {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      const next = tabs[(i + (e.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length];
      select(next);
      next.focus();
    });
  });

  return select;
}

// Carrusel de la portada
const hero = document.querySelector(".hero");
const heroTabs = [...document.querySelectorAll(".hero__tab")];
const slides = heroTabs.map((t) => document.getElementById(t.getAttribute("aria-controls")));
const SLIDE_TIME = 7000;
let timer = null;
let paused = reduceMotion;

hero.style.setProperty("--slide-time", SLIDE_TIME + "ms");

// Con JavaScript las diapositivas se ocultan con opacidad (para el fundido) en lugar de "hidden"
slides.forEach((s) => {
  s.hidden = false;
  if (!s.classList.contains("is-active")) {
    s.inert = true;
    s.setAttribute("aria-hidden", "true");
  }
});

// Las imágenes de las diapositivas ocultas usan data-src/data-srcset para no competir con la carga inicial
function loadSlideImages(slide) {
  slide.querySelectorAll("img[data-src]").forEach((img) => {
    img.srcset = img.dataset.srcset;
    img.src = img.dataset.src;
    img.removeAttribute("data-src");
    img.removeAttribute("data-srcset");
  });
}
window.addEventListener("load", () => {
  const loadAll = () => slides.forEach(loadSlideImages);
  if ("requestIdleCallback" in window) requestIdleCallback(loadAll, { timeout: 2000 });
  else setTimeout(loadAll, 1000);
});

const selectSlide = setupTabs(heroTabs, (tab) => {
  slides.forEach((s) => {
    const active = s.id === tab.getAttribute("aria-controls");
    if (active) loadSlideImages(s);
    s.classList.toggle("is-active", active);
    s.inert = !active;
    s.setAttribute("aria-hidden", String(!active));
  });
  // En celular, desplaza la fila de pestañas para que se vea la activa
  tab.parentElement.scrollTo({ left: tab.offsetLeft - 20, behavior: reduceMotion ? "auto" : "smooth" });
  // Reinicia la barra de progreso
  const bar = tab.querySelector(".hero__progress");
  bar.style.animation = "none";
  void bar.offsetWidth;
  bar.style.animation = "";
  schedule();
});

function schedule() {
  clearTimeout(timer);
  if (paused) return;
  timer = setTimeout(() => {
    const i = heroTabs.findIndex((t) => t.classList.contains("is-active"));
    selectSlide(heroTabs[(i + 1) % heroTabs.length]);
  }, SLIDE_TIME);
}

const pauseBtn = document.getElementById("hero-pause");
function setPaused(value) {
  paused = value;
  hero.classList.toggle("is-paused", paused);
  pauseBtn.setAttribute("aria-label", paused ? "Reproducir el carrusel" : "Pausar el carrusel");
  if (paused) {
    clearTimeout(timer);
  } else {
    selectSlide(heroTabs.find((t) => t.classList.contains("is-active")));
  }
}
pauseBtn.addEventListener("click", () => setPaused(!paused));
setPaused(paused);

// Enlace directo a una diapositiva, por ejemplo fdpsoftware.com/#slide-4
const linkedTab = heroTabs.find((t) => "#" + t.getAttribute("aria-controls") === location.hash);
if (linkedTab) selectSlide(linkedTab);

// Pausa automática cuando la hoja de contenido tapa la portada
// (la portada es "sticky", así que siempre cuenta como visible para el navegador)
let userPaused = false;
pauseBtn.addEventListener("click", () => (userPaused = paused));
window.addEventListener("scroll", () => {
  if (userPaused || reduceMotion) return;
  const covered = window.scrollY > hero.offsetHeight * 0.7;
  if (covered !== paused) setPaused(covered);
}, { passive: true });

// Pestañas de sectores
const sectorTabs = [...document.querySelectorAll(".pill")];
setupTabs(sectorTabs, (tab) => {
  sectorTabs.forEach((t) => {
    document.getElementById(t.getAttribute("aria-controls")).hidden = t !== tab;
  });
});

// Botones del carril de soluciones
const rail = document.getElementById("rail");
document.querySelectorAll("[data-rail]").forEach((btn) => {
  btn.addEventListener("click", () => {
    rail.scrollBy({ left: Number(btn.dataset.rail) * 340, behavior: reduceMotion ? "auto" : "smooth" });
  });
});

// Aparición suave de los elementos al hacer scroll
const revealItems = document.querySelectorAll(".section__head, .rail-card, .feature, .media-card, .sector, .quote, .step, .about, .brand, .app-card, .team__card");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  revealItems.forEach((el) => {
    el.classList.add("reveal");
    observer.observe(el);
  });
}
