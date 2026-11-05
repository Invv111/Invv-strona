<div align="center">

# 🪑 Lounge

**Sit, lay and crawl anywhere. Built for Paper and Folia, with zero dependencies.**

Right-click a stair to sit on it. Type `/lay` and lie down with your own skin. Crawl through 1-block gaps.
Ride your friends around. It just works, from **1.20 up to 26.x**, with no ProtocolLib and no setup.

</div>

---

## ✨ Features

### 🪑 Chairs
- **Right-click** stairs, slabs or carpets with an empty hand to sit down.
- You **face away from the backrest** automatically and sit *on* the step, not inside it.
- Works with **every stair, slab and carpet** out of the box, read from Minecraft's own block tags, so new wood types from future updates work without a plugin update.
- Upside-down stairs, top slabs and blocks with no headroom are skipped, so nothing looks wrong.
- **One player per chair.** Break the chair and whoever sits on it stands up.
- Building still works: holding a block or sneaking never makes you sit.

### 💺 /sit
Sit down right where you stand. Run it again or **sneak** to get up.

### 🛌 /lay
Lie down on the ground. Lounge spawns a sleeping **mannequin with your skin, armor and held items** while your real body stays hidden.
No packets, no NPC library, no fake players in the tab list. *(Needs Minecraft 1.21.9+, the version that added mannequins.)*

### 🐛 /crawl
Crawl on land in the swimming pose to get through **1-block gaps**. Everyone sees you crawl and your hitbox really shrinks.
Optional **double-sneak to crawl**. Sneak once to stand up.

### 🧍 Player stacking
**Right-click a player** to sit on their head. Make a tower of up to 3 (configurable).
The player at the bottom **sneaks to throw everyone off**, and `/lounge toggle` stops others from sitting on you at all. The choice is saved on the player, so there's no database.

### 🧹 Clean and safe
- When you get up, you're put back **where you were standing**, so nobody gets stuck in stairs.
- Seats are invisible marker entities that are **never saved to disk**. A crash or `/stop` never leaves armor stands behind.
- Protection plugins are respected: if WorldGuard, GriefPrevention, Lands and the like deny the click, you don't sit.
- Quit, die, teleport or change worlds while sitting, and everything is cleaned up.

---

## ⌨️ Commands

| Command | Description | Permission |
|---|---|---|
| `/sit` | Sit where you stand (again to get up) | `lounge.sit` |
| `/lay` | Lie down (again to get up) | `lounge.lay` |
| `/crawl` | Start or stop crawling | `lounge.crawl` |
| `/lounge toggle` | Allow or block others sitting on you | `lounge.toggle` |
| `/lounge stand <player\|*>` | Make players stand up | `lounge.admin` |
| `/lounge reload` | Reload config and messages | `lounge.admin` |

Right-clicking chairs needs `lounge.chair`, and sitting on players needs `lounge.stack`. Every player permission is **on by default**.
`lounge.notify` (op) tells admins about updates.

---

## ⚙️ Configuration

Everything can be switched off: chairs, `/sit`, `/lay`, `/crawl` and stacking, each with its own options. You can also turn Lounge off in chosen worlds.
Add your own chairs in one line, by name or by tag:

```yaml
chairs:
  blocks:
    '#stairs': 0.5
    '#slabs': 0.5
    '#wool_carpets': 0.0625
    hay_block: 1.0      # your own
```

All messages use **MiniMessage** (gradients, hover, click). **English and Polish** come included, and you can add your own `lang/<name>.yml`.

---

## 🧩 For developers

- **Events:** `PlayerSitEvent` (cancellable), `PlayerStandEvent`, `PlayerCrawlEvent` (cancellable), `PlayerStackEvent` (cancellable)
- **API:** `LoungeAPI.isSeated(player)`, `getSeatType`, `sit`, `lay`, `stand`, `startCrawling`, `stopCrawling`, `allowsStacking`
- **PlaceholderAPI:** `%lounge_pose%` (standing / sitting / laying / crawling / riding), `%lounge_sitting%`, `%lounge_laying%`, `%lounge_crawling%`, `%lounge_stacking%`

---

## ✅ Compatibility

| | |
|---|---|
| **Servers** | Paper, Folia, Purpur and other Paper forks |
| **Versions** | 1.20 → 26.x (`/lay` from 1.21.9) |
| **Java** | 17+ |
| **Dependencies** | None (PlaceholderAPI optional) |

Tested with a real client and bots on Paper 1.20.6, 1.21.4, 1.21.11, 26.1.2 and Folia 1.20.6, and checked to start cleanly on Paper and Folia 26.3.
Every seat runs on its player's own region scheduler, so it is **fully Folia-safe**, not just "it loads".

---

<div align="center">

Made by **Invv** · Check out my other plugins: [Tpa](https://modrinth.com/plugin/tpaa) · [Antixray](https://modrinth.com/plugin/antyxray) · [SetSpawn](https://modrinth.com/plugin/set.spawn) · [Nametags](https://modrinth.com/plugin/nametags)

*Found a bug or have an idea? Leave a comment, I read all of them.* 💬

</div>
