const main = document.getElementById("main");

/** @type {Generator<number, never, never>} */
let pagesIter;

async function changePage() {
  if (!pagesIter) {
    return;
  }

  const pageId = pagesIter.next().value
  const page = await fetch(`/pages/${pageId}`)
    .then((res) => res.text());
  main.innerHTML = page;

  setTimeout(changePage, 5000);
}

fetch("/pages")
  .then((res) => res.json())
  .then((p) => {
    const length = p.length;
    function* pages() {
      let count = 0;
      while (true) {
        const index = count % length;
        yield p[index];
        count++;
      }
    }
    pagesIter = pages();
  })
  .then(() => changePage());
