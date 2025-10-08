// Animated Greeting System with Rotating Motivational Quotes

// Motivational quotes array
const motivationalQuotes = [];

// Time-based greetings
const greetings = [
    "Good Morning,",
    "Good Afternoon,",
    "Good Evening,",
    "Good to See You,",
    "Great to Have You,"
];

// Current quote index
let currentQuoteIndex = 0;

// Typing animation state
let typingTimeout = null;

/**
 * Get time-appropriate greeting
 */
function getTimeBasedGreeting() {
    const hour = new Date().getHours();

    if (hour >= 5 && hour < 12) {
        return greetings[0]; // Good Morning
    } else if (hour >= 12 && hour < 17) {
        return greetings[1]; // Good Afternoon
    } else if (hour >= 17 && hour < 22) {
        return greetings[2]; // Good Evening
    } else {
        // Randomly choose between "Good to See You" or "Great to Have You" for late night/early morning
        return Math.random() < 0.5 ? greetings[3] : greetings[4];
    }
}

/**
 * Load motivational quotes from server
 */
async function loadMotivationalQuotes() {
    try {
        const response = await fetch('/api/motivational-quotes');
        if (response.ok) {
            const quotes = await response.json();
            motivationalQuotes.length = 0; // Clear array
            motivationalQuotes.push(...quotes);
            // Shuffle quotes for variety
            shuffleArray(motivationalQuotes);
            console.log('Loaded', motivationalQuotes.length, 'motivational quotes');
        } else {
            console.error('Failed to load motivational quotes, status:', response.status);
        }
    } catch (error) {
        console.error('Error loading motivational quotes:', error);
    }
}

/**
 * Shuffle array in place
 */
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

/**
 * Typing animation effect
 */
function typeText(element, text, speed = 50) {
    return new Promise((resolve) => {
        element.textContent = '';
        element.style.opacity = '1';
        element.classList.add('typing');
        let i = 0;

        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                typingTimeout = setTimeout(type, speed);
            } else {
                // Remove typing class to hide cursor
                setTimeout(() => {
                    element.classList.remove('typing');
                    resolve();
                }, 500);
            }
        }

        type();
    });
}

/**
 * Fade in animation
 */
function fadeIn(element, duration = 500) {
    return new Promise((resolve) => {
        element.style.opacity = '0';
        element.style.transition = `opacity ${duration}ms ease-in`;

        requestAnimationFrame(() => {
            element.style.opacity = '1';
        });

        setTimeout(resolve, duration);
    });
}

/**
 * Fade out animation
 */
function fadeOut(element, duration = 500) {
    return new Promise((resolve) => {
        element.style.transition = `opacity ${duration}ms ease-out`;
        element.style.opacity = '0';
        setTimeout(resolve, duration);
    });
}

/**
 * Initialize greeting system
 */
async function initGreetingSystem() {
    try {
        // Get greeting elements first
        const greetingElement = document.getElementById('animatedGreeting');
        const nameElement = document.getElementById('highlightedName');
        const quoteElement = document.getElementById('rotatingQuote');

        if (!greetingElement || !nameElement || !quoteElement) {
            console.error('Greeting elements not found');
            return;
        }

        // Load quotes - MUST complete before continuing
        await loadMotivationalQuotes();

        // Get user info - display only name without role
        const user = auth.getUser();
        let userName = 'Guest';

        if (user) {
            // Use full_name or username, remove any role indicators
            userName = (user.full_name || user.username).replace(/\s*\([^)]*\)\s*/g, '').trim();
        }

        // Set the name immediately with color animation
        nameElement.textContent = userName;
        nameElement.classList.add('animated-color-name');

        // Animate the greeting text with typing effect
        const greeting = getTimeBasedGreeting();
        await typeText(greetingElement, greeting, 50);

        // Show the name with fade-in
        await fadeIn(nameElement, 400);

        // Add blinking cursor after exclamation mark
        setTimeout(() => {
            nameElement.classList.add('show-cursor');
        }, 500);

        // GUARANTEE quotes display - with fallback
        if (motivationalQuotes.length === 0) {
            // Fallback quotes if API fails
            motivationalQuotes.push({
                id: 1,
                text: "Success doesn't come from what you do occasionally. It comes from what you do consistently.",
                author: "Marie Forleo"
            });
        }

        // Display first quote immediately
        await rotateQuote();

        // Rotate every 3 minutes (180000ms)
        setInterval(rotateQuote, 180000);

        console.log('Greeting system initialized successfully with', motivationalQuotes.length, 'quotes');
    } catch (error) {
        console.error('Error initializing greeting system:', error);
        // Even if there's an error, try to display something
        const quoteElement = document.getElementById('rotatingQuote');
        if (quoteElement) {
            quoteElement.innerHTML = '<span class="quote-text">"Great things never come from comfort zones."</span>';
            quoteElement.style.opacity = '1';
        }
    }
}

/**
 * Rotate to next quote with typing animation
 */
async function rotateQuote() {
    const quoteElement = document.getElementById('rotatingQuote');
    if (!quoteElement) {
        console.error('Quote element not found');
        return;
    }

    if (motivationalQuotes.length === 0) {
        console.error('No quotes available');
        return;
    }

    // Fade out current quote if it has content
    if (quoteElement.innerHTML.trim()) {
        await fadeOut(quoteElement, 200);
    }

    // Get next quote
    const quote = motivationalQuotes[currentQuoteIndex];
    currentQuoteIndex = (currentQuoteIndex + 1) % motivationalQuotes.length;

    // Create elements for typing animation
    quoteElement.innerHTML = `
        <span class="quote-text" id="quoteText"></span>
        ${quote.author ? `<span class="quote-author">— ${quote.author}</span>` : ''}
    `;

    // Show container
    quoteElement.style.opacity = '1';

    // Type the quote text with animation
    const quoteTextElement = document.getElementById('quoteText');
    if (quoteTextElement) {
        await typeText(quoteTextElement, `"${quote.text}"`, 30);
    }

    console.log('Displayed quote:', quote.text.substring(0, 50) + '...');
}

/**
 * Update greeting periodically (e.g., when time of day changes)
 */
function updateGreeting() {
    const greetingElement = document.getElementById('animatedGreeting');
    if (!greetingElement) return;

    const newGreeting = getTimeBasedGreeting();
    if (greetingElement.textContent !== newGreeting) {
        typeText(greetingElement, newGreeting, 60);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Small delay to ensure auth system is ready
    setTimeout(initGreetingSystem, 100);

    // Update greeting every hour
    setInterval(updateGreeting, 3600000);
});

// Export functions for external use
window.greetingSystem = {
    init: initGreetingSystem,
    rotateQuote: rotateQuote,
    updateGreeting: updateGreeting
};
