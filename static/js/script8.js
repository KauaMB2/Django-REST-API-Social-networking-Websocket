const dropdownOptions=document.querySelector(".dropdown-options")
const dropdownButton=document.querySelector(".dropdown-button")
dropdownButton.addEventListener('click',(event)=>{
  dropdownOptions.classList.toggle('show')
})