// Get references of elements from the html page
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const upload = document.getElementById("upload");

// --- Load image ---
// Wait for image to be entered and read and process the image
upload.addEventListener("change", function () {
    // Read file
    const reader = new FileReader();
    reader.onload = function (e) {
        const img = new Image();
        // Once image is loaded
        img.onload = function () {
            // Resize html canvas to match image
            canvas.width = img.width;
            canvas.height = img.height;
            // Apply a slight blur
            ctx.filter = 'blur(0.6px)';
            ctx.drawImage(img, 0, 0);
            ctx.filter = 'none';
            // Call function
            processCanvas();
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(upload.files[0]);
});

// --- Process image ---
function processCanvas() {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    // Loop through pixel data
    for (let i = 0; i < data.length; i += 4) {
        // Extract pixel data
        const r = data[i], g = data[i + 1], b = data[i + 2];

        // Calculate brightness
        const brightness = 0.299 * r + 0.587 * g + 0.114 * b;
        // Fade pixels at edges
        const alphaRatio = Math.pow((255 - brightness) / 255, 2.8);
        const alpha = Math.floor(alphaRatio * 255);

        // Soften lines
        data[i] = data[i + 1] = data[i + 2] = 0;
        data[i + 3] = alpha;
    }

    ctx.putImageData(imageData, 0, 0);

    // Set up option to download
    canvas.toBlob(blob => { // Convert canvas to a Blob
        const download = document.getElementById("download");
        download.href = URL.createObjectURL(blob);
        download.download = "anti-aliased.png";
        download.style.display = "inline";
    }, "image/png");
}

// Set up option to copy to clipboard
document.getElementById("copy").addEventListener("click", () => { // Wait for click
    canvas.toBlob(blob => { // Convert canvas to a Blob
        const item = new ClipboardItem({ "image/png": blob });
        navigator.clipboard.write([item])
            .then(() => alert("Copied!"))
            .catch(err => console.error("Clipboard failed:", err));
    });
});