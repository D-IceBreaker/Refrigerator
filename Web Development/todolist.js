loadEvents();

function loadEvents(){
    document.getElementById('addButton').addEventListener('submit', submit);
    document.querySelector('ul').addEventListener('click', deleteOrCheck);
}

function submit(e){
    if(e) 
        e.preventDefault();
    let input = document.getElementById('taskInput');
    if(input.value != '')
        addTask(input.value);
    input.value = '';
}

function addTask(task){
    let ul = document.querySelector('ul');
    let li = document.createElement('li');
    li.innerHTML = `<input type="checkbox"><label>${task}</label><button class="deleteButton">X</button>`;
    ul.appendChild(li);
    document.querySelector('.taskBoard').style.display = 'block';
  }

function deleteOrCheck(e){
    if(e.target.className == 'deleteButton')
      deleteTask(e);
    else {
      checkTask(e);
    }
  }

function deleteTask(e){
    let remove = e.target.parentNode;
    let parentNode = remove.parentNode;
    parentNode.removeChild(remove);
}

function checkTask(e){
    let tick = e.target.parentNode;
    if(e.target.checked) {
        tick.classList.add("checked");
    } else {
        tick.classList.remove("checked");
    }
}

