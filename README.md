# Hackathon SPEI® Banxico 2025 — archivo personal

Copia del micrositio del Hackathon SPEI® Banxico, conservada como recuerdo del equipo ganador de la Benemérita Universidad Autónoma de Puebla: Paul Sebastian Rosales Lamarque, Francisco Ivan Torres Flores y Carlos Manuel Ibarra Cervantes, con asesoría de Luis Enrique Morales Aguilar.

![Equipo ganador](img/EquipoGanador.JPG)

Fuente: https://www.banxico.org.mx/hackathonspei/  
Captura: 21 de septiembre de 2026, hora de Ciudad de México (22 de septiembre UTC).

## Contenido preservado

- HTML original, dos hojas de estilo, Bootstrap y jQuery.
- Fotografías del equipo ganador y finalistas, logotipos, fondos y gráficos para escritorio y móvil.
- PDF de las bases, favicon y mapas de depuración disponibles o recuperados.
- Fuentes Poppins regular y negrita recuperadas de una distribución pública.
- Inventario de URLs, tamaños y huellas SHA-256 en `archive/manifest.json`; procedencia de los archivos complementarios en `archive/recovered.json`.

El HTML, CSS, JavaScript e imágenes descargados de Banxico se conservan byte por byte, incluida su codificación original. Las rutas ya eran relativas y funcionan tanto en la raíz como en una subcarpeta de GitHub Pages. No hay compilación, CDN ni servicios externos necesarios para mostrar la copia.

## Ver en tu computadora

Desde la carpeta del repositorio, con Python 3.10 o posterior:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Abre http://127.0.0.1:8000/ . Para verificar la integridad y las referencias locales:

```sh
python3 scripts/verify.py
```

## Repositorio y página publicada

- Repositorio: https://github.com/ivanblueberry/HackBanxico
- Sitio: https://ivanblueberry.github.io/HackBanxico/

GitHub Pages está configurado para publicar desde la rama `main`, carpeta `/ (root)`, sin compilación. `.nojekyll` conserva los archivos estáticos tal como están. Cada push a `main` actualiza la página.

Antes de subir cambios:

```sh
python3 scripts/verify.py
git add .
git commit -m "Actualiza el archivo"
git push origin main
```

En **Settings → Pages**, la opción es **Deploy from a branch**, rama `main`, carpeta `/ (root)`.

Se conserva un workflow opcional como plantilla en `archive/pages-workflow.example.yml`; no está activo. Para usarlo en otro momento, muévelo a `.github/workflows/pages.yml` y selecciona **GitHub Actions** en Pages. La publicación actual no lo necesita.

## Alcance y recuperación

Esta copia conserva los recursos públicos referenciados por el micrositio y sus estilos. No es un respaldo del servidor ni incluye archivos privados, recursos no enlazados o el sistema de registro. Las redes sociales, el correo y las páginas bibliográficas externas conservan sus enlaces originales; su contenido no está archivado aquí.

Tres URLs del servidor original devolvieron HTTP 404 durante la captura:

- `fonts/Poppins-Regular.woff`
- `fonts/Poppins-Bold.woff`
- `js/bootstrap.bundle.min.js.map`

Las fuentes se sustituyeron por Poppins Latin 400 y 700 de `@fontsource/poppins@5.2.7`. Esto restaura la tipografía declarada por el CSS, aunque puede diferir de la apariencia del sitio original cuando sus fuentes fallan. El mapa JavaScript procede de Bootstrap 5.3.3, la versión identificada en el archivo original. Estos complementos no se presentan como originales de Banxico. Sus URLs y hashes están en `archive/recovered.json` y las licencias correspondientes en `archive/licenses/`.

`scripts/archive_site.py` documenta y permite repetir la descarga con Python y curl. **Volver a ejecutarlo sobrescribe la captura y el inventario**; úsalo en otra copia o rama si quieres conservar esta versión histórica. Sale con error si el servidor sigue sin entregar recursos necesarios, aun cuando existan sustitutos locales. No se ejecuta durante el despliegue.

## Créditos

Archivo personal y no oficial, sin afiliación institucional. Los textos, fotografías, marcas y diseño originales pertenecen a sus respectivos titulares; este repositorio no les asigna una licencia nueva. Se conservan los avisos incluidos en las dependencias de terceros y sus licencias complementarias.
