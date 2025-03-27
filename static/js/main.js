
// code function to search employee
function searchTable() {
    let input = document.getElementById("searchInput");
    let filter = input.value.toLowerCase();
    let table = document.getElementById("dataTable");
    let rows = Array.from(table.getElementsByTagName("tr")).slice(1);

    rows.forEach(row => {
        let cells = Array.from(row.getElementsByTagName("td"));
        let rowMatch = cells.some(cell => cell.textContent.toLowerCase().includes(filter));
        row.style.display = rowMatch ? "" : "none";
    });
}

// function to side bar toggeling

function toggleMenu() {
    document.getElementById("sidebar").classList.toggle("active");
}