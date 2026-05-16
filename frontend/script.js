// Custom Popup Function
function showPopup(message, refresh = false) {

    // Remove old popup if exists
    const oldPopup = document.getElementById("customPopup");

    if (oldPopup) {
        oldPopup.remove();
    }

    // Overlay
    const overlay = document.createElement("div");

    overlay.id = "customPopup";

    overlay.style.position = "fixed";
    overlay.style.top = "0";
    overlay.style.left = "0";
    overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.backgroundColor = "rgba(0,0,0,0.5)";
    overlay.style.display = "flex";
    overlay.style.justifyContent = "center";
    overlay.style.alignItems = "center";
    overlay.style.zIndex = "9999";

    // Popup Box
    const popup = document.createElement("div");

    popup.style.background = "#fff";
    popup.style.padding = "25px";
    popup.style.borderRadius = "10px";
    popup.style.width = "350px";
    popup.style.textAlign = "center";
    popup.style.boxShadow = "0 0 15px rgba(0,0,0,0.3)";

    popup.innerHTML = `
        <h3 style="margin-bottom:15px;color:red;">
            Alert
        </h3>

        <p style="margin-bottom:20px;">
            ${message}
        </p>

        <button id="popupBtn"
            style="
                padding:10px 20px;
                border:none;
                background:#007bff;
                color:white;
                border-radius:5px;
                cursor:pointer;
            ">
            OK
        </button>
    `;

    overlay.appendChild(popup);

    document.body.appendChild(overlay);

    document
        .getElementById("popupBtn")
        .addEventListener("click", () => {

            overlay.remove();

            if (refresh) {
                location.reload();
            }
        });
}


// Upload PDF
async function uploadPDF() {

    const fileInput =
        document.getElementById("pdfFile");

    const file = fileInput.files[0];

    // No file selected
    if (!file) {

        showPopup("Please select a PDF file.");

        return;
    }

    // Validate PDF
    if (file.type !== "application/pdf") {

        showPopup(
            "Only PDF files are allowed.",
            true
        );

        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        showPopup(
            data.message || data.error
        );

    } catch (error) {

        showPopup(
            "Upload failed. Please try again."
        );
    }
}


// Ask Question
async function askQuestion() {

    const question =
        document.getElementById("question").value;

    if (!question.trim()) {

        showPopup(
            "Please enter a question."
        );

        return;
    }

    const chatContainer =
        document.getElementById("chatContainer");

    // User Message
    chatContainer.innerHTML += `
        <div class="user">
            <b>You:</b> ${question}
        </div>
    `;

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/ask?question=${encodeURIComponent(question)}`
        );

        const data = await response.json();

        // AI Message
        chatContainer.innerHTML += `
            <div class="bot">
                <b>AI:</b> ${data.answer || data.error}
            </div>
        `;

        // Auto scroll
        chatContainer.scrollTop =
            chatContainer.scrollHeight;

    } catch (error) {

        chatContainer.innerHTML += `
            <div class="bot">
                <b>AI:</b> Error processing request.
            </div>
        `;
    }

    // Clear input
    document.getElementById("question").value = "";
}
