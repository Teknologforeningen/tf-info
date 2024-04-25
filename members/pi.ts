export async function fetchPiTemp(): Promise<number | null> {
  try {
    const res = await fetch("https://mask.tf.fi/data/pi/temperature");
    return Math.round(await res.json());
  } catch (e: unknown) {
    console.error("Failed to fetch pi temp:", e);
    return null;
  }
}
