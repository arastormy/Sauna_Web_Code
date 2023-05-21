// タブを開く
function openTab(evt, tabName) {
    // タブコンテンツを非表示にする
    let i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    
    // タブボタンに「active」クラスを削除する
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    // クリックしたタブのコンテンツを表示し、そのタブボタンに「active」クラスを追加する
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// 最初のタブを開く
document.getElementById("defaultOpen").click();


// テーブルを初期化
let table = $('#myTable').DataTable({
    lengthMenu: [[100], [100]],
    bLengthChange: false,
    info: false,
    data: data,
    order: [[7, 'asc']],
    columns: [
        { data: "名称" },
        { data: "サウナ温度" },
        { data: "水風呂温度" },
        { data: "外気浴" },
        { data: "ロウリュ" },
        { data: "料金" },
        { data: "サ活" },
        { data: "県名" }
    ],
    autoWidth: false
});

// サウナ温度フィルター
$('#sauna-form').on('submit', function(event) {
    event.preventDefault();
    table.draw();
});

$.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    // フィルター条件を取得
    let minSauna = parseInt($('#min-sauna').val()) || 0;
    let maxSauna = parseInt($('#max-sauna').val()) || 100;

    // 年齢を取得
    let sauna = parseInt(data[1]);

    // フィルター条件に合致する場合は検索対象とする
    if ($('#min-sauna').val() === "" && $('#max-sauna').val() === "") {
        return true;
    } else {
        return (sauna >= minSauna && sauna <= maxSauna);
    }
});

// サウナ温度フィルターのリセット
$('#reset-sauna-filter').on('click', function() {
    $('#min-sauna').val(''); // 最小値をクリア
    $('#max-sauna').val(''); // 最大値をクリア
    table.draw(); // テーブルを再描画
});

// 水風呂温度フィルター
$('#mizuburo-form').on('submit', function(event) {
    event.preventDefault();
    table.draw();
});

$.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    // フィルター条件を取得
    let minMizuburo = parseInt($('#min-mizuburo').val()) || 0;
    let maxMizuburo = parseInt($('#max-mizuburo').val()) || 100;

    // 水風呂温度を取得
    let mizuburo = parseInt(data[2]);

    // フィルター条件に合致する場合は検索対象とする
    if ($('#min-mizuburo').val() === "" && $('#max-mizuburo').val() === "") {
        return true;
    } else {
        return (mizuburo >= minMizuburo && mizuburo <= maxMizuburo);
    }
});

// 水風呂温度フィルターのリセット
$('#reset-mizuburo-filter').on('click', function() {
    $('#min-mizuburo').val(''); // 最小値をクリア
    $('#max-mizuburo').val(''); // 最大値をクリア
    table.draw(); // テーブルを再描画
});


// 料金フィルター
$('#price-form').on('submit', function(event) {
    event.preventDefault();
    table.draw();
});

$.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    // フィルター条件を取得
    let minPrice = parseInt($('#min-price').val()) || 0;
    let maxPrice = parseInt($('#max-price').val()) || 100;

    // 料金を取得
    let price = parseInt(data[5]);

    // フィルター条件に合致する場合は検索対象とする
    if ($('#min-price').val() === "" && $('#max-price').val() === "") {
        return true;
    } else {
        return (price >= minPrice && price <= maxPrice);
    }
});

// 料金フィルターのリセット
$('#reset-price-filter').on('click', function() {
    $('#min-price').val(''); // 最小値をクリア
    $('#max-price').val(''); // 最大値をクリア
    table.draw(); // テーブルを再描画
});

// 外気浴フィルター
$('#gaikiyoku-form').on('submit', function(event) {
    event.preventDefault();
    table.draw();
});

$.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    // フィルター条件を取得
    let gaikiyokuFilter = $('input[name=gaikiyoku-filter]:checked').val();
    
    // フィルター条件が未設定の場合は検索対象とする
    if (!gaikiyokuFilter) {
        return true;
    }

    // 外気浴を取得
    let gaikiyoku = data[3];

    // フィルター条件に合致する場合は検索対象とする
    if (gaikiyokuFilter === gaikiyoku) {
        return true;
    }

    // それ以外の場合は検索対象としない
    return false;
});

// 外気浴フィルターのリセット
$("#reset-gaikiyoku-filter").click(function(){
    $('input[name="gaikiyoku-filter"]').prop("checked", false);
    table.draw();
});

// ロウリュフィルター
$('#louly-form').on('submit', function(event) {
    event.preventDefault();
    table.draw();
});

$.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    // フィルター条件を取得
    let loulyFilter = $('input[name=louly-filter]:checked').val();
    
    // フィルター条件が未設定の場合は検索対象とする
    if (!loulyFilter) {
        return true;
    }

    // ロウリュを取得
    let louly = data[4];

    // フィルター条件に合致する場合は検索対象とする
    if (loulyFilter === louly) {
        return true;
    }

    // それ以外の場合は検索対象としない
    return false;
});

// ロウリュフィルターのリセット
$("#reset-louly-filter").click(function(){
    $('input[name="louly-filter"]').prop("checked", false);
    table.draw();
});

// 県名フィルター
$('#location-form').on('submit', function(event) {
    event.preventDefault();
    table.draw();
});
$.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
    let locationFilters = $('input[name="location"]:checked').map(function() {
        return $(this).val();
    }).get();
    if (locationFilters.length === 0) {
        return true;
    }
    let location = data[7];
    return locationFilters.includes(location);
});

// 県名フィルターのリセット
$('#reset-location-filter').on('click', function() {
    $('input[name="location"]').prop('checked', false); // チェックを外す
    table.draw(); // テーブルを再描画
});

// ページロード時にフィルタリングを実行
table.draw();

  