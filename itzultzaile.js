let diccionario = {};

function cargarTraducciones(idiomaPorDefecto = "eu") {
    fetch("/static/traducciones.json")
        .then(res => res.json())
        .then(data => {
        diccionario = data;
        const idiomaGuardado = localStorage.getItem("idioma") || idiomaPorDefecto;
        traducir(idiomaGuardado);
        });
    }

function traducir(idioma) {
    document.querySelectorAll("[data-i18n]").forEach(el => {
    const clave = el.getAttribute("data-i18n");
    el.textContent = diccionario[idioma][clave] || clave;
    });
}
/*luego habría que añadir a todos los .html despues de los botones de traducir esto:
<script src="{{ url_for('static', filename='itzultzaile.js') }}"></script>
<script>
  traducir(); // idioma por defecto: inglés
</script>

*/
