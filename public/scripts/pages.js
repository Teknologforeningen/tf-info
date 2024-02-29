const main = document.getElementById("main");

/** @type {Generator<number, never, never>} */
let pagesIter;

async function changePage() {
  if (!pagesIter) {
    return;
  }

  const pageId = pagesIter.next().value;
  let timeout = 10000;
  try {
    const page = await fetch(`/pages/${pageId}`)
      .then((res) => res.json());
    timeout = page.timeout;
    main.innerHTML = page.html;
  } catch (e) {
    console.error("failed to fetch page", e);
  }
  setTimeout(changePage, timeout);
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
