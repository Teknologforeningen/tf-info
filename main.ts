import "@std/dotenv";

import { serveDir } from "@std/http";
import { fetchPageData, PAGE_ROUTE, pageHandler, PAGES } from "./members/handler.ts";
import { env } from "./env.ts";
import { fetchPiTemp } from "./members/pi.ts";
import { render } from "./render.ts";
import { dagsenHandler } from "./dagsen/handler.ts";

async function handler(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const pathname = url.pathname;

  // handle static before anything else
  if (pathname.startsWith("/static")) {
    return serveDir(req, {
      fsRoot: "public",
      urlRoot: "static",
    });
  }

  const pages = PAGES
    .filter((p) => p.condition(env.ylonzDate))
    .map((p) => p.id);

  // special cases e.g. path variables
  const pageMatch = PAGE_ROUTE.exec(req.url);
  if (pageMatch) return pageHandler(pages, pageMatch);

  // paths
  switch (pathname) {
    case "/pi-temp": {
      return render("/members/pi-temp", { piTemp: await fetchPiTemp() });
    }
    case "/dagsen": {
      return dagsenHandler(url.searchParams);
    }

    default: {
      const renderData = await fetchPageData(pages, "");
      return render("/members/index", renderData);
    }
  }
}

Deno.serve(handler);
