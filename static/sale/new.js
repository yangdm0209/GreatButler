var products=[]
var productItem = '<tr><td class="hidden">-1</td><td class="select-product">请选择产品</td><td class="editable-num">输入数量</td><td class="editable-price">输入价格</td><td class="editable-scale">1</td><td><a onclick="insertTr(this);" ><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></a><a onclick="deleteTr(this);"><span class="glyphicon glyphicon-minus" aria-hidden="true"></span></a></td></tr>';

function getProductPrice(index){
    for (item in products){
        if (products[item].id==index){
        return products[item].price
        }
    }
    return ''
}

function makeEditable(){
    $('.select-product').editable({
        type: 'select',
        mode: 'inline',
        url: '',
        title: '选择产品',
        source: function () {
            var result=[];
            for (item in products){
                result.push({ value: products[item].id, text: products[item].name });
            }
            return result;
        },
        success: function(response, newValue) {
            var price = getProductPrice(newValue);
            this.parentNode.children[0].innerText=newValue;
            this.parentNode.children[3].innerText=1;
            this.parentNode.children[4].innerText=price;
            updateTotal();
        }
    });
    $('.editable-num').editable({
        type: 'text',
        mode: 'inline',
        url: '',
        title: '修改数量',
        success: function(response, newValue) {
            this.innerText = newValue;
            updateTotal();
        }
    });
    $('.editable-price').editable({
        type: 'text',
        mode: 'inline',
        url: '',
        title: '修改价格',
        success: function(response, newValue) {
            this.innerText = newValue;
            updateTotal();
        }
    });
    $('.editable-scale').editable({
        type: 'text',
        mode: 'inline',
        url: '',
        title: '修改折扣',
        success: function(response, newValue) {
            if (newValue >= 0.1 && newValue <= 1){
                this.innerText = newValue;
                updateTotal();
            }
            else {
                return '折扣率必须为0.1到1之间';
            }
        }
    });
}

function getAllProduct(){
    $.get("/product/list/",function(data,status){
        products=data.data
        makeEditable()
    });
}

//当前行后插入一行
function insertTr(nowTr){
    $(nowTr).parent().parent().after(productItem);
    makeEditable();
}
//删除当前行
function deleteTr(nowTr){
    $(nowTr).parent().parent().remove();
    updateTotal();
}

// 统计总数
function updateTotal(){
    var trList = $("tbody").children("tr")
    var totalPro = 0;
    var totalNums = 0;
    var totalPrice = 0;
    var items=[];

    for (var i=0;i<trList.length;i++) {
        var tdArr = trList.eq(i).find("td");
        var proId = tdArr.eq(0).text();
        if (proId > 0){
            totalPro += 1;
            totalNums += parseInt(tdArr.eq(2).text());
            totalPrice += tdArr.eq(2).text() * tdArr.eq(3).text()*tdArr.eq(4).text();

            items.push({pid: proId, pnum:tdArr.eq(2).text(), pprice:tdArr.eq(3).text(), pscale:tdArr.eq(4).text()});
        }
    }
    $("#totalPros").text(totalPro);
    $("#totalNums").text(totalNums);
    $("#totalPrice").text(totalPrice);
    if (totalPrice > 0){
        $("#submit").removeClass("disabled")
    }
    return items
}

function submit(){
    var detail = updateTotal();
    var stock = $('#stock').find("option:selected").attr('data-index');
    var supporter = $('#supporter').find("option:selected").attr('data-index');
    if (detail.length == 0){
        alert('还没有选择商品');
        return;
    }

    $.post("/sale/new/",
    {
        data:JSON.stringify({stock:stock,
                             supporter:supporter,
                             detail: detail}),
        csrfmiddlewaretoken:$("input[name='csrfmiddlewaretoken']") .val()
    },
    function(data,status){
        if (data.msg=="success"){
            alert(data.data)
            location.reload();
        }
        else{
            alert(data.data)
        }
    });
}
getAllProduct();
$("tbody").html(productItem);