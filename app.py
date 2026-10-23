import math
from collections import OrderedDict


def init_tijeral_state():
    cfg = st.session_state.config
    defaults = {
        "tij_A": 1.20, "tij_B": 0.60, "tij_C": 0.60,
        "tij_n_vert": 8,
        "tij_vert_tipo": "Tubo Cuadrado", "tij_vert_perfil": "40 x 40 | 2 mm",
        "tij_dA_tipo": "Tubo Cuadrado", "tij_dA_perfil": "40 x 40 | 2 mm",
        "tij_dB_tipo": "Tubo Cuadrado", "tij_dB_perfil": "40 x 40 | 2 mm",
    }
    for k, v in defaults.items():
        cfg.setdefault(k, v)
    # Diagonales por panel: patrón espejo por defecto (A en mitad izquierda, B en la derecha)
    n_pan = int(cfg["tij_n_vert"]) + 1
    for p in range(n_pan):
        st.session_state.setdefault(f"tij_diag_{p}", "A" if p < n_pan / 2 else "B")


def calcular_tijeral(L, A, B, C, n_vert, diag_por_panel):
    """Devuelve geometría completa; longitudes medidas entre ejes de bridas (línea de centros)."""
    n_pan = n_vert + 1
    s = L / n_pan
    xs = [i * s for i in range(n_pan + 1)]

    def y_bot(x):
        return C * (1.0 - x / L)

    def h(x):
        return A + (B - A) * x / L

    def y_top(x):
        return y_bot(x) + h(x)

    verticales = [{"id": f"V{i}", "x": xs[i], "altura": h(xs[i])} for i in range(1, n_vert + 1)]
    diagonales = []
    for p in range(n_pan):
        t = diag_por_panel[p]
        if t == "A":
            p1, p2 = (xs[p], y_top(xs[p])), (xs[p + 1], y_bot(xs[p + 1]))
        elif t == "B":
            p1, p2 = (xs[p], y_bot(xs[p])), (xs[p + 1], y_top(xs[p + 1]))
        else:
            continue
        diagonales.append({
            "id": f"D{p + 1}", "tipo": t, "panel": p + 1,
            "largo": math.hypot(p2[0] - p1[0], p2[1] - p1[1]),
        })
    return {
        "L": L, "s": s, "xs": xs, "n_pan": n_pan,
        "y_top": y_top, "y_bot": y_bot,
        "L_sup": math.hypot(L, (C + A) - B),
        "L_inf": math.hypot(L, C),
        "pend_sup_pct": ((C + A - B) / L) * 100.0 if L > 0 else 0.0,
        "ang_sup_deg": math.degrees(math.atan2((C + A - B), L)),
        "verticales": verticales, "diagonales": diagonales,
        "ymax": max(C + A, B, 0.1),
    }


def _diag_por_panel_actual():
    n_pan = int(st.session_state.config["tij_n_vert"]) + 1
    return [st.session_state.get(f"tij_diag_{p}", "N") for p in range(n_pan)]


def obtener_geometria_tijeral_actual():
    cfg = st.session_state.config
    return calcular_tijeral(
        float(cfg["ancho_portico_m"]), float(cfg["tij_A"]), float(cfg["tij_B"]),
        float(cfg["tij_C"]), int(cfg["tij_n_vert"]), _diag_por_panel_actual()
    )


def obtener_partidas_tijeral_parametrico():
    """Convierte el tijeral paramétrico en partidas para el motor de optimización (Paso 4)."""
    cfg = st.session_state.config
    nt = int(cfg["num_tijerales"])
    geo = obtener_geometria_tijeral_actual()
    items = []

    for clave, largo in (("brida_sup", geo["L_sup"]), ("brida_inf", geo["L_inf"])):
        it = st.session_state.partidas[clave]
        if it["activo"]:
            items.append({
                "nombre": it["nombre"], "tipo": it["tipo"], "perfil": it["perfil"],
                "cantidad_total": int(it["cantidad"]) * nt, "longitud_m": round(largo, 2),
                "largo_barra_m": obtener_largo_comercial_por_tipo(it["tipo"]),
            })

    # Montantes verticales: se agrupan por altura (redondeada a 2 decimales)
    grupos = OrderedDict()
    for v in geo["verticales"]:
        grupos.setdefault(round(v["altura"], 2), []).append(v["id"])
    for altura, ids in grupos.items():
        items.append({
            "nombre": f"Tijeral - Montantes verticales [{', '.join(ids)}]",
            "tipo": cfg["tij_vert_tipo"], "perfil": cfg["tij_vert_perfil"],
            "cantidad_total": len(ids) * nt, "longitud_m": altura,
            "largo_barra_m": obtener_largo_comercial_por_tipo(cfg["tij_vert_tipo"]),
        })

    # Diagonales A y B: se agrupan por (tipo, largo)
    grupos_d = OrderedDict()
    for d in geo["diagonales"]:
        grupos_d.setdefault((d["tipo"], round(d["largo"], 2)), []).append(d["id"])
    for (t, largo), ids in grupos_d.items():
        pref = "tij_dA" if t == "A" else "tij_dB"
        items.append({
            "nombre": f"Tijeral - Montantes diagonales {t} [{', '.join(ids)}]",
            "tipo": cfg[f"{pref}_tipo"], "perfil": cfg[f"{pref}_perfil"],
            "cantidad_total": len(ids) * nt, "longitud_m": largo,
            "largo_barra_m": obtener_largo_comercial_por_tipo(cfg[f"{pref}_tipo"]),
        })
    return items


