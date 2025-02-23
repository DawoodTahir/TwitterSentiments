document.getElementById("search-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent default form submission

    let keyword = document.getElementById("keyword").value;
    let formData = new FormData();
    formData.append("keyword", keyword);

    fetch("/search", {  
        method: "POST",  // 🔹 Ensure we send a POST requestxa
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("tweet-view").innerHTML = `<p class="text-danger">${data.error}</p>`;
            return;
        }

        let resultsDiv = document.getElementById("tweet-view");
        resultsDiv.innerHTML = `<h3>Tweets & Sentiments</h3><div class="row">`;

        data.tweets.forEach(([sentiment, tweet]) => {
            resultsDiv.innerHTML += `
                <div class="col-md-6"><strong>${sentiment}</strong></div>
                <div class="col-md-6">${tweet}</div>
            `;
        });

        resultsDiv.innerHTML += "</div>";

        // Load charts when toggled
        document.getElementById("pie-chart").src = data.charts.pie;
        document.getElementById("histogram").src = data.charts.hist;
        
        document.getElementById("toggle-view").style.display = "block";
    });
});

document.getElementById("toggle-view").addEventListener("click", function() {
    let tweetView = document.getElementById("tweet-view");
    let chartView = document.getElementById("chart-view");

    if (chartView.style.display === "none") {
        chartView.style.display = "block";
        tweetView.style.display = "none";
        this.textContent = "View Tweets";
    } else {
        chartView.style.display = "none";
        tweetView.style.display = "block";
        this.textContent = "Visualize";
    }
});
