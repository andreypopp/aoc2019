import collections
from fractions import gcd
from pprint import pprint

Moon = collections.namedtuple('Moon', 'name x y z vx vy vz')

def update(state):
    next_state = []
    for this in state:
        vx, vy, vz = this.vx, this.vy, this.vz
        for moon in state:
            if this == moon:
                continue
            if this.x < moon.x:
                vx += 1
            elif this.x > moon.x:
                vx -= 1
            if this.y < moon.y:
                vy += 1
            elif this.y > moon.y:
                vy -= 1
            if this.z < moon.z:
                vz += 1
            elif this.z > moon.z:
                vz -= 1
        this = this._replace(
            vx=vx, vy=vy, vz=vz,
            x=this.x+vx, y=this.y+vy, z=this.z+vz
        )
        next_state.append(this)
    return next_state


def update_x(state):
    next_state = []
    for this in state:
        vx, vy, vz = this.vx, this.vy, this.vz
        for moon in state:
            if this == moon:
                continue
            if this.x < moon.x:
                vx += 1
            elif this.x > moon.x:
                vx -= 1
        this = this._replace(vx=vx, x=this.x+vx)
        next_state.append(this)
    return next_state


input = [
    Moon('A', x=-1, y=7, z=3, vx=0, vy=0, vz=0),
    Moon('B', x=12, y=2, z=-13, vx=0, vy=0, vz=0),
    Moon('C', x=14, y=18, z=-8, vx=0, vy=0, vz=0),
    Moon('D', x=17, y=4, z=-4, vx=0, vy=0, vz=0),
]

ex1 = [
    Moon('A', x=-1, y=0, z=2, vx=0, vy=0, vz=0),
    Moon('B', x=2, y=-10, z=-7, vx=0, vy=0, vz=0),
    Moon('C', x=4, y=-8, z=8, vx=0, vy=0, vz=0),
    Moon('D', x=3, y=5, z=-1, vx=0, vy=0, vz=0),
]


# For part 1

def energy(state):
    e = 0
    for moon in state:
        p = abs(moon.x) + abs(moon.y) + abs(moon.z)
        k = abs(moon.vx) + abs(moon.vy) + abs(moon.vz)
        e = e + p * k
    return e

# For part 2

def eq((ax, bx, cx, dx), (ay, by, cy, dy)):
    return ax == ay and bx == by and cx == cy and dx == dy

# TODO: this is b/c if a bad repr!
def eq_x((ax, bx, cx, dx), (ay, by, cy, dy)):
    return (
        ax.x == ay.x and bx.x == by.x and cx.x == cy.x and dx.x == dy.x
        and ax.vx == ay.vx and bx.vx == by.vx and cx.vx == cy.vx and dx.vx == dy.vx
    )

def eq_y((ax, bx, cx, dx), (ay, by, cy, dy)):
    return (
        ax.y == ay.y and bx.y == by.y and cx.y == cy.y and dx.y == dy.y
        and ax.vy == ay.vy and bx.vy == by.vy and cx.vy == cy.vy and dx.vy == dy.vy
    )


def eq_z((ax, bx, cx, dx), (ay, by, cy, dy)):
    return (
        ax.z == ay.z and bx.z == by.z and cx.z == cy.z and dx.z == dy.z
        and ax.vz == ay.vz and bx.vz == by.vz and cx.vz == cy.vz and dx.vz == dy.vz
    )

def run(init, update=update, eq=eq):
    step = 0
    state = init
    while True:
        state = update(state)
        step += 1
        if step % 1000000 == 0:
            print step
        if eq(state, init):
            return step

# Find cycles for each dim separately
cx = run(input, update, eq_x)
cy = run(input, update, eq_y)
cz = run(input, update, eq_z)

# Find LCM
cxy = cx * cy / gcd(cx, cy)
cxyz = cxy * cz / gcd(cxy, cz)
print cxyz
