document.addEventListener("DOMContentLoaded", () => {
    
    const codeInput = document.getElementById("codeInput");
    const checkButton = document.getElementById("checkButton");
    const outputArea = document.getElementById("outputArea");
    const languageSelect = document.getElementById("languageSelect");

    checkButton.addEventListener("click", () => {
        const userCode = codeInput.value;
        const selectedLanguage = languageSelect.value;
        
        if (userCode.trim() === "") {
            outputArea.innerHTML = '<pre class="placeholder">Please enter some code first.</pre>';
            return;
        }

        formatAndDisplayErrors("checking"); 

        
        callBackendAPI(userCode, selectedLanguage)
            .then(data => {
                formatAndDisplayErrors(data);
            })
            .catch(error => {
                outputArea.innerHTML = `<pre class="result-error">Error: ${error.message}</pre>`;
            });
    });


    function formatAndDisplayErrors(data) {
        outputArea.innerHTML = "";

        if (data === "checking") {
            outputArea.innerHTML = '<pre class="result-checking">Analyzing your code...</pre>';
            return;
        }

        if (data.errors && data.errors.length === 0) {
            outputArea.innerHTML = '<pre class="result-success">✅ Analysis complete. No keyword typos found!</pre>';
            return;
        }

        if (data.errors && data.errors.length > 0) {
            let htmlOutput = data.errors.map(err => {
                return `
                    <div class="error-line">
                        <span class="line-num">Line ${err.line}:</span>
                        Found typo <strong class="typo">"${err.typo}"</strong>. 
                        Did you mean <strong class="suggestion">"${err.suggestion}"</strong>?
                    </div>
                `;
            }).join('');
            
            outputArea.innerHTML = htmlOutput;
            return;
        }
        
        outputArea.innerHTML = '<pre class="result-error">Error: Received an unexpected response from the server.</pre>';
    }

    function callMockBackend(code) {
        console.log("Simulating backend call...");
        return new Promise((resolve) => {
            setTimeout(() => {
                if (code.includes("functoin")) {
                    resolve({ errors: [{ line: 1, typo: "functoin", suggestion: "function" }] });
                } else {
                    resolve({ errors: [] });
                }
            }, 1000);
        });
    }

    async function callBackendAPI(code, language) {
        const backendUrl = 'http://127.0.0.1:5001/api/checkcode';

        const response = await fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                code: code,
                language: language 
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }

        return await response.json(); 
    }
});