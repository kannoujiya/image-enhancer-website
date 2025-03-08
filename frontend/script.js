document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const file = document.getElementById('imageInput').files[0];
  const resolution = document.getElementById('resolution').value;
  const colorize = document.getElementById('colorize').checked;

  const formData = new FormData();
  formData.append('image', file);
  formData.append('resolution', resolution);
  formData.append('colorize', colorize);

  const response = await fetch('/enhance', {
    method: 'POST',
    body: formData,
  });

  const result = await response.json();

  if (result.url) {
    document.getElementById('enhancedImage').src = result.url;
    document.getElementById('downloadLink').href = result.url;
    document.getElementById('result').style.display = 'block';
  }
});