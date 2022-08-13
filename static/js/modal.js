const getStartedBtn = document.querySelector('.getstarted');
const signInBtn = document.querySelector('.signin-btn');
const modal = document.querySelector('.signup-modal');
const signInModal = document.querySelector('.signin-modal');
const closebtn = document.querySelector('.btn-close');
const closeSignInBtn = document.querySelector('.close-signin');

// eventlistener
getStartedBtn.addEventListener('click', displayModal)
signInBtn.addEventListener('click', displaySignInModal)

closebtn.addEventListener('click', closeModal)
closeSignInBtn.addEventListener('click', closeSignInModal)



function displayModal(e) {
    modal.style.display = 'block'
    
    e.preventDefault()
}
function displaySignInModal(e) {
    signInModal.style.display = 'block'
    
    e.preventDefault()
}

function closeModal (e) {
    modal.style.display = 'none'

    e.preventDefault()
}

function closeSignInModal (e) {
    signInModal.style.display = 'none'

    e.preventDefault()
}
