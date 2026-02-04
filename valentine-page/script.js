const noButton = document.getElementById('noBtn');
const yesButton = document.querySelector('.yes');
let avoidX = 0;
let avoidY = 0;

function moveNoButton() {
  const btnRect = noButton.getBoundingClientRect();
  const parentRect = noButton.parentElement.getBoundingClientRect();
  const offsetX = Math.random() * (parentRect.width - btnRect.width) - btnRect.left + parentRect.left;
  const offsetY = Math.random() * (parentRect.height - btnRect.height) - btnRect.top + parentRect.top;
  const translateX = (Math.random() > 0.5 ? 1 : -1) * (Math.random() * 120 + 20);
  const translateY = (Math.random() > 0.5 ? 1 : -1) * (Math.random() * 80 + 10);
  noButton.style.transform = `translate(${translateX}px, ${translateY}px)`;
}

noButton.addEventListener('mouseenter', moveNoButton);
noButton.addEventListener('focus', moveNoButton);

yesButton.addEventListener('click', () => {
  yesButton.textContent = 'Forever ❤️';
  // simple confetti
  const backgroundImagePath = './us1.jpg';
  const canvas = document.getElementById('confetti');
  const card = document.querySelector('.card');
  const intro  = document.querySelector('.intro');
  if (canvas.getContext) {
    card.style.backgroundImage = `url("${backgroundImagePath}")`;
    intro.style.visibility = 'hidden';
    // Resize the background to fit the card.
    // Use 'cover' to fill the card (may crop) or 'contain' to fit fully (may letterbox).
    card.style.backgroundSize = 'cover';
    card.style.backgroundPosition = 'center';
    card.style.backgroundRepeat = 'no-repeat';
    // canvas.style.backgroundSize = 'cover';
    // canvas.style.backgroundPosition = 'center';
    // canvas.style.backgroundRepeat = 'no-repeat';
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < 80; i += 1) {
      ctx.fillStyle = `hsl(${Math.random() * 60 + 330}, 80%, 65%)`;
      const x = Math.random() * canvas.width;
      const y = Math.random() * canvas.height;
      const size = Math.random() * 12 + 4;
      ctx.fillRect(x, y, size, size / 3);
    }
    setTimeout(() => ctx.clearRect(0, 0, canvas.width, canvas.height), 1500);
  }
});
