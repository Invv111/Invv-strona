<div align="center">

# 🌾 Reap

**Farming without the busywork. Right-click a grown crop and it's harvested and planted again. Swing a better hoe and the whole field around you is reaped in one sweeping wave.**

No more breaking, picking up and replanting crop by crop, and no more fields full of holes.
Server-side only. **No resource pack, no mods, no dependencies.** Bukkit, Spigot, Paper, Purpur and Folia, **1.20 → 26.x**.

</div>

---

## ✨ Features

### 🖱️ Right-click harvesting
- **Right-click a fully grown crop** to harvest it. The drops pop out and the crop is **replanted on the spot**.
- Works on **wheat, carrots, potatoes, beetroots, nether wart and cocoa**. Cocoa stays on its side of the jungle log.
- **One seed is taken from the drops** for the replant, so you never lose seeds from your inventory.
- Unripe crops are left alone, so a misclick can't ruin a fresh field.
- **Fortune works.** A Fortune III hoe gives the same extra drops as breaking crops by hand.

### 🌊 Hoes reap a whole area, in a wave
- With a hoe in hand, every grown crop around the one you click is harvested too, **spreading out ring by ring** like a wave through the field.
- **Better hoe, bigger area.** By default: stone/iron/copper 3×3, gold/diamond 5×5, netherite **7×7**. Each tier is configurable, with an optional Efficiency bonus.
- Works on slopes and terraces: crops a block above or below are included.
- **Sneak** to harvest just one crop.
- The hoe loses **1 durability per swing, not per crop**, and Unbreaking is respected.

### 🎋 Sugar cane, cactus and bamboo
- Right-click any part of a column and everything **above the bottom block** is cut, so it **grows back on its own**.
- Hoes cut every grown column in their area too.

### 🛡️ Farmland that stays farmland
- **No more trampling.** Jumping players and wandering mobs can't turn your farmland back into dirt.
- Players and mobs can be set separately. `reap.trample.bypass` lets chosen players trample anyway.

### ✨ Feels good to use
- A crunchy crop sound with a little pitch variation, block crumbs, and green sparkles where a crop is replanted.
- An **action bar summary** after every harvest: `+24 crops · Wheat ×31, Wheat Seeds ×12`.
- Optional **auto-pickup** (drops go straight into your inventory) and optional **XP** per crop.
- `/reap stats` counts every crop you've ever harvested.
- `/reap toggle` lets each player turn it off for themselves. The setting is kept across restarts.

### 🤝 Plays nicely with other plugins
- **Protection plugins are respected.** WorldGuard, GriefPrevention, Lands, Towny, Residence and friends are asked first, so nobody can harvest a field they can't build in.
- Every harvested crop counts as a broken block, so **Jobs, quests, logs (CoreProtect) and McMMO-style plugins** keep working.
- **Folia native**, with the wave running on the region that owns the field.
- Per-world: whitelist or blacklist worlds.

---

## ⌨️ Commands

| Command | Description | Permission |
|---|---|---|
| `/reap` | Help | — |
| `/reap toggle` | Turn right-click harvesting on or off for yourself | `reap.toggle` |
| `/reap stats [player]` | How many crops you (or someone else) have harvested | `reap.stats` |
| `/reap reload` | Reload config and messages | `reap.admin` |

Alias: `/harvest`.

| Permission | Default | |
|---|---|---|
| `reap.use` | everyone | Right-click harvesting |
| `reap.area` | everyone | Hoes harvest an area |
| `reap.trample.bypass` | nobody | Can trample farmland anyway |
| `reap.admin` | op | Reload, other players' stats |
| `reap.notify` | op | Update notices |

---

## ⚙️ Configuration

```yaml
harvest:
  right-click: true
  require-hoe: false        # true = only hoes harvest
  replant: true
  auto-pickup: false
  experience: 0.0           # XP orbs per crop
  respect-protection: true

area:
  enabled: true
  radius:                   # 1 = 3x3, 2 = 5x5, 3 = 7x7
    wooden: 0
    stone: 1
    copper: 1
    iron: 1
    golden: 2
    diamond: 2
    netherite: 3
  efficiency-bonus: 0
  height: 1
  sneak-for-single: true
  wave-ticks: 1             # 0 = everything at once
  durability: 1             # per swing, not per crop

farmland:
  protect-from-players: true
  protect-from-mobs: true
```

Every message supports **color codes and hex colors** (`&#e8b84a`). **English and Polish** are included, and you can add your own `lang/<name>.yml`. `/reap reload` applies everything live.

---

## 🔌 PlaceholderAPI

| Placeholder | Value |
|---|---|
| `%reap_harvested%` | Crops the player has harvested |
| `%reap_enabled%` | `true` when the player has right-click harvesting on |

## 🧑‍💻 For developers

`CropHarvestEvent` (cancellable) fires for every crop, after protection plugins have agreed. Change the drops, stop the replant or cancel it.

```java
@EventHandler
public void onHarvest(CropHarvestEvent event) {
    if (event.getBlock().getType() == Material.WHEAT) {
        event.getDrops().add(new ItemStack(Material.BREAD));
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
| **Dependencies** | None. PlaceholderAPI optional |
| **Clients** | Vanilla. Nothing to install |

---

<div align="center">

### 🐞 Found a bug or have an idea?

**Report it on our [Discord](https://discord.gg/E9hpUj3E6G).** That is the only place bug reports are handled, so please don't use other channels.

Made by **Invv** · [More plugins](https://modrinth.com/user/invv) · [Discord](https://discord.gg/E9hpUj3E6G)

</div>
