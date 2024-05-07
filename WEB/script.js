var searchInput = "tognoek"
const urlApi = "http://localhost:7000"
var textSearch = "Đà Nẵng"
var suggest = document.getElementById("suggest");
var hot_destination = document.getElementById("right-suggest")
var tours = document.getElementById("tours");

function formatTime(chuoi) {
    var index = 0;
    while (index < chuoi.length) {
        var indexN = chuoi.indexOf("N", index);
        if (indexN !== -1) {
            var indexD = chuoi.indexOf("D", indexN + 2);
            if (indexD !== -1) {
                var indexSoN = indexN - 1
                while (!isNaN(parseInt(chuoi[indexSoN]))) {
                    indexSoN--;
                }
                var indexSoD = indexD - 1
                while (!isNaN(parseInt(chuoi[indexSoD]))) {
                    indexSoD--;
                }
                var soD = chuoi.substring(indexSoD + 1, indexD);
                var soN = chuoi.substring(indexSoN + 1, indexN);
                if (indexSoD === indexN && soN.length > 0 && soD.length > 0) {
                    return (soN + " Ngày " + soD + " Đêm");
                }
            }
            index = index + 2;
        }
        else {
            return ("Chưa được cung cấp");
            break;
        }
    }
}
function formatMoney(money) {
    money = money.toString();
    var res = "";
    var count = 0;
    for (var i = money.length - 1; i > -1; i--) {
        if (count === 3) {
            count = 0;
            res = "," + res;
        }
        res = money[i] + res;
        count++;
    }
    return res;
}
function hasParentTour(element) {
    return element.parentNode !== document;
}
async function search(searchInput) {
    try {
        const response = await fetch(urlApi + `/search_tours_list_tour_all/?search_input=${searchInput}`);
        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
}
async function get_suggest() {
    try {
        const response = await fetch(urlApi + `/get_all_data_list_tour`);
        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        return data;
    }
    catch (error) {
        console.error("Error:", error);
        throw error;
    }
}
async function get_hot_destination() {
    try {
        const response = await fetch(urlApi + `/get_all_data_hot_destination`);
        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        return data;
    }
    catch (error) {
        console.error("Error:", error);
        throw error;
    }
}

function tao_item(stringSearch){
    search(stringSearch)
    .then(data => {
        // console.log("Dữ liệu từ API:", data);
        while (tours.firstChild) {
            tours.removeChild(tours.firstChild);
        }
        while (suggest.firstChild) {
            suggest.removeChild(suggest.firstChild);
        }
        for (let index = 0; index < data.length; index++) {
            const li = document.createElement("li");
            li.innerHTML = `
            <div>
                <div class="image">
                    <img src="${data[index][5]}" alt="">
                </div>
                <div class="info">
                    <div class="text1">${data[index][1]}</div>
                    <div class="text2">Mã: ${data[index][8]}</div>
                    <div class="text2">Thời gian: ${formatTime(data[index][8])}</div>
                    <div class="text2">Khởi hành: ${data[index][7]}</div>
                    <div class="text1">
                    ${data[index][4] !== 2904 ? `<div>${formatMoney(data[index][4])}<sup>đ</sup></div>` : `<div>Chưa được cung cấp thông tin</div>`}
                        <button class="button">
                            <a href="${data[index][2]}">Xem chi tiết</a>
                        </button>
                    </div>
                </div>
            </div>
            `;
            tours.appendChild(li);
        };
        timKiem();
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
function isUpperCase(character) {
    return character === character.toUpperCase() &&
           character !== character.toLowerCase() &&
           isNaN(parseInt(character, 10));
}
function get_name_tour(params) {
    params += " tognoek";
    var tachTu = params.split(" ");
    for (var t = 0; t < tachTu.length; t++) {
        if (tachTu[t] == "lịch") {
            var res = "";
            for (var r = t + 1; r < tachTu.length; r++) {
                if (isUpperCase(tachTu[r][0])) {
                    res += tachTu[r] + " ";
                }else{
                    return res.trim();
                }
            }
        }
    }
    return "Đà Nẵng"
}
function timKiem(){
    var list_item = document.getElementsByClassName("item");
    for (var i = 0; i < list_item.length; i++){
        var btn_search = list_item[i].querySelector(".btn_search");
        let textSearch = list_item[i].querySelector(".name").textContent;
        btn_search.addEventListener("click", ()=>{
            console.log(get_name_tour(textSearch));
            tao_item(get_name_tour(textSearch));
        });
    };
}

document.getElementById("myForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Ngăn chặn form gửi yêu cầu mặc định
    searchInput = document.getElementById("searchInput").value;
    tao_item(searchInput)
    
});
if (!hasParentTour(document.querySelector(".tours"))) {
    // console.log("Xin chao")
}
else {
    get_suggest()
        .then(data => {
            while (suggest.firstChild) {
                suggest.removeChild(suggest.firstChild);
            }
            for (let index = 0; index < data.length; index++) {
                const div = document.createElement("div");
                console.log(data[index]);
                div.innerHTML = `
                    <img src="${data[index][2]}" alt="">
                    <div class = "item">
                        <p class = "name">${data[index][1]}</p>
                       <div>
                            <button class="button btn_search">
                                Tìm kiếm
                            </button>
                            <button class="button">
                                <a href="${data[index][3]}">Xem chi tiết</a>
                            </button>
                        </div>
                    </div>
                `;
                suggest.appendChild(div);
            }
            timKiem();
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
get_hot_destination()
    .then(data => {
        console.log(data)
        for (let index = 0; index < data.length; index++) {
            const div = document.createElement("div");
            console.log(data[index]);
            div.innerHTML = `
            <img src="${data[index][2]}" alt="">
            <div class = "item">
                <p class = "name">${data[index][3]}</p>
                <div>
                    <button class="button btn_search">
                        Tìm kiếm
                    </button>
                    <button  class="button">
                        <a href="${data[index][4]}">Xem chi tiết</a>
                    </button>
                </div>
            `;
            hot_destination.appendChild(div);
        }
        timKiem();
    })
    .catch(error => {
        console.error("Error:", error);
    });
