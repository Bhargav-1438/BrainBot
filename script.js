document.getElementById("formulaForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const input = document.getElementById("formula").value;
    const resultDiv = document.getElementById("result");

    resultDiv.textContent = "Solving...";

    const response = await fetch("/solve", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: input })
    });

    const data = await response.json();
    resultDiv.textContent = data.answer || "Sorry, couldn't solve that.";
});
