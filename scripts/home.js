var createButton = document.getElementById("create-plan-button");
var homeBox = document.getElementById("home-box");
var createBox = document.getElementById("create-box");
var createWrap = document.getElementById("create-wrap");

createButton.addEventListener("click", () => {
    setTimeout(() => {
        document.getElementById("home-box").classList.add("hidden");
    }, 200);
    
    setTimeout(() => {
        showCreateSequence();
    }, 500);
})

var allSections = document.getElementById("create-wrap").children;
var i_section = 0;
var i_min = 0;
var i_max = allSections.length;

function showCreateSequence() {
    homeBox.style.display = "none";
    createBox.style.display = "block";

    let i = 0;
    let intv = setInterval(() => {
        allSections[i].classList.add("section-in");
        ++i;
        if (i == i_max) clearInterval(intv);
    }, 150);
}

backBtns = document.getElementsByClassName("back-button");
forwardBtns = document.getElementsByClassName("forward-button");

for (let i = 0; i < backBtns.length; ++i) {
    let btn = backBtns[i];
    btn.addEventListener("click", () => {
        if (i_section - 1 >= i_min) setCreateSection(--i_section);
    })
};

for (let i = 0; i < forwardBtns.length; ++i) {
    let btn = forwardBtns[i];
    btn.addEventListener("click", () => {
        if (i_section + 1 < i_max) setCreateSection(++i_section);
    })
};

function disable(element) {
    element.removeAttribute("disabled");
    element.removeAttribute("aria-disabled");
}

function enable(element) {
    element.setAttribute("disabled", "");
    element.setAttribute("aria-disabled", "");
}

function setCreateSection(index) {
    createWrap.style.left = "-" + 100*i_section + "%";
    for (let i = 0; i < i_max; ++i) {
        let section = allSections[i];
        let backBtn = section.getElementsByClassName("back-button")[0];
        let forwardBtn = section.getElementsByClassName("forward-button")[0];

        if (i == index) {
            section.classList.remove("section-disabled");
            if (backBtn) disable(backBtn);
            if (forwardBtn) disable(forwardBtn);
        } else {
            section.classList.add("section-disabled")
            if (backBtn) enable(backBtn);
            if (forwardBtn) enable(forwardBtn);
        }

    }
}