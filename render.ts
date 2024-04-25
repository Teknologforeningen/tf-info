import { Eta } from "eta";

const templatePath = Deno.cwd() + "/templates/";
const eta = new Eta({ views: templatePath });

export async function render(template: string, data: object): Promise<Response> {
  const html = await eta.renderAsync(template, data);
  return new Response(html, {
    headers: new Headers({ "Content-Type": "text/html" }),
  });
}
