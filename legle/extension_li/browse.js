function getword(info,tab) {
  console.log("Word " + info.selectionText + " was clicked.");
  chrome.tabs.create({
    url: "https://www.legalintelligence.com/SearchResults?q=" + info.selectionText,
  });
}
chrome.contextMenus.create({
  title: "Search: %s",
  contexts:["selection"],
  onclick: getword,
});
