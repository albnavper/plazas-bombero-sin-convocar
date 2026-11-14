# Plazas de bombero aprobadas y sin convocar en España

Datos abiertos de las ofertas de empleo público (OEP) de **servicios de bomberos urbanos** con plazas de turno libre aprobadas y todavía sin convocar, con su boletín oficial y la fecha en que caducan (art. 70 del EBEP: tres años).

- Página: https://albnavper.github.io/plazas-bombero-sin-convocar/
- Descargas: [`datos/plazas-sin-convocar.csv`](datos/plazas-sin-convocar.csv) · [`datos/plazas-sin-convocar.json`](datos/plazas-sin-convocar.json)
- Fuente y versión siempre al día: **[Lo que viene · Ojo de Fuego](https://ojodefuego.com/lo-que-viene)**. El [Radar de convocatorias](https://ojodefuego.com/radar) de [Ojo de Fuego](https://ojodefuego.com) sigue además cada convocatoria con sus documentos oficiales.

## Campos

| Campo | Qué es |
|---|---|
| `comunidad` | Comunidad autónoma |
| `lugar` | Ciudad o provincia y tipo de ente |
| `organismo` | Organismo que aprobó la oferta |
| `categoria` | Categoría o puesto |
| `oep_anio` | Año de la oferta de empleo público |
| `plazas_sin_convocar` | Plazas de turno libre aún sin convocar |
| `debe_convocarse_antes` | Fecha límite (AAAA-MM-DD) antes de que caduque la oferta |
| `boletin`, `boletin_url` | Publicación oficial de la oferta |

Solo cuentan plazas de turno libre comprobadas en su boletín. No incluye promoción interna, movilidad, mandos, bomberos forestales ni servicios privados. Prevalece siempre la publicación oficial.

## Actualización

Cada lunes, una tarea de GitHub Actions ejecuta `actualizar.py` (solo biblioteca estándar de Python) y guarda los cambios.

## Licencia

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es). Cita: «Ojo de Fuego (ojodefuego.com)».
