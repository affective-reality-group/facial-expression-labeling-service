function labelImage(label) {
    const imageElement = document.getElementById('image-to-label');
    const imageName = imageElement.src.split('/').pop();

    fetch('/label', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({image_name: imageName, label: label}),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            window.location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
