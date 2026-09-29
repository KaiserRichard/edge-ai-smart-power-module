* Authored open behavioral model; no vendor model or third-party circuit copied.
* NOT RUN in ngspice. Numerical auxiliaries are not physical components.
* Electrical inputs and evidence labels are in each generated .cir wrapper.
* V(il_state) represents inductor current in A; C=1 implements dI/dt.
* V(cb_state) represents crowbar current in A, held at zero until action.
* Timer voltages represent elapsed microseconds: 1 mA / 1 nF = 1 V/us.
* ASSUMED numerical reset RC = 1 ps; latch seed = 1 uV (1 ps timer time).

Vsource source 0 {VSOURCE}
Befuse source cin I={min(max((v(source)-v(cin))/REFUSE,0),ILIMIT)}
Cin cin 0 {CINPUT} IC={VSOURCE}
Craw raw 0 {CRAW} IC={VINITIAL}
Cload load 0 {CLOAD} IC={VINITIAL}

* Same discontinuous differential inductance as Python, not a flux-table model.
Cil il_state 0 1 IC={ILOAD}
Bil_state 0 il_state I={(v(cin)-v(raw)-v(il_state)*RLOSS)/(abs(v(il_state))<=ISAT ? LNOM : LNOM*LSAT)}
Bpowerstage cin raw I={v(il_state)}

* With CBULK=0 the branch current is exactly zero. Cbulk's 1 F auxiliary
* only avoids a zero capacitor value; it is decoupled in that case.
Bbulk raw bulk I={CBULK>0 ? (v(raw)-v(bulk))/RBULK : 0}
Cbulk bulk 0 {CBULK>0 ? CBULK : 1} IC={VINITIAL}

* First upward threshold crossing starts a persistent elapsed-time clock.
* Its retained charge is the fault memory; raw falling does not reset it.
Ctrip trip_clock 0 1n IC=0
Btrip 0 trip_clock I={(v(raw)>=VTRIP || v(trip_clock)>1u) ? 1m : 0}
Baction action 0 V={v(trip_clock)>=DELAY_US ? 1 : 0}

* Reverse current must persist for REVERSE_US, as in Python. Reset whenever
* forward/zero current returns; a triggered reverse cutoff latches permanently.
Crev reverse_clock 0 1n IC=0
Brev 0 reverse_clock I={(v(connected)>0.5 && v(raw)<v(load)) ? 1m : -v(reverse_clock)/1m}
Crev_latch reverse_latch 0 1n IC=0
Brev_latch 0 reverse_latch I={(v(reverse_clock)>=REVERSE_US || v(reverse_latch)>1u) ? 1m : 0}
Bconnected connected 0 V={((DISCONNECT>0.5 && v(action)>0.5) || v(reverse_latch)>1u) ? 0 : 1}
Bpath raw load I={v(connected)>0.5 ? (v(raw)-v(load))/RPATH : 0}
Bload load 0 I={v(load)>LOAD_FLOOR ? ILOAD : ILOAD*v(load)/LOAD_FLOOR}

* Crowbar begins from zero current and stays active after the trip action.
Ccb cb_state 0 1 IC=0
Bcb_state 0 cb_state I={(DISCONNECT<0.5 && v(action)>0.5) ? (v(raw)-v(cb_state)*RCROWBAR)/LCROWBAR : 0}
Bcrowbar raw 0 I={v(cb_state)}

.options method=gear maxord=2 reltol=1e-7 abstol=1e-12 vntol=1e-10
.save v(raw) v(load) v(cin) v(bulk) v(il_state) v(cb_state)
+ v(trip_clock) v(action) v(connected) v(reverse_clock) v(reverse_latch)
.tran {MAXSTEP} {TSTOP} 0 {MAXSTEP} UIC
.meas tran peak_load MAX v(load)
.meas tran peak_raw MAX v(raw)
.meas tran peak_inductor MAX v(il_state)
.meas tran peak_crowbar MAX v(cb_state)
.meas tran final_action FIND v(action) AT={TSTOP}
.meas tran final_connected FIND v(connected) AT={TSTOP}
.meas tran final_reverse_latch FIND v(reverse_latch) AT={TSTOP}
.meas tran initial_action FIND v(action) AT=1n
.meas tran initial_connected FIND v(connected) AT=1n
