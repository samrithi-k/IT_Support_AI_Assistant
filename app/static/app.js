const questionInput =
    document.getElementById("question");

const submitButton =
    document.getElementById("submit-button");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const errorMessage =
    document.getElementById("error-message");

const answer =
    document.getElementById("answer");

const characterCount =
    document.getElementById("character-count");


// Character counter

questionInput.addEventListener(
    "input",
    () => {

        characterCount.textContent =
            `${questionInput.value.length} / 1000`;

    }
);


// Press Enter to submit

questionInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter"
            && !event.shiftKey
        ) {

            event.preventDefault();

            submitButton.click();

        }

    }
);


// Submit question

submitButton.addEventListener(
    "click",
    async () => {

        const question =
            questionInput.value.trim();


        errorMessage.classList.add(
            "hidden"
        );

        result.classList.add(
            "hidden"
        );


        // Validation

        if (question.length < 5) {

            showError(
                "Please describe your technical problem in at least 5 characters."
            );

            return;
        }


        if (question.length > 1000) {

            showError(
                "Your question is too long. Please keep it under 1000 characters."
            );

            return;
        }


        // Loading state

        submitButton.disabled = true;

        submitButton.textContent =
            "Analyzing...";

        loading.classList.remove(
            "hidden"
        );


        try {

            const response =
                await fetch(
                    "/api/ask",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            question: question
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Unable to process your support request."
                );

            }


            // Display ONLY the solution

            answer.textContent =
                data.answer;


            result.classList.remove(
                "hidden"
            );


            // Scroll to solution

            setTimeout(
                () => {

                    result.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                },
                100
            );


        } catch (error) {

            showError(
                error.message ||
                "Something went wrong. Please try again."
            );


        } finally {

            loading.classList.add(
                "hidden"
            );

            submitButton.disabled = false;

            submitButton.textContent =
                "Get Troubleshooting Help";

        }

    }
);


// Error helper

function showError(message) {

    errorMessage.textContent =
        message;

    errorMessage.classList.remove(
        "hidden"
    );

    errorMessage.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}