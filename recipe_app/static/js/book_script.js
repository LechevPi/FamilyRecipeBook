// Functions
document.addEventListener("DOMContentLoaded", function() {

    // Function to create search button
    function createSearchButtonFromInput() {
        var searchText = document.getElementById("searchInput").value.trim();
        if (searchText !== "") {
            createSearchButton(searchText);
            document.getElementById("searchInput").value = ""; // Clearing the search input field after creating the button
        }
    }

    function createSearchButton(txt) {
        var button_name = '\u2716 contains: ' + txt;
        var searchField = document.createElement("button");
        searchField.textContent = button_name;
        searchField.setAttribute("data-tagType", "s");
        searchField.className  = "tag"
        selectedTagContainer.appendChild(searchField);
        activeSearch = txt;
        updateDisplay()
    }

    function moveButton(tag) {
        var tagType = tag.getAttribute("data-tagType"); // Get the value of data-tagType attribute

        if (tagType === "s") {
            selectedTagContainer.removeChild(tag);
            activeSearch = "";
            updateDisplay();
        } else if (tagType === "filt") {
            if (tag.parentElement === unselectedTagContainer) {
                addCrossButtonText(tag);
                selectedTagContainer.appendChild(tag);
            } else if (tag.parentElement === selectedTagContainer) {
                removeCrossButtonText(tag);
                unselectedTagContainer.appendChild(tag);
            }
            updateActiveFilters(tag.dataset.filter);
        }
    }


    function removeCrossButtonText(tag) {
        var buttonText = tag.textContent;
        tag.textContent = buttonText.substring(2);
    }

    function addCrossButtonText(tag) {
        var buttonText = tag.textContent;
        tag.textContent = '\u2716' + ' ' + buttonText;
    }

    function updateActiveFilters(filter) {
        if (activeFilters.includes(filter)) {
            activeFilters.splice(activeFilters.indexOf(filter), 1);
        } else {
            activeFilters.push(filter);
        }
        updateDisplay();
    }

    function updateDisplay() {
        var recipeBoxes = document.getElementsByClassName("recipeBox");
        var potentialButtons = [];
        for (var i = 0; i < recipeBoxes.length; i++) {
            var recipeName = recipeBoxes[i].querySelector("h3").textContent.trim();
            var includesSearchTerm = recipeName.toLowerCase().includes(activeSearch.toLowerCase());

            if ((activeFilters.length === 0 || (activeFilters.every(cls => Array.from(recipeBoxes[i].classList).includes(cls)))) && includesSearchTerm) {
                recipeBoxes[i].style.display = "inline-block";
                Array.from(recipeBoxes[i].classList).forEach(className => {
                    if (!potentialButtons.includes(className)) {
                        potentialButtons.push(className);
                    }
                });
            } else {
                recipeBoxes[i].style.display = "none";
            }
        }
        updateButtons(potentialButtons);
    }


    function updateButtons(potentialButtons) {
        var tags = document.getElementsByClassName("tag");
        for (var i = 0; i < tags.length; i++) {
            if (tags[i].parentElement === unselectedTagContainer) {
                if (potentialButtons.includes(tags[i].dataset.filter)) {
                    tags[i].style.display = "inline-block";
                } else {
                    tags[i].style.display = "none";
                }
            }
        }
        reorderButtons(unselectedTagContainer);
    }

    function reorderButtons(container) {
        const buttons = Array.from(container.querySelectorAll(".tag"));
        buttons.sort(function(a, b) {
            return a.dataset.initialOrder - b.dataset.initialOrder;
        });

        buttons.forEach(function(tag) {
            container.appendChild(tag);
        });
    }

    // Event Listener

    document.addEventListener("click", function(event) {
        if (event.target.classList.contains("tag")) {
            moveButton(event.target);
        }
    });

    // Event listener for "Enter" key press on search input field
    document.getElementById("searchInput").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            createSearchButtonFromInput();
        }
    });

    // Page Initialization
    var activeFilters = [];
    var activeSearch = "";
    var unselectedTagContainer = document.getElementById("unselectedTagContainer");
    var selectedTagContainer = document.getElementById("selectedTagContainer");

    // Retrieve the value stored in sessionStorage
    var category = sessionStorage.getItem('selectedCategory');

    // Call updateActiveFilters to update the display as if the user clicked on a button
    if (category) {
        // Find the button associated with the category
        var tag = document.querySelector("[data-filter='" + category + "']");

        // Move the button if found
        if (tag) {
            moveButton(tag)
        }
    } else {
        updateDisplay();
    }

    // Reset the value stored in sessionStorage to "none"
    sessionStorage.setItem('selectedCategory', []);

    // Retrieve the value stored in sessionStorage
    var searchText = sessionStorage.getItem('searchText');

    // Check if there is a stored search text
    if (searchText) {
        // Set the value of the search input field
        document.getElementById("searchInput").value = searchText;
        // Call the function to create a search button from the input
        createSearchButtonFromInput();
    } else {
        // If there is no stored search text, update the display
        updateDisplay();
    }

    // Reset the value stored in sessionStorage to "none"
    sessionStorage.setItem('searchText', '');
});

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "inline-block") {
      content.style.display = "none";
    } else {
      content.style.display = "inline-block";
    }
  });
}

