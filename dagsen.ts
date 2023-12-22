export type Menu = {
  dayname: string;
  main?: string;
  vegetarian?: string;
  salad?: string;
  soup?: string;
  alacarte?: string;
  extra?: string;
};

// TODO: Remove
const client = Deno.createHttpClient({
  proxy: {
    url: "socks5://127.0.0.1:9090",
  },
});

export async function fetchMenu(
  day: 0 | 1 = dayNumber(new Date()),
): Promise<Menu | null> {
  try {
    const res = await fetch(`http://api.teknolog.fi/taffa/sv/json/${day}`, {
      client,
    });
    return res.json();
  } catch (e) {
    console.error("Failed to fetch menu from lunch API.", e);
    return null;
  }
}

function dayNumber(now: Date): 0 | 1 {
  const weekday = now.getDay();
  return 0 < weekday && weekday < 6 && now.getHours() > 16 ? 1 : 0;
}

export async function fetchAlaCarte(): Promise<string | null> {
  try {
    const res = await fetch(
      "http://info.teknolog.fi/82.130.59.164/alacartenumber.txt",
      { client },
    );
    const alacarte = await res.json();
    return isNaN(parseInt(alacarte)) ? null : alacarte;
  } catch (e) {
    console.error("Failed to fetch Á la carte from lunch API.", e);
    return null;
  }
}
