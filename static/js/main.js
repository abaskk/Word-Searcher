// axios and send request to python backend
// 3 pieces of data: grid, words, image
const solver = document.getElementById('solver-btn')


checkValid = (wordsElem,heightElem,widthElem,imgElem) =>{
    let errorIndicate = {
        searchWords: "",
        height: "",
        width: "",
        img: "",
        valid: true
    }

    let heightAsNum = parseInt(heightElem.value);
    let widthAsNum = parseInt(widthElem.value);
    console.log(heightAsNum);

    if(!(imgElem.files[0])){
        errorIndicate.valid = false;
        errorIndicate.img = "Enter a valid Image";
    }

    if(Number.isInteger(heightAsNum) === false || heightAsNum <= 0){
        errorIndicate.valid = false;
        errorIndicate.height = "Enter height as a valid integer";

    }

    if(Number.isInteger(widthAsNum) === false || widthAsNum <= 0){
        errorIndicate.valid = false;
        errorIndicate.width = "Enter width as a valid integer";
        
    }

    if(!(wordsElem.value) || /^\s*$/.test(wordsElem.value) === true){
        errorIndicate.valid = false;
        errorIndicate.searchWords = "Please enter some words";
        
    }
    return errorIndicate;
    
};

errorRender = (errorObj) =>{
    let errorDiv = document.getElementById('errors');
    errorDiv.style.display = "block";
    for(let prop in errorObj){
        if(!(typeof errorObj[prop] == "boolean")){
            let errorMsg = "<p class = 'my-0 text-danger'>"+errorObj[prop]+"</p>";
            errorDiv.innerHTML += errorMsg;
        }
    }

    setTimeout(()=>{
        errorDiv.innerHTML = '';
    }, 2000);


};


spinnerShow = () =>{
    const solver = document.getElementById("solver-btn");
    const spinner = document.createElement('span');

    solver.innerHTML = '';
    spinner.setAttribute("id", "reqSpinner");
    spinner.setAttribute("class", "spinner-border spinner-border-sm");
    solver.appendChild(spinner)
    solver.disabled = true;
}

spinnerHide = () =>{
    const solver = document.getElementById("solver-btn");
    document.getElementById("reqSpinner").remove();
    solver.disabled = false;
    solver.innerHTML = 'Solve'

}


sendRequest = (obj) =>{
    spinnerShow()
    let jsonObj = JSON.stringify(obj);
    const xhr = new XMLHttpRequest();
    let url = "http://127.0.0.1:5000/solve_search";
    //let url = "https://word-searcher.herokuapp.com/solve_search"
    xhr.open("POST",url);
    xhr.onload = (e) => {
        spinnerHide()
        console.log("sent")
        let imSrc = `data:image/jpg;base64, ${xhr.responseText}`  
        console.log(imSrc);
        const searchWords = document.getElementById('solved-crossword-view');
        searchWords.src = imSrc;
        
    };
    xhr.onerror= function(e) {
        alert("Backend servers are down, try again later");
        spinnerHide()
    };
    xhr.send(jsonObj);
};

solver.addEventListener("click", () => {
    const searchWords = document.getElementById('search-words');
    const imgDrop = document.getElementById('crossword-upload');
    const gridHeight = document.getElementById('g-height');
    const gridWidth = document.getElementById('g-width');
    const gridOutline = document.getElementById("g-outline").checked
    let validity = checkValid(searchWords,gridHeight,gridWidth,imgDrop);
    if(validity.valid === false){
        errorRender(validity);   
    }else{
        let reader = new FileReader();
        let encodedImg = "";
        reader.onload = (e) =>{
            encodedImg = e.target.result;
            let reqObj = {
                gHeight: parseInt(gridHeight.value),
                gWidth: parseInt(gridWidth.value),
                gOutline: gridOutline,
                search: searchWords.value.split(","),
                img : encodedImg
            };

            sendRequest(reqObj)
        }
        reader.readAsDataURL(imgDrop.files[0]);
    }
});

