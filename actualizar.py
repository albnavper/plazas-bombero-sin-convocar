#!/usr/bin/env python3
"""Descarga https://ojodefuego.com/lo-que-viene y genera datos/plazas-sin-convocar.{csv,json} e index.html.

Solo biblioteca estándar. Si no encuentra ofertas, termina con error y no toca nada.
"""
import csv, datetime as dt, html, json, re, sys, urllib.request
from pathlib import Path

URL = "https://ojodefuego.com/lo-que-viene"
AQUI = Path(__file__).resolve().parent
CAMPOS = ["comunidad", "lugar", "organismo", "categoria", "oep_anio", "plazas_sin_convocar",
          "debe_convocarse_antes", "boletin", "boletin_url"]


def texto(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).replace("\xa0", " ").strip()


def leer(pagina):
    filas = []
    partes = re.split(r'<h3 class="lqv-grupo"[^>]*>', pagina)[1:]
    for parte in partes:
        cab, _, cuerpo = parte.partition("</h3>")
        comunidad = texto(re.sub(r"<span>.*?</span>", "", cab))
        cuerpo = cuerpo.split('<h3 ', 1)[0]
        for li in re.findall(r'<li class="lqv-oep">(.*?)</li>', cuerpo, re.S):
            n = int(texto(re.search(r'<p class="lqv-n"><strong>(\d+)</strong>', li).group(1)))
            lugar = texto(re.search(r'<h4 class="lqv-lugar">(.*?)</h4>', li, re.S).group(1))
            org = texto(re.search(r'<p class="lqv-org">(.*?)</p>', li, re.S).group(1))
            linea = re.search(r'<p>([^<]*?) · OEP&nbsp;(\d{4}) · <a href="([^"]+)"[^>]*title="([^"]*)"', li, re.S)
            caduca = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', li).group(1)
            filas.append({
                "comunidad": comunidad, "lugar": lugar, "organismo": org,
                "categoria": texto(linea.group(1)), "oep_anio": int(linea.group(2)),
                "plazas_sin_convocar": n, "debe_convocarse_antes": caduca,
                "boletin": html.unescape(linea.group(4)), "boletin_url": html.unescape(linea.group(3)),
            })
    return filas


def actualizado(pagina):
    m = re.search(r'Actualizado el\s*<time datetime="(\d{4}-\d{2}-\d{2})"', pagina)
    return m.group(1) if m else ""


def pagina_html(filas, fecha_web, hoy):
    total = sum(f["plazas_sin_convocar"] for f in filas)
    trs = "\n".join(
        f"<tr><td>{html.escape(f['comunidad'])}</td><td>{html.escape(f['organismo'])}</td>"
        f"<td>{html.escape(f['categoria'])}</td><td>{f['oep_anio']}</td><td class=n>{f['plazas_sin_convocar']}</td>"
        f"<td>{f['debe_convocarse_antes']}</td><td><a href=\"{html.escape(f['boletin_url'])}\" rel=\"nofollow noopener\">"
        f"{html.escape(f['boletin'])}</a></td></tr>" for f in filas)
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Plazas de bombero aprobadas y sin convocar en España · datos abiertos</title>
<meta name="description" content="{total} plazas de bombero aprobadas en ofertas de empleo público y aún sin convocar, con su boletín oficial y la fecha en que caducan. Datos abiertos CC BY 4.0 de Ojo de Fuego.">
<link rel="canonical" href="https://albnavper.github.io/plazas-bombero-sin-convocar/">
<style>body{{font:15px/1.5 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#1d1f22}}
h1{{font-size:1.6rem}}table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{border-bottom:1px solid #ddd;padding:6px 8px;text-align:left;vertical-align:top}}
th{{background:#f4f4f4}}.n{{text-align:right;font-weight:600}}.nota{{color:#555;font-size:13px}}a{{color:#b8410f}}</style></head>
<body>
<h1>Plazas de bombero aprobadas y sin convocar en España</h1>
<p><strong>{total} plazas</strong> en {len(filas)} ofertas de empleo público (OEP) de servicios de bomberos urbanos que aún no se han convocado.
Una OEP que no se convoca en tres años caduca (art. 70 del Estatuto Básico del Empleado Público).</p>
<p>Fuente y versión siempre al día: <a href="https://ojodefuego.com/lo-que-viene">Lo que viene · Ojo de Fuego</a>
(datos de la web del {html.escape(fecha_web)}). Copia generada el {hoy}.</p>
<p>Descargas: <a href="datos/plazas-sin-convocar.csv">CSV</a> · <a href="datos/plazas-sin-convocar.json">JSON</a>.
Licencia <a href="https://creativecommons.org/licenses/by/4.0/deed.es">CC BY 4.0</a>: cita «Ojo de Fuego (ojodefuego.com)».</p>
<table><thead><tr><th>Comunidad</th><th>Organismo</th><th>Categoría</th><th>OEP</th><th>Plazas</th><th>Convocar antes del</th><th>Boletín oficial</th></tr></thead>
<tbody>
{trs}
</tbody></table>
<p class="nota">Solo plazas de turno libre comprobadas en su boletín oficial. No incluye promoción interna, movilidad, mandos, bomberos forestales ni servicios privados.
Prevalece siempre la publicación oficial. Más convocatorias y documentos en el <a href="https://ojodefuego.com/radar">Radar de convocatorias de bombero</a>.</p>
</body></html>
"""


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "plazas-bombero-sin-convocar (+https://github.com/albnavper/plazas-bombero-sin-convocar)"})
    pagina = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    filas = leer(pagina)
    if not filas:
        sys.exit("No se han encontrado ofertas: no se toca nada.")
    hoy = dt.date.today().isoformat()
    (AQUI / "datos").mkdir(exist_ok=True)
    with open(AQUI / "datos/plazas-sin-convocar.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS); w.writeheader(); w.writerows(filas)
    meta = {"fuente": URL, "actualizado_en_la_web": actualizado(pagina), "generado": hoy,
            "licencia": "CC BY 4.0 · Ojo de Fuego (ojodefuego.com)",
            "plazas": sum(f["plazas_sin_convocar"] for f in filas), "ofertas": len(filas), "filas": filas}
    (AQUI / "datos/plazas-sin-convocar.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    (AQUI / "index.html").write_text(pagina_html(filas, meta["actualizado_en_la_web"], hoy), encoding="utf-8")
    print(f"{meta['ofertas']} ofertas, {meta['plazas']} plazas")


if __name__ == "__main__":
    main()
