import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RecruitIQ", layout="wide")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("RecruitIQ")
    st.caption("AI-powered resume screening")
    st.divider()
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste the full job description",
        height=350,
        placeholder="Include required skills, experience level, tech stack..."
    )
    st.divider()
    st.markdown("""
    **How it works**
    1. Paste a job description
    2. Upload candidate PDFs
    3. Click Screen Candidates
    4. Get ranked results with insights
    """)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("AI Resume Screening System")
st.caption("Upload resumes · Extract skills · Rank candidates · Get insights")
st.divider()

# ── Upload ────────────────────────────────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

col_btn, col_info = st.columns([1, 4])
with col_btn:
    screen_btn = st.button("⚡ Screen Candidates", type="primary", use_container_width=True)
with col_info:
    if uploaded_files:
        st.info(f"{len(uploaded_files)} resume(s) ready to screen")

st.divider()


# ── Radar chart ───────────────────────────────────────────────────────────────
def render_radar_chart(candidate, jd):
    categories = [
        "Programming",
        "Machine Learning",
        "Cloud & DevOps",
        "Databases",
        "Frameworks & APIs",
    ]
    category_keywords = {
        "Programming":       ["python", "java", "javascript", "typescript", "c++", "golang"],
        "Machine Learning":  ["machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "scikit-learn", "llm"],
        "Cloud & DevOps":    ["aws", "gcp", "azure", "docker", "kubernetes", "linux", "terraform"],
        "Databases":         ["sql", "postgresql", "mongodb", "mysql", "redis", "elasticsearch"],
        "Frameworks & APIs": ["fastapi", "django", "flask", "react", "node.js", "langchain", "rest"],
    }

    skills_lower = [s.lower() for s in candidate.get("matching_skills", [])]
    jd_lower     = jd.lower()

    candidate_scores = []
    required_scores  = []

    for cat, keywords in category_keywords.items():
        cand_hits = sum(1 for k in keywords if k in skills_lower)
        jd_hits   = sum(1 for k in keywords if k in jd_lower)
        total     = len(keywords)
        candidate_scores.append(round((cand_hits / total) * 100))
        required_scores.append(round((jd_hits   / total) * 100))

    cats = categories + [categories[0]]
    c_s  = candidate_scores + [candidate_scores[0]]
    r_s  = required_scores  + [required_scores[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_s, theta=cats, fill="toself",
        name="Job Requirements",
        line=dict(color="#7c6fff", width=2),
        fillcolor="rgba(124,111,255,0.15)"
    ))
    fig.add_trace(go.Scatterpolar(
        r=c_s, theta=cats, fill="toself",
        name="Candidate",
        line=dict(color="#4ade80", width=2),
        fillcolor="rgba(74,222,128,0.15)"
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,100],
                tickfont=dict(color="#6b6b8a", size=10),
                gridcolor="#1e1e30", linecolor="#1e1e30"),
            angularaxis=dict(
                tickfont=dict(color="#b0b0c8", size=11),
                gridcolor="#1e1e30", linecolor="#1e1e30")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#b0b0c8", size=11), bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20, b=20, l=40, r=40),
        height=350,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Comparison table ──────────────────────────────────────────────────────────
def render_comparison_table(candidates):
    st.subheader("Candidate Comparison Table")
    st.caption("Sortable overview of all candidates")

    rows = []
    for i, c in enumerate(candidates, start=1):
        score = c.get("score", 0)
        rec   = c.get("recommendation", "Not a Fit")
        if i == 1:        medal = "🥇"
        elif i == 2:      medal = "🥈"
        elif i == 3:      medal = "🥉"
        elif score >= 70: medal = "🟢"
        elif score >= 40: medal = "🟡"
        else:             medal = "🔴"

        rows.append({
            "Rank":           f"{medal} #{i}",
            "Name":           c.get("name", "Unknown"),
            "Email":          c.get("email", "N/A"),
            "Score":          score,
            "Recommendation": rec,
            "Matches":        len(c.get("matching_skills", [])),
            "Gaps":           len(c.get("missing_skills",  [])),
            "Top Skills":     ", ".join(c.get("matching_skills", [])[:3]) or "—",
            "Top Gaps":       ", ".join(c.get("missing_skills",  [])[:2]) or "—",
            "File":           c.get("filename", ""),
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score", min_value=0, max_value=100, format="%d"
            ),
            "Matches": st.column_config.NumberColumn("✦ Matches"),
            "Gaps":    st.column_config.NumberColumn("✗ Gaps"),
        }
    )

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download Rankings as CSV",
        data=csv,
        file_name="candidate_rankings.csv",
        mime="text/csv"
    )


