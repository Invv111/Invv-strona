<div align="center">

# 🛗 Elevate

**Elevators for your server. Stand on an elevator and jump to go up a floor, or sneak to go down. That's it.**

No ladders, no water columns, no slow scaffolding climbs. Craft an elevator from wool, put one on every floor of your base, and move between them in a blink, with a floor number on screen as you arrive.
Server-side only. **No resource pack, no mods, no dependencies.** Bukkit, Spigot, Paper, Purpur and Folia, **1.20 → 26.x**.

</div>

---

## ✨ Features

### ⬆️ Jump up, sneak down
- **Jump** on an elevator and you're on the next elevator above. **Sneak** and you're on the one below.
- Works over any distance: 3 blocks or 300, through floors, ceilings and solid rock.
- You keep your exact spot on the block and the way you're facing, so arriving feels seamless.
- Floors that are blocked (no two free blocks to stand in) are skipped and you go on to the next one.
- A short cooldown stops one jump from flying you up several floors.

### 🏢 Floors with numbers and names
- Arrive to a **title**: `▲ Floor 3/5`, with the floor's name underneath.
- **Name a floor by renaming the elevator in an anvil** before you place it: `Kitchen`, `Storage`, `Nether portal`. No commands needed.
- Step onto an elevator and the **action bar** shows where you are and which way you can go: `jump ▲ · Floor 2/4 · Storage · ▼ sneak`.
- `/elevate info` lists every floor in the shaft, with heights and names.
- Place your first elevator and it tells you where the next one goes.

### 🎨 Sixteen colors, many shafts
- **Craft an elevator** from 8 wool of one color around an ender pearl. All 16 wool colors work.
- Colors only connect to the same color, so **several shafts can run side by side or through each other**: the red one goes to the vault, the blue one to the farms.
- The elevator item glints and keeps its name, so it's easy to spot in a chest.
- Break one and you get the elevator back, name included. Wool in your builds **never** becomes an elevator by accident.

### 🧱 Or turn any block into an elevator
- Prefer the classic "iron block elevator"? Switch `mode` to `blocks` and every block on your list is an elevator, no crafting needed.
- `both` mode mixes crafted and block elevators.

### 🛡️ Safe and sturdy
- Elevators can't be **burned, pushed by pistons or taken by endermen**.
- **Explosions** pop them out as elevator items instead of plain wool.
- Elevator items can't be crafted into beds or carpets by mistake.
- Players never land in lava, fire or a wall.
- Elevator data lives **inside the chunk itself**: no database, no files to back up, nothing to clean up. Moving, copying or trimming the world just works.

### ✨ Feels good to use
- Portal particles where you leave, a sparkle where you land, and a soft bell on arrival, pitched up going up and down going down.
- Every sound, particle and message can be changed or turned off.

### 🤝 Plays nicely with other plugins
- Uses normal plugin teleports, so anti-cheat and logging plugins see a regular teleport.
- **Folia native**: the elevator and the player are always in the same region, so there's no cross-thread work at all.
- Disable it per world.

---

## 🛠️ Crafting

```
 W W W
 W P W      W = wool of one color
 W W W      P = ender pearl
```

You get one elevator of that wool's color. The middle item and the amount are configurable, and the recipe can be turned off so elevators only come from `/elevate give`.

---

## ⌨️ Commands

| Command | Description | Permission |
|---|---|---|
| `/elevate` | Help | — |
| `/elevate info` | Floors of the elevator you stand on | `elevate.info` |
| `/elevate name <name\|clear>` | Name or rename the floor you stand on | `elevate.name` |
| `/elevate give <player> [color] [amount]` | Give elevator items | `elevate.admin` |
| `/elevate reload` | Reload config and messages | `elevate.admin` |

Aliases: `/elevator`, `/lift`.

| Permission | Default | |
|---|---|---|
| `elevate.use` | everyone | Ride elevators |
| `elevate.place` | everyone | Place crafted elevators |
| `elevate.craft` | everyone | Craft elevators |
| `elevate.info` | everyone | `/elevate info` |
| `elevate.name` | op | `/elevate name` (anvil naming works for everyone) |
| `elevate.admin` | op | Give and reload |
| `elevate.notify` | op | Update notices |

---

## ⚙️ Configuration

```yaml
mode: crafted              # crafted, blocks or both
blocks:                    # used by 'blocks' and 'both'
  - IRON_BLOCK
  - DAYLIGHT_DETECTOR
same-color-only: true      # elevators only connect to the same block
max-distance: 0            # 0 = the whole height of the world
require-space: true        # skip floors without room to stand

controls:
  jump-up: true
  sneak-down: true
  cooldown-ticks: 6

display:
  arrival: title           # title, actionbar or none
  hint: true               # action bar when stepping onto an elevator

effects:
  particles: true
  sounds-up:
    - 'minecraft:entity.enderman.teleport:0.25:1.9'
    - 'minecraft:block.note_block.bell:0.55:1.5'

recipe:
  enabled: true
  center: ENDER_PEARL
  amount: 1
  discover: true           # unlock the recipe in everyone's recipe book

disabled-worlds: []
```

Every message supports **color codes and hex colors** (`&#7fd7ff`). **English and Polish** are included, and you can add your own `lang/<name>.yml`. `/elevate reload` applies everything live.

---

## 🧑‍💻 For developers

`ElevatorUseEvent` (cancellable) fires before every ride, with the start and target block, the direction and the floor number. Cancel it, or point the player somewhere else.

```java
@EventHandler
public void onRide(ElevatorUseEvent event) {
    if (event.isUp() && !event.getPlayer().hasPermission("vip.penthouse")
            && event.getFloor() == event.getFloors()) {
        event.setCancelled(true);
    }
}
```

---

## 📦 Compatibility

| | |
|---|---|
| **Servers** | Bukkit, Spigot, Paper, Purpur, Folia and their forks |
| **Versions** | 1.20 → 26.x |
| **Java** | 17+ (21+ for 1.20.5 and newer, as Minecraft itself requires) |
| **Dependencies** | None |
| **Clients** | Vanilla. Nothing to install |

---

<div align="center">

### 🐞 Found a bug or have an idea?

**Report it on our [Discord](https://discord.gg/E9hpUj3E6G).** That is the only place bug reports are handled, so please don't use other channels.

Made by **Invv** · [More plugins](https://modrinth.com/user/invv) · [Discord](https://discord.gg/E9hpUj3E6G)

</div>
