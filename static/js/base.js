const API_KEY = document.getElementById("API_KEY");
const SECRET_KEY = document.getElementById("SECRET_KEY");
const API_URL = document.getElementById("API_URL");
const abstract = document.getElementById("abstract");
const title = document.getElementById("title");
const submitButton = document.getElementById("submit");
const submitButtonText = document.querySelector("#submit span");
const counter = document.getElementById("counter");
let isPersistedstate = false;
let isPrefix = false;

const getPayload = () => {
  const payload = {
    API_KEY: API_KEY.value,
    SECRET_KEY: SECRET_KEY.value,
    API_URL: API_URL.value,
    abstract: abstract.value,
    with_prefix: isPrefix
  };
  if (payload.API_KEY === '') {
    alert("请输入API KEY");
    return false;
  }
  if (payload.SECRET_KEY === '') {
    alert("请输入SECRET KEY");
    return false;
  }
  if (payload.API_URL === '') {
    alert("请输入API URL");
    return false;
  }
  if (payload.abstract === '') {
    alert("请输入论文摘要");
    return false;
  }
  return payload;
}

const getAbstractLen = () => {
  const len = abstract.value.length;
  counter.innerText = `${len}/350`
}

const setButtonDisabled = (flag) => {
  if (flag) {
    submitButtonText.innerText = "请稍等片刻";
    submitButton.setAttribute("disabled", true);
  } else {
    submitButtonText.innerText = "生成标题";
    submitButton.removeAttribute("disabled");
  }
}
// 从 local storage 读取缓存的配置数据
const syncConfigFromLocalStorage = () => {
  const API_KEY_V = window.localStorage.getItem("API_KEY") || "";
  const SECRET_KEY_V = window.localStorage.getItem("SECRET_KEY") || "";
  const API_URL_V = window.localStorage.getItem("API_URL") || "";
  API_KEY.value = API_KEY_V;
  SECRET_KEY.value = SECRET_KEY_V;
  API_URL.value = API_URL_V;
}

const syncConfigToLocalStorage = (API_KEY_V, SECRET_KEY_V, API_URL_V) => {
  window.localStorage.setItem("API_KEY", API_KEY_V);
  window.localStorage.setItem("SECRET_KEY", SECRET_KEY_V);
  window.localStorage.setItem("API_URL", API_URL_V);
}

const init = (with_storage, with_prefix) => {
  isPersistedstate = with_storage;
  isPrefix = with_prefix;
  if (isPersistedstate) {
    syncConfigFromLocalStorage();
  }
  getAbstractLen();
}

abstract.oninput = () => {
  getAbstractLen();
}
submitButton.onclick = () => {
  const payload = getPayload();
  if (payload) {
    if (isPersistedstate) {
      syncConfigToLocalStorage(payload.API_KEY, payload.SECRET_KEY, payload.API_URL);
    }
    setButtonDisabled(true);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/text_gen", true);
    xhr.setRequestHeader('content-type', 'application/json');
    xhr.responseType = "json";
    xhr.send(JSON.stringify(payload));
    xhr.onload = () => {
      const result = xhr.response;
      if (xhr.status == 200) {
        title.innerText = result.title;
      } else if (xhr.status == 401) {
        alert(result.msg);
      } else if (xhr.status == 403) {
        alert(result.msg);
      } else {
        alert("网络请求出现错误，请向网站管理员反馈");
      }
    }
    xhr.onloadend = () => {
      setButtonDisabled(false);
    }
  }
}