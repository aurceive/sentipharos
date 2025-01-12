// Define the URL of the FastAPI service
const url = 'https://fes-262238016563.europe-north1.run.app/predict';

// Function to send a POST request to the FastAPI service
async function testFeatureExtraction(inputs) {
  try {
    // Start timing the request
    const startTime = Date.now();

    // Prepare the request body
    const data = {
      inputs: inputs  // Accept the text(s) dynamically
    };

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();

    // Calculate the elapsed time in seconds
    const elapsedTime = (Date.now() - startTime) / 1000;

    console.log("Model:", result.model);
    console.log("Embeddings:", result.outputs);
    console.log("Time taken (seconds):", elapsedTime.toFixed(3)); // Limit to 3 decimal places
  } catch (error) {
    console.error("Error:", error);
  }
}

function grt(length = 240) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const space = ' ';
    let result = '';
    let consecutive = 0; // Счётчик символов без пробела

    for (let i = 0; i < length; i++) {
        if (consecutive >= 13) {
            // Если достигнуто 13 символов подряд, вставляем пробел
            result += space;
            consecutive = 0;
        } else {
            // Случайно выбираем, вставить пробел или символ
            const isSpace = consecutive > 0 && Math.random() < 0.15; // 15% шанс вставить пробел после символа
            if (isSpace) {
                result += space;
                consecutive = 0; // Сбрасываем счётчик
            } else {
                result += characters.charAt(Math.floor(Math.random() * characters.length));
                consecutive++;
            }
        }
    }

    return result;
}

// Example usage
// grt()
// testFeatureExtraction([grt()]);
// testFeatureExtraction([grt(), grt()]);
testFeatureExtraction([grt(), grt(), grt(), grt(), grt(), grt(), grt(), grt(), grt(), grt(), grt(), grt(), grt(), grt(), grt(), grt()]);
