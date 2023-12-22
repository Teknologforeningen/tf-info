import { serveDir } from "https://deno.land/std@0.207.0/http/file_server.ts";
import { Eta } from "https://deno.land/x/eta@v3.1.0/src/index.ts";
import { fetchAlaCarte, fetchMenu } from "./dagsen.ts";

const CAM_URL = "https://info.teknolog.fi/snapshot.jpg";

const templatePath = Deno.cwd() + "/templates/";
const eta = new Eta({ views: templatePath });

async function handler(req: Request): Promise<Response> {
  const pathname = new URL(req.url).pathname;

  if (pathname.startsWith("/static")) {
    return serveDir(req, {
      fsRoot: "public",
      urlRoot: "static",
    });
  }

  const data = await Promise.all([
    fetchPiTemp(),
    fetchMenu(),
    fetchAlaCarte(),
  ]);

  const body = await eta.renderAsync("./index", {
    piTemp: data[0],
    menu: data[1],
    alacarte: data[2],
    cam: CAM_URL,
  });

  return new Response(body, {
    headers: new Headers({ "Content-Type": "text/html" }),
  });
}

Deno.serve(handler);

async function fetchPiTemp(): Promise<number> {
  const res = await fetch("https://mask.tf.fi/data/pi/temperature");
  return res.json();
}
