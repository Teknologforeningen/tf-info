export function helsinkiDate(): Date {
  return new Date(
    new Date().toLocaleString("en-US", { timeZone: "Europe/Helsinki" }),
  );
}
