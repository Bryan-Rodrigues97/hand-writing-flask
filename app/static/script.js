document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    const resetBtn = document.getElementById('resetBtn');
    const predictBtn = document.getElementById('predictBtn');
    const resultDiv = document.getElementById('result');
    const resultLabelSpan = document.getElementById('resultLabelSpan');
    const asciiCodeSpan = document.getElementById('asciiCodeSpan');
    const emnistClass = document.getElementById('emnistClass')

    let drawing = false;

    // Drawing canvas function
    function startDrawing(event) {
      drawing = true;
      draw(event);
    }

    function stopDrawing() {
      drawing = false;
      ctx.beginPath();
    }

    function draw(event) {
        if (!drawing) 
            return;
    
        ctx.lineWidth = 20;
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'white'; 
        
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
    
        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
    }
    

    // Drawing event listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseleave', stopDrawing);

    // Canvas reset
    resetBtn.addEventListener('click', () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      resultDiv.hidden = true
    });

    // Predict
    predictBtn.addEventListener('click', () => {
      var imgJpegUrl = canvas.toDataURL("image/jpeg");
      
      fetch(`/predict`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ 
            img: imgJpegUrl
        })
      })
      .then(response => response.json())
      .then(data => {
        resultDiv.hidden = false
        resultLabelSpan.innerText = data.label
        asciiCodeSpan.innerText = data.ascii_code
        emnistClass.innerText = data.emnist_class
      })
      .catch(error => console.error('Error:', error));
    });
});