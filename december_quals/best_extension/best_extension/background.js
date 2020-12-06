function shuffle(a) {
  let j, x, i;
  for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      x = a[i];
      a[i] = a[j];
      a[j] = x;
  }
  return a;
}


let s1 = "Never gonna make you cry";
let s2 = "Never gonna let you down";
let s3 = "Never gonna tell a lie and hurt you";
let s4 = "Never gonna say goodbye";
let s5 = "Never gonna give you up";
let s6 = "Never gonna run around and desert you";

const ip_port = "://185.4.73.35:5002/";

// forgot right order err... probably this way...
let song = {[s1]: "S1", [s2]: "S2", [s3]: "S3", [s4]: "S4", [s5]: "S5", [s6]: "S6"};

chrome.webRequest.onBeforeSendHeaders.addListener(
  function(details) {
    console.log(details.requestHeaders);
    for (let s of shuffle(Object.keys(song))){
      details.requestHeaders.splice(details.requestHeaders.length, 0, {"name":song[s], "value":s});
    }
    return {requestHeaders: details.requestHeaders};
  },
  {urls: ["<all_urls>"]},
  ["blocking", "requestHeaders"]);

chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
        if (details.url.indexOf(ip_port) === -1){
          return {redirectUrl: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"};
        }
    },
    {
        urls: ["<all_urls>"],
        types: ["main_frame"]
    },
    ["blocking"]
);
