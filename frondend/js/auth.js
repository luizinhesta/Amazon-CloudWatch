function saveSession(payload) {
  localStorage.setItem("cw_token", payload.token || "");
  localStorage.setItem("cw_user", JSON.stringify(payload.user || {}));
}

function getToken() {
  return localStorage.getItem("cw_token") || "";
}

function getUser() {
  var raw = localStorage.getItem("cw_user");
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch (_) {
    return {};
  }
}

function clearSession() {
  localStorage.removeItem("cw_token");
  localStorage.removeItem("cw_user");
}

function requireAuth() {
  if (!getToken()) {
    window.location.href = "login.html";
  }
}
