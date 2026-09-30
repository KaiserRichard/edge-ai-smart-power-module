# TASK 3 — test-board hooks and bounded fault fixture

**PROPOSED ONLY. NOT FOR FABRICATION — ENGINEERING REVIEW REQUIRED.** No fixture is built or qualified. Every new reference is a reservation to check at capture. Fixture engineering is required before fault energization; this document does not authorize PCB fabrication.

**DECISION:** use the real selected harness terminating in a passive Pi-header emulator with a dummy load. The Pi/SBC, USB and host I2C are physically absent. Use removable Phoenix 1776508/1777989 mating connections for the 5 A load path, and a removed JST host plug for I2C. Small 2.54 mm signal jumpers are not rated substitutes for a 5 A/fault force connection. Preserve both positive pins 2/4 and GND6/9/14/20/25/30/34/39 at the far end. Its mating male contact construction remains an ASSUMED emulator, not qualification of an actual Pi header.

```mermaid
flowchart LR
  F[Main eFuse] --> P[VIN_PROTECTED and counted Cin]
  P --> X[Removable external high-side fault switch]
  X --> S[BUCK_SW]
  S --> L[L201 + minimal current-probe link]
  L --> R[VOUT_5V1 / existing bulk bank / raw dump]
  R --> Q[BSC034 opposed pair]
  Q --> O[VOUT_PROTECTED / protected crowbar]
  O --> T[2 mΩ telemetry shunt and J502]
  T --> H[Real send and return harness]
  H --> D[Far-end dummy R / C and load]
```

**FAULT INJECTION proposal:** removable external QF1 BSC034N06NSATMA1, drain VIN_PROTECTED/source BUCK_SW, bridges the actual buck high-side conduction path so fault current still passes through L201. Drive it with a separately isolated/source-referenced gate fixture (LTC7001IMSE#PBF research driver), default-low command and gate-source discharge. Verify its actual VGS/VDS/current/turn-on/turn-off and pulse/SOA; its 60 V rating is not a hot fault-current rating. Gate timing is not the fault-onset endpoint. At an initial current-limited low-energy check, force buck EN low and verify both internal switches are inactive before injection. Otherwise a conducting internal low-side FET plus the injected high-side can produce a VIN-to-GND shoot-through unrelated to the intended output-path experiment. Manufacturer EN/shutdown/reverse-flow behavior must be checked; a live-PWM silicon-short experiment is a separately reviewed mode. Disabling the controller tests the output containment network, not every live silicon failure.

QF1 and its supply must have no energy reservoir outside the counted main Cin/source boundary. Install any driver bypass on its isolated control side; measure capacitive coupling/backfeed. A stiff external supply connected to VOUT_5V1 bypasses L201 and introduces new voltage/current/energy; it is **not** an equivalent test of the Gate3b source bound. It may be used only as a separately bounded output-bank/current-boundary characterization through measured impedance and measured upstream reservoirs, with its additional energy included. Do not describe that result as the actual high-side-short test.

**Two source-cutoff modes:** A, autonomous board trigger and source shutdown; B, independent fixture pulse that asserts SHDN after a measured delay to exercise the conditional ≤10 µs/≤100 µC source contract. Record both. Mode B alone cannot PASS autonomous containment. The injector may open as an emergency ceiling after a fault persists; any protective result that depends on that fixture opening is not a DUT PASS. Abort endpoint/time/current/energy must be set from the fixture's reviewed hot ratings before energizing. A bench supply current limit can act too slowly and must not be the only energy limit.

Required physical hooks (separate force and sense; paired local returns):

| Reservation / location | What it exposes | Capture/qualification purpose |
|---|---|---|
| TP201/TP202 plus paired GND | VIN_PROTECTED, BUCK_SW and both L201 terminals; reserve extra pad if names conflict | Differential L voltage; `Ldiff=(VL−I·DCR)/(dI/dt)`; verify switch-node common-mode rating |
| JP201 / external force connector | VIN_PROTECTED↔QF1↔BUCK_SW, normally absent | Minimal-area fault injection loop; cannot bypass L201 or local-C accounting |
| IL201_FORCE loop/link, separate sense pads | Series with L201 between its output terminal and raw bank | DC current probe through cutoff/tail; keep added L/R measured and include in model; no long convenient probe cable |
| IMAIN_FORCE link before local main Cin | U101 OUT→all C201…204/main VIN reservoirs | Replenishment `Q+=integral(max(Iin,0)dt)`; captures commutation/reverse tail; AUX branch excluded only if proved independent |
| Existing TP301 plus dedicated paired GND | VOUT_5V1 directly at raw bulk | Raw peak/ringing/discharge; no claim from protected voltage alone |
| Dedicated VPROT/GND pad pair after Q302 | VOUT_PROTECTED at protected bank/crowbar | Capture series current-off and protected clamp waveform |
| Kelvin Q301/Q302 gate/source/drain pads | Common source, gates, each drain and driver BST | Loaded source-referenced VGS, physical VDS/current trajectory, turn-off/avalanche screening |
| TP306…TP312 plus new raw-driver gate pads | OV_DIV, comparator out, latched FAULT, crowbar VGS, DRV_HOLD, DET5, SHDN | Analog/digital timing endpoints, partial power and stored-drive action; probe loading included |
| TP402/403 and TP405/406/GND | Shunt sense K+/K− separate from force terminals | 10 mV nominal at5 A; fault pulse/INA pin exposure; differential filter excludes force current |
| Raw/protected dump current-probe links | Each ballast/Q303/Q330 force branch separately | `E=integral(V·I dt)` and resistor sharing; links add parasitics and need final-layout correlation |
| J502 removable load connector / JP501 fixture reservation | Real harness or local dummy, never parallel SBC feed | Physical lockout and load change only with power off and all banks discharged |
| Remote paired sense pads at emulator 5 V/GND contacts | Both physical positives and loaded return reference plane | Far-end peak/minimum/current sharing; measure local module voltage simultaneously |

**Layout requirements for authorized future capture:** switching/injection/disposal loops short with paired returns; large fault current must not share detector/reference Kelvin returns. Keep divider/ref away from SW. Measure current and voltage at identical energy reference planes and deskew them. Add fixture parasitic L/C/R to the model rather than silently subtracting it. A probe loop that changes peak/timing requires re-correlation with the final layout; a copper jumper closes it during ordinary operation. Include temperature attachment points at all ballast terminals, series FETs, input pass/eFuse, inductor, connector/crimps and detector/driver devices.

**Grounding requirement:** use rated differential/isolated measurements on the harness and switch/gate nodes. Oscilloscope earth, electronic-load earth, USB/control equipment and probe returns must not form an alternate low-resistance harness return or bypass the series protection. Keep instruments' protective earth intact. Establish the actual ground/return diagram with continuity checks before power; use a floating-load arrangement only where the equipment is designed for it.

**Measured fault epoch:** define `t0` at actual QF1 conduction/VL change, with stated threshold and measurement uncertainty; record injector command as a separate trace. Define useful crowbar action by measured current/voltage clamp, series cutoff by actual current cessation, source cutoff by current at IMAIN_FORCE, and tail completion by IL201 and both node voltages. Record raw files and range/bandwidth/deskew/calibration. The full [bench plan](TEST_PLAN.md) follows TASK 4.
