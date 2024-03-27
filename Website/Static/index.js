function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function deleteJoke(jokeId) {
  fetch('/delete-jokes', {
      method: 'POST',
      body: JSON.stringify({ jokeId: jokeId }),
      headers: {
          'Content-Type': 'application/json'
      }
  }).then(response => {
      if (response.ok) {
          window.location.reload(); // Reload the page to update the list of jokes
      }
  }).catch(error => console.error('Error:', error));
}

function deleteMeme(memeId) {
fetch('/delete-meme', {
    method: 'POST',
    body: JSON.stringify({ memeId: memeId }),
    headers: {
        'Content-Type': 'application/json'
    }
}).then(response => {
    if (response.ok) {
        document.getElementById('meme-' + memeId).remove(); // Removes the meme element from the page
    }
}).catch(error => console.error('Error:', error));
}

function deleteVideo(videoId) {
fetch("/delete-video", {
  method: "POST",
  body: JSON.stringify({ videoId: videoId }),
  headers: {
      'Content-Type': 'application/json'
  }
}).then(response => {
  if (response.ok) {
    // Remove the video element from the page
    document.querySelector('.video-item[data-id="' + videoId + '"]').remove();
  }
}).catch(error => console.error('Error:', error));
}

function getYouTubeVideoID(url) {
var regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
var match = url.match(regExp);
if (match && match[2].length == 11) {
  return match[2];
} else {
  return null;
}
}

function deleteVideo(videoId) {
  fetch("/delete-video", {
    method: "POST",
    body: JSON.stringify({ videoId: videoId }),
    headers: {
        'Content-Type': 'application/json'
    }
  }).then(response => {
    if (response.ok) {
      // The video was successfully deleted, now reload the page
      window.location.reload();
    } else {
      // Handle the error, maybe show a message to the user
      console.error('Failed to delete the video.');
    }
  }).catch(error => {
    // Handle any other errors
    console.error('Error:', error);
  });
}
