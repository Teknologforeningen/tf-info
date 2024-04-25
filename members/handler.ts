import { fetchPiTemp } from "./pi.ts";
import { env } from "../env.ts";
import * as dagsen from "../dagsen/api.ts";
import { render } from "../render.ts";
import { helsinkiDate } from "../date.ts";

export async function pageHandler(pages: readonly string[], match: URLPatternResult): Promise<Response> {
  const pageId = match.pathname.groups.id ?? "";
  if (!pages.includes(pageId)) {
    return new Response("Page not found", { status: 404 });
  }

  const pageData = await fetchPageData(pages, pageId);
  return render(`/members/${pageId}`, pageData);
}

export const PAGE_ROUTE = new URLPattern({ pathname: "/pages/:id" });

export interface Page {
  id: string;
  condition: (x?: unknown) => boolean;
}

export const PAGES = [
  createPage("dagsen"),
  createPage(
    "countdown",
    (ylonzDate: unknown) => {
      const date = ylonzDate as Date;
      return !isNaN(date.getTime()) && date.getTime() > Date.now();
    },
  ),
] as const;

function createPage(id: string, condition?: (x?: unknown) => boolean): Page {
  return {
    id,
    condition: condition ?? (() => true),
  };
}

export function nextPage(pages: readonly string[], currentPage: string): string {
  const pagesLength = pages.length;
  const nextIndex = pages.indexOf(currentPage) + 1;
  return `/pages/${pages[nextIndex % pagesLength]}`;
}

type PageData = {
  nextPage: string;
  pageTimeout: string;
  piTemp: number | null;
  menu: dagsen.Menu | null;
  alacarte: string | null;
  cam: string;
  ylonzDate: Date;
  secondsUntilRefresh: number;
  votes: string;
};

export async function fetchPageData(pages: readonly string[], pageId: string): Promise<PageData> {
  const res = await Promise.all([
    fetchPiTemp(),
    dagsen.fetchMenuJSON(),
    dagsen.fetchAlaCarte(),
  ]);

  return {
    nextPage: nextPage(pages, pageId),
    pageTimeout: env.pageTimeout,
    piTemp: res[0],
    menu: res[1],
    alacarte: res[2],
    cam: `${env.camUrl}?${Date.now()}`,
    votes: env.votesUrl,
    ylonzDate: env.ylonzDate,
    secondsUntilRefresh: calculateSecondsUntilRefresh(helsinkiDate(), env.refreshTime),
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
