# Asteroids (Python)

A Python port of the Asteroids reference game from
[agerber/proJava](https://github.com/agerber/proJava). The Java original
passes a `java.awt.Graphics` object through `Movable.draw(Graphics g)`;
this port replicates that pattern with a thin `Graphics` wrapper around
PIL's `Image` + `ImageDraw`, so every sprite gets a stateful drawing
context — not a buffered image.

## Run

Uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf python-tk@3.14
uv sync           # create .venv and install pinned deps from pyproject.toml + uv.lock
uv run main.py    # launch the game, or run game from the gui
```

Controls:

| Key            | Action                       |
| -------------- | ---------------------------- |
| `S`            | start                        |
| `P`            | pause                        |
| `Q`            | quit                         |
| arrows         | rotate / thrust              |
| space          | fire                         |
| `F`            | nuke                         |
| `M`            | toggle music                 |
| `A`            | toggle radar                 |
| `V`            | kill all foes (debug)        |

## Architecture

Classic MVC, mirroring the Java reference. The Java `Graphics g`
parameter is replaced by a thin `Graphics` wrapper class so the
`Movable.draw(g)` contract is faithful to the Java side.

```
                            +-----------------------+
                            |       main.py         |
                            |  (entry — boots Game) |
                            +----------+------------+
                                       |
                                       v
+----------------------------+   +-----+---------------+   +--------------------------+
|        CONTROLLER          |   |        VIEW         |   |          MODEL           |
+----------------------------+   +---------------------+   +--------------------------+
| Game (Thread)              |   | GameFrame (tk.Tk)   |   | Movable  <<interface>>   |
|  - animation loop          |-->| GamePanel           |   |  + move()                |
|  - key bindings            |   |  + update()         |   |  + draw(g: Graphics)     |
|  - collisions              |   |   creates off-      |   |  + getCenter/Radius/Team |
|  - level / floater spawn   |   |   screen Image,     |   |  + addToGame/removeFrom  |
|                            |   |   wraps in Graphics |   +-----------+--------------+
| CommandCenter (Singleton)  |   |   passes g to every |               ^
|  - movFriends/Foes/        |<--+   mov.draw(g)       |               |
|    Floaters/Debris (lists) |   | Graphics  <-+       |   +-----------+--------------+
|  - falcon, radar, frame,   |   |  + setColor |       |   | Sprite (abstract)        |
|    score, level, universe  |   |  + drawRect/Oval/   |   |  - center, deltaX/Y      |
|                            |   |    Polygon/String   |   |  - cartesians[]/raster  |
| GameOpsQueue / GameOp      |   |  + drawImage        |   |  + renderVector(g)       |
|  - deferred add/remove     |   |  +-------+----------+   |  + renderRaster(g, img)  |
|    (avoids mutating lists  |   |          | wraps        +-----------+--------------+
|     during iteration)      |   |          v                          ^
|                            |   |   PIL Image +                       |
| ImageLoader, SoundLoader   |   |   PIL ImageDraw                     |
|  - singleton resource caches                                         |
+----------------------------+                                         |
                                                                       |
                  Concrete sprites (each implements move(), draw(g))   |
                  Falcon, Asteroid, Bullet, Nuke,                      |
                  Floater <- ShieldFloater, NukeFloater,        ------/
                  WhiteCloudDebris, Star, Radar
```

### The Graphics context

Java's `java.awt.Graphics` is a stateful drawing context: callers
`setColor`, `setFont`, then issue `drawRect`/`drawString`/`drawPolygon`
calls that consume that state. PIL exposes the same primitives through
`ImageDraw`, but stateless and split across two objects (`Image` for
raster blits, `ImageDraw` for vector primitives). The `Graphics` class
in `mvc/view/Graphics.py` binds them together and presents the same
Java-style API, so `Movable.draw(g)` is a 1:1 port of the Java
`void draw(Graphics g)` signature.

```
+-------------------+        +---------------------+
| Java AWT          |        | Python              |
+-------------------+        +---------------------+
| Graphics g        |  -->   | Graphics g          |
|  - color (state)  |        |  - _color (state)   |
|  - font  (state)  |        |  - _font  (state)   |
|  - g.drawPolygon()|        |  - g.drawPolygon()  |
|  - g.fillRect()   |        |  - g.fillRect()     |
|  - g.drawString() |        |  - g.drawString()   |
|  - g.drawImage()  |        |  - g.drawImage()    |
+-------------------+        +----------+----------+
                                        |
                                        v
                             +----------+----------+
                             |   PIL.Image (raster)|
                             |   PIL.ImageDraw     |
                             +---------------------+
```

### Frame loop

```
Game.run() (animation thread)
   |
   v
GamePanel.update()
   |--- create off-screen Image (double-buffer)
   |--- g = Graphics(image)
   |--- moveDrawMovables(g, debris, floaters, foes, friends)
   |       for each mov: mov.move(); mov.draw(g)
   |--- drawMeters(g) / drawFalconStatus(g) / drawNumberShipsRemaining(g)
   '--- blit image via ImageTk.PhotoImage onto tk Label
```
