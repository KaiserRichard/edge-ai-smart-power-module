"""Small, exact schematic excerpts allowed by the owner's final feedback.

These are teaching excerpts of the review PDF, never new circuit designs.
Analogy, layout, block and realistic illustrations remain ChatGPT prompts.
All coordinates are drawing coordinates, not PCB geometry or dimensions.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent.parent
WIRE = "#354659"
SENSE = "#087f8c"
BLUE = "#1764ab"
PURPLE = "#7645a5"
ORANGE = "#bd6107"


class Circuit:
    def __init__(self, title, subtitle, width=14, height=7):
        self.fig, self.ax = plt.subplots(figsize=(width, height))
        self.ax.set(xlim=(0, 14), ylim=(0, 7))
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.fig.suptitle(title, fontsize=17, weight="bold", y=.96)
        self.fig.text(.5, .89, subtitle, ha="center", fontsize=10, color=WIRE)

    def wire(self, *points, color=WIRE, dashed=False):
        self.ax.plot(*zip(*points), color=color, lw=1.7,
                     ls="--" if dashed else "-", solid_capstyle="round")

    def node(self, x, y, color=WIRE):
        self.ax.plot(x, y, "o", ms=4.5, color=color)

    def text(self, x, y, label, size=11, color=WIRE, ha="center", va="center"):
        self.ax.text(x, y, label, fontsize=size, color=color, ha=ha, va=va)

    def terminal(self, x, y, label, side="left", color=WIRE):
        self.ax.plot(x, y, "o", ms=6, mfc="white", mec=color, mew=1.5)
        dx = -.13 if side == "left" else .13
        self.text(x+dx, y, label, ha="right" if side == "left" else "left", color=color)

    def resistor(self, x1, y1, x2, y2, label, side=1, color=WIRE):
        # IEC rectangle, with long external leads to keep labels readable.
        if y1 == y2:
            mid=(x1+x2)/2
            self.wire((x1,y1),(mid-.45,y1),color=color)
            self.wire((mid+.45,y1),(x2,y2),color=color)
            self.ax.add_patch(Rectangle((mid-.45,y1-.15),.9,.3,
                                       facecolor="white",edgecolor=color,lw=1.7))
            self.text(mid,y1+side*.52,label,size=10,color=color)
        elif x1 == x2:
            mid=(y1+y2)/2
            self.wire((x1,y1),(x1,mid+.45),color=color)
            self.wire((x1,mid-.45),(x2,y2),color=color)
            self.ax.add_patch(Rectangle((x1-.15,mid-.45),.3,.9,
                                       facecolor="white",edgecolor=color,lw=1.7))
            self.text(x1+side*.34,mid,label,size=10,color=color,
                      ha="left" if side>0 else "right")
        else:
            raise ValueError("Resistor must be horizontal or vertical")

    def capacitor(self, x, top, bottom, label, side=1):
        mid=(top+bottom)/2
        self.wire((x,top),(x,mid+.1))
        self.wire((x,bottom),(x,mid-.1))
        for y in (mid-.1,mid+.1): self.wire((x-.3,y),(x+.3,y))
        self.text(x+side*.42,mid,label,size=10,ha="left" if side>0 else "right")

    def ground(self, x, y, label="GND"):
        self.wire((x,y),(x,y-.18))
        for dy,w in ((.18,.30),(.30,.20),(.42,.09)):
            self.wire((x-w,y-dy),(x+w,y-dy))
        if label: self.text(x,y-.65,label,size=10)

    def box(self, x, y, w, h, label, color=BLUE):
        self.ax.add_patch(Rectangle((x,y),w,h,facecolor="#f5f9fc",edgecolor=color,lw=1.5))
        self.text(x+w/2,y+h/2,label,color=color)

    def save(self, filename, note):
        self.fig.text(.5,.085,note,ha="center",va="center",fontsize=9,color=WIRE)
        self.fig.text(.5,.025,"SCHEMATIC TEACHING EXCERPT · omitted circuitry must be read in the source PDF\n"
                      "NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED",
                      ha="center",fontsize=9,color="#9b2929")
        self.fig.subplots_adjust(top=.85,bottom=.15,left=.035,right=.965)
        OUT.mkdir(parents=True,exist_ok=True)
        self.fig.savefig(OUT/filename,dpi=180,facecolor="white")
        plt.close(self.fig)
        print(OUT/filename)
