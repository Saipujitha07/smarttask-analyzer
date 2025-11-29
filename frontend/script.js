async function analyze() {
    const raw = document.getElementById("jsonInput").value;
    const strategy = document.getElementById("strategy").value;

    let tasks = [];
    try {
        tasks = JSON.parse(raw);
    } catch {
        alert("Invalid JSON format 😭");
        return;
    }

    const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            strategy: strategy,
            tasks: tasks
        })
    });

    if (!response.ok) {
        alert("Backend error 😭: " + response.status);
        console.log("Sending request to backend...");

        return;
    }

    const data = await response.json();
    render(data.tasks);
}

function render(tasks) {
    const out = document.getElementById("output");
    out.innerHTML = "";

    tasks.forEach((t) => {
        let color = t.score > 0.8 ? "high" : t.score > 0.5 ? "medium" : "low";

        out.innerHTML += `
            <div class="task ${color}">
                <h3>${t.title}</h3>
                <p><b>Score:</b> ${t.score}</p>
                <p><b>Due Date:</b> ${t.due_date}</p>
                <p><b>Importance:</b> ${t.importance}</p>
                <p><b>Hours:</b> ${t.estimated_hours}</p>
                <p><b>Why:</b> ${t.explanation ?? "Balanced priority"}</p>
            </div>
        `;
    });
}
