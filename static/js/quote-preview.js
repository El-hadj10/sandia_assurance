function initQuotePreview() {
    const nameField = document.querySelector("#name");
    const ageField = document.querySelector("#age");
    const typeField = document.querySelector("#vehicle_type");
    const coverageField = document.querySelector("#coverage");
    const previewName = document.querySelector("#preview-name");
    const previewAge = document.querySelector("#preview-age");
    const previewType = document.querySelector("#preview-type");
    const previewCoverage = document.querySelector("#preview-coverage");
    const previewPrice = document.querySelector("#preview-price");

    if (!nameField || !ageField || !typeField || !coverageField || !previewName) {
        return;
    }

    const computePrice = () => {
        const name = nameField.value || "Client";
        const age = parseInt(ageField.value, 10) || 25;
        const vehicleType = typeField.value;
        const coverage = coverageField.value;

        let basePrice = 240;
        if (vehicleType === "moto") basePrice = 210;
        if (vehicleType === "habitation") basePrice = 190;
        if (vehicleType === "sante") basePrice = 220;

        const ageFactor = age < 25 ? 1.45 : 1.0;
        const coverageFactor = coverage === "standard" ? 1.0 : 1.4;
        const totalPrice = Math.round(basePrice * ageFactor * coverageFactor * 100) / 100;

        previewName.textContent = name;
        previewAge.textContent = age;
        previewType.textContent = vehicleType;
        previewCoverage.textContent = coverage;
        previewPrice.textContent = `${totalPrice.toFixed(2)} €`;
    };

    [nameField, ageField, typeField, coverageField].forEach((input) => {
        input.addEventListener("input", computePrice);
        input.addEventListener("change", computePrice);
    });

    computePrice();
}