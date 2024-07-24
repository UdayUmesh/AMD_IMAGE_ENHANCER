document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/enhance', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        document.getElementById('enhanced-image').src = url;
        document.getElementById('download-link').href = url;
        document.getElementById('result').style.display = 'block';
    } else {
        alert('Error enhancing image. Please try again.');
    }
});
