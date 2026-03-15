#!/usr/bin/env python3
"""
Marathon Training & Weight Loss Tracker
Goal: 65kg → 60kg, Run full marathon on 2026-11-08
"""

import json
import os
import sys
from datetime import date, datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
START_DATE = date(2026, 3, 15)
RACE_DATE = date(2026, 11, 8)
START_WEIGHT = 65.0
GOAL_WEIGHT = 60.0
TOTAL_WEEKS = (RACE_DATE - START_DATE).days // 7  # 34

# ---------------------------------------------------------------------------
# Training Plan Definition
# ---------------------------------------------------------------------------

def build_training_plan():
    """
    34-week marathon plan from zero-to-race.

    Phase 1  (W01-W08): Base building  – aerobic foundation
    Phase 2  (W09-W16): Development   – tempo + mid-long runs
    Phase 3  (W17-W24): Build         – marathon-pace work
    Phase 4  (W25-W32): Peak          – peak mileage
    Phase 5  (W33-W34): Taper         – rest & race-ready
    """
    plan = {}

    # Weekly blueprint: (phase, weekly_km, description)
    weekly_blueprints = [
        # W01-W08 Base
        (1, "Base", 20,  "やさしいジョグ中心。週4日走り、体を慣らす"),
        (1, "Base", 24,  "距離を少しずつ伸ばす。ペースは会話できる程度"),
        (1, "Base", 28,  "ロング走を初導入（10km）"),
        (1, "Base", 32,  "週1回テンポ走（楽なペース+30秒/km）を追加"),
        (1, "Base", 32,  "回復週 — 前週の80%に落とす"),
        (1, "Base", 36,  "ロング走14km"),
        (1, "Base", 40,  "ロング走16km"),
        (1, "Base", 40,  "回復週"),
        # W09-W16 Development
        (2, "Development", 44,  "ロング走18km、週1テンポ走5km"),
        (2, "Development", 48,  "ロング走20km"),
        (2, "Development", 48,  "回復週"),
        (2, "Development", 52,  "ロング走22km、テンポ走8km"),
        (2, "Development", 56,  "ロング走24km"),
        (2, "Development", 56,  "回復週"),
        (2, "Development", 60,  "ロング走26km、ハーフマラソン試走推奨"),
        (2, "Development", 56,  "回復週"),
        # W17-W24 Build
        (3, "Build", 64,  "ロング走28km、マラソンペース走8km"),
        (3, "Build", 64,  "回復週"),
        (3, "Build", 68,  "ロング走30km"),
        (3, "Build", 68,  "回復週"),
        (3, "Build", 72,  "ロング走32km"),
        (3, "Build", 72,  "回復週"),
        (3, "Build", 76,  "ロング走32km、マラソンペース走12km"),
        (3, "Build", 68,  "回復週"),
        # W25-W32 Peak
        (4, "Peak", 80,  "最高距離週。ロング走35km"),
        (4, "Peak", 72,  "回復週"),
        (4, "Peak", 80,  "ロング走35km（2回目）"),
        (4, "Peak", 72,  "回復週"),
        (4, "Peak", 76,  "ロング走32km"),
        (4, "Peak", 64,  "回復週"),
        (4, "Peak", 56,  "ロング走29km — テーパー開始"),
        (4, "Peak", 48,  "回復週"),
        # W33-W34 Taper
        (5, "Taper", 40,  "テーパー。ロング走21km、脚を溜める"),
        (5, "Taper", 24,  "レース週！月〜水ジョグのみ。日曜レース！"),
    ]

    for i, (phase_num, phase_name, km, desc) in enumerate(weekly_blueprints):
        week_num = i + 1
        week_start = START_DATE + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)
        plan[week_num] = {
            "phase": phase_num,
            "phase_name": phase_name,
            "week": week_num,
            "km": km,
            "description": desc,
            "start": week_start.isoformat(),
            "end": week_end.isoformat(),
        }

    return plan


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"weight_log": {}, "workout_log": {}}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(args=None):
    today = date.today()
    data = load_data()
    plan = build_training_plan()

    days_left = (RACE_DATE - today).days
    weeks_done = (today - START_DATE).days // 7 + 1
    current_week = min(max(weeks_done, 1), TOTAL_WEEKS)
    week_info = plan.get(current_week, {})

    # Latest weight
    weight_log = data.get("weight_log", {})
    if weight_log:
        latest_date = max(weight_log.keys())
        current_weight = weight_log[latest_date]
    else:
        current_weight = START_WEIGHT
        latest_date = "未記録"

    weight_lost = START_WEIGHT - current_weight
    weight_remaining = current_weight - GOAL_WEIGHT
    weight_pct = max(0, min(100, weight_lost / (START_WEIGHT - GOAL_WEIGHT) * 100))

    # Weekly progress
    week_workouts = {
        k: v for k, v in data.get("workout_log", {}).items()
        if week_info.get("start", "") <= k <= week_info.get("end", "")
    }
    week_km_done = sum(w.get("km", 0) for w in week_workouts.values())
    week_km_target = week_info.get("km", 0)

    print("=" * 58)
    print("  🏃 マラソントレーニング & 体重管理ダッシュボード")
    print("=" * 58)
    print(f"  今日:          {today}  （レースまであと {days_left} 日）")
    print(f"  レース:        {RACE_DATE}  フルマラソン")
    print()
    print(f"  ── 体重 ──────────────────────────────────")
    print(f"  スタート:      {START_WEIGHT} kg")
    print(f"  現在:          {current_weight} kg  （{latest_date}）")
    print(f"  目標:          {GOAL_WEIGHT} kg")
    print(f"  残り:          {weight_remaining:.1f} kg  [{_bar(weight_pct)}] {weight_pct:.0f}%")
    print()
    print(f"  ── 今週のトレーニング (W{current_week:02d}) ───────────────")
    print(f"  フェーズ:      {week_info.get('phase_name', '-')} ({week_info.get('start', '-')} 〜 {week_info.get('end', '-')})")
    print(f"  目標距離:      {week_km_target} km")
    print(f"  完了距離:      {week_km_done:.1f} km")
    pct = (week_km_done / week_km_target * 100) if week_km_target else 0
    print(f"  進捗:          [{_bar(pct)}] {pct:.0f}%")
    print(f"  メモ:          {week_info.get('description', '-')}")
    print("=" * 58)


