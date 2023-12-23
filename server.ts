import "https://deno.land/std@0.210.0/dotenv/load.ts";
import { serveDir } from "https://deno.land/std@0.207.0/http/file_server.ts";
import { Eta } from "https://deno.land/x/eta@v3.1.0/src/index.ts";
import { fetchAlaCarte, fetchMenu, Menu } from "./dagsen.ts";

// TODO: Make page refresh at night

const {
  CAM_URL,
} = Deno.env.toObject();

const templatePath = Deno.cwd() + "/templates/";
const eta = new Eta({ views: templatePath });

const PAGE_ROUTE = new URLPattern({ pathname: "/pages/:id" });

const PAGES = ["countdown", "dagsen"];

async function handler(req: Request): Promise<Response> {
  const pathname = new URL(req.url).pathname;

  if (pathname.startsWith("/static")) {
    return serveDir(req, {
      fsRoot: "public",
      urlRoot: "static",
    });
  }

  const renderData = await fetchRenderData()

  const pageMatch = PAGE_ROUTE.exec(req.url);
  if (pageMatch) {
    const page = pageMatch.pathname.groups.id ?? "";

    if (!PAGES.includes(page)) {
      return new Response("Page not found", { status: 404 });
    }

    const body = await eta.renderAsync(page, renderData);
    return new Response(body, {
      headers: new Headers({ "Content-Type": "text/html" }),
    });
  }
  if (pathname.startsWith("/pages")) {
    return Response.json(PAGES);
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
  };
}
