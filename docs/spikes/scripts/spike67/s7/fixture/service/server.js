// Tiny service: GET /hello?name=x -> {"greeting":"hello x"}; POST /count -> {"count":n}
// PORT=0 picks a free port; the chosen port is printed as "LISTENING <port>".
// FAIL_START=1 exits before listening (to simulate a broken build).
const http = require("http");
if (process.env.FAIL_START) { console.error("boom: refusing to start"); process.exit(3); }
let count = 0;
const s = http.createServer((q, r) => {
  const u = new URL(q.url, "http://x");
  r.setHeader("content-type", "application/json");
  if (u.pathname === "/hello") return r.end(JSON.stringify({ greeting: "hello " + (u.searchParams.get("name") || "world") }));
  if (u.pathname === "/count" && q.method === "POST") return r.end(JSON.stringify({ count: ++count }));
  r.statusCode = 404; r.end("{}");
});
s.listen(Number(process.env.PORT || 0), "127.0.0.1", () => console.log("LISTENING " + s.address().port));
