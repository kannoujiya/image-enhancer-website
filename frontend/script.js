let userPoints = 0;

document.getElementById('dropzone').addEventListener('click', () => {
  document.getElementById('imageInput').click();
});

document.getElementById('imageInput').addEventListener('change', (e) => {
  const files = e.target.files;
  if (files.length > 0) {
    const reader = new FileReader();
    reader.onload = (event) => {
      document.getElementById('originalImage').src = event.target.result;
    };
    reader.readAsDataURL(files[0]);
  }
});

document.getElementById('enhanceButton').addEventListener('click', async () => {
  const file = document.getElementById('imageInput').files[0];
  const resolution = document.getElementById('resolution').value;
  const sharpness = document.getElementById('sharpness').value;
  const colorize = document.getElementById('colorize').checked;

  if ((resolution === "3840" && userPoints < 100) || (resolution === "7680" && userPoints < 200)) {
    alert("You don't have enough points to unlock this resolution. Complete offers to earn points!");
    return;
  }

  const formData = new FormData();
  formData.append('image', file);
  formData.append('resolution', resolution);
  formData.append('sharpness', sharpness);
  formData.append('colorize', colorize);

  const response = await fetch('/enhance', {
    method: 'POST',
    body: formData,
  });

  const result = await response.json();
  if (result.url) {
    document.getElementById('enhancedImage').src = result.url;
    document.getElementById('downloadLink').href = result.url;
  }
});

document.getElementById('openOfferwall').addEventListener('click', () => {
  window.open('https://mylead.global/offerwall', '_blank');
});

function updatePoints(points) {
  userPoints = points;
  document.getElementById('points').textContent = points;
}

// Simulate points update (replace with actual MyLead API integration)
setTimeout(() => updatePoints(50), 3000);