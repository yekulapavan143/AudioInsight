// Update file name when selected and enable audio player
function updateFileName() {
    const fileInput = document.getElementById('audioFile');
    const fileName = fileInput.files[0].name;
    document.getElementById('fileName').innerText = `Selected File: ${fileName}`;

    // Display audio player
    const audioPlayer = document.getElementById('audioPlayer');
    const fileURL = URL.createObjectURL(fileInput.files[0]);
    audioPlayer.src = fileURL;
    audioPlayer.style.display = 'block';
}

// Upload audio file and process
function uploadAudio() {
    const fileInput = document.getElementById('audioFile');
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select an audio file.");
        return;
    }

    const formData = new FormData();
    formData.append('audio', file);

    // Show progress bar
    const progressBar = document.getElementById('progress');
    progressBar.style.display = 'block';
    progressBar.style.width = '0%';

    // Update status
    const status = document.getElementById('status');
    status.innerText = 'Processing...';
    status.className = 'loading';

    // Send the file to the backend
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/process-audio', true);

    xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
            const progress = (e.loaded / e.total) * 100;
            progressBar.style.width = `${progress}%`;
        }
    });

    xhr.onload = function () {
        try {
            if (xhr.status === 200) {
                console.log('Response received:', xhr.responseText);
                const data = JSON.parse(xhr.responseText);
                console.log('Parsed data:', data);

                // Update status
                status.innerText = 'Processing Complete';
                status.className = 'success';

                // Clear previous results
                clearResults();
                
                // Display transcription
                displayTranscription(data.transcription);
                
                // Display keywords
                displayKeywords(data.keywords);

                // Show download button
                const downloadBtn = document.getElementById('downloadBtn');
                downloadBtn.style.display = 'block';
                downloadBtn.dataset.transcription = data.transcription;
            } else {
                handleError(`Server error: ${xhr.status} ${xhr.statusText}`);
            }
        } catch (error) {
            handleError(`Error processing response: ${error.message}`);
            console.error('Error details:', error);
        }
    };

    xhr.onerror = function () {
        handleError('Network error occurred');
    };

    xhr.send(formData);
}

// Display transcription
function displayTranscription(text) {
    const transcriptionDiv = document.getElementById('transcription');
    if (transcriptionDiv) {
        transcriptionDiv.textContent = text;
        console.log('Transcription displayed');
    }
}

// Display keywords
function displayKeywords(keywords) {
    // Display Named Entities
    const namedEntitiesDiv = document.getElementById('namedEntities');
    if (namedEntitiesDiv && keywords.named_entities) {
        keywords.named_entities.forEach(entity => {
            const chip = createKeywordChip(entity.text, entity.type);
            namedEntitiesDiv.appendChild(chip);
        });
        console.log('Named entities displayed');
    }

    // Display Key Phrases
    const keyPhrasesDiv = document.getElementById('keyPhrases');
    if (keyPhrasesDiv && keywords.key_phrases) {
        keywords.key_phrases.forEach(phrase => {
            const chip = createKeywordChip(phrase);
            keyPhrasesDiv.appendChild(chip);
        });
        console.log('Key phrases displayed');
    }

    // Display Frequent Words
    const frequentWordsDiv = document.getElementById('frequentWords');
    if (frequentWordsDiv && keywords.frequent_words) {
        keywords.frequent_words.forEach(word => {
            const chip = createKeywordChip(word);
            frequentWordsDiv.appendChild(chip);
        });
        console.log('Frequent words displayed');
    }
}

// Create a keyword chip element
function createKeywordChip(text, type = null) {
    const chip = document.createElement('div');
    chip.className = 'keyword-chip';

    if (type) {
        const textSpan = document.createElement('span');
        textSpan.className = 'keyword-text';
        textSpan.textContent = text;

        const typeSpan = document.createElement('span');
        typeSpan.className = 'keyword-type';
        typeSpan.textContent = type;

        chip.appendChild(textSpan);
        chip.appendChild(typeSpan);
    } else {
        chip.textContent = text;
    }

    return chip;
}

// Handle errors
function handleError(message) {
    const status = document.getElementById('status');
    status.innerText = message;
    status.className = 'error';
    console.error(message);
}

// Clear all results
function clearResults() {
    // Clear transcription
    const transcriptionDiv = document.getElementById('transcription');
    if (transcriptionDiv) {
        transcriptionDiv.textContent = '';
    }

    // Clear keywords
    ['namedEntities', 'keyPhrases', 'frequentWords'].forEach(id => {
        const div = document.getElementById(id);
        if (div) {
            div.innerHTML = '';
        }
    });

    // Hide download button
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.style.display = 'none';
    }
}

// Download transcription
function downloadTranscription() {
    const downloadBtn = document.getElementById('downloadBtn');
    const transcription = downloadBtn.dataset.transcription;
    
    const blob = new Blob([transcription], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'transcription.txt';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Clear file and reset interface
function clearFile() {
    // Reset file input
    const fileInput = document.getElementById('audioFile');
    fileInput.value = '';
    
    // Hide audio player
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.style.display = 'none';
    audioPlayer.src = '';
    
    // Reset file name display
    document.getElementById('fileName').innerText = '';
    
    // Reset status
    const status = document.getElementById('status');
    status.innerText = 'Select a file to begin';
    status.className = '';
    
    // Clear results
    clearResults();
}