def generar_svg_elevacion_tijeral(geo, A, B, C, diag):
    L, xs = geo["L"], geo["xs"]
    sc = min(820.0 / L, 230.0 / geo["ymax"])
    ox, oy = 80, 45
    W = int(ox + L * sc + 80)
    H = int(oy + geo["ymax"] * sc + 55)
    X = lambda x: ox + x * sc
    Y = lambda y: oy + (geo["ymax"] - y) * sc
    yt, yb = geo["y_top"], geo["y_bot"]

    s = [
        '<div style="overflow-x:auto;background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:10px;">',
        f'<svg viewBox="0 0 {W} {H}" width="100%" style="min-width:{min(W, 760)}px;font-family:monospace,sans-serif;">',
        f'<rect width="{W}" height="{H}" fill="#fff"/>',
        # Nivel 0 (línea roja)
        f'<line x1="{X(0)-30}" y1="{Y(0)}" x2="{X(L)+40}" y2="{Y(0)}" stroke="#d1242f" stroke-width="1" stroke-dasharray="10,5"/>',
        # Ejes 1 y 2
        f'<line x1="{X(0)}" y1="{oy-30}" x2="{X(0)}" y2="{H-25}" stroke="#6e7781" stroke-dasharray="12,4,2,4"/>',
        f'<line x1="{X(L)}" y1="{oy-30}" x2="{X(L)}" y2="{H-25}" stroke="#6e7781" stroke-dasharray="12,4,2,4"/>',
        f'<circle cx="{X(0)}" cy="{oy-30}" r="13" fill="#fff" stroke="#1f2328"/><text x="{X(0)}" y="{oy-25}" text-anchor="middle" font-size="13">1</text>',
        f'<circle cx="{X(L)}" cy="{oy-30}" r="13" fill="#fff" stroke="#1f2328"/><text x="{X(L)}" y="{oy-25}" text-anchor="middle" font-size="13">2</text>',
        # Bridas
        f'<line x1="{X(0)}" y1="{Y(yt(0))}" x2="{X(L)}" y2="{Y(yt(L))}" stroke="#1f2328" stroke-width="3"/>',
        f'<line x1="{X(0)}" y1="{Y(yb(0))}" x2="{X(L)}" y2="{Y(yb(L))}" stroke="#1f2328" stroke-width="3"/>',
        # Peraltes A y B
        f'<line x1="{X(0)}" y1="{Y(C)}" x2="{X(0)}" y2="{Y(C+A)}" stroke="#0969da" stroke-width="5"/>',
        f'<line x1="{X(L)}" y1="{Y(0)}" x2="{X(L)}" y2="{Y(B)}" stroke="#0969da" stroke-width="5"/>',
    ]
    # Montantes verticales
    for i in range(1, len(xs) - 1):
        x = xs[i]
        s.append(f'<line x1="{X(x)}" y1="{Y(yt(x))}" x2="{X(x)}" y2="{Y(yb(x))}" stroke="#1a7f37" stroke-width="2.4"/>')
        s.append(
            f'<text x="{X(x)-4}" y="{(Y(yt(x))+Y(yb(x)))/2}" font-size="9" fill="#1a7f37" '
            f'transform="rotate(-90 {X(x)-4} {(Y(yt(x))+Y(yb(x)))/2})" text-anchor="middle">V{i} {yt(x)-yb(x):.2f}</text>'
        )
    # Diagonales
    for p in range(len(xs) - 1):
        t = diag[p]
        if t == "N":
            continue
        x1, x2 = xs[p], xs[p + 1]
        if t == "A":
            a, b = (X(x1), Y(yt(x1))), (X(x2), Y(yb(x2)))
            col = "#bc4c00"
        else:
            a, b = (X(x1), Y(yb(x1))), (X(x2), Y(yt(x2)))
            col = "#8250df"
        s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{col}" stroke-width="2.2"/>')
        largo = math.hypot((x2 - x1), (yt(x2) - yb(x1)) if t == "B" else (yb(x2) - yt(x1)))
        s.append(f'<text x="{(a[0]+b[0])/2}" y="{(a[1]+b[1])/2 - 4}" font-size="9" fill="{col}" text-anchor="middle">D{p+1} {largo:.2f}</text>')
    # Cotas A, B, C
    s.append(f'<text x="{X(0)-12}" y="{(Y(C)+Y(C+A))/2}" font-size="12" fill="#bc4c00" text-anchor="end">A={A:.2f}</text>')
    s.append(f'<text x="{X(L)+12}" y="{(Y(0)+Y(B))/2}" font-size="12" fill="#bc4c00">B={B:.2f}</text>')
    if C > 0:
        s.append(f'<text x="{X(0)-12}" y="{(Y(0)+Y(C))/2}" font-size="12" fill="#bc4c00" text-anchor="end">C={C:.2f}</text>')
    s.append(
        f'<text x="{W/2}" y="{H-8}" text-anchor="middle" font-size="12" font-weight="bold" fill="#1f2328">'
        f'ELEVACIÓN DEL TIJERAL — LUZ = {L:.2f} m | verde: verticales | naranja: diagonal A (\\) | violeta: diagonal B (/)</text>'
    )
    s.append('</svg></div>')
    return "\n".join(s)


def _aplicar_patron_diagonales(patron, n_pan):
    for p in range(n_pan):
        if patron == "A":
            v = "A"
        elif patron == "B":
            v = "B"
        elif patron == "espejo":
            v = "A" if p < n_pan / 2 else "B"
        elif patron == "alterna":
            v = "A" if p % 2 == 0 else "B"
        else:
            v = "N"
        st.session_state[f"tij_diag_{p}"] = v


def _selector_perfil(etiqueta, pref, columnas_key):
    cfg = st.session_state.config
    opciones_tipo = ["Tubo Cuadrado", "Tubo Rectangular", "Viga H (WF)", "Tubo Schedule (SCH)"]
    c1, c2 = st.columns([1.4, 3])
    with c1:
        cfg[f"{pref}_tipo"] = st.selectbox(f"{etiqueta} — Familia", opciones_tipo,
                                           index=opciones_tipo.index(cfg[f"{pref}_tipo"]), key=f"{columnas_key}_t")
    with c2:
        lista = LISTAS_POR_TIPO[cfg[f"{pref}_tipo"]]
        idx = lista.index(cfg[f"{pref}_perfil"]) if cfg[f"{pref}_perfil"] in lista else 0
        cfg[f"{pref}_perfil"] = st.selectbox(f"{etiqueta} — Perfil", lista, index=idx, key=f"{columnas_key}_p")


