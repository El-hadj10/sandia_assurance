function initServicePreview() {
    const serviceCards = document.querySelectorAll(".service-card[data-title]");
    const previewTitle = document.querySelector("#service-preview-title");
    const previewDescription = document.querySelector("#service-preview-description");
    const previewImage = document.querySelector("#service-preview-image");

    if (!serviceCards.length || !previewTitle || !previewDescription || !previewImage) {
        return;
    }

    const updatePreview = (card) => {
        const title = card.dataset.title;
        const description = card.dataset.description;
        const image = card.dataset.img;

        previewTitle.textContent = title;
        previewDescription.textContent = description;
        previewImage.src = image;
        previewImage.alt = title;

        serviceCards.forEach((item) => item.classList.toggle("selected", item === card));
    };

    serviceCards.forEach((card) => {
        card.addEventListener("click", () => updatePreview(card));
    });

    updatePreview(serviceCards[0]);
}