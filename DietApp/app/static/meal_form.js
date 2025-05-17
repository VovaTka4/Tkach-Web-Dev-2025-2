document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.querySelector('#products-table tbody');
    const addBtn = document.getElementById('add-product');

    addBtn?.addEventListener('click', function () {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><input type="text" name="product_name" class="form-control" /></td>
            <td><input type="number" name="weight" class="form-control" /></td>
            <td><input type="number" name="calories" class="form-control" /></td>
            <td><input type="number" name="protein" class="form-control" /></td>
            <td><input type="number" name="fat" class="form-control" /></td>
            <td><input type="number" name="carbs" class="form-control" /></td>
            <td><button type="button" class="btn btn-danger btn-sm remove-product">Удалить</button></td>
        `;
        tableBody.appendChild(row);
    });

    tableBody?.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-product')) {
            const row = e.target.closest('tr');
            row.remove();
        }
    });
});