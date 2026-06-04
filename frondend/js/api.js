function buildUrl(path) {
  return window.APP_CONFIG.apiBaseUrl + path;
}

async function apiRequest(path, method, body, token) {
  var headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = "Bearer " + token;

  var response = await fetch(buildUrl(path), {
    method: method,
    headers: headers,
    body: body ? JSON.stringify(body) : undefined
  });

  var data = null;
  try {
    data = await response.json();
  } catch (_) {
    data = null;
  }

  if (!response.ok) {
    var errorMessage = (data && (data.message || data.error)) || "Erro na requisicao.";
    throw new Error(errorMessage);
  }

  return data;
}
