const actionSelect = document.querySelector("#action-select");

if (actionSelect) {
  actionSelect.addEventListener("change", () => {
    const observation = document.querySelector('input[name="observacion_accion"]');
    if (!observation) return;

    if (actionSelect.value === "Otra acción.") {
      observation.placeholder = "Describe la acción correctiva";
      observation.focus();
    } else {
      observation.placeholder = "Ej. Se llamó a sucursal antes de salir";
    }
  });
}

document.querySelectorAll("[data-confirm-delete]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    const confirmed = window.confirm("¿Seguro que deseas eliminar esta entrega?");
    if (!confirmed) {
      event.preventDefault();
    }
  });
});

const productTypeSelect = document.querySelector("#product-type-select");
const rangePreview = document.querySelector("#temperature-range-preview");

if (productTypeSelect && rangePreview) {
  productTypeSelect.addEventListener("change", () => {
    const selected = productTypeSelect.options[productTypeSelect.selectedIndex];
    rangePreview.value = selected.dataset.range || "No definido";
  });
}
