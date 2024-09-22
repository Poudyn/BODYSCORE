const DASHBOARD = `
  <div class="dashboard">
            <div class="title">پنل مدیریت</div>
            <div class="examplebox">
                <div class="exbox">
                    <div class="extitle">
                        <input type="file" class="inputcontent" id="bodyinput"
                            onchange="bexupload()" />
                        نمونه های بدن
                        <div class="uploadex" onclick="uploadex('bex')"><img
                                class="uploadeximg"
                                src="https://img.icons8.com/?size=100&id=60019&format=png&color=2d273b"></div>
                    </div>
                    <div class="excontent" id="bodybox">
                    </div>
                </div>
                <div class="exbox">
                    <div class="extitle">
                        <input type="file" class="inputcontent" id="faceinput"
                            onchange="fexupload()" />
                        نمونه های صورت
                        <div class="uploadex" onclick="uploadex('fex')"><img
                                class="uploadeximg"
                                src="https://img.icons8.com/?size=100&id=60019&format=png&color=2d273b"></div>
                    </div>
                    <div class="excontent" id="facebox">
                    </div>
                </div>
            </div>
            <div class="profilephoto">
                <div class="parttitle">تغییر پروفایل</div>
                <div class="profholder">
                    <img class="profimg" id="profimg"
                        src=HOST + "/static/photos/profile.jpg">
                </div>
                <input type="file" class="inputcontent" id="profinput"
                    onchange="profileuploaded()" />
                <div class="uploadbtn" onclick="uploadprof()"><img
                        class="uploadimg"
                        src="https://img.icons8.com/?size=100&id=60019&format=png&color=fa8072"></div>
            </div>
            <div class="getusers">
                <div class="parttitle">دانلود کاربر ها</div>
                <div class="uploadbtn" onclick="getusers()"><img class="uploadimg"
                        src="https://img.icons8.com/?size=100&id=2945&format=png&color=fa8072"></div>
            </div></div>
`;
const LOGIN = `
            <div class="login">
                <div class="loginbox">
                    <div class="loginboxtitle">ورود</div>
                    <input id="usernamefield" class="txtinput" type="text"
                        placeholder="Username" />
                    <input id="passwordfield" class="txtinput" type="text"
                        placeholder="Password" />
                    <button class="cusbtn" onclick="login()">ورود</button>
                </div>
            </div>`;

const HOST = 'https://31dd-2a01-5ec0-b800-747c-e709-45fc-17cd-3b50.ngrok-free.app'

window.onload = () => {
    console.log(localStorage.getItem("status"))
    if (localStorage.getItem("status") == "dashboard") {
        fetch(HOST + "/status",{
            headers: {
                Authorization: "Bearer " + localStorage.getItem("adtok"),
            },
        }).then(x=>{
            if (x.ok){
                localStorage.setItem("status","dashboard") 
                document.getElementById("container").innerHTML = DASHBOARD
                loadexams()
            }else{
                localStorage.setItem("status","login") 
                document.getElementById("container").innerHTML = LOGIN
            }
        })
    } else {
        document.getElementById("container").innerHTML = LOGIN
    }
};

function login() {
    var username = document.getElementById("usernamefield").value;
    var password = document.getElementById("passwordfield").value;
    var body = JSON.stringify({
        username: username,
        password: password,
    });
    fetch(HOST + "/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: body,
    }).then((x) => {
        if (x.ok) {
            x.json().then((j) => {
                console.log(j.access_token);
                localStorage.setItem("adtok", j.access_token);
                localStorage.setItem("status", "dashboard");
                document.getElementById("container").innerHTML = DASHBOARD;
                loadexams();
            });
        }
    });
}

function uploadprof() {
    document.getElementById("profinput").click();
}

function getRandom() {
    return Math.floor(Math.random() * 200);
}

function uploadex(part) {
    if (part == "bex") {
        document.getElementById("bodyinput").click();
    } else {
        document.getElementById("faceinput").click();
    }
}

