// Wait for the DOM to be fully loaded before running scripts
document.addEventListener('DOMContentLoaded', function() {
    
    console.log("Mentilink JS loaded successfully.");

    // --- Smooth Fade-In Animation for Cards and Forms ---
    // Select all elements you want to animate
    const elementsToAnimate = document.querySelectorAll('.card, .hero-section');

    // Create an observer
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add the 'visible' class when the element comes into view
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1 // Trigger when 10% of the element is visible
    });

    // Observe each element
    elementsToAnimate.forEach(element => {
        observer.observe(element);
    });

});