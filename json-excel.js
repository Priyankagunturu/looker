
const data = [{
    "Segment": "Government",
    "Country": "Canada",
    "Product": "Carretera",
    "Discount": "None",
},
{
    "Segment": "Government",
    "Country": "Germany",
    "Product": "Carretera",
    "Discount": "None",
},
{
    "Segment": "Midmarket",
    "Country": "France",
    "Product": "Carretera",
    "Discount": "None",
}];

const data2 = [{
    "Segment": "public",
    "Country": "US",
    "Product": "JEANS",
    "Discount": "None",
},
{
    "Segment": "Government",
    "Country": "Germany",
    "Product": "Carretera",
    "Discount": "None",
},
{
    "Segment": "Midmarket",
    "Country": "France",
    "Product": "Carretera",
    "Discount": "None",
}];
document.getElementById("json").innerHTML = JSON.stringify(data, undefined, 4);
document.getElementById("json").innerHTML = JSON.stringify(data2, undefined, 4);


const EXCEL_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8';
const EXCEL_EXTENSION = '.xlsx';

console.log(window);

function downloadAsExcel(){
    const worksheet = XLSX.utils.json_to_sheet(data,data2);
    const workbook = {
        Sheets:{
            'data':worksheet,
            'data2': worksheet
        },
        SheetNames:['data','data2']
    };
    const excelBuffer = XLSX.write(workbook,{bookType:'xlsx',type:'array'});
    console.log(excelBuffer);
    saveAsExcel(excelBuffer,'myfile')
}

function saveAsExcel(buffer,filename){
    const data= new Blob([buffer],{type:EXCEL_TYPE});
    saveAs(data,filename+'_export_'+new Date().getTime()+EXCEL_EXTENSION);
}





