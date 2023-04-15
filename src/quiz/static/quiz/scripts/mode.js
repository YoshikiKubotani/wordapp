let currentCheckedButton = document.querySelector('.radio-inline__input:checked');
const radioButtons = document.querySelectorAll('.radio-inline__input');
for (const radioButton of radioButtons) {
  radioButton.addEventListener('click', (event) => {
    if (event.target === currentCheckedButton) {
      window.location.href = event.target.dataset.href;
    } else {
      currentCheckedButton = event.target;
    }
  });
}