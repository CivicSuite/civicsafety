"""HTML landing surface for the CivicSafety runtime."""


def render_public_lookup_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CivicSafety v0.1.0</title>
  <style>
    :root{--ink:#13211d;--muted:#52625d;--line:#cfe1d8;--paper:#f7fbf8;--card:#ffffff;--accent:#0b6b4f;--gold:#c78618}
    *{box-sizing:border-box}body{margin:0;font-family:Georgia,'Times New Roman',serif;background:radial-gradient(circle at top left,#dff2e8,transparent 32rem),linear-gradient(135deg,#fbfff9,#eef7f1);color:var(--ink)}
    main{max-width:1120px;margin:0 auto;padding:3rem 1.25rem}.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:2rem;align-items:center}
    h1{font-size:clamp(2.5rem,7vw,5rem);line-height:.92;margin:.25rem 0}.eyebrow{font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
    p{font-size:1.08rem;line-height:1.65;color:var(--muted)}.panel,.card{background:rgba(255,255,255,.86);border:1px solid var(--line);border-radius:28px;box-shadow:0 20px 60px rgba(19,33,29,.1)}
    .panel{padding:1.5rem}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:2rem 0}.card{padding:1.2rem}.card h2{margin-top:0;color:var(--accent)}
    code{background:#e8f4ed;padding:.15rem .35rem;border-radius:.35rem}.boundary{border-left:6px solid var(--gold);padding-left:1rem}
    a{color:var(--accent);font-weight:700}@media(max-width:760px){.hero,.cards{grid-template-columns:1fr}main{padding:2rem 1rem}h1{font-size:3rem}}
  </style>
</head>
<body>
<main>
  <section class="hero">
    <div>
      <p class="eyebrow">CivicSuite / CivicSafety</p>
      <h1>Non-CJIS public-safety admin support.</h1>
      <p>CivicSafety v0.1.0 helps public-safety administrative staff answer SOP questions with citations, prepare non-CJI training checklists, draft PIO updates, and summarize aggregate public statistics.</p>
    </div>
    <div class="panel">
      <h2>v0.1.0 boundary</h2>
      <p class="boundary">No CJI ingestion, no CAD/RMS integration, no dispatch, no enforcement, no investigations, no evidence workflows, no legal advice, no live LLM calls, and no connector runtime ship in this release.</p>
    </div>
  </section>
  <section class="cards">
    <article class="card"><h2>Ships Today</h2><p>Policy/SOP Q&A, training checklists, PIO draft support, aggregate public stats, and deterministic API endpoints.</p></article>
    <article class="card"><h2>Review Required</h2><p>Supervisors and PIO staff verify every answer, checklist, statistic, and public draft before use.</p></article>
    <article class="card"><h2>CJIS Gate</h2><p>Inputs marked as CJI are blocked from policy answers. This module stays on the non-CJIS administrative side.</p></article>
  </section>
  <section class="panel">
    <h2>Architecture</h2>
    <p><strong>Staff request</strong> -> CivicSafety deterministic API -> CivicCore foundation. Sensitive public-safety connectors are future isolated adapters, not v0.1.0 paths.</p>
    <p>Dependency: <code>civiccore==0.2.0</code>. Repo: <a href="https://github.com/CivicSuite/civicsafety">CivicSuite/civicsafety</a>.</p>
  </section>
</main>
</body>
</html>"""
