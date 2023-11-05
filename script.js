let imageCount = 0;  // Counter for captured images

document.getElementById('registrationForm').addEventListener('submit', function(event) {
  event.preventDefault();  // Prevents the form from submitting via HTTP
  // Access form fields and their values
  const studentName = document.getElementById('studentName').value;
  const studentID = document.getElementById('studentID').value;
  const password = document.getElementById('password').value;

  // Add logic to send this data to the server or perform further actions
  console.log('Student Name:', studentName);
  console.log('Student ID:', studentID);
  console.log('Password:', password);
});

document.getElementById('startScanButton').addEventListener('click', () => {
  // Check if 20 images have been captured
  if (imageCount < 20) {
    const video = document.getElementById('video');
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    // Get user media (camera access)
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;

        // Capture image when the video stream is ready
        context.drawImage(video, 0, 0, 640, 480);
        const imageData = canvas.toDataURL('image/jpeg');  // Convert captured frame to base64 image

        // Send the image data to the server
        sendDataToServer(imageData);
      })
      .catch(err => {
        console.error('Error accessing the camera:', err);
      });
  } else {
    // Enable the "Finish" button
    document.getElementById('finishButton').disabled = false;
  }
});

document.getElementById('finishButton').addEventListener('click', () => {
  // Trigger face recognition
  triggerFaceRecognition();
});

document.addEventListener('keypress', (event) => {
  if (event.key === 's') {
    // Increment the image count and display a message
    imageCount++;
    console.log(`Image ${imageCount} stored. Press 'Capture' to capture the next image.`);
  }
});

function sendDataToServer(imageData) {
  // Send the imageData to the server using AJAX or fetch
  // Example using fetch:
  fetch('/process_image', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: imageData })
  })
    .then(response => response.json())
    .then(data => {
      // Handle the response from the server (e.g., display recognition result)
      console.log('Recognition result:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function triggerFaceRecognition() {
  // Send a request to trigger face recognition (you can implement this function)
  // Example: fetch('/trigger_face_recognition', { method: 'POST' });
  console.log('Face recognition triggered.');
}
