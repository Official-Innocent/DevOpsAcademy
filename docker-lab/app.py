#!/usr/bin/env python3
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

OWNER = os.getenv('OWNER_NAME', 'Innocent Obute')
PORT = int(os.getenv('PORT', 5000))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CamSync — Photographer Time Reference</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}

  body {{
    background:#080808;
    color:#fff;
    font-family:'Courier New',monospace;
    min-height:100vh;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    padding:2rem 1rem;
  }}

  .app-title {{
    font-size:clamp(2.5rem,8vw,5rem);
    font-weight:900;
    letter-spacing:0.15em;
    text-transform:uppercase;
    margin-bottom:0.2rem;
    background: linear-gradient(90deg,#ffffff,#e85d04);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
  }}

  .app-sub {{
    font-size:0.7rem;
    letter-spacing:0.5em;
    color:#444;
    text-transform:uppercase;
    margin-bottom:0.5rem;
  }}

  .by-line {{
    font-size:0.65rem;
    color:#333;
    letter-spacing:0.3em;
    text-transform:uppercase;
    margin-bottom:3rem;
  }}

  .by-line span {{ color:#e85d04; }}

  .tz-selector {{
    margin-bottom:2.5rem;
    text-align:center;
  }}

  .tz-selector label {{
    font-size:0.65rem;
    letter-spacing:0.4em;
    color:#444;
    text-transform:uppercase;
    display:block;
    margin-bottom:0.6rem;
  }}

  .tz-selector select {{
    background:#111;
    color:#fff;
    border:1px solid #222;
    padding:0.6rem 1.2rem;
    font-family:'Courier New',monospace;
    font-size:0.85rem;
    letter-spacing:0.1em;
    cursor:pointer;
    outline:none;
    border-radius:2px;
    min-width:280px;
  }}

  .tz-selector select:focus {{
    border-color:#e85d04;
  }}

  .clock-wrapper {{
    text-align:center;
    margin-bottom:2.5rem;
  }}

  .tz-badge {{
    font-size:0.65rem;
    letter-spacing:0.5em;
    color:#444;
    text-transform:uppercase;
    margin-bottom:1rem;
  }}

  .time {{
    font-size:clamp(4rem,15vw,10rem);
    font-weight:900;
    letter-spacing:0.05em;
    line-height:1;
    font-variant-numeric:tabular-nums;
  }}

  .milliseconds {{
    font-size:clamp(1.5rem,5vw,3rem);
    color:#e85d04;
    letter-spacing:0.1em;
    margin-top:0.4rem;
    font-variant-numeric:tabular-nums;
  }}

  .date {{
    font-size:clamp(0.9rem,2.5vw,1.3rem);
    color:#555;
    letter-spacing:0.2em;
    margin-top:1.2rem;
    text-transform:uppercase;
  }}

  .offset-badge {{
    display:inline-block;
    border:1px solid #e85d04;
    color:#e85d04;
    font-size:0.65rem;
    letter-spacing:0.3em;
    padding:0.25rem 0.8rem;
    margin-top:1.2rem;
    text-transform:uppercase;
  }}

  .divider {{
    width:40px;
    height:1px;
    background:#1a1a1a;
    margin:2rem auto;
  }}

  .sync-guide {{
    text-align:center;
    max-width:480px;
    width:100%;
    padding:0 1rem;
  }}

  .sync-guide h2 {{
    font-size:0.65rem;
    letter-spacing:0.5em;
    color:#333;
    text-transform:uppercase;
    margin-bottom:1.2rem;
  }}

  .steps {{
    list-style:none;
    text-align:left;
  }}

  .steps li {{
    font-size:0.78rem;
    color:#444;
    padding:0.5rem 0;
    border-bottom:1px solid #111;
    display:flex;
    gap:1rem;
    align-items:center;
  }}

  .steps li span {{
    color:#e85d04;
    min-width:1.5rem;
    font-size:0.65rem;
  }}

  .footer {{
    margin-top:3rem;
    font-size:0.6rem;
    color:#222;
    letter-spacing:0.25em;
    text-transform:uppercase;
    text-align:center;
  }}

  .footer a {{
    color:#333;
    text-decoration:none;
  }}

  .footer a:hover {{ color:#e85d04; }}

  .pulse {{
    display:inline-block;
    width:5px;
    height:5px;
    border-radius:50%;
    background:#e85d04;
    margin-right:0.4rem;
    animation:pulse 1s infinite;
  }}

  @keyframes pulse {{
    0%,100%{{opacity:1}}
    50%{{opacity:0.15}}
  }}
</style>
</head>
<body>

<div class="app-title">CamSync</div>
<div class="app-sub">Photographer Time Reference Tool</div>
<div class="by-line">by <span>{owner}</span></div>

<div class="tz-selector">
  <label>Select timezone</label>
  <select id="tz-select" onchange="setTZ(this.value)">
    <option value="0" selected>GMT +0 — London (winter), Reykjavik, Accra</option>
    <option value="1">GMT +1 — London (summer/BST), Lagos, Paris, Berlin</option>
    <option value="2">GMT +2 — Cairo, Johannesburg, Athens, Kiev</option>
    <option value="3">GMT +3 — Nairobi, Moscow, Riyadh, Istanbul</option>
    <option value="4">GMT +4 — Dubai, Baku, Tbilisi</option>
    <option value="5">GMT +5 — Karachi, Tashkent, Yekaterinburg</option>
    <option value="5.5">GMT +5:30 — Mumbai, New Delhi, Colombo</option>
    <option value="6">GMT +6 — Dhaka, Almaty, Omsk</option>
    <option value="7">GMT +7 — Bangkok, Jakarta, Hanoi</option>
    <option value="8">GMT +8 — Singapore, Beijing, Perth, Hong Kong</option>
    <option value="9">GMT +9 — Tokyo, Seoul, Pyongyang</option>
    <option value="9.5">GMT +9:30 — Adelaide, Darwin</option>
    <option value="10">GMT +10 — Sydney, Melbourne, Brisbane</option>
    <option value="12">GMT +12 — Auckland, Fiji</option>
    <option value="-1">GMT -1 — Azores, Cape Verde</option>
    <option value="-3">GMT -3 — Buenos Aires, Sao Paulo</option>
    <option value="-4">GMT -4 — New York (summer/EDT), Santiago</option>
    <option value="-5">GMT -5 — New York (winter/EST), Toronto, Bogota</option>
    <option value="-6">GMT -6 — Chicago, Mexico City, Guatemala</option>
    <option value="-7">GMT -7 — Denver, Phoenix, Calgary</option>
    <option value="-8">GMT -8 — Los Angeles, Vancouver, Seattle</option>
    <option value="-9">GMT -9 — Anchorage, Alaska</option>
    <option value="-10">GMT -10 — Honolulu, Hawaii</option>
  </select>
</div>

<div class="clock-wrapper">
  <div class="tz-badge" id="tz-label">
    <span class="pulse"></span>Greenwich Mean Time &mdash; UTC &plusmn; 0
  </div>
  <div class="time" id="time">00:00:00</div>
  <div class="milliseconds" id="ms">.000</div>
  <div class="date" id="date">Loading...</div>
  <div class="offset-badge" id="offset-badge">UTC &plusmn; 0</div>
</div>

<div class="divider"></div>

<div class="sync-guide">
  <h2>How to sync your camera</h2>
  <ul class="steps">
    <li><span>01</span>Select your local timezone above</li>
    <li><span>02</span>Open your camera date/time settings</li>
    <li><span>03</span>Match hours, minutes and seconds exactly</li>
    <li><span>04</span>Confirm when the seconds digit ticks over</li>
    <li><span>05</span>All cameras on set now share one reference time</li>
  </ul>
</div>

<div class="footer">
  <a href="https://github.com/Official-Innocent" target="_blank">
    github.com/Official-Innocent
  </a>
  &nbsp;&mdash;&nbsp; Built with Docker &middot; Python &middot; DevOps
</div>

<script>
  const days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const months=['January','February','March','April','May','June',
                'July','August','September','October','November','December'];

  let offsetHours = 0;

  function pad(n,len){{ return String(n).padStart(len,'0'); }}

  function setTZ(val) {{
    offsetHours = parseFloat(val);
    const select = document.getElementById('tz-select');
    const label = select.options[select.selectedIndex].text;
    document.getElementById('tz-label').innerHTML =
      '<span class="pulse"></span>' + label;
    const sign = offsetHours >= 0 ? '+' : '';
    const display = Number.isInteger(offsetHours)
      ? sign + offsetHours + ':00'
      : sign + Math.trunc(offsetHours) + ':30';
    document.getElementById('offset-badge').textContent = 'UTC ' + display;
  }}

  function tick() {{
    const now = new Date();
    const utcMs = now.getTime();
    const local = new Date(utcMs + (offsetHours * 3600000));

    const h = pad(local.getUTCHours(),2);
    const m = pad(local.getUTCMinutes(),2);
    const s = pad(local.getUTCSeconds(),2);
    const ms = pad(local.getUTCMilliseconds(),3);

    document.getElementById('time').textContent = h+':'+m+':'+s;
    document.getElementById('ms').textContent = '.'+ms;
    document.getElementById('date').textContent =
      days[local.getUTCDay()] + ' ' +
      local.getUTCDate() + ' ' +
      months[local.getUTCMonth()] + ' ' +
      local.getUTCFullYear();
  }}

  setInterval(tick, 50);
  tick();
</script>
</body>
</html>"""

class CamSyncHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        page = HTML.format(owner=OWNER)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(page.encode())

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    print(f"CamSync starting on port {PORT}")
    print(f"Owner: {OWNER}")
    HTTPServer(('0.0.0.0', PORT), CamSyncHandler).serve_forever()
