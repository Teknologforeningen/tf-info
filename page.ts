export interface Page {
  id: string;
  condition: () => boolean;
}

export function createPage(id: string, condition?: () => boolean): Page {
  return {
    id,
    condition: condition ?? (() => true),
  };
}
