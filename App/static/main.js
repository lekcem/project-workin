
async function getUserData(){
    const response = await fetch('/api/users');
    return response.json();
}

function loadTable(users){
    const table = document.querySelector('#result');
    for(let user of users){
        table.innerHTML += `<tr>
            <td>${user.id}</td>
            <td>${user.username}</td>
        </tr>`;
    }
}


async function getUserData2(){
    const response = await fetch('/api/reports');
    return response.json();
}

function loadTable2(reports){
    const table = document.querySelector('#result2');
    for(let report of reports){
        table.innerHTML += `<tr>
            <td>${report.id}</td>
            <td>${report.year}</td>
            <td>${report.campus}</td>
            <td>${report.excelfile}</td>
        </tr>`;
    }
}

async function main(){
    const users = await getUserData();
    loadTable(users);
    const reports = await getUserData2();
    loadTable2(reports);
}


main();