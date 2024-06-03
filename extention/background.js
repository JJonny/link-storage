chrome.contextMenus.create({
  title: "Send Text to Backend",
  contexts: ["selection"],
  onclick: sendTextToBackend
});

function sendTextToBackend(info, tab) {
  const selectedText = info.selectionText;
  const url = tab.url;

  // Отправка данных на backend Python-приложение
  fetch('http://127.0.0.1:8000/save', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: selectedText, url: url })
  })
  .then(response => {
    if (response.ok) {
      console.log('Text sent successfully');
    } else {
      console.error('Failed to send text');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}