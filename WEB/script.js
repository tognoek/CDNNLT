var searchInput = "tognoek"
const urlApi = "http://localhost:7000"

suggest = document.getElementById("suggest");

hot_destination = document.getElementById("right-suggest");

tours = document.getElementById("tours");

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
document.getElementById("myForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Ngăn chặn form gửi yêu cầu mặc định
    searchInput = document.getElementById("searchInput").value;
    // Gọi API và xử lý dữ liệu
    search(searchInput)
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
        })
        .catch(error => {
            console.error("Error:", error);
        });
});
if (!hasParentTour(document.querySelector('.tours'))) {
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
                    <div>
                        <p>${data[index][1]}</p>
                       <div>
                            <button class="button">
                                <a href="#">Tìm kiếm</a>
                            </button>
                            <button class="button">
                                <a href="${data[index][3]}">Xem chi tiết</a>
                            </button>
                        </div>
                    </div>
                `;
                suggest.appendChild(div);
            }
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
            <div>
                <p>${data[index][3]}</p>
                <div>
                    <button class="button">
                        <a href="#">Tìm kiếm</a>
                    </button>
                    <button  class="button">
                        <a href="${data[index][4]}">Xem chi tiết</a>
                    </button>
                </div>
            `;
            hot_destination.appendChild(div);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });