def define_3ph_pvsystem(dss, bus, kv, kva, pmpp):

    dss.text("New XYCurve.MyPvsT npts=4  xarray=[0  25  75  100]  yarray=[1 1 1 1]")
    dss.text("New XYCurve.MyEff npts=4  xarray=[.1  .2  .4  1.0]  yarray=[1 1 1 1]")

    dss.text("New PVSystem.PV_{} phases=3 conn=wye  bus1={} kV={} kVA={} Pmpp={} pf=1"
             " effcurve=Myeff  P-TCurve=MyPvsT vmaxpu=2 vminpu=0.5".format(bus, bus, kv * 1.73, kva, pmpp))

def increment_pv_size(dss, p_step, kva_to_kw, pf, i):
    dss.pvsystems_first()
    for _ in range(dss.pvsystems_count()):
        dss.text(f"edit pvsystem.{dss.pvsystems_read_name()} pmpp={p_step * i} kva={kva_to_kw * p_step * i} pf={pf} pfpriority=yes")
        dss.pvsystems_next()
    dss.solution_solve()

