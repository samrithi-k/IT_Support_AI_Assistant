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

const context =
    document.getElementById("context");

const ticketId =
    document.getElementById("ticket-id");

const characterCount =
    document.getElementById("character-count");


questionInput.addEventListener(
    "input",
    () => {

        characterCount.textContent =
            `${questionInput.value.length} / 1000`;

    }
);


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


        if (question.length < 5) {

            errorMessage.textContent =
                "Please enter a technical support question with at least 5 characters.";

            errorMessage.classList.remove(
                "hidden"
            );

            return;
        }


        submitButton.disabled = true;

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
                    "Unable to process the request."
                );

            }


            answer.textContent =
                data.answer;


            context.textContent =
                data.retrieved_context;


            ticketId.textContent =
                `Ticket #${data.ticket_id}`;


            result.classList.remove(
                "hidden"
            );


        } catch (error) {

            errorMessage.textContent =
                error.message ||
                "Something went wrong. Please try again.";


            errorMessage.classList.remove(
                "hidden"
            );


        } finally {

            loading.classList.add(
                "hidden"
            );

            submitButton.disabled = false;

        }

    }
);