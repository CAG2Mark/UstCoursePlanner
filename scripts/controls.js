let filterBoxes = document.getElementsByClassName("filter-container");

for (let i = 0; i < filterBoxes.length; ++i) {
    let box = filterBoxes[i];

    let filterInput = box.getElementsByClassName("filter-input")[0];
    let filterList = box.getElementsByClassName("filter-list")[0];
    filterInput.addEventListener("input", () => {
        let fL = filterList;
        let fI = filterInput;

        let items = fL.children;
        for (let j = 0; j < items.length; ++j) {
            let item = items[j];
            let content = item.getElementsByClassName("filter-content")[0].innerHTML.toLowerCase();
            item.style.display = content.includes(fI.value) ? "block" : "none";

        }
    })
}