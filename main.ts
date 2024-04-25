import "https://deno.land/std@0.210.0/dotenv/load.ts";
import { serveDir } from "https://deno.land/std@0.207.0/http/file_server.ts";
import { Eta } from "https://deno.land/x/eta@v3.1.0/src/index.ts";
import * as dagsen from "./dagsen/api.ts";
import { createPage, Page } from "./page.ts";
import { helsinkiDate } from "./date.ts";

const {
  CAM_URL,
  YLONZ_DATE,
  VOTES_URL,
  PAGE_TIMEOUT = "10s",
  REFRESH_TIME = "04:00",
} = Deno.env.toObject();

const ylonzDate = new Date(YLONZ_DATE);

const templatePath = Deno.cwd() + "/templates/";
const eta = new Eta({ views: templatePath });

const PAGE_ROUTE = new URLPattern({ pathname: "/pages/:id" });

type PageResponse = {
  id: string;
  timeout: number;
  nextPage: string;
  html: string;
};

const PAGES: readonly Page[] = [
  createPage("dagsen"),
  createPage(
    "countdown",
    () => !isNaN(ylonzDate.getTime()) && ylonzDate.getTime() > Date.now(),
  ),
] as const;

async function handler(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const pathname = url.pathname;

  if (pathname.startsWith("/static")) {
    return serveDir(req, {
      fsRoot: "public",
      urlRoot: "static",
    });
  }

  if (pathname.startsWith("/dagsen")) return dagsenHandler(url.searchParams);

  const pages = PAGES
    .filter((p) => p.condition())
    .map((p) => p.id);

  const pageMatch = PAGE_ROUTE.exec(req.url);
  if (pageMatch) return pageHandler(pages, pageMatch);

  switch (pathname) {
    case "/pi-temp": {
      const html = await eta.renderAsync("pi-temp", {
        piTemp: await fetchPiTemp(),
      });
      return new Response(html, {
        headers: new Headers({ "Content-Type": "text/html" }),
      });
    }
  }

  if (pathname.startsWith("/pages")) {
    return Response.json(pages);
  }

  const renderData = await fetchRenderData(pages, "");
  const body = await eta.renderAsync("index", renderData);
  return new Response(body, {
    headers: new Headers({ "Content-Type": "text/html" }),
  });
}

Deno.serve(handler);

async function pageHandler(pages: readonly string[], match: URLPatternResult): Promise<Response> {
  const pageId = match.pathname.groups.id ?? "";
  if (!pages.includes(pageId)) {
    return new Response("Page not found", { status: 404 });
  }

  const renderData = await fetchRenderData(pages, pageId);
  const html = await eta.renderAsync(pageId, renderData);
  return new Response(html, {
    headers: new Headers({ "Content-Type": "text/html" }),
  });
}

async function dagsenHandler(params: URLSearchParams): Promise<Response> {
  let lang = params.get("lang") as dagsen.Language | null;

  if (lang !== null) {
    const renderData = await fetchDagsenRenderData(lang);
    const html = await eta.renderAsync("dagsen/menu", renderData);
    return new Response(html, {
      headers: new Headers({ "Content-Type": "text/html" }),
    });
  }

  lang = lang ?? "sv";
  if (!dagsen.LANGUAGES.includes(lang)) {
    lang = "sv";
  }

  const renderData = await fetchDagsenRenderData(lang);
  const html = await eta.renderAsync("dagsen/index", renderData);
  return new Response(html, {
    headers: new Headers({ "Content-Type": "text/html" }),
  });
}

async function fetchPiTemp(): Promise<number | null> {
  try {
    const res = await fetch("https://mask.tf.fi/data/pi/temperature");
    return Math.round(await res.json());
  } catch (e: unknown) {
    console.error("Failed to fetch pi temp:", e);
    return null;
  }
}

type RenderData = {
  nextPage: PageResponse["id"];
  pageTimeout: string;
  piTemp: number | null;
  menu: dagsen.Menu | null;
  alacarte: string | null;
  cam: typeof CAM_URL;
  ylonzDate: Date;
  secondsUntilRefresh: number;
  votes: typeof VOTES_URL;
};

async function fetchRenderData(pages: readonly string[], pageId: string): Promise<RenderData> {
  const res = await Promise.all([
    fetchPiTemp(),
    dagsen.fetchMenuJSON(),
    dagsen.fetchAlaCarte(),
  ]);

  return {
    nextPage: nextPage(pages, pageId),
    pageTimeout: PAGE_TIMEOUT,
    piTemp: res[0],
    menu: res[1],
    alacarte: res[2],
    cam: `${CAM_URL}?${Date.now()}`,
    votes: VOTES_URL,
    ylonzDate,
    secondsUntilRefresh: calculateSecondsUntilRefresh(
      helsinkiDate(),
      REFRESH_TIME,
    ),
  };
}

type DagsenRenderData = {
  date: string;
  menuItems: string[];
  openTime: string;
  nextPage: string;
  pageTimeout: string;
};

async function fetchDagsenRenderData(language: dagsen.Language): Promise<DagsenRenderData> {
  const now = new Date();

  const date = now.toLocaleDateString("en-GB", { year: "2-digit", month: "2-digit", "day": "2-digit" })
    .split("/")
    .slice(0, 2)
    .join("/");

  const menuItems = (await dagsen.fetchMenuText(language))?.split("\r\n") ?? [];

  return {
    date,
    menuItems: menuItems,
    openTime: dagsen.openTime(now),
    nextPage: nextDagsenPage(dagsen.LANGUAGES, language),
    pageTimeout: "5s",
  };
}

/**
 * @param refreshTime time in format of HH:MM
 */
function calculateSecondsUntilRefresh(now: Date, refreshTime: string): number {
  const [hours, minutes] = refreshTime.split(":");
  const refreshDate = new Date(now);
  refreshDate.setHours(parseInt(hours), parseInt(minutes));

  // Page should be updated 'today'
  if (now.getTime() < refreshDate.getTime()) {
    return (refreshDate.getTime() - now.getTime()) / 1000;
  }

  refreshDate.setDate(now.getDate() + 1);
  return (refreshDate.getTime() - now.getTime()) / 1000;
}

function nextPage(pages: readonly string[], currentPage: PageResponse["id"]): PageResponse["id"] {
  const pagesLength = pages.length;
  const nextIndex = pages.indexOf(currentPage) + 1;
  return `/pages/${pages[nextIndex % pagesLength]}`;
}

function nextDagsenPage(languages: readonly dagsen.Language[], currentLanguage: dagsen.Language): string {
  const languagesLength = languages.length;
  const nextIndex = languages.indexOf(currentLanguage) + 1;
  return `/dagsen?lang=${languages[nextIndex % languagesLength]}`;
}
