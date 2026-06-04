document.addEventListener('DOMContentLoaded', () => {
    const albumCards = document.querySelectorAll('.album-card');

    albumCards.forEach(card => {
        card.addEventListener('click', () => {
            const selectedEra = card.getAttribute('data-era');
            document.body.setAttribute('data-theme', selectedEra);
            console.log(`Switched to Taylor's Era: ${selectedEra}`);
        });
    });
});