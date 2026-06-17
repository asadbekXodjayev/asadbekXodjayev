# -*- coding: utf-8 -*-
"""
Technical Portfolio Report generator.
Produces one professional PDF per app into ./ (the profile repo /docs folder).
Author dossier for: Asadbek Xodjayev
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
    KeepTogether, ListFlowable, ListItem
)

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- palette ----
INK      = colors.HexColor("#0f172a")   # slate-900
SUB      = colors.HexColor("#475569")   # slate-600
ACCENT   = colors.HexColor("#0e7490")   # cyan-700
GOLD     = colors.HexColor("#b45309")   # amber-700
LINE     = colors.HexColor("#e2e8f0")   # slate-200
BG_SOFT  = colors.HexColor("#f1f5f9")   # slate-100

CAT_COLORS = {
    "Production":   colors.HexColor("#15803d"),  # green-700
    "Portfolio":    colors.HexColor("#0e7490"),  # cyan-700
    "Masters":      colors.HexColor("#7c3aed"),  # violet-600
    "Proud":        colors.HexColor("#b45309"),  # amber-700
    "For-fun":      colors.HexColor("#64748b"),  # slate-500
}

styles = getSampleStyleSheet()
def S(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

st_title   = S("t",  fontName="Helvetica-Bold", fontSize=22, leading=25, textColor=INK)
st_tag     = S("tg", fontName="Helvetica-Oblique", fontSize=11, leading=15, textColor=SUB)
st_h2      = S("h2", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=ACCENT, spaceBefore=10, spaceAfter=4)
st_body    = S("b",  fontName="Helvetica", fontSize=9.5, leading=14, textColor=INK)
st_small   = S("sm", fontName="Helvetica", fontSize=8, leading=11, textColor=SUB)
st_meta    = S("mt", fontName="Helvetica", fontSize=8.5, leading=12, textColor=INK)
st_metab   = S("mtb",fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=SUB)
st_li      = S("li", fontName="Helvetica", fontSize=9.5, leading=13, textColor=INK)


def badge(text, color):
    return Paragraph(f'<font color="white"><b>&nbsp;{text}&nbsp;</b></font>',
                     S("bdg", fontName="Helvetica-Bold", fontSize=7.5, leading=11,
                       backColor=color, textColor=colors.white, alignment=TA_LEFT,
                       borderPadding=(2,3,2,3)))


def bullets(items, style=st_li):
    return ListFlowable(
        [ListItem(Paragraph(x, style), leftIndent=6, value="•") for x in items],
        bulletType="bullet", bulletColor=ACCENT, leftIndent=10, bulletFontSize=8,
    )


def kv_table(rows):
    data = [[Paragraph(k, st_metab), Paragraph(v, st_meta)] for k, v in rows]
    t = Table(data, colWidths=[32*mm, 138*mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LINEBELOW", (0,0), (-1,-2), 0.4, LINE),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.5)
    canvas.line(20*mm, 15*mm, 190*mm, 15*mm)
    canvas.setFont("Helvetica", 7.5); canvas.setFillColor(SUB)
    canvas.drawString(20*mm, 10*mm, "Asadbek Xodjayev  -  Technical Portfolio Dossier")
    canvas.drawRightString(190*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()


def build(app):
    slug = app["slug"]
    path = os.path.join(OUT, f"{slug}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=18*mm, bottomMargin=20*mm,
                            title=f"{app['name']} - Technical Report",
                            author="Asadbek Xodjayev")
    F = []

    # ---- header band ----
    F.append(Paragraph(app["name"], st_title))
    F.append(Paragraph(app["tagline"], st_tag))
    F.append(Spacer(1, 5))

    # category badges row
    cells = [badge(c, CAT_COLORS.get(c, SUB)) for c in app["categories"]]
    if app.get("standout"):
        cells.insert(0, badge("★ MASTERS STANDOUT", colors.HexColor("#7c3aed")))
    bt = Table([cells], colWidths=[None]*len(cells), hAlign="LEFT")
    bt.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),
                            ("RIGHTPADDING",(0,0),(-1,-1),6),
                            ("TOPPADDING",(0,0),(-1,-1),0),
                            ("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    F.append(bt)
    F.append(Spacer(1, 6))
    F.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT))
    F.append(Spacer(1, 4))

    # ---- meta table ----
    F.append(kv_table([
        ("Repo / Path", app["path"]),
        ("Domain", app["domain"]),
        ("Stack", app["stack"]),
        ("Status", app["status"]),
        ("Live / Deploy", app.get("live", "Not publicly deployed")),
    ]))

    # ---- overview ----
    F.append(Paragraph("Overview", st_h2))
    F.append(Paragraph(app["overview"], st_body))

    # ---- features ----
    F.append(Paragraph("Key Features &amp; Technical Highlights", st_h2))
    F.append(bullets(app["features"]))

    # ---- evidence ----
    F.append(Paragraph("Engineering Evidence &amp; Metrics", st_h2))
    F.append(bullets(app["evidence"]))

    # ---- talking points ----
    F.append(Paragraph("Why It Matters (application / interview talking points)", st_h2))
    F.append(bullets(app["talking"]))

    # ---- caveats ----
    if app.get("caveats"):
        F.append(Paragraph("Honest Caveats", st_h2))
        F.append(bullets(app["caveats"], style=st_small))

    doc.build(F, onFirstPage=footer, onLaterPages=footer)
    return path


# ============================================================
# APP DATASET  (accurate, from deep per-app analysis)
# ============================================================
APPS = [
 {
  "slug":"sarbon-frontend","name":"Sarbon Frontend","standout":True,
  "tagline":"Production B2B logistics / freight-management SaaS platform",
  "categories":["Production","Portfolio","Masters","Proud"],
  "path":"sarbon-frontend-main","domain":"Logistics / freight marketplace (B2B SaaS)",
  "stack":"React 19, TypeScript 5.9 (strict), Vite 7, Ant Design 6, TanStack Query 5, Zustand 5, Axios, i18next (10 langs), WebRTC, SSE, Yandex Maps",
  "status":"Live production product - ~90% complete",
  "live":"sarbon.me / api.sarbon.me",
  "overview":"A serious multilingual logistics platform connecting cargo owners, dispatchers, driver-managers and drivers. Supports multi-step cargo creation (split / negotiable / request payments), a cargo marketplace with filters, favourites and XLSX export, an offer accept/reject lifecycle, trip management with ratings, role-protected live GPS tracking, real-time chat with media / voice / presence, WebRTC audio calls, and a full admin console (moderation, companies, analytics funnels, push diagnostics, geo, users).",
  "features":[
    "Centralised typed API layer with a single Axios client and a real refresh-token queue (concurrent 401s coalesced into one refresh).",
    "Real-time layer built on fetch-based SSE streaming; WebRTC audio calls with signaling relayed over SSE/chat.",
    "Role-sensitive live GPS tracking with privacy gating, rendered on Yandex Maps.",
    "10-language i18n (locale files 120-190KB each - genuinely translated, not stubs).",
    "Clean separation of server state (TanStack Query) and client state (Zustand + immer + devtools).",
    "Lazy + Suspense routing nested under /:lang? with error boundaries.",
  ],
  "evidence":[
    "446 TypeScript/TSX files, ~78,000 LOC.",
    "36 test files / 358 Vitest + RTL tests covering payload builders, permissions, formatters, GPS/chat helpers and stores.",
    "Two GitHub Actions workflows (prod + staging) that build and deploy dist/* to the server.",
    "Husky pre-commit running lint-staged + type-check; ESLint --max-warnings 0; Knip dead-code checks.",
    "Full OpenAPI spec set (base/root ~130KB each + ~30 path files) backing a live api.sarbon.me.",
    "203 git commits, PR-based workflow; 47KB developer guide + flow docs for calls/chat/maps.",
  ],
  "talking":[
    "Strongest evidence of real-world, team-scale engineering capability in the portfolio.",
    "Demonstrates mastery of hard frontend problems: token-refresh concurrency, real-time transport, WebRTC, i18n at scale.",
  ],
  "caveats":[
    "Reads as team / commercial work (org-tagged itgenius24, PR workflow) - in applications, state your specific contribution clearly.",
    "2 known-failing unit tests (pre-existing payment-payload bug); README still says 5 languages while code ships 10.",
  ],
 },
 {
  "slug":"imposter-android","name":"Imposter (Android)","standout":True,
  "tagline":"Play-Store-shippable native party game in Kotlin / Jetpack Compose",
  "categories":["Production","Portfolio","Masters","Proud"],
  "path":"asadbek/Imposter (+ signed builds in asadbek/mobile)","domain":"Mobile game (offline party / social deduction)",
  "stack":"Kotlin 2.0.21, Jetpack Compose + Material 3, Hilt, Navigation-Compose, DataStore, kotlinx-serialization, MVVM/StateFlow, AGP 8.7.3, JDK 17",
  "status":"Production-ready - ~90-95% complete; signed release artifacts built",
  "live":"Signed AAB/APK built (play + full flavors)",
  "overview":"A native Kotlin port of the Imposter pass-and-play party game (3-12 players on one device): a complete flow of setup -> deal roles -> clues -> discussion -> vote -> eliminate -> final guess -> results. Built to professional Android standards and ready for Play Store submission.",
  "features":[
    "Complete game state machine implemented as a pure, testable engine.",
    "Clean Compose + Hilt + MVVM/StateFlow architecture with Navigation-Compose.",
    "9 word packs (~50 word pairs each) localised in English, Russian and Uzbek.",
    "play / full product flavors; real signing config with a release keystore.",
    "DataStore persistence, age-gate and ads handling, privacy policy and localised store listings.",
  ],
  "evidence":[
    "38 Kotlin files, ~4,720 LOC.",
    "4 unit-test files, 788 LOC of tests on the game engine.",
    "Real signing chain (release-keystore.jks) + multi-flavor Gradle build.",
    "PRIVACY.md + localised store listings; signed release AAB/APK already produced.",
  ],
  "talking":[
    "The single most production-real piece in the portfolio - the only project with a full signing chain, tests, store assets and shippable artifacts.",
    "Shows you can take a product from engine design to a store-ready, tested, localised mobile app end to end.",
  ],
  "caveats":[
    "Uses AdMob test IDs; no instrumented (UI) tests yet; no store screenshots committed.",
  ],
 },
 {
  "slug":"cargolink","name":"CargoLink","standout":False,
  "tagline":"Freight & warehouse marketplace on a live backend",
  "categories":["Production","Portfolio","Masters","Proud"],
  "path":"cargolink-app","domain":"Logistics marketplace (Uzbekistan / CIS)",
  "stack":"Next.js 16 (App Router), React 19, TypeScript (strict), Tailwind v4, Zustand 5, shadcn/radix, motion, Vitest, Playwright",
  "status":"Working MVP, mid-integration - ~75% complete",
  "live":"Wired to live 'Karvon' backend (https://fan.sarbon.me)",
  "overview":"A freight & warehouse marketplace with three listing domains (cargo shipments, transport vehicles, warehouse spaces), phone/OTP authentication, and a token economy (1 token = 1 contact reveal, subscriptions, 30-day free re-reveals), plus company verification and a multi-tab profile dashboard. Trilingual (en/ru/uz).",
  "features":[
    "Single typed HTTP layer (src/lib/api.ts) against a real backend - not a mock.",
    "Real auth: single-flight token refresh, 401 retry, HTTPS enforcement, JWT expiry peeking, OTP lockout.",
    "Token economy for contact reveals with subscription tiers.",
    "Server-side filtering, sorting and pagination on cargo & warehouse listings.",
    "Separate admin/moderator API realm; hardened CSP and full security-header set.",
  ],
  "evidence":[
    "61 TS/TSX source files; 16 routes; ~52 conventional-commit messages.",
    "~51 Vitest unit tests across api / security / stores.",
    "QA discipline: two dated QA reports with live backend contract probing, a Playwright auth harness, screenshots, console/network logs and a test ledger.",
    "vercel.json + next.config.ts with hardened CSP.",
  ],
  "talking":[
    "Demonstrates real integration engineering (auth, refresh, security headers) and genuine QA discipline.",
    "Honest, self-tracked gap list shows engineering maturity.",
  ],
  "caveats":[
    "Mid-integration: post forms not yet POSTing; favorites/routes/notifications defined but unwired; transport has no backend yet; no CI; CLAUDE.md is stale.",
  ],
 },
 {
  "slug":"novastore","name":"NOVA Store","standout":False,
  "tagline":"Full-stack e-commerce storefront with a real backend",
  "categories":["Production","Portfolio","Proud","Masters"],
  "path":"asadbek/e-commerse/novastore","domain":"E-commerce",
  "stack":"Next.js 16, React 19, TypeScript, Tailwind v4, shadcn, TanStack Query, Zustand, react-hook-form + Zod, Framer Motion, Lenis, PocketBase",
  "status":"Near-production - ~80% complete",
  "live":"store.xodjayev.uz",
  "overview":"A complete e-commerce storefront: catalog, product pages, cart, wishlist, checkout, orders, profile and authentication. Architected feature-sliced, with a real PocketBase backend plus a clever production fallback.",
  "features":[
    "Real PocketBase backend: bundled server, 6 collections via pb_migrations/, and seed scripts.",
    "Graceful dummyjson.com fallback so the store still renders when statically deployed.",
    "13+ routes; Feature-Sliced Design slices; Google OAuth.",
    "TanStack Query for server state, Zustand for cart/wishlist, RHF + Zod forms.",
  ],
  "evidence":[
    "Real database with migrations and seeding (not mock data).",
    "Live deployment at store.xodjayev.uz.",
    "Production fallback strategy shows thoughtful deploy engineering.",
  ],
  "talking":[
    "The most complete full-stack web project: real backend + migrations + seeding + OAuth.",
    "Good example of designing for graceful degradation in production.",
  ],
  "caveats":["No automated tests."],
 },
 {
  "slug":"spotify-stats","name":"Spotify Stats","standout":False,
  "tagline":"Personal Spotify analytics dashboard with real OAuth",
  "categories":["Portfolio","Production","For-fun"],
  "path":"asadbek/spotify-app/spotify-stats","domain":"Music analytics / data viz",
  "stack":"Next.js 16, React 19, TypeScript, Tailwind v4, TanStack Query, Zustand, spotify-web-api-node, Recharts, three/r3f, next-intl (en/ru/uz)",
  "status":"Working MVP - ~75% complete; deployed",
  "live":"Vercel (live URL configured)",
  "overview":"A personal Spotify analytics dashboard: OAuth login, top tracks/artists, recently played, a genre chart, an 'obsession score' and shareable cards.",
  "features":[
    "Server-side OAuth code->token exchange with cookie sessions.",
    "5 live Spotify Web API proxy routes returning real user data.",
    "Recharts visualisations + share-card generation; trilingual UI.",
    "Vercel deploy config with a live URL.",
  ],
  "evidence":[
    "Real third-party OAuth + live API integration (not mock).",
    "Deployed on Vercel.",
  ],
  "talking":[
    "Best 'real backend' example among the smaller web apps - proper OAuth and a live API integration.",
  ],
  "caveats":[
    "The 'AI roast' feature is hardcoded, not real AI; tests/ dirs are empty; sample secrets in .env.local.example.",
  ],
 },
 {
  "slug":"tattoo-studio","name":"Tattoo Studio (Yun)","standout":False,
  "tagline":"Deployed marketing site for a real tattoo studio",
  "categories":["Production","Portfolio","Proud"],
  "path":"asadbek/yun/tattoo-studio","domain":"Client marketing site",
  "stack":"React 19, Vite, Tailwind v3, Framer Motion, react-i18next, react-router, sharp",
  "status":"Near-production - ~80% complete; built",
  "live":"Deployed client site",
  "overview":"A gothic-styled marketing site for a real tattoo studio: home, works gallery, prices, about, contact, privacy and terms - trilingual (RU/EN/UZ).",
  "features":[
    "Real studio portfolio (~27 works) with optimised webp+jpg pairs generated via a sharp script.",
    "URL-based language routing across RU/EN/UZ.",
    "Telegram contact integration; vercel.json; production dist/ built.",
  ],
  "evidence":[
    "Real client deliverable with a built production bundle.",
    "Image optimisation pipeline (sharp) for performance.",
  ],
  "talking":[
    "Evidence of shipping for a real client with real content and a performance-conscious asset pipeline.",
  ],
 },
 {
  "slug":"davinci-codex","name":"Da Vinci Codex","standout":False,
  "tagline":"Renaissance illuminated-manuscript editorial experience",
  "categories":["Portfolio","Proud","Masters","Production"],
  "path":"asadbek/da vinchi/davinci","domain":"Editorial / art-history web experience",
  "stack":"Next.js 15, React 19, TypeScript, Tailwind v4, Framer Motion, Zustand, FSD, Turbopack",
  "status":"Polished - ~85% complete; deployed",
  "live":"art.asadbe.uz",
  "overview":"A Renaissance illuminated-manuscript editorial site on Leonardo da Vinci: artworks, inventions, a biography timeline and his legacy - built with exceptional design craft.",
  "features":[
    "Large curated static dataset (50+ records) with deterministic slug derivation.",
    "Public-domain Wikimedia imagery via Special:FilePath.",
    "Bespoke visual effects: gold leaf, parchment textures, drop caps, Ken Burns, cursor glow, skeleton loaders.",
  ],
  "evidence":[
    "Live at art.asadbe.uz; sophisticated, distinctive design system.",
    "Content-engineering depth (curated dataset + image resolution strategy).",
  ],
  "talking":[
    "Standout for visual design craft and content engineering - distinctive, not templated.",
  ],
 },
 {
  "slug":"steel-therapy","name":"Steel Therapy","standout":False,
  "tagline":"Shipped Flutter fitness / workout app (release artifacts)",
  "categories":["Production"],
  "path":"asadbek/mobile (release artifacts only; source not in this collection)","domain":"Mobile fitness app",
  "stack":"Flutter / Dart (Android AAB + APK)",
  "status":"Shipped release builds present (source elsewhere)",
  "live":"Signed AAB/APK produced",
  "overview":"A separately-shipped Flutter fitness/workout app. Only its signed release artifacts are present in this collection; the source lives in a different repository.",
  "features":[
    "Bundles a ~2MB exercises.json exercise database.",
    "Built as a signed Android App Bundle and APK.",
  ],
  "evidence":[
    "Release artifact evidence (libflutter.so + Dart libapp.so) of a shipped app.",
  ],
  "talking":[
    "Demonstrates breadth across native frameworks (Flutter in addition to Kotlin).",
  ],
  "caveats":["Source code is not part of this folder set - artifacts only."],
 },

 # ---------- AI / ML ----------
 {
  "slug":"mathvis-model","name":"MathVis Model","standout":True,
  "tagline":"A decoder-only transformer trained FROM SCRATCH",
  "categories":["Masters","Proud","Portfolio"],
  "path":"asadbek/AI ML/ai-edu/mathvis-model (frontend: mathvis-app)","domain":"Machine learning / NLP research",
  "stack":"Python, PyTorch (from-scratch transformer), custom BPE tokenizer; Next.js frontend; FastAPI server",
  "status":"Working research project - original ML work",
  "overview":"An original ~5M-parameter decoder-only transformer built and trained from scratch: 8 layers / 8 heads with SwiGLU activations and RoPE positional encoding, a custom 8192-vocab BPE tokenizer, a synthetic dataset generator, an AdamW + cosine training loop, an evaluation script and a FastAPI serving layer, with a Next.js frontend.",
  "features":[
    "Modern transformer architecture implemented by hand: RoPE, SwiGLU, multi-head attention.",
    "Custom Byte-Pair-Encoding tokenizer (8192 vocab) written from scratch.",
    "Synthetic dataset generation + full training loop (AdamW, cosine schedule).",
    "Evaluation script and a FastAPI inference server; Next.js demo app.",
  ],
  "evidence":[
    "Genuine from-scratch model training - not fine-tuning or calling a pretrained API.",
    "End-to-end pipeline: tokenizer -> data -> train -> eval -> serve -> UI.",
  ],
  "talking":[
    "The single strongest research signal in the portfolio for an ML/CS masters application.",
    "Shows you understand transformer internals deeply enough to reimplement them, not just use libraries.",
  ],
  "caveats":[
    "Lives inside the 'ai-edu' workspace alongside cloned reference repos - keep your original work clearly separated when presenting.",
  ],
 },
 {
  "slug":"digit-recognizer","name":"Digit Recognizer","standout":True,
  "tagline":"CNN trained on MNIST with a live drawing canvas",
  "categories":["Masters","Portfolio","Proud"],
  "path":"asadbek/AI ML/2-project","domain":"Computer vision / deep learning",
  "stack":"PyTorch CNN + torchvision (MNIST), FastAPI; React 18 + Vite + Tailwind",
  "status":"Working - ~90% complete; ~99% test accuracy",
  "overview":"A handwritten-digit recogniser: draw on a browser canvas and a CNN predicts the digit with live confidence bars. The model is a real convolutional network trained on the actual MNIST dataset.",
  "features":[
    "2 conv blocks with BatchNorm + Dropout and a 512-unit dense head.",
    "Trained on the real 60k/10k MNIST split with affine data augmentation and best-checkpoint saving.",
    "Documented preprocessing contract (center-of-mass 28x28) shared across train and serve.",
    "Clean train/serve split; trained weights (mnist_model.pth) committed.",
  ],
  "evidence":[
    "Real model training on a real dataset with augmentation; ~99% reported test accuracy.",
    "Per-class accuracy reporting.",
  ],
  "talking":[
    "Strong, classic ML evidence: you trained a model (not just called an API) and reported rigorous metrics.",
  ],
 },
 {
  "slug":"rag-chatbot","name":"RAG Document Chatbot","standout":False,
  "tagline":"Fully local retrieval-augmented document Q&A",
  "categories":["Portfolio","Masters"],
  "path":"asadbek/AI ML/3-project","domain":"LLM / retrieval-augmented generation",
  "stack":"LangChain + ChromaDB, Ollama (nomic-embed-text + llama3.2), FastAPI; React 19 + TS + Tailwind v4",
  "status":"Working - ~85% complete",
  "overview":"A fully local RAG chatbot: upload PDFs / text, ask questions, and get cited answers - all running locally with no external API.",
  "features":[
    "Complete RAG pipeline: chunk -> embed -> persist -> similarity search -> grounded prompt -> generate.",
    "Persistent Chroma vector store with live add/delete of documents.",
    "Local embeddings + LLM via Ollama; typed REST contract.",
  ],
  "evidence":[
    "Real end-to-end RAG system with a pre-built vector store and sample docs.",
    "Engineering-heavy (pipeline design) using pretrained models.",
  ],
  "talking":[
    "Demonstrates practical LLM engineering and retrieval design - relevant to applied-AI programs.",
  ],
 },
 {
  "slug":"chess-engine","name":"Chess Engine","standout":False,
  "tagline":"Classical negamax chess AI you can play in the browser",
  "categories":["Portfolio","Proud"],
  "path":"asadbek/AI ML/4-chess bot","domain":"Game AI / algorithms",
  "stack":"Pure-Python engine (python-chess) + FastAPI; React 18 + Vite + Tailwind",
  "status":"Working - ~90% complete",
  "overview":"Play chess in the browser against a custom Python engine. Despite its folder name, this is a strong classical search engine, not a neural network.",
  "features":[
    "~727-line engine: iterative-deepening negamax, alpha-beta, transposition table, null-move pruning, late-move reductions, check extensions, quiescence search.",
    "Tapered bitboard evaluation; opening book; Boltzmann-sampled difficulty.",
  ],
  "evidence":[
    "Substantial, correct classical-AI implementation - strong CS/algorithms evidence.",
  ],
  "talking":[
    "Great algorithms showcase (search, pruning, evaluation) - frame it as classical game AI, not ML.",
  ],
  "caveats":["Legacy torch/.pth files are unused; README was corrected to reflect the real negamax engine."],
 },
 {
  "slug":"facescan","name":"FaceScan","standout":False,
  "tagline":"Real-time webcam face analysis + recognition",
  "categories":["Portfolio","Proud"],
  "path":"asadbek/AI ML/5-project-face-recognition","domain":"Computer vision (applied)",
  "stack":"FastAPI + DeepFace + face_recognition (dlib) + OpenCV; React 18 + TS + Tailwind + Zustand + Framer Motion + i18n",
  "status":"Working - ~85% complete",
  "overview":"Real-time webcam face analysis (age / gender / emotion / pose / landmarks) plus identity enrollment and recognition, behind a polished trilingual cyberpunk UI.",
  "features":[
    "Integrates real pretrained CV models with graceful dlib-optional degradation.",
    "128-d face-encoding registry for enrollment / recognition.",
    "Polished multilingual (en/ru/uz) animated UI.",
  ],
  "evidence":[
    "Strong product engineering over off-the-shelf CV models.",
  ],
  "talking":[
    "Shows you can integrate and productise real CV models with a refined UX.",
  ],
  "caveats":["Applies pretrained models; limited novel ML."],
 },
 {
  "slug":"real-estate-predictor","name":"Real-Estate Predictor","standout":False,
  "tagline":"Property-price regression with a clean sklearn pipeline",
  "categories":["Portfolio","For-fun"],
  "path":"asadbek/AI ML/real-estate-predictor","domain":"Tabular ML",
  "stack":"scikit-learn GradientBoostingRegressor in a ColumnTransformer pipeline, FastAPI; React + Vite + Tailwind",
  "status":"Working - ~85% complete",
  "overview":"Predicts a property's price from input features via a web form, backed by a properly structured scikit-learn pipeline.",
  "features":[
    "ColumnTransformer pipeline (imputer / scaler / one-hot) serialized with joblib.",
    "Train/test split with R2 / RMSE / MAE reporting.",
  ],
  "evidence":[
    "Clean, idiomatic sklearn pipeline engineering.",
  ],
  "talking":[
    "Good demonstration of ML engineering hygiene (pipelines, serialization, metrics).",
  ],
  "caveats":["Trained only on synthetically generated mock data, so predictions are circular / tutorial-grade."],
 },

 # ---------- Web apps ----------
 {
  "slug":"appgraph","name":"AppGraph","standout":False,
  "tagline":"Meta-tool that renders every project's architecture graphs",
  "categories":["Portfolio","Proud"],
  "path":"asadbek/appgraph","domain":"Developer tooling / data visualization",
  "stack":"Next.js 15, React 19, TypeScript, Tailwind v4, d3-force/drag/zoom, elkjs, jspdf + svg2pdf, Playwright",
  "status":"Working MVP - ~75% complete",
  "overview":"An internal hub that renders every other project's architecture graphs (file trees, system topology, app flows) using a collision-free ELK.js layout engine, ingesting the sys-design 4-file diagram suites.",
  "features":[
    "Custom ELK.js-based graph layout with d3 force / drag / zoom.",
    "Ingests 31 app datasets via an npm run ingest (tsx) pipeline.",
    "SVG + PDF export and a Playwright screenshot script.",
  ],
  "evidence":[
    "31 ingested datasets; real export and screenshot tooling.",
  ],
  "talking":[
    "Impressive meta-tooling - shows systems thinking and custom graph-rendering engineering.",
  ],
  "caveats":["Local-only dev tool; no backend/auth/tests."],
 },
 {
  "slug":"codex-luminara","name":"Codex Luminara","standout":False,
  "tagline":"Cinematic art-history web experience",
  "categories":["Portfolio","Proud"],
  "path":"asadbek/codex-art","domain":"Editorial / immersive web",
  "stack":"Next.js 15, React 19, TypeScript, Feature-Sliced Design, Tailwind v3 + shadcn, Framer Motion, Zustand, next/image + sharp",
  "status":"Working MVP - ~80% complete",
  "overview":"A 'living illuminated manuscript': a scrolling home, an era timeline, a gallery and immersive artwork-detail pages with Ken Burns / parallax motion and ambient audio.",
  "features":[
    "Large hand-authored static content (artwork-details ~1,314 lines) with 18 webp backgrounds and 10 audio tracks.",
    "Keyless Met / Rijksmuseum API fallback.",
    "Feature-Sliced Design + shadcn; sharp image optimisation.",
  ],
  "evidence":[
    "Substantial authored content and a distinctive, cinematic design system.",
  ],
  "talking":[
    "Strong design + content-engineering showcase.",
  ],
  "caveats":["No DB despite spec mentioning Prisma; an audio-path bug (/music vs public/music2); no tests/deploy."],
 },
 {
  "slug":"cosmos-space","name":"COSMOS (Atlas)","standout":False,
  "tagline":"Interactive atlas of the cosmos",
  "categories":["Portfolio","Proud"],
  "path":"asadbek/space","domain":"Educational / data-driven web",
  "stack":"Next.js 16, React 19, TypeScript, Tailwind v4 + shadcn/Radix, Motion v12, Zustand (persisted), i18next, Recharts, Vercel Analytics",
  "status":"Working MVP - ~80% complete",
  "overview":"An interactive atlas of the cosmos: an animated solar system plus a searchable catalog of 52 authored celestial objects, each with a detail page (prose, stats, composition charts, facts).",
  "features":[
    "52 fully-authored static objects with SSG via generateStaticParams.",
    "Complete loading / error / empty / not-found states; persisted 'explored' counter.",
    "Recharts composition charts; i18n wired.",
  ],
  "evidence":[
    "Substantial authored dataset; complete state handling on every view.",
  ],
  "talking":[
    "Good example of content-driven SSG with disciplined UX states.",
  ],
  "caveats":["i18n wired but currently English-only; no backend/tests."],
 },
 {
  "slug":"imposter-web","name":"Imposter (Web)","standout":False,
  "tagline":"Pass-and-play party bluffing game in the browser",
  "categories":["Portfolio","Proud"],
  "path":"asadbek/imposter-web","domain":"Web game",
  "stack":"Next.js 16 (Turbopack), React 19, Tailwind v4, shadcn/base-ui, Motion, Zustand",
  "status":"Working MVP - ~80% complete",
  "overview":"The web version of the Imposter game: 3-12 players on one device, full flow from setup to deal, clues, discussion, vote, eliminate, final guess and results.",
  "features":[
    "Pure game engine (engine.ts) with state-machine stores.",
    "15+ trilingual themes (~414 theme entries) plus a theme editor and chaos mode.",
    "Web Audio + haptics; vercel.json with security headers.",
  ],
  "evidence":[
    "Clean engine/UI separation; large localised content set.",
  ],
  "talking":[
    "Pairs with the Android version to show one product across web + native.",
  ],
  "caveats":["Fully client-side by design; no tests."],
 },
 {
  "slug":"show-data","name":"Show Data","standout":False,
  "tagline":"Interactive data-structures & algorithms visualizer",
  "categories":["Portfolio","Proud","For-fun"],
  "path":"asadbek/DATA/show-data","domain":"CS education / visualization",
  "stack":"Next.js 16, React 19, TypeScript, Tailwind v4, shadcn, Zustand, Framer Motion, Feature-Sliced Design",
  "status":"Working MVP - ~75% complete",
  "overview":"An interactive DSA visualizer covering sorting (with audio), a pathfinding grid, and BST / AVL / Heap tree structures.",
  "features":[
    "Three real algorithm modules each with their own entities (avl/bst/heap, grid algorithms, sort + sound).",
    "Global HUD controls; vercel.json.",
    "A correctness test script (npm run test:sorts).",
  ],
  "evidence":[
    "Real algorithm implementations with a correctness test harness.",
  ],
  "talking":[
    "Demonstrates algorithmic understanding plus the ability to make it visual and interactive.",
  ],
 },
 {
  "slug":"recipe-ai","name":"Recipe AI","standout":False,
  "tagline":"LLM-powered recipe generator with graceful fallback",
  "categories":["Portfolio","Proud","Masters"],
  "path":"asadbek/ai-recipe/recipe-ai","domain":"Applied LLM / product",
  "stack":"Next.js 16, React 19, TypeScript, Tailwind v4, shadcn, Framer Motion, RHF + Zod; Groq LLM API",
  "status":"Working MVP - ~80% complete",
  "overview":"Enter ingredients and an LLM returns recipes, behind a polished marketing landing page.",
  "features":[
    "Real /api/generate-recipe route calling Groq with primary + backup keys and model fallback.",
    "Trilingual prompts; ingredient-match scoring; saved-recipes and detail pages.",
    "Graceful fallback to a large predefined-recipe set when no API key is present.",
  ],
  "evidence":[
    "Real LLM integration with resilient key/model fallback; CASE_STUDY, DEPLOYMENT and PLANNING docs.",
  ],
  "talking":[
    "Good applied-AI product with production-minded resilience (fallback chains).",
  ],
 },

 # ---------- Three.js / WebGL ----------
 {
  "slug":"interactive-works","name":"Interactive Works","standout":True,
  "tagline":"WebGL sphere-gallery portfolio with a custom lens shader",
  "categories":["Portfolio","Proud","Masters","Production"],
  "path":"asadbek/threeJs","domain":"Creative WebGL / portfolio",
  "stack":"Three.js, GLSL, GSAP, TypeScript, Vite (standalone, no React)",
  "status":"Polished - ~80% complete; deployed",
  "live":"asadbe.uz",
  "overview":"A Phantom.land-style WebGL portfolio: the camera sits inside a sphere walled with ~38 project cards; inertial drag lets you wander and tap to open a case study.",
  "features":[
    "Custom GLSL lens-distortion post-processing pass (barrel / vignette / blur / grain).",
    "Inertial sphere controls with idle auto-drift; EffectComposer pipeline.",
    "Client-side routing; immutable-asset caching via a sophisticated vercel.json.",
  ],
  "evidence":[
    "From-scratch shader + camera physics; live at asadbe.uz.",
  ],
  "talking":[
    "Strong technical WebGL signal - hand-written shaders and camera physics read very well for a masters application.",
  ],
 },
 {
  "slug":"threejs-backrooms","name":"The Backrooms (Three.js)","standout":True,
  "tagline":"First-person liminal-horror game with provably-sealed procedural mazes",
  "categories":["Portfolio","Proud","Masters"],
  "path":"asadbek/3Js/threeJs-backrooms","domain":"3D game / procedural generation",
  "stack":"Three.js, TypeScript, Vite, custom capsule controller, custom GLSL grade, Playwright",
  "status":"Working / production - ~88% complete",
  "overview":"A first-person liminal-horror game: a sealed, infinite procedural maze with a sanity system driving fog, grain, hum and entity aggression, descending levels and found-footage post-FX.",
  "features":[
    "Watertight chunked maze generation that is provably sealed (no escape gaps).",
    "Sanity system coupling gameplay to post-processing intensity.",
    "Hand-tuned capsule character controller (no physics library); custom GLSL grade.",
  ],
  "evidence":[
    "24 files, ~3,430 LOC (the largest Three.js app); full SPEC.md with 12 quality gates.",
    "18-file QA harness with measured metrics (70 draw calls, flat memory, 0 console errors over 200 seeds x 3 levels).",
  ],
  "talking":[
    "The most rigorous project in the WebGL set - procedural generation + measured QA is excellent engineering evidence.",
  ],
 },
 {
  "slug":"lullaby-house","name":"The Lullaby House","standout":True,
  "tagline":"First-person horror game with an AI enemy and Dijkstra navigation",
  "categories":["Portfolio","Proud","Masters","For-fun"],
  "path":"asadbek/3Js/scaryThreeJs","domain":"3D game / physics + AI",
  "stack":"Three.js (WebGL2), Rapier physics, rigged GLB animation, synth positional Web Audio, custom post-FX shader",
  "status":"Working - ~85% complete",
  "overview":"A first-person psychological-horror survival game (Granny-style): escape a sealed house while evading 'Agnes', an AI enemy, through a multi-step objective chain with three branching endings.",
  "features":[
    "Rapier physics with a kinematic character controller.",
    "Full enemy AI: a state machine + Dijkstra navigation over the house graph.",
    "Procedural fallbacks for every asset; a sanity system; a no-soft-lock objective lock-graph.",
  ],
  "evidence":[
    "24 files, ~3,412 LOC; the most complete game in the set.",
  ],
  "talking":[
    "Combines real physics, pathfinding AI and narrative design - a rich, masters-worthy systems project.",
  ],
 },
 {
  "slug":"substrate","name":"SUBSTRATE (Tech-ThreeJs)","standout":True,
  "tagline":"Scroll-driven journey across nine orders of magnitude",
  "categories":["Portfolio","Proud","Masters","Production"],
  "path":"asadbek/3Js/Tech-ThreeJs","domain":"Creative WebGL / scrollytelling",
  "stack":"Three.js, TypeScript, Vite, GSAP, Lenis, custom circuit-trace GLSL shader, UnrealBloom",
  "status":"Production - ~88% complete",
  "overview":"Scroll equals zoom: the scene travels across ~9 orders of magnitude - transistor -> chip die -> device stack -> network -> planet-scale data field - assembling at each rung.",
  "features":[
    "Custom circuit-trace GLSL shader; fully procedural (no downloaded models).",
    "Instanced 1,400-node network rendered in a single draw call.",
    "'Scale Gauge' + 'Lab Instrument' design system; 19-file QA harness.",
  ],
  "evidence":[
    "7 files, ~1,122 LOC; instanced-everything craft with original shaders.",
  ],
  "talking":[
    "Best of the scroll experiences for original shader work and rendering efficiency.",
  ],
 },
 {
  "slug":"compile","name":"COMPILE (Codign-ThreeJs)","standout":False,
  "tagline":"'Source becomes system' - force-directed 3D dependency graph",
  "categories":["Portfolio","Proud","Production"],
  "path":"asadbek/3Js/Codign-ThreeJs","domain":"Creative WebGL / scrollytelling",
  "stack":"Three.js, TypeScript, Vite, GSAP, Lenis, custom Fruchterman-Reingold solver, UnrealBloom",
  "status":"Production - ~90% complete",
  "overview":"A scroll-driven experience where typed source assembles into a force-directed 3D dependency graph, ignites into a running system, then morphs into an architecture 'city'.",
  "features":[
    "Custom Fruchterman-Reingold force-directed graph solver.",
    "Instanced graph rendered in ~3 draw calls; UnrealBloom; one custom shader.",
    "Fully procedural; 21-file QA harness.",
  ],
  "evidence":[
    "9 files, ~1,330 LOC; original layout-solver implementation.",
  ],
  "talking":[
    "Shows algorithmic creativity (graph layout) fused with polished WebGL presentation.",
  ],
 },
 {
  "slug":"vantage","name":"VANTAGE (cars-ThreeJs)","standout":False,
  "tagline":"Scroll-driven 3D car walkaround & configurator",
  "categories":["Portfolio","Proud","Production"],
  "path":"asadbek/3Js/cars-ThreeJs","domain":"Creative WebGL / product viz",
  "stack":"Three.js, TypeScript, Vite, GSAP, Lenis, Draco-compressed GLB",
  "status":"Production - ~90% complete",
  "overview":"A scroll-driven car experience: the official Three.js Ferrari glTF is revealed and dissected by scroll - silhouette, exterior, exploded teardown, a live clearcoat configurator and spec telemetry.",
  "features":[
    "Draco-compressed GLB with baked ambient occlusion; 8 webp paint swatches.",
    "Live clearcoat colour configurator; History-API routing; OG cards.",
    "14-file QA harness; Vercel config.",
  ],
  "evidence":[
    "8 files, ~895 LOC; polished product-viz with a real configurator.",
  ],
  "talking":[
    "Great example of product-visualisation craft (the kind of work agencies pay for).",
  ],
 },
 {
  "slug":"strata","name":"STRATA (history-ThreeJs)","standout":False,
  "tagline":"'Scroll is time' - fly a 3D timeline past procedural monuments",
  "categories":["Portfolio","Proud","Production"],
  "path":"asadbek/3Js/history-ThreeJs","domain":"Creative WebGL / scrollytelling",
  "stack":"Three.js, TypeScript, Vite, GSAP, Lenis, public-domain art textures",
  "status":"Production - ~88% complete",
  "overview":"Scroll is time: the camera flies along a 3D timeline ribbon past six procedural monuments docked to their dates, with lighting and fog re-tinting per century.",
  "features":[
    "Procedurally generated monuments; 7 public-domain art plates as 3D textures.",
    "'Stratum Gauge' signature UI; OG shells; museum-grade design system.",
    "44-file QA harness (the largest).",
  ],
  "evidence":[
    "6 files, ~1,287 LOC; the most thorough QA harness in the set.",
  ],
  "talking":[
    "Demonstrates narrative design + procedural geometry + strong QA discipline.",
  ],
 },
 {
  "slug":"codex-luminara-gallery","name":"Codex Luminara (3D Gallery)","standout":False,
  "tagline":"Spherical Renaissance art gallery you stand inside",
  "categories":["Portfolio","Proud","Production"],
  "path":"asadbek/3Js/threeJs-codex","domain":"Creative WebGL / gallery",
  "stack":"Three.js, TypeScript, Vite, GSAP, custom lens shader, real webp art + ogg audio",
  "status":"Production - ~85% complete",
  "overview":"Stand inside a sphere hung with 13 masterworks; drag to wander, tap to open a folio. Includes an era filter and ambient audio (Fur Elise / Lacrimosa).",
  "features":[
    "13 public-domain art plates; custom lens shader; ambient ogg audio.",
    "Roman-numeral theme; Vercel config.",
  ],
  "evidence":[
    "9 files, ~1,863 LOC; sibling to the Interactive Works gallery.",
  ],
  "talking":[
    "Polished, atmospheric gallery - good companion piece to Interactive Works.",
  ],
 },
 {
  "slug":"sarbon-atlas","name":"Sarbon Atlas","standout":False,
  "tagline":"Interactive 3D freight-route globe (R3F)",
  "categories":["Portfolio","Proud","Production"],
  "path":"asadbek/3Js/sarbonThreeJs","domain":"Creative WebGL / data viz",
  "stack":"React + react-three-fiber + drei + @react-three/postprocessing + Zustand; 2 custom shaders",
  "status":"Working / production - ~80% complete",
  "overview":"An interactive 3D freight-route globe for the Central Asia logistics corridor: an auto-rotating mission-control globe with glowing cargo arcs from Tashkent to 10 cities; click a city to focus and watch a truck animate the route.",
  "features":[
    "The only R3F app in the set - clean react-three-fiber component split.",
    "Custom shaders: additive tube-flow arcs + a fresnel atmosphere.",
    "Instanced markers; bloom; reduced-motion path; includes a Next.js porting guide.",
  ],
  "evidence":[
    "20 files, ~881 LOC; production-minded (a11y + porting guide).",
  ],
  "talking":[
    "Shows R3F (React) WebGL skills and ties visually to the Sarbon product domain.",
  ],
 },
 {
  "slug":"endless-drive","name":"Endless Drive (game-threeJs)","standout":False,
  "tagline":"Chill endless procedural driving game",
  "categories":["Portfolio","Proud","For-fun"],
  "path":"asadbek/3Js/game-threeJs","domain":"3D game",
  "stack":"Three.js, TypeScript, Vite, GSAP, procedural Web Audio, 2 shaders, Draco GLB",
  "status":"Working / production - ~85% complete",
  "overview":"A chill endless procedural road-trip game: a low-poly car cruises an infinite highway that cross-fades between biomes, with weather, day/night and a 100% procedural Web Audio engine.",
  "features":[
    "Procedural endless world with biome cross-fades and weather.",
    "Fully procedural Web Audio engine sound; a small custom physics layer.",
    "Director state system; object pooling + adaptive performance; seeded determinism.",
  ],
  "evidence":[
    "21 files, ~3,193 LOC (the most game logic of the set); 38-file QA harness.",
  ],
  "talking":[
    "Substantial game-systems engineering (procedural world, audio synthesis, perf management).",
  ],
 },

 # ---------- CS / Desktop ----------
 {
  "slug":"dijkstra-csharp","name":"Dijkstra Visualizer (C# / .NET 8)","standout":False,
  "tagline":"Interactive shortest-path visualizer in modern C#",
  "categories":["Portfolio","Proud"],
  "path":"asadbek/code/WinFormsApp1","domain":"Algorithms / desktop",
  "stack":"C# / .NET 8, WinForms + GDI+, SHA-256 auth (JSON store)",
  "status":"Working - ~90% complete",
  "overview":"An interactive Dijkstra shortest-path visualizer with a full graph editor, the most modern of three language implementations.",
  "features":[
    "Full graph editor with animated Dijkstra and equal-cost path highlighting.",
    "SHA-256 auth guard with a JSON credential store.",
  ],
  "evidence":[
    "~1,675 LOC; modern .NET 8 stack.",
  ],
  "talking":[
    "Part of a three-language Dijkstra study (C#, Python, C++/CLI) - good general CS evidence and language breadth.",
  ],
 },
 {
  "slug":"dijkstra-python","name":"Dijkstra Visualizer (Python)","standout":False,
  "tagline":"Cleanest implementation of the shortest-path visualizer",
  "categories":["Portfolio","Proud","For-fun"],
  "path":"asadbek/code/PyCharmMiscProject","domain":"Algorithms / desktop",
  "stack":"Python 3 + Tkinter (stdlib) + heapq",
  "status":"Working - ~90% complete",
  "overview":"The Python implementation of the Dijkstra visualizer - the cleanest of the three, using a proper generator-based algorithm.",
  "features":[
    "Generator-based Dijkstra with lazy heap deletion (heapq).",
    "File-backed login; animated steps.",
  ],
  "evidence":[
    "~1,294 LOC; the most idiomatic implementation.",
  ],
  "talking":[
    "Demonstrates clean algorithmic Python and good use of the standard library.",
  ],
 },
 {
  "slug":"dijkstra-cpp","name":"Dijkstra Visualizer (C++/CLI)","standout":False,
  "tagline":"Managed-C++ shortest-path visualizer",
  "categories":["Portfolio","For-fun"],
  "path":"asadbek/code/Project1","domain":"Algorithms / desktop",
  "stack":"C++/CLI (managed C++), .NET Framework, WinForms + GDI+",
  "status":"Working - ~85% complete",
  "overview":"The C++/CLI implementation of the Dijkstra visualizer, with an animated splash, login and an interactive graph editor.",
  "features":[
    "Real Dijkstra with step animation via a Timer.",
    "Animated splash -> login -> graph editor flow.",
  ],
  "evidence":[
    "~2,805 LOC (with some dormant orphan files).",
  ],
  "talking":[
    "Shows willingness to work in lower-level / managed-C++ territory - rounds out the three-language study.",
  ],
 },
]


def main():
    made = []
    for app in APPS:
        made.append(build(app))
    # index markdown
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("# Technical Portfolio Dossier\n\n")
        f.write("Per-app technical reports (PDF) for Asadbek Xodjayev's project portfolio.\n\n")
        f.write("> Generated from a deep per-app code analysis. The 7 **Masters Standouts** are marked with a star.\n\n")
        groups = {}
        for a in APPS:
            primary = a["categories"][0]
            groups.setdefault(primary, []).append(a)
        order = ["Production","Masters","Portfolio"]
        seen = set()
        for g in order + [k for k in groups if k not in order]:
            if g not in groups:
                continue
            f.write(f"## {g}\n\n")
            for a in groups[g]:
                if a["slug"] in seen:
                    continue
                seen.add(a["slug"])
                star = " ⭐" if a.get("standout") else ""
                f.write(f"- [{a['name']}{star}]({a['slug']}.pdf) — {a['tagline']}\n")
            f.write("\n")
    print(f"Generated {len(made)} PDFs into {OUT}")
    for m in made:
        print(" -", os.path.basename(m))


if __name__ == "__main__":
    main()
