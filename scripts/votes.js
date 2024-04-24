let votes = document.getElementById("votes");
const INITIAL_VOTE_MAIN_WIDTH = 32;
const VOTE_COL_WIDTH = 20;

// Votes returns some styles without a property,
// which makes the browser render them wrong.
// This *could* be fixed with JS, but the JS doesn't return the properties correctly either.
const votesRegex = /((?:width|left): ?\d{1,3})(?!px)(;|")/g;

/**
 * voteMain has a hardcoded width of 32px, which is not the actual width of the element,
 * by setting the correct width the element will be centered correctly.
 */
function centerVotes() {
  if (!votes) {
    votes = document.getElementById("votes");
  }
  votes.innerHTML = votes.innerHTML.replace(votesRegex, "$1px$2");
  const voteMain = votes.querySelector("#voteMain");
  voteMain.style.width = votesWidth(voteMain) + "px";
}

function votesWidth(voteMain) {
  let width = INITIAL_VOTE_MAIN_WIDTH;
  const children = voteMain.children;
  for (let i = 0; i < children.length; i++) {
    const c = children[i];
    const w = parseInt(c.style.left.replace("px", ""));
    if (w > width) {
      width = w;
    }
  }
  return width + VOTE_COL_WIDTH;
}
