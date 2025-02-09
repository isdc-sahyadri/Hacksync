document.getElementById("uploadForm").onsubmit = async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById("fileInput").files[0];
    
    if (!fileInput) {
        alert("⚠️ Please select a file!");
        return;
    }

    // Show "Uploading..." message
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("result").classList.add("hidden");

    let formData = new FormData();
    formData.append("file", fileInput);

    // Display the uploaded file name
    document.getElementById("uploadStatus").innerHTML = `✅ Uploaded: ${fileInput.name}`;

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", { 
            method: "POST", 
            body: formData 
        });

        const data = await response.json();
        
        document.getElementById("score").innerText = data.similarity_score;
        document.getElementById("highlightedText").innerHTML = data.highlighted_text;

        document.getElementById("loading").classList.add("hidden");
        document.getElementById("result").classList.remove("hidden");

    } catch (error) {
        alert("❌ Error checking plagiarism. Try again.");
        document.getElementById("loading").classList.add("hidden");
    }
};
