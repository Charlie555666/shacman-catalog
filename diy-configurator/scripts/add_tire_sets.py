"""Add tire complete-set pricing info to accessories.json"""
import json, os

DATA = r"c:\Users\Administrator\WorkBuddy\20260605101515\shacman-catalog\diy-configurator\data"
TIRE_CATS = {"米其林", "三角", "玲珑", "双钱", "中策", "金宇", "成山", "轮辋"}

# Tire count per drive type (complete set = road tires + 1 spare)
TIRE_COUNT = {
    "4×2": 7,
    "4x2": 7,
    "6×4": 11,
    "6x4": 11,
    "8×4": 13,
    "8x4": 13,
}

acc = json.load(open(os.path.join(DATA, "accessories.json"), "r", encoding="utf-8"))
for item in acc["items"]:
    if item["category"] in TIRE_CATS:
        item["is_tire_set"] = True
        item["tire_count"] = TIRE_COUNT  # map of drive→count

with open(os.path.join(DATA, "accessories.json"), "w", encoding="utf-8") as f:
    json.dump(acc, f, ensure_ascii=False, indent=2)

tire_items = sum(1 for i in acc["items"] if i.get("is_tire_set"))
print(f"Tire set items: {tire_items}")
print("Done!")
