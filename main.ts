import "https://deno.land/std@0.210.0/dotenv/load.ts";
import { serveDir } from "https://deno.land/std@0.207.0/http/file_server.ts";
import { Eta } from "https://deno.land/x/eta@v3.1.0/src/index.ts";
import { fetchAlaCarte, fetchMenu, Menu } from "./dagsen.ts";
import { Page } from "./page.ts";
import { createPage } from "./page.ts";
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
  const pathname = new URL(req.url).pathname;

  if (pathname.startsWith("/static")) {
    return serveDir(req, {
      fsRoot: "public",
      urlRoot: "static",
    });
  }

  const pages = PAGES
    .filter((p) => p.condition())
    .map((p) => p.id);

  const pageMatch = PAGE_ROUTE.exec(req.url);
  if (pageMatch) return pageHandler(pages, pageMatch);

  const renderData = await fetchRenderData(pages, "");

  switch (pathname) {
    case "/pi-temp": {
      const html = await eta.renderAsync("pi-temp", renderData);
      return new Response(html);
    }
  }

  if (pathname.startsWith("/pages")) {
    return Response.json(pages);
  }

  const body = await eta.renderAsync("index", renderData);

  return new Response(body, {
    headers: new Headers({ "Content-Type": "text/html" }),
  });
}

Deno.serve(handler);

async function pageHandler(
  pages: readonly string[],
  match: URLPatternResult,
): Promise<Response> {
  const pageId = match.pathname.groups.id ?? "";
  if (!pages.includes(pageId)) {
    return new Response("Page not found", { status: 404 });
  }

  const renderData = await fetchRenderData(pages, pageId);
  const html = await eta.renderAsync(pageId, renderData);
  return new Response(html);
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
  menu: Menu | null;
  alacarte: string | null;
  cam: typeof CAM_URL;
  ylonzDate: Date;
  secondsUntilRefresh: number;
  votes: typeof VOTES_URL;
};

async function fetchRenderData(
  pages: readonly string[],
  pageId: string,
): Promise<RenderData> {
  const res = await Promise.all([
    fetchPiTemp(),
    fetchMenu(),
    fetchAlaCarte(),
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

function nextPage(
  pages: readonly string[],
  currentPage: PageResponse["id"],
): PageResponse["id"] {
  const pagesLength = pages.length;
  const nextIndex = pages.indexOf(currentPage) + 1;
  return `/pages/${pages[nextIndex % pagesLength]}`;
}