def renderizar_paso3_tijeral_parametrico():
    cfg = st.session_state.config
    init_tijeral_state()
    opciones_tipo = ["Tubo Cuadrado", "Tubo Rectangular", "Viga H (WF)", "Tubo Schedule (SCH)"]

    # --- 1. Geometría ---
    with st.container(border=True):
        st.markdown("#### 📐 Geometría del Tijeral (Peralte A, Peralte B y Cota C)")
        g1, g2, g3, g4, g5 = st.columns(5)
        cfg["ancho_portico_m"] = g1.number_input("Luz L (m)", min_value=0.50, value=float(cfg["ancho_portico_m"]), step=0.50, format="%.2f")
        cfg["tij_A"] = g2.number_input("A: Peralte A (m)", min_value=0.05, value=float(cfg["tij_A"]), step=0.05, format="%.2f")
        cfg["tij_B"] = g3.number_input("B: Peralte B (m)", min_value=0.05, value=float(cfg["tij_B"]), step=0.05, format="%.2f")
        cfg["tij_C"] = g4.number_input("C: Inicio del Peralte A (m)", min_value=0.0, value=float(cfg["tij_C"]), step=0.05, format="%.2f",
                                       help="Altura sobre el nivel de la base del Peralte B donde inicia el Peralte A. C = 0 y A = B → bridas horizontales.")
        cfg["num_tijerales"] = g5.number_input("N.° de tijerales iguales", min_value=1, value=int(cfg["num_tijerales"]), step=1)

    # --- 2. Montantes verticales y diagonales ---
    with st.container(border=True):
        st.markdown("#### ⏸️ Montantes Verticales (equidistantes) y Diagonales por tramo")
        cfg["tij_n_vert"] = st.number_input(
            "Cantidad de montantes verticales intermedios", min_value=0, max_value=40, value=int(cfg["tij_n_vert"]), step=1,
            help="Se reparten a igual distancia entre los Peraltes A y B. Con N montantes resultan N+1 tramos."
        )
        n_pan = int(cfg["tij_n_vert"]) + 1
        for p in range(n_pan):  # asegurar claves si cambió N
            st.session_state.setdefault(f"tij_diag_{p}", "A" if p < n_pan / 2 else "B")

        st.caption("Patrón rápido para las diagonales (luego puedes cambiar tramo por tramo):")
        pb = st.columns(5)
        pb[0].button("Todas A (\\)", on_click=_aplicar_patron_diagonales, args=("A", n_pan), use_container_width=True)
        pb[1].button("Todas B (/)", on_click=_aplicar_patron_diagonales, args=("B", n_pan), use_container_width=True)
        pb[2].button("Espejo (A | B)", on_click=_aplicar_patron_diagonales, args=("espejo", n_pan), use_container_width=True)
        pb[3].button("Alternadas", on_click=_aplicar_patron_diagonales, args=("alterna", n_pan), use_container_width=True)
        pb[4].button("Sin diagonales", on_click=_aplicar_patron_diagonales, args=("N", n_pan), use_container_width=True)

        etiquetas = {"A": "Diagonal A  \\", "B": "Diagonal B  /", "N": "Sin diagonal"}
        por_fila = 6
        for ini in range(0, n_pan, por_fila):
            cols = st.columns(por_fila)
            for j, p in enumerate(range(ini, min(ini + por_fila, n_pan))):
                with cols[j]:
                    st.selectbox(f"Tramo {p + 1}", ["A", "B", "N"], key=f"tij_diag_{p}",
                                 format_func=lambda k: etiquetas[k])

    diag = _diag_por_panel_actual()
    geo = calcular_tijeral(float(cfg["ancho_portico_m"]), float(cfg["tij_A"]), float(cfg["tij_B"]),
                           float(cfg["tij_C"]), int(cfg["tij_n_vert"]), diag)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Brida superior", f"{geo['L_sup']:.2f} m")
    m2.metric("Brida inferior", f"{geo['L_inf']:.2f} m")
    m3.metric("Pendiente brida sup.", f"{geo['pend_sup_pct']:.2f} %")
    m4.metric("Ángulo", f"{geo['ang_sup_deg']:.2f}°")
    m5.metric("Separación entre montantes", f"{geo['s']:.3f} m")

    st.markdown(generar_svg_elevacion_tijeral(geo, float(cfg["tij_A"]), float(cfg["tij_B"]), float(cfg["tij_C"]), diag),
                unsafe_allow_html=True)

    # --- 3. Perfiles ---
    with st.container(border=True):
        st.markdown("#### 🔩 Perfiles del Tijeral")
        for clave, titulo in (("brida_sup", "🔼 Brida Superior"), ("brida_inf", "🔽 Brida Inferior")):
            datos = st.session_state.partidas[clave]
            f1, f2, f3, f4 = st.columns([0.8, 1.4, 2.6, 1.0])
            datos["activo"] = f1.checkbox("Incluir", value=datos["activo"], key=f"chk_{clave}_p")
            datos["tipo"] = f2.selectbox(titulo, opciones_tipo, index=opciones_tipo.index(datos["tipo"]), key=f"tipo_{clave}_p")
            lista = LISTAS_POR_TIPO[datos["tipo"]]
            datos["perfil"] = f3.selectbox("Perfil", lista, index=lista.index(datos["perfil"]) if datos["perfil"] in lista else 0, key=f"perf_{clave}_p")
            datos["cantidad"] = f4.number_input("Cant. x tijeral", min_value=1, value=int(datos["cantidad"]), key=f"cant_{clave}_p")
            largo = geo["L_sup"] if clave == "brida_sup" else geo["L_inf"]
            datos["longitud_m"] = round(largo, 2)
            st.caption(f"Longitud calculada automáticamente: **{largo:.2f} m**")
        _selector_perfil("Montantes verticales", "tij_vert", "tij_vert")
        _selector_perfil("Diagonales A (\\)", "tij_dA", "tij_dA")
        _selector_perfil("Diagonales B (/)", "tij_dB", "tij_dB")

    # --- 4. Tablas de longitudes ---
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("###### Montantes verticales")
        if geo["verticales"]:
            st.dataframe(pd.DataFrame([{"ID": v["id"], "Posición x (m)": round(v["x"], 3), "Altura (m)": round(v["altura"], 3)}
                                       for v in geo["verticales"]]), hide_index=True, use_container_width=True)
        else:
            st.caption("Sin montantes verticales intermedios.")
    with t2:
        st.markdown("###### Montantes diagonales")
        if geo["diagonales"]:
            st.dataframe(pd.DataFrame([{"ID": d["id"], "Tramo": d["panel"], "Tipo": d["tipo"], "Longitud (m)": round(d["largo"], 3)}
                                       for d in geo["diagonales"]]), hide_index=True, use_container_width=True)
