import { render } from "../render.ts";
import * as dagsen from "./api.ts";

export async function dagsenHandler(params: URLSearchParams): Promise<Response> {
  let lang = params.get("lang") as dagsen.Language | null;

  if (lang !== null) {
    const renderData = await fetchRenderData(lang);
    return render("/dagsen/menu", renderData);
  }

  lang = lang ?? "sv";
  if (!dagsen.LANGUAGES.includes(lang)) {
    lang = "sv";
  }

  const renderData = await fetchRenderData(lang);
  return render("/dagsen/index", renderData);
}

type RenderData = {
  date: string;
  menuItems: string[];
  openTime: string;
  nextPage: string;
  pageTimeout: string;
};

async function fetchRenderData(language: dagsen.Language): Promise<RenderData> {
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

function nextDagsenPage(languages: readonly dagsen.Language[], currentLanguage: dagsen.Language): string {
  const languagesLength = languages.length;
  const nextIndex = languages.indexOf(currentLanguage) + 1;
  return `/dagsen?lang=${languages[nextIndex % languagesLength]}`;
}
