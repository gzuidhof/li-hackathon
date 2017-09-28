function getword(info,tab) {
  console.log("Word " + info.selectionText + " was clicked.");
  chrome.tabs.create({
    url: "http://localhost:8080/?q=" + info.selectionText,
  });
}
chrome.contextMenus.create({
  title: "Search: %s",
  contexts:["selection"],
  onclick: getword,
});
