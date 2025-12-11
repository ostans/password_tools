import streamlit as st
from pathlib import Path
import secrets


st.set_page_config(
    page_title="Password Tools", layout="wide", initial_sidebar_state="expanded"
)


# Minimal styling to make the landing page look nicer
st.markdown(
    """
	<style>
	.hero {padding: 1rem 0;}
	.hero h1{font-size:36px;margin-bottom:0.25rem}
	.card {background:#f8f9fa;padding:18px;border-radius:8px}
	.muted {color:#586069}
	</style>
	""",
    unsafe_allow_html=True,
)


# Paths
_HERE = Path(__file__).parent
IMG_GEN = _HERE / "images" / "generator.png"


def _maybe_image(path: Path, width: int | None = None):
    try:
        st.image(str(path), use_container_width=(width is None))
    except Exception:
        # silent fallback
        st.markdown("<div style='font-size:48px'>🔐</div>", unsafe_allow_html=True)


def sample_password():
    # lightweight, no external imports required — deterministic but varied
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return (
        secrets.choice(alphabet).upper()
        + "".join(secrets.choice(alphabet) for _ in range(6))
        + secrets.choice("0123456789")
        + secrets.choice("!@#$%")
    )


# --- Page content ---
st.markdown('<div class="hero">', unsafe_allow_html=True)
col_l, col_r = st.columns([2, 1])
with col_l:
    st.markdown("## Password Tools — Simple, Secure, Reliable")
    st.markdown(
        "Build better habits: evaluate password strength, generate safe passwords, and learn practical tips for daily security."
    )
    st.caption(
        "No sign-ups. No telemetry. Just helpful tools to improve your password hygiene."
    )

with col_r:
    _maybe_image(IMG_GEN)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Features
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("### 🛡️ Strength Checker")
    st.markdown(
        "Run quick checks and get actionable suggestions to harden weak passwords."
    )
    st.markdown(
        "<span class='muted'>Checks: length, entropy, dictionary words, username reuse</span>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with f2:
    st.markdown("### 🎲 Password Generator")
    st.markdown(
        "Generate random, memorable, or PIN-style passwords tailored to your needs."
    )
    st.markdown(f"**Sample:** `{sample_password()}`")
    st.markdown("</div>", unsafe_allow_html=True)

with f3:
    st.markdown("### 📚 Best Practices")
    st.markdown("Short, practical advice to maintain healthy password habits.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Tips two-column
tc1, tc2 = st.columns(2)
with tc1:
    st.markdown("#### Quick Tips")
    st.markdown(
        "- Use unique passwords for each service.\n- Prefer long passphrases over short complex strings."
    )
with tc2:
    st.markdown("#### Tools")
    st.markdown(
        "- Use a password manager to store and sync credentials.\n- Enable Multi-Factor Authentication (MFA) where available."
    )

st.markdown("---")
st.caption(
    "Built with care — use these tools as a learning aid, not a substitute for professional security advice."
)
