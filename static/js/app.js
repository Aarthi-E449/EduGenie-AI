
let currentTool = "qa";

const tools = {
    qa: {
        title: "Ask a Question",
        endpoint: "/qa"
    },
    explain: {
        title: "Explain a Concept",
        endpoint: "/explain"
    },
    quiz: {
        title: "Generate Quiz",
        endpoint: "/quiz"
    },
    summarize: {
        title: "Summarize Notes",
        endpoint: "/summarize"
    },
    learn: {
        title: "Learning Path",
        endpoint: "/learn/recommendations"
    }
};

// Change the selected learning tool
function showTool(tool) {
    currentTool = tool;

    document.getElementById("tool-title").textContent =
        tools[tool].title;

    document.getElementById("user-input").value = "";
    document.getElementById("result").textContent = "";

    document.getElementById("level-container").hidden =
        tool !== "learn";
}

// Send the student's input to FastAPI
async function submitTool() {
    const input = document.getElementById("user-input");
    const result = document.getElementById("result");
    const button = document.getElementById("submit-btn");

    const text = input.value.trim();

    if (text.length < 2) {
        result.textContent =
            "Please enter a question or topic.";
        return;
    }

    const data = { text: text };

    if (currentTool === "learn") {
        data.level =
            document.getElementById("level").value;
    }

    button.disabled = true;
    button.textContent = "Generating...";
    result.textContent = "Please wait...";

    try {
        const response = await fetch(
            tools[currentTool].endpoint,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        const output = await response.json();

        if (!response.ok) {
            throw new Error(
                output.detail || "Something went wrong."
            );
        }

        if (currentTool === "quiz") {
            displayQuiz(output.questions);
        } else {
            result.textContent = output.result;
        }

    } catch (error) {
        result.textContent =
            "Error: " + error.message;
    } finally {
        button.disabled = false;
        button.textContent = "Generate";
    }
}

// Display multiple-choice questions
function displayQuiz(questions) {
    const result = document.getElementById("result");
    result.replaceChildren();

    questions.forEach((item, questionIndex) => {
        const container = document.createElement("div");
        container.style.marginBottom = "25px";

        const heading = document.createElement("h3");
        heading.textContent =
            `${questionIndex + 1}. ${item.question}`;
        container.appendChild(heading);

        const feedback = document.createElement("p");

        item.options.forEach((option, optionIndex) => {
            const label = document.createElement("label");
            label.style.display = "block";
            label.style.marginBottom = "10px";

            const radio = document.createElement("input");
            radio.type = "radio";
            radio.name = `question-${questionIndex}`;
            radio.value = optionIndex;

            radio.addEventListener("change", () => {
                const correct =
                    optionIndex === item.correct_answer;

                feedback.textContent = correct
                    ? "Correct! " + item.explanation
                    : "Incorrect. " + item.explanation;
            });

            label.appendChild(radio);
            label.append(
                " " + String.fromCharCode(65 + optionIndex)
                + ". " + option
            );

            container.appendChild(label);
        });

        container.appendChild(feedback);
        result.appendChild(container);
    });
}