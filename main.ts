import "https://deno.land/std@0.210.0/dotenv/load.ts";
import { serveDir } from "https://deno.land/std@0.207.0/http/file_server.ts";
import { Eta } from "https://deno.land/x/eta@v3.1.0/src/index.ts";
import { fetchAlaCarte, fetchMenu, Menu } from "./dagsen.ts";
import { Page } from "./page.ts";
import { createPage } from "./page.ts";

const {
  CAM_URL,
  YLONZ_DATE,
  PAGE_TIMEOUT = 10000,
  REFRESH_TIME = "14:00",
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

  const renderData = await fetchRenderData();

  const pages = PAGES
    .filter((p) => p.condition())
    .map((p) => p.id);

  const pageMatch = PAGE_ROUTE.exec(req.url);
  if (pageMatch) {
    let pageId = pageMatch.pathname.groups.id ?? "";
    if (!pages.includes(pageId)) {
      const pageNumber = parseInt(pageId);
      if (0 <= pageNumber && pageNumber < pages.length) {
        pageId = pages[pageNumber];
      } else {
        return new Response("Page not found", { status: 404 });
      }
    }

    const html = await eta.renderAsync(pageId, renderData);

    const page: PageResponse = {
      id: pageId,
      nextPage: nextPage(pages, pageId),
      timeout: PAGE_TIMEOUT as number,
      html,
    };

    return Response.json(page);
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

async function fetchPiTemp(): Promise<number> {
  const res = await fetch("https://mask.tf.fi/data/pi/temperature");
  return res.json();
}

type RenderData = {
  piTemp: number;
  menu: Menu | null;
  alacarte: string | null;
  cam: typeof CAM_URL;
  ylonzDate: Date;
  secondsUntilRefresh: number;
};

async function fetchRenderData(): Promise<RenderData> {
  const res = await Promise.all([
    fetchPiTemp(),
    fetchMenu(),
    fetchAlaCarte(),
  ]);

  return {
    piTemp: res[0],
    menu: res[1],
    alacarte: res[2],
    cam: CAM_URL,
    ylonzDate,
    secondsUntilRefresh: calculateSecondsUntilRefresh(new Date(), REFRESH_TIME),
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
  return pages[nextIndex % pagesLength];
}
