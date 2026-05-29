"""
niyam.py  —  Bot Schedule & Rage-Mode Rules
Works on any server: Railway, Replit, VPS, local, etc.
Timezone: Asia/Kolkata (IST)

Rules summary
─────────────
Normal days  : Bot runs 08:00 AM – 07:00 PM IST.

Evening zones (IST):
  08:00–18:40  → NORMAL  — everything allowed
  18:40–18:50  → CAUTION — ongoing recordings allowed, no cancellation
  18:50–18:58  → DANGER  — new recording triggers Rage Mode
                            (culprit's ALL recordings cancelled)
  18:58–19:00  → EXTREME — same + immediate offline; next-day schedule shifts
  19:00+       → OFFLINE — bot sleeps

Rage Mode (12 hours):
  Owner    : 09:00 AM – 06:00 PM
  Verified : 10:00 AM – 04:00 PM
  Normal   : 10:00 AM – 04:00 PM  (same as verified)
  On startup: culprit @username announced once in group/owner chat.
  Auto-reset after 12 h → normal schedule resumes for everyone.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytz

IST = pytz.timezone("Asia/Kolkata")

# ── Persistent state file (same dir as this script) ───────────────────────
_STATE = Path(__file__).parent / "niyam_state.json"

# ── Normal schedule ────────────────────────────────────────────────────────
OPEN_H  = 8    # 08:00 AM
CLOSE_H = 19   # 07:00 PM

# ── Evening danger thresholds (minutes since midnight) ────────────────────
_CAUTION_MIN = 18 * 60 + 40   # 6:40 PM
_DANGER_MIN  = 18 * 60 + 50   # 6:50 PM
_EXTREME_MIN = 18 * 60 + 58   # 6:58 PM
_CLOSE_MIN   = 19 * 60        # 7:00 PM
_OPEN_MIN    = 8  * 60        # 8:00 AM

# ── Rage-mode access windows ───────────────────────────────────────────────
OWNER_START    = 9    # 9:00 AM
OWNER_END      = 18   # 6:00 PM
VERIFIED_START = 10   # 10:00 AM
VERIFIED_END   = 16   # 4:00 PM
RAGE_HOURS     = 12

# ── Zone constants ─────────────────────────────────────────────────────────
OFFLINE = "offline"
NORMAL  = "normal"
CAUTION = "caution"
DANGER  = "danger"
EXTREME = "extreme"


# ═══════════════════════════════════════════════════════════════════════════
# Internal helpers
# ═══════════════════════════════════════════════════════════════════════════

def _now() -> datetime:
    return datetime.now(IST)


def _load() -> dict:
    try:
        with open(_STATE) as f:
            return json.load(f)
    except Exception:
        return {}


def _save(state: dict) -> None:
    with open(_STATE, "w") as f:
        json.dump(state, f, indent=2)


def _fmt_time(h: int) -> str:
    suffix = "AM" if h < 12 else "PM"
    h12    = h if h <= 12 else h - 12
    return f"{h12:02d}:00 {suffix}"


# ═══════════════════════════════════════════════════════════════════════════
# Zone detection
# ═══════════════════════════════════════════════════════════════════════════

def current_zone() -> str:
    """Return one of: offline | normal | caution | danger | extreme."""
    now = _now()
    m   = now.hour * 60 + now.minute
    if m < _OPEN_MIN or m >= _CLOSE_MIN:
        return OFFLINE
    if m >= _EXTREME_MIN:
        return EXTREME
    if m >= _DANGER_MIN:
        return DANGER
    if m >= _CAUTION_MIN:
        return CAUTION
    return NORMAL


# ═══════════════════════════════════════════════════════════════════════════
# Rage mode
# ═══════════════════════════════════════════════════════════════════════════

def is_rage_active() -> bool:
    """True if rage mode is active and not yet expired."""
    state = _load()
    ts    = state.get("rage_until")
    if not ts:
        return False
    if _now().timestamp() < float(ts):
        return True
    # Auto-reset
    _save({})
    return False


def activate_rage(culprit_id: int, culprit_username: str) -> None:
    """Start rage mode for RAGE_HOURS hours."""
    until = (_now() + timedelta(hours=RAGE_HOURS)).timestamp()
    _save({
        "rage_mode":          True,
        "rage_until":         until,
        "culprit":            culprit_id,
        "culprit_username":   culprit_username or str(culprit_id),
        "culprit_announced":  False,
    })


def rage_until_str() -> str:
    """Human-readable reset time, e.g. '08:50 AM IST'."""
    state = _load()
    ts    = state.get("rage_until")
    if not ts:
        return ""
    dt = datetime.fromtimestamp(float(ts), tz=IST)
    return dt.strftime("%I:%M %p IST")


def rage_remaining_str() -> str:
    """Human-readable time left in rage mode, e.g. '11h 42m'."""
    state = _load()
    ts    = state.get("rage_until")
    if not ts:
        return ""
    secs = float(ts) - _now().timestamp()
    if secs <= 0:
        return ""
    h, rem = divmod(int(secs), 3600)
    m      = rem // 60
    return f"{h}h {m}m"


def pop_culprit_announcement() -> str | None:
    """
    Returns a one-time announcement string the FIRST time this is called
    after rage mode activates (e.g. on bot startup).
    Returns None on all subsequent calls.
    """
    state = _load()
    if not state.get("rage_mode"):
        return None
    if state.get("culprit_announced"):
        return None
    state["culprit_announced"] = True
    _save(state)
    uname    = state.get("culprit_username", "unknown")
    until    = rage_until_str()
    return (
        "🔥 **RAGE MODE IS ACTIVE**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Culprit:** @{uname}\n"
        f"⏳ **Resets at:** {until}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 Owner access : {_fmt_time(OWNER_START)} – {_fmt_time(OWNER_END)}\n"
        f"✅ Verified     : {_fmt_time(VERIFIED_START)} – {_fmt_time(VERIFIED_END)}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ Bot is online but access is restricted until rage resets."
    )


# ═══════════════════════════════════════════════════════════════════════════
# Access gate
# ═══════════════════════════════════════════════════════════════════════════

def check_access(user_id: int,
                 *,
                 is_owner: bool = False,
                 is_verified: bool = False) -> tuple[bool, str]:
    """
    Returns (allowed: bool, denial_message: str).
    denial_message is "" when allowed is True.
    """
    now = _now()
    h   = now.hour

    # ── Rage-mode restrictions ─────────────────────────────────────────────
    if is_rage_active():
        state = _load()
        culprit = state.get("culprit_username", "someone")
        until   = rage_until_str()

        s, e = (OWNER_START, OWNER_END) if is_owner else (VERIFIED_START, VERIFIED_END)

        if not (s <= h < e):
            remaining = rage_remaining_str()
            return False, (
                "🚫 **ACCESS DENIED — Rage Mode Active**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 Culprit: @{culprit}\n"
                f"⏳ Resets in: **{remaining}** (at {until})\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🕐 Your access window: **{_fmt_time(s)} – {_fmt_time(e)}**\n"
                "Come back during your access window."
            )
        return True, ""

    # ── Normal schedule ────────────────────────────────────────────────────
    if not (OPEN_H <= h < CLOSE_H):
        return False, (
            "💤 **Bot is Sleeping!**\n"
            f"⏰ Active hours: **{_fmt_time(OPEN_H)} – {_fmt_time(CLOSE_H)} IST**\n"
            "Please come back during active hours."
        )

    return True, ""


# ═══════════════════════════════════════════════════════════════════════════
# New-recording guard
# ═══════════════════════════════════════════════════════════════════════════

def guard_new_recording(user_id: int,
                        username: str) -> tuple[str, bool]:
    """
    Call before accepting any new recording/download request.

    Returns (action, rage_triggered):
      action values:
        "allow"   — proceed normally
        "caution" — within safe window; allow (ongoing recordings continue)
        "block"   — offline or danger zone; deny the new request
        "extreme" — extreme zone; deny + immediate offline
      rage_triggered:
        True  — rage mode was just activated (caller must cancel ALL jobs)
        False — no change in rage state
    """
    # Access check first (rage, offline)
    allowed, _ = check_access(user_id)
    if not allowed:
        return "block", False

    zone = current_zone()

    if zone in (NORMAL, CAUTION):
        return "caution" if zone == CAUTION else "allow", False

    if zone == DANGER:
        activate_rage(user_id, username)
        return "block", True

    if zone == EXTREME:
        activate_rage(user_id, username)
        return "extreme", True

    # OFFLINE (belt-and-suspenders)
    return "block", False


def guard_message(action: str, zone: str | None = None) -> str:
    """Human-readable denial string for guard_new_recording results."""
    z = zone or current_zone()
    if action == "extreme":
        return (
            "🔥 **EXTREME DANGER ZONE (6:58 PM)**\n\n"
            "Ab toh had ho gayi!\n"
            "Bot **turant offline** ja raha hai.\n"
            "Teri aur baaki sabki recordings cancel ho gayi.\n\n"
            "🔥 Rage Mode activated for 12 hours.\n"
            f"👑 Owner: {_fmt_time(OWNER_START)}–{_fmt_time(OWNER_END)}\n"
            f"✅ Verified: {_fmt_time(VERIFIED_START)}–{_fmt_time(VERIFIED_END)}"
        )
    if action == "block" and z == DANGER:
        return (
            "🔴 **DANGER ZONE (6:50 PM)**\n\n"
            "Shaam ko masti?\n"
            "Teri nayi + purani DONO recordings cancel ho gayi!\n\n"
            "🔥 **Rage Mode** activated for 12 hours.\n"
            f"👑 Owner: {_fmt_time(OWNER_START)}–{_fmt_time(OWNER_END)}\n"
            f"✅ Verified: {_fmt_time(VERIFIED_START)}–{_fmt_time(VERIFIED_END)}"
        )
    if action == "block":
        return (
            "💤 **Bot is offline right now.**\n"
            f"⏰ Active: {_fmt_time(OPEN_H)} – {_fmt_time(CLOSE_H)} IST"
        )
    return "❌ Request blocked."


# ═══════════════════════════════════════════════════════════════════════════
# Status helpers
# ═══════════════════════════════════════════════════════════════════════════

def status_line() -> str:
    """One-line status badge for /status or startup messages."""
    zone = current_zone()
    rage = is_rage_active()
    now  = _now()

    emoji = {
        NORMAL:  "🟢",
        CAUTION: "🟡",
        DANGER:  "🔴",
        EXTREME: "🔥",
        OFFLINE: "💤",
    }.get(zone, "⚪")

    time_str = now.strftime("%I:%M %p IST")

    if rage:
        remaining = rage_remaining_str()
        culprit   = _load().get("culprit_username", "?")
        return f"🔥 RAGE MODE — @{culprit} | resets in {remaining}"
    if zone == OFFLINE:
        return f"💤 Offline | Back at {_fmt_time(OPEN_H)} IST"
    if zone == CAUTION:
        return f"🟡 Caution Zone | {time_str} | Closing at {_fmt_time(CLOSE_H)}"
    if zone == DANGER:
        return f"🔴 DANGER ZONE | {time_str} — New recordings blocked!"
    return f"{emoji} Online | {time_str}"
