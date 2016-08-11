$(document).ready(function () {
    $("#jqxgrid").jqxGrid({ theme: "custom" });
    $("#button").click(function() { pagerFix();}); 
});

function pagerFix() {
    var paginginformation = $('#jqxgrid').jqxGrid('getpaginginformation');
    var curr_page = paginginformation.pagenum
    // $("#jqxgrid").jqxGrid('updatebounddata');
    // // After updatebounddata, grid defaults to page1
    // // goto the current page.
    // $("#jqxgrid").jqxGrid('gotopage', curr_page);
    // fix the column size
    $("#jqxgrid").jqxGrid('autoresizecolumns');
}


function createGraphs(jsonData, lgdfList) {
    // prepare the data

    var data =
    {
        datatype: "json",
        localdata: jsonData,

        datafields: [
            { name: 'time'}
        ],
        id: 'id',
        pagesize: 25,
        pagenum: Math.trunc(jsonData.length/25)+1,
        sortcolumn: 'time',
        sortdirection: 'asc'

    };

    var width=100/(lgdfList.length + 1)
    columns = [
        { text: 'TIME', datafield: 'time', width: width+"%"},
    ]
    
    for (i = 0; i<lgdfList.length; i++) {
        var my_obj = {name: lgdfList[i]}
        data['datafields'].push(my_obj)
        var my_obj = {
            text: lgdfList[i].toUpperCase(),
            datafield: lgdfList[i],
            //width: width+"%",
            // datafield: lgdfList[i],
        }

        columns.push(my_obj)
    }

    // load virtual data.
    // VIRTUAL DATA MUST BE USED OR ELES DATA GETS DISPLAYED WRONG
    var rendergridrows = function (params) {
        var mydata = jsonData;
        return mydata;
    }
    var totalcolumnrenderer = function (row, column, cellvalue) {
        var cellvalue = $.jqx.dataFormat.formatnumber(cellvalue, 'c2');
        return '<span style="margin: 6px 3px; font-size: 12px; float: right; font-weight: bold;">' + cellvalue + '</span>';
    }
    var dataAdapter = new $.jqx.dataAdapter(data);
    $("#jqxgrid").jqxGrid(
        {   
            width: "100%",
            autoheight: true,
            source: dataAdapter,
            columnsresize: true,
            virtualmode: true,
            rendergridrows: rendergridrows,
            selectionmode: 'multiplecellsadvanced',
            pageable: true,
            pagermode: 'simple',
            columns: columns,
          

        }
    );
    $("#jqxgrid").jqxGrid('autoresizecolumns');

   
} 
