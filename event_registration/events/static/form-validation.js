document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("forma");

    forma.addEventListener("submit", function(event) {
        let isValid = true;
        const titleInput = document.getElementById("eventTitle");
        const dateInput = document.getElementById("eventDate");
        const descriptionInput = document.getElementById("eventDescription");
        const photoInput = document.getElementById("eventImage");
        const photoDescriptionInput = document.getElementById("photoDescription");

        clearErrors();

        if (titleInput.value.trim() === "") {
            isValid = false;
            showError(titleInput, "Название мероприятия обязательно");
        }

        if (dateInput.value.trim() === "") {
            isValid = false;
            showError(dateInput, "Дата мероприятия обязательна");
        }

        if (descriptionInput.value.trim() === "") {
            isValid = false;
            showError(descriptionInput, "Описание мероприятия обязательно");
        }

        if (photoInput.files.length === 0) {
            isValid = false;
            showError(photoInput, "Пожалуйста, выберите фото");
        }

        if (photoDescriptionInput.value.length > 255) {
            isValid = false;
            showError(photoDescriptionInput, "Описание фото должно быть меньше 256 символов");
        }

        if (!isValid) {
            event.preventDefault();
        }
    });

    function showError(input, message) {
        const errorMessage = document.createElement("div");
        errorMessage.className = "error-message";
        errorMessage.textContent = message;
        input.parentNode.insertBefore(errorMessage, input.nextSibling);
    }

    function clearErrors() {
        const errorMessages = document.querySelectorAll(".error-message");
        errorMessages.forEach(function(message) {
            message.remove();
        });
    }
});