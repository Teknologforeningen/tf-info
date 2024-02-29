const main = document.getElementById("main");

let nextPage;

async function changePage() {
  let timeout = 10000;
  try {
    const page = await fetch(`/pages/${nextPage ?? 0}`)
      .then((res) => res.json());
    nextPage = page.nextPage;
    timeout = page.timeout;
    main.innerHTML = page.html;
  } catch (e) {
    console.error("failed to fetch page", e);
  }
  setTimeout(changePage, timeout);
}

changePage();
