var videoStream; 
var videoElement;
function startCamera() {
    // Check if the video stream is not already set
    if (!videoStream) {
        // Attempt to access the user's camera
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                // If successful, store the stream in the videoStream variable
                videoStream = stream;
                // Display the video stream
                displayVideo(stream);
            })
            .catch(function(err) {
                // If an error occurs, log it
                console.error('Error accessing the camera:', err);
            });
    } else {
        // If the video stream is already set, display it
        displayVideo(videoStream); 
    }
}


function displayVideo(stream) {
    videoElement = document.createElement('video');
    videoElement.srcObject = stream;
    document.getElementById('snapshotContainer').innerHTML = ''; 
    document.getElementById('snapshotContainer').appendChild(videoElement);
    
    videoElement.play();
    
    var snapButton = document.createElement('button');
    snapButton.type = 'button';
    snapButton.className = 'btn btn-secondary';
    snapButton.textContent = 'Take A Snap';
    snapButton.onclick = captureSnapshot;
    document.getElementById('snapshotContainer').appendChild(snapButton);
}

function captureSnapshot() {
    if (!videoStream) {
        console.error('Camera stream not available.');
        return;
    }
    
    var canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    var context = canvas.getContext('2d');
    
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    
    var imageURL = canvas.toDataURL('image/png');
    
    var image = document.createElement('img');
    image.src = imageURL;
    document.getElementById('snapshotContainer').appendChild(image);
}