def cmd_log_weight(args):
    if not args:
        print("使い方: python marathon_tracker.py weight <体重kg>")
        print("例:     python marathon_tracker.py weight 64.5")
        return
    try:
        weight = float(args[0])
    except ValueError:
        print("エラー: 数値で入力してください（例: 64.5）")
        return

    today = date.today().isoformat()
    data = load_data()
    data.setdefault("weight_log", {})[today] = weight
    save_data(data)
    diff = START_WEIGHT - weight
    print(f"[{today}] 体重 {weight} kg を記録しました。")
    print(f"スタートから {diff:+.1f} kg （目標まであと {weight - GOAL_WEIGHT:.1f} kg）")


def cmd_log_workout(args):
    """
    Usage: workout <km> [type] [note]
    type: easy | tempo | long | race | rest
    """
    if not args:
        print("使い方: python marathon_tracker.py workout <距離km> [タイプ] [メモ]")
        print("タイプ: easy(ジョグ) | tempo(テンポ走) | long(ロング走) | race(レース) | rest(休息)")
        print("例:     python marathon_tracker.py workout 10 easy '気持ちよく走れた'")
        return
    try:
        km = float(args[0])
    except ValueError:
        print("エラー: 距離は数値で入力してください")
        return

    run_type = args[1] if len(args) > 1 else "easy"
    note = args[2] if len(args) > 2 else ""

    today = date.today().isoformat()
    data = load_data()
    data.setdefault("workout_log", {})[today] = {
        "km": km,
        "type": run_type,
        "note": note,
    }
    save_data(data)
    print(f"[{today}] {run_type} {km} km を記録しました。{('— ' + note) if note else ''}")


def cmd_plan(args):
    plan = build_training_plan()
    today = date.today()

    # Optional filter: phase number
    filter_phase = int(args[0]) if args else None

    phase_labels = {1: "Base", 2: "Development", 3: "Build", 4: "Peak", 5: "Taper"}
    phase_colors = {1: "【P1 Base】", 2: "【P2 Dev 】", 3: "【P3 Build】", 4: "【P4 Peak】", 5: "【P5 Taper】"}

    current_week_num = min(max((today - START_DATE).days // 7 + 1, 1), TOTAL_WEEKS)

    print("=" * 70)
    print("  34週 フルマラソントレーニングプラン")
    print(f"  {START_DATE} → {RACE_DATE}")
    print("=" * 70)

    prev_phase = None
    for w, info in plan.items():
        if filter_phase and info["phase"] != filter_phase:
            continue
        if info["phase"] != prev_phase:
            print(f"\n  ──── Phase {info['phase']}: {info['phase_name']} ────────────────────────")
            prev_phase = info["phase"]

        marker = " ◀ 今週" if w == current_week_num else "      "
        print(f"  W{w:02d} ({info['start']}〜{info['end']})  {info['km']:>3}km  {info['description']}{marker}")

    print()
    print(f"  合計: {sum(v['km'] for v in plan.values())} km  /  34週")
    print("=" * 70)


def cmd_history(args):
    data = load_data()
    n = int(args[0]) if args else 14

    print(f"  ── 直近 {n} 日間の記録 ──────────────────────────────")
    today = date.today()
    for i in range(n - 1, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        w = data["weight_log"].get(d)
        run = data["workout_log"].get(d)
        if w or run:
            w_str = f"{w} kg" if w else "     -   "
            r_str = f"{run['type']} {run['km']}km {run.get('note','')}" if run else "-"
            print(f"  {d}  体重:{w_str:>8}   走行:{r_str}")


def _bar(pct, width=20):
    filled = int(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

COMMANDS = {
    "status":  (cmd_status,       "進捗ダッシュボードを表示"),
    "weight":  (cmd_log_weight,   "体重を記録    例: weight 64.2"),
    "workout": (cmd_log_workout,  "トレーニングを記録  例: workout 10 easy"),
    "plan":    (cmd_plan,         "全トレーニングプランを表示  例: plan [1-5]"),
    "history": (cmd_history,      "直近の記録を表示  例: history [日数]"),
}

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print("\n  Marathon Tracker — 使い方\n")
        for cmd, (_, desc) in COMMANDS.items():
            print(f"    python marathon_tracker.py {cmd:<10} {desc}")
        print()
        return

    cmd = args[0].lower()
    if cmd not in COMMANDS:
        print(f"不明なコマンド: {cmd}")
        return

    COMMANDS[cmd][0](args[1:])


if __name__ == "__main__":
    main()