function bexupload() {
    console.log("uploaded");
    var image = document.getElementById("bodyinput").files[0];
    var reader = new FileReader();
    reader.onload = async function (e) {
        var formData = new FormData();
        formData.append("image", image);
        const xhr = new XMLHttpRequest();
        xhr.onload = function () {
            if (xhr.status == 200) {
                loadexams();
            }
        };
        xhr.open("POST", HOST + "/set/bex");
        xhr.setRequestHeader(
            "Authorization",
            "Bearer " + localStorage.getItem("adtok")
        );
        xhr.send(formData);
    };
    reader.readAsDataURL(image);
}

function fexupload() {
    console.log("uploaded");
    var image = document.getElementById("faceinput").files[0];
    var reader = new FileReader();
    reader.onload = async function (e) {
        var formData = new FormData();
        formData.append("image", image);
        const xhr = new XMLHttpRequest();
        xhr.onload = function () {
            if (xhr.status == 200) {
                loadexams();
            }
        };
        xhr.open("POST", HOST + "/set/fex");
        xhr.setRequestHeader(
            "Authorization",
            "Bearer " + localStorage.getItem("adtok")
        );
        xhr.send(formData);
    };
    reader.readAsDataURL(image);
}

function profileuploaded() {
    console.log("uploaded");
    var image = document.getElementById("profinput").files[0];
    var reader = new FileReader();
    reader.onload = async function (e) {
        var formData = new FormData();
        formData.append("image", image);
        const xhr = new XMLHttpRequest();
        xhr.onload = function () {
            if (xhr.status == 200) {
                document.getElementById("profimg").src =
                    HOST + "/static/photos/profile.jpg?v=" +
                    String(getRandom());
            }
        };
        xhr.open("POST", HOST + "/set/profile");
        xhr.setRequestHeader(
            "Authorization",
            "Bearer " + localStorage.getItem("adtok")
        );
        xhr.send(formData);
    };
    reader.readAsDataURL(image);
}

function createImgBox(url, part, filename) {
    return `
                <div class="boximage">
                    <img class="img" src=${url}>
                    <div class="rembox" onclick="remex('${part}','${filename}')">
                        <img class="remimg" src="https://img.icons8.com/?size=100&id=78581&format=png&color=fa8072">
                    </div>
                </div>
`;
}

function loadexams() {
    var fbox = document.getElementById("facebox");
    var bbox = document.getElementById("bodybox");
    fbox.innerHTML = "";
    bbox.innerHTML = "";
    fetch(HOST + "/fex").then((x) =>
        x.json().then((j) => {
            j.files.forEach((filename) => {
                var url = HOST + "/static/photos/faceex/" + filename;
                var imgbox = createImgBox(url, "fex", filename);
                fbox.insertAdjacentHTML("beforeend", imgbox);
            });
        })
    );

    fetch(HOST + "/bex").then((x) =>
        x.json().then((j) => {
            j.files.forEach((filename) => {
                var url = HOST + "/static/photos/bodyex/" + filename;
                var imgbox = createImgBox(url, "bex", filename);
                bbox.insertAdjacentHTML("beforeend", imgbox);
            });
        })
    );
}

function remex(part, filename) {
    fetch(HOST + "/rem/" + part, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("adtok"),
        },
        body: JSON.stringify({
            exname: filename,
        }),
    }).then((x) => {
        if (x.ok) {
            loadexams();
        }
    });
}

function getusers() {
    fetch(HOST + "/getusers", {
        headers: {
            Authorization: "Bearer " + localStorage.getItem("adtok"),
        },
    }).then((x) => {
        if (x.ok) {
            x.blob().then((b) => {
                const url = URL.createObjectURL(b);
                const link = document.createElement("a");
                link.href = url;
                link.download = "users.txt";
                link.id = "downdb";
                document.body.appendChild(link);
                link.click();
                link.remove();
                URL.revokeObjectURL(url); // پس از استفاده URL را آزاد می‌کنیم
            });
        }
    });
}