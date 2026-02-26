/* =====================================
   MyGSTIndia HSN Search Engine
   SAFE VERSION - No Design Changes
===================================== */

console.log("HSN Search Engine Loaded");

/* ===============================
WAIT UNTIL PAGE + DATA LOAD
=============================== */

window.addEventListener("DOMContentLoaded", () => {

  if (!window.hsnDatabase) {
    console.error("HSN Database not loaded");
    return;
  }

  if (!window.findHSNFromKeyword) {
    console.error("Keyword engine not loaded");
    return;
  }

  const searchInput = document.getElementById("searchInput");
  const resultsDiv = document.getElementById("results");
  const loadingDiv = document.getElementById("loading");

  if (!searchInput || !resultsDiv) {
    console.error("Search elements missing");
    return;
  }

  /* ===============================
  BUILD FAST SEARCH INDEX
  =============================== */

  const normalizedHSN = hsnDatabase.map(item => ({
    ...item,
    searchText:
      (item.description + " " + item.code)
        .toLowerCase()
  }));

  let typingTimer;

  /* ===============================
  INPUT LISTENER
  =============================== */

  searchInput.addEventListener("input", function () {

    clearTimeout(typingTimer);

    const query = this.value.toLowerCase().trim();

    if (query.length < 2) {
      resultsDiv.style.display = "none";
      return;
    }

    if (loadingDiv)
      loadingDiv.style.display = "block";

    typingTimer = setTimeout(() => {
      runSearch(query);
    }, 250);

  });


  /* ===============================
  MAIN SEARCH
  =============================== */

  function runSearch(query) {

    let results = [];

    /* Keyword mapping search */
    const keywordHSN = findHSNFromKeyword(query);

    if (keywordHSN) {
      results = normalizedHSN.filter(item =>
        keywordHSN.includes(item.code.substring(0, 4))
      );
    }

    /* Text fallback search */
    if (results.length === 0) {
      results = normalizedHSN.filter(item =>
        item.searchText.includes(query)
      );
    }

    if (loadingDiv)
      loadingDiv.style.display = "none";

    displayResults(results.slice(0, 40), query);
  }


  /* ===============================
  DISPLAY RESULTS
  =============================== */

  function displayResults(results, query) {

    if (!results.length) {
      resultsDiv.innerHTML = `
        <div class="no-results">
          <div class="no-results-icon">🔍</div>
          <h3>No HSN found for "${query}"</h3>
          <p>Try simpler words like:</p>
          <p><strong>mobile, rice, cement, chair</strong></p>
        </div>
      `;
      resultsDiv.style.display = "block";
      return;
    }

    resultsDiv.innerHTML = results.map(item => `
      <div class="result-card">
        <div class="result-header">
          <div class="hsn-code">HSN ${item.code}</div>
          <div class="gst-rate">${item.gst}</div>
        </div>

        <div class="result-description">
          ${item.description}
        </div>

        <div class="result-meta">
          <div class="result-meta-item">
            📁 ${item.category}
          </div>
        </div>
      </div>
    `).join("");

    resultsDiv.style.display = "block";
  }

});
