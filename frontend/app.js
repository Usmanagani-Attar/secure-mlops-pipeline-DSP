const jsonInput = document.getElementById("jsonInput");
const predictBtn = document.getElementById("predictBtn");
const errorBox = document.getElementById("errorBox");
const jsonStatus = document.getElementById("jsonStatus");
const resultEmpty = document.getElementById("resultEmpty");
const resultContent = document.getElementById("resultContent");
const prediction = document.getElementById("prediction");
const responseBody = document.getElementById("responseBody");
const statusCode = document.getElementById("statusCode");

const cammeoSample = {
    Area: 15231,
    Perimeter: 525.578979,
    Major_Axis_Length: 229.749878,
    Minor_Axis_Length: 85.093788,
    Eccentricity: 0.928882,
    Convex_Area: 15617,
    Extent: 0.572896
};

const osmancikSample = {
    Area: 13447,
    Perimeter: 455.648010,
    Major_Axis_Length: 183.957581,
    Minor_Axis_Length: 94.458138,
    Eccentricity: 0.858103,
    Convex_Area: 13867,
    Extent: 0.625908
};

function setJson(data) {
    jsonInput.value = JSON.stringify(data, null, 2);

    jsonStatus.textContent = "Valid JSON sample loaded";
    jsonStatus.className = "json-status valid";

    errorBox.classList.add("hidden");

    // Reset result area
    resultEmpty.classList.remove("hidden");
    resultContent.classList.add("hidden");
}

document.getElementById("cammeoBtn").onclick = function () {
    setJson(cammeoSample);
};

document.getElementById("osmancikBtn").onclick = function () {
    setJson(osmancikSample);
};

document.getElementById("clearBtn").onclick = function () {
    jsonInput.value = "";

    jsonStatus.textContent = "Enter a JSON request";
    jsonStatus.className = "json-status";

    errorBox.classList.add("hidden");

    resultEmpty.classList.remove("hidden");
    resultContent.classList.add("hidden");
};

predictBtn.onclick = async function () {

    errorBox.classList.add("hidden");

    let data;

    // -------------------------
    // STEP 1: Check JSON
    // -------------------------

    try {

        data = JSON.parse(jsonInput.value);

        jsonStatus.textContent = "Valid JSON format";
        jsonStatus.className = "json-status valid";

    } catch (error) {

        jsonStatus.textContent = "Invalid JSON format";
        jsonStatus.className = "json-status invalid";

        errorBox.textContent =
            "Request rejected: Invalid JSON format.";

        errorBox.classList.remove("hidden");

        return;
    }

    // -------------------------
    // STEP 2: Send request
    // -------------------------

    predictBtn.disabled = true;

    predictBtn.querySelector("span:first-child").textContent =
        "Processing...";

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });

        const body = await response.json();

        // Show API response
        responseBody.textContent =
            JSON.stringify(body, null, 2);

        // -------------------------
        // SUCCESS
        // -------------------------

        if (response.ok) {

            statusCode.textContent =
                `${response.status} OK`;

            statusCode.className =
                "status-code success";

            prediction.textContent =
                body.prediction;

            resultEmpty.classList.add("hidden");

            resultContent.classList.remove("hidden");

            errorBox.classList.add("hidden");

        }

        // -------------------------
        // VALIDATION FAILURE
        // -------------------------

        else {

            statusCode.textContent =
                `${response.status} Rejected`;

            statusCode.className =
                "status-code danger";

            prediction.textContent =
                "Rejected";

            resultEmpty.classList.add("hidden");

            resultContent.classList.remove("hidden");

            let detail = "Invalid input";

            if (Array.isArray(body.detail)) {

                detail = body.detail
                    .map(item => item.msg)
                    .join(", ");

            } else if (body.detail) {

                detail = body.detail;

            }

            errorBox.textContent =
                "Request rejected: " + detail;

            errorBox.classList.remove("hidden");

        }

    } catch (error) {

        statusCode.textContent =
            "Connection Error";

        statusCode.className =
            "status-code danger";

        prediction.textContent =
            "Error";

        resultEmpty.classList.add("hidden");

        resultContent.classList.remove("hidden");

        responseBody.textContent =
            JSON.stringify({
                error: "Could not connect to API"
            }, null, 2);

        errorBox.textContent =
            "Could not connect to the prediction API.";

        errorBox.classList.remove("hidden");

    } finally {

        predictBtn.disabled = false;

        predictBtn.querySelector("span:first-child").textContent =
            "Run Secure Prediction";

    }
};