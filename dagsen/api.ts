import { helsinkiDate } from "../date.ts";

export type Menu = {
  dayname: string;
  main?: string;
  vegetarian?: string;
  salad?: string;
  soup?: string;
  alacarte?: string;
  extra?: string;
};

export const LANGUAGES = ["sv", "fi", "en"] as const;
export type Language = typeof LANGUAGES[number];

export async function fetchMenuJSON(day: 0 | 1 = dayNumber(helsinkiDate())): Promise<Menu | null> {
  try {
    const res = await fetch(`http://newapi.tf.fi/taffa/sv/json/${day}`);
    const obj = await res.json();

    const mappedMenu: Menu = {
      dayname: obj["dayName"],
      main: obj["Fisk/Kött"],
      vegetarian: obj["Vegetariskt alternativ"],
      salad: obj["Sallad"],
      soup: obj["Soppa"],
      alacarte: obj["A la carte"]
    };
    return mappedMenu;
  } catch (e) {
    console.error("Failed to fetch menu from lunch API:", e);
    return null;
  }
}

export async function fetchMenuText(lang: Language): Promise<string | null> {
  try {
    const res = await fetch(`http://newapi.tf.fi/taffa/${lang}/today`);
    return await res.text();
  } catch (e) {
    console.error("Failed to fetch menu from lunch API:", e);
    return null;
  }
}

function dayNumber(now: Date): 0 | 1 {
  const weekday = now.getDay();
  return 0 < weekday && weekday < 6 && now.getHours() >= 15 ? 1 : 0;
}

export async function fetchAlaCarte(): Promise<string | null> {
  try {
    const res = await fetch(
      "http://info.teknolog.fi/82.130.59.164/alacartenumber.txt",
    );
    const alacarte = await res.json();
    return isNaN(parseInt(alacarte)) ? null : alacarte;
  } catch (e) {
    console.error("Failed to fetch Á la carte from lunch API:", e);
    return null;
  }
}

export function openTime(now: Date): string {
  const weekday = now.getDay();
  return 0 < weekday && weekday < 6 ? "10:30 - 15:00" : "";
}
