document.getElementById('analyzeBtn').addEventListener('click', () => {
  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = '<p>Analyzing, please wait...</p>';

  // This gets the URL of the tab you are currently viewing.
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentUrl = tabs[0].url;

    // This sends the URL to your Flask API server with the corrected URL format.
    fetch('http://127.0.0.1:5000/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: currentUrl })
    })
    .then(response => {
      // First, check if the response from the server is okay
      if (!response.ok) {
        // If not, throw an error to be caught by the .catch block
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // This displays the report received from the Flask server.
      if (data.error || data.analysis_errors) {
        resultDiv.innerHTML = `<p><strong>Error:</strong> ${data.error || data.analysis_errors}</p>`;
      } else {
        resultDiv.innerHTML = `
          <p><strong>Verdict:</strong> ${data.final_verdict}</p>
          <p><strong>AI Score:</strong> ${data.ai_score}</p>
          <p><strong>Heuristic Score:</strong> ${data.heuristic_score}</p>
          <p><strong>Justification:</strong> ${data.ai_justification}</p>
        `;
      }
    })
    .catch(error => {
      // This error shows if the Flask server isn't running or there's a network issue.
      resultDiv.innerHTML = `<p><strong>Connection Error:</strong> Could not connect to the PhishGuard AI server. Please ensure it is running and accessible.</p>`;
      console.error('Error during fetch:', error);
    });
  });
});