# ── Candidate detail card ─────────────────────────────────────────────────────
def render_candidate(candidate, rank, jd=""):
    score      = candidate.get("score", 0)
    name       = candidate.get("name", "Unknown")
    email      = candidate.get("email", "N/A")
    fname      = candidate.get("filename", "")
    summary    = candidate.get("summary", "")
    matching   = candidate.get("matching_skills", [])
    missing    = candidate.get("missing_skills",  [])
    rec        = candidate.get("recommendation",  "Not a Fit")
    strengths  = candidate.get("strengths",  [])
    weaknesses = candidate.get("weaknesses", [])
    improvs    = candidate.get("improvements", [])

    if score >= 70:   color = "green"
    elif score >= 40: color = "orange"
    else:             color = "red"

    if rank == 1:   medal = "🥇"
    elif rank == 2: medal = "🥈"
    elif rank == 3: medal = "🥉"
    else:           medal = f"#{rank}"

    with st.expander(f"{medal}  {name}  —  :{color}[{score}/100]  {rec}", expanded=(rank <= 2)):

        # ── Score + meta ──────────────────────────────────────────────────────
        c1, c2 = st.columns([1, 3])
        with c1:
            st.metric("Match Score", f"{score}/100")
            st.progress(score / 100)
        with c2:
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**File:** {fname}")
            if rec == "Strong Fit":     st.success(f"✓  {rec}")
            elif rec == "Possible Fit": st.warning(f"~  {rec}")
            else:                       st.error(f"✗  {rec}")

        st.divider()

        # ── Summary ───────────────────────────────────────────────────────────
        st.subheader("Summary")
        st.info(summary)

        st.divider()

        # ── Radar chart ───────────────────────────────────────────────────────
        st.subheader("Skills Radar Chart")
        st.caption("🟣 Job requirements  ·  🟢 Candidate coverage")
        render_radar_chart(candidate, jd)

        st.divider()

        # ── Skills ────────────────────────────────────────────────────────────
        col_m, col_g = st.columns(2)
        with col_m:
            st.subheader("✦ Matching Skills")
            if matching:
                for s in matching: st.success(s)
            else:
                st.caption("No matching skills detected")
        with col_g:
            st.subheader("✗ Missing Skills")
            if missing:
                for s in missing: st.error(s)
            else:
                st.caption("No skill gaps found")

        st.divider()

        # ── Insights ──────────────────────────────────────────────────────────
        st.subheader("💡 Candidate Insights")

        if strengths:
            st.markdown("**🟢 Strengths**")
            for s in strengths: st.success(s)

        if weaknesses:
            st.markdown("**🔴 Weaknesses**")
            for w in weaknesses: st.error(w)

        if improvs:
            st.markdown("**🟡 How to Improve This Resume**")
            for i in improvs: st.warning(i)

        if not strengths and not weaknesses and not improvs:
            st.caption("Detailed insights not available for this candidate.")


# ── Main logic ────────────────────────────────────────────────────────────────
if screen_btn:
    if not uploaded_files:
        st.warning("Please upload at least one resume PDF.")
        st.stop()
    if not job_description.strip():
        st.warning("Please add a job description in the sidebar.")
        st.stop()

    with st.spinner(f"Analyzing {len(uploaded_files)} resume(s) with AI..."):
        files_payload = [
            ("files", (f.name, f.read(), "application/pdf"))
            for f in uploaded_files
        ]
        try:
            r = requests.post(
                f"{API_URL}/screen",
                files=files_payload,
                data={"job_description": job_description},
                timeout=120
            )
            r.raise_for_status()
            result = r.json()
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Make sure `uvicorn main:app --reload --port 8000` is running.")
            st.stop()
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    candidates = result.get("candidates", [])

    if not candidates:
        st.warning("No candidates returned. Check your backend logs.")
        st.stop()

    # ── Summary metrics ───────────────────────────────────────────────────────
    strong   = sum(1 for c in candidates if c.get("recommendation") == "Strong Fit")
    possible = sum(1 for c in candidates if c.get("recommendation") == "Possible Fit")
    no_fit   = sum(1 for c in candidates if c.get("recommendation") == "Not a Fit")
    avg_score = round(sum(c.get("score", 0) for c in candidates) / len(candidates))

    st.success(f"✓ Screened {len(candidates)} candidates successfully")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Screened",  len(candidates))
    m2.metric("🥇 Strong Fit",   strong)
    m3.metric("🟡 Possible Fit", possible)
    m4.metric("🔴 Not a Fit",    no_fit)

    st.divider()

    # ── Comparison table ──────────────────────────────────────────────────────
    render_comparison_table(candidates)

    st.divider()

    # ── Filter + sort ─────────────────────────────────────────────────────────
    st.subheader("Detailed Candidate Reports")

    f_col, s_col = st.columns(2)
    with f_col:
        filter_opt = st.selectbox(
            "Filter by recommendation",
            ["All", "Strong Fit", "Possible Fit", "Not a Fit"]
        )
    with s_col:
        sort_opt = st.selectbox(
            "Sort by",
            ["Score (High to Low)", "Score (Low to High)", "Name A-Z"]
        )

    filtered = candidates if filter_opt == "All" else \
               [c for c in candidates if c.get("recommendation") == filter_opt]

    if sort_opt == "Score (High to Low)":
        filtered = sorted(filtered, key=lambda c: c.get("score", 0), reverse=True)
    elif sort_opt == "Score (Low to High)":
        filtered = sorted(filtered, key=lambda c: c.get("score", 0))
    elif sort_opt == "Name A-Z":
        filtered = sorted(filtered, key=lambda c: c.get("name", ""))

    if not filtered:
        st.info(f"No candidates match the filter: {filter_opt}")
    else:
        st.caption(f"Showing {len(filtered)} of {len(candidates)} candidates")
        for rank, candidate in enumerate(filtered, start=1):
            render_candidate(candidate, rank, job_description)