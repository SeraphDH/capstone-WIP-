function toggleEdit(elementId) {
    var element = document.getElementById(elementId)
    var button = document.getElementById(elementId+"_edit")
    if(element.getAttribute("readonly") == "true") {
        element.removeAttribute("readonly")
        button.textContent = "Cancel"
        button.value = "cancel"
    }
    else{
        element.setAttribute("readonly", "true")
        button.textContent = "Edit"
        button.value = "edit"
    }
    console.log(element)
}