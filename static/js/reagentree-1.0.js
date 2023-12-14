// Version: 1.0
// This file contains functions used by the reagentree app.

/**
 * Initialize the Bootstrap tooltip.
 */
document.addEventListener("DOMContentLoaded", function(){
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
  });
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
