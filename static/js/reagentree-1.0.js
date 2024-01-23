// Version: 1.0
// This file contains functions used by the reagentree app.

AlertsAutoDismissal("auto-dismiss", 2000); // auto dismiss alerts after 2 seconds

/**
 * DOMContentLoaded event listener
 */
document.addEventListener("DOMContentLoaded", function () {
  // Initialize the Bootstrap tooltip.
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );

  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  /**
   *
   * HTMX event listeners
   *
   * **/
  /** HTMX: afterSwap **/
  document.body.addEventListener("htmx:afterSwap", (event) => {
    applyHideAfterAnimation(); // remove fade out hide elements
  });
});

/** HTMX: bfforeOnLoad **/
document.body.addEventListener("htmx:beforeOnLoad", function (event) {
  if (event.target.id === "search-results-panel") {
    var resultsPanel = document.getElementById("search-results-panel");
    // Show the results panel before the HTMX request loads
    resultsPanel.style.display = "block";
  }
});

/** HTMX: ffterOnLoad **/
document.body.addEventListener("htmx:afterOnLoad", function (event) {
  var resultsPanel = document.getElementById("search-results-panel");
  if (event.target.id === "search-results-panel") {
    if (resultsPanel.innerHTML.trim() === "") {
      resultsPanel.style.display = "none";
    }
  }
});

/**
 * This function configures a listener for search results.
 *
 * @param {Object} config - Configuration object.
 * @param {string} config.searchBoxId - The id of the search box, e.g. "search-box".
 * @param {string} config.textInputId - The id of the hidden input box
 * @param {string} config.resultsDivId - The id of the div containing the search results, e.g. "search-results".
 * @param {string} config.resultClass - The class of the search result items, e.g. "search-result-item".
 * @param {string} config.valueAttribute - The attribute of the search result items containing the value, e.g. "data-value".
 */
function TypeSearchResultListenerConfig({
  searchBoxId,
  textInputId,
  resultsDivId,
  resultClass,
  valueAttribute,
}) {
  // Add a click event listener to the document
  document.addEventListener(
    "click",
    function (event) {
      // If the clicked element contains the resultClass
      if (event.target.classList.contains(resultClass)) {
        // Get the search box element
        var searchBox = document.getElementById(searchBoxId);
        // Set the search box value to the text content of the clicked element
        searchBox.value = event.target.textContent;

        // Get the hidden input box element
        var input = document.getElementById(textInputId);
        // Set the input box value to the value attribute of the clicked element
        input.value = event.target.getAttribute(valueAttribute);

        // Clear the search results by setting the innerHTML of the results div to an empty string
        document.getElementById(resultsDivId).innerHTML = "";
      }
    },
    false
  );
}

/**
 * This function set a timer to close and remove alerts from DOM
 * @param {string} autoCloseClass - The class of the alert to be closed
 * @param {number} timeInterval - The time interval in milliseconds
 *
 */
function AlertsAutoDismissal(autoCloseClass, timeInterval) {
  document.addEventListener("DOMContentLoaded", function () {
    const autoCloseAlerts = document.querySelectorAll("." + autoCloseClass);

    autoCloseAlerts.forEach(function (alert) {
      setTimeout(function () {
        alert.classList.add("hide");

        alert.addEventListener("transitionend", function () {
          alert.remove(); // Remove after the transition ends
        });
      }, timeInterval);
    });
  });
}

/**
 * in line confirmation dialog for submitting forms
 */
function confirmationDialog(question) {
  return confirm(question);
}

/**
 * This function adds a listener to all .fade-out-hide elements to hide them after the fade out animation ends.
 */
function applyHideAfterAnimation() {
  document.querySelectorAll(".hide-after-animation").forEach((element) => {
    if (!element.classList.contains("fade-out-processed")) {
      element.classList.add("fade-out-processed"); // Mark the element as processed
      element.addEventListener("animationend", function () {
        this.style.display = "none";
      });
    }
  });
}

/**
 * This function toggles the visibility of the tool tray icons.
 * @param {string} triggerId - The ID of the trigger element.
 * @param {string} containerIdentifier - The identifier (ID or class) of the container.
 **/
function toggleToolTrayIcons(triggerId, containerIdentifier) {
  var triggerIcon = document.getElementById(triggerId);
  triggerIcon.innerHTML = triggerIcon.innerHTML.includes("bi-tools")
    ? '<i class="bi bi-three-dots fw-bold text-primary"></i>' // Change to a 'close' icon
    : '<i class="bi bi-tools fw-bold text-gray-500"></i>'; // Change back to the 'tools' icon

  if (containerIdentifier.startsWith("#")) {
    var container = document.getElementById(containerIdentifier.slice(1));
    container.classList.toggle("d-none");
  } else if (containerIdentifier.startsWith(".")) {
    var containers = document.getElementsByClassName(
      containerIdentifier.slice(1)
    );
    for (let container of containers) {
      container.classList.toggle("d-none");
    }
  }
}

/**
 * The following functions are used by the search form.
 * Together with HTMX AfterOnLoad and BeforeOnLoad events above
 **/

/** hide the search results panel when clicking outside the search form **/
function hideResultsPanel() {
  var resultsPanel = document.getElementById("search-results-panel");
  resultsPanel.style.display = "none";
}

/**   window click event listener **/
window.addEventListener("click", function (event) {
  var searchForm = document.getElementById("htmx-search-form");
  if (!searchForm.contains(event.target)) {
    hideResultsPanel();
  }
});

/** object focus event listener **/
document
  .getElementById("htmx-search-form")
  .querySelector('input[type="search"]')
  .addEventListener("focus", function () {
    var resultsPanel = document.getElementById("search-results-panel");
    if (resultsPanel.innerHTML.trim() !== "") {
      resultsPanel.style.display = "block";
    }
  });
/** Search form functions end **/
