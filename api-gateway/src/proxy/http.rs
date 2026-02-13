use std::collections::HashMap;

use axum::{
    extract::{Path, Query, State},
    http::{HeaderMap, Method, StatusCode},
    response::{IntoResponse, Response},
};
use serde_json::Value;

use crate::state::AppState;

pub async fn proxy_request(
    state: &AppState,
    method: Method,
    path: &str,
    headers: HeaderMap,
    query: &HashMap<String, String>,
    body: bytes::Bytes,
    target_base: &str,
    rewrite_from: &str,
    rewrite_to: &str,
) -> Response {
    let rewritten_path = path.replacen(rewrite_from, rewrite_to, 1);
    let mut target_url = format!("{}{}", target_base, rewritten_path);

    if !query.is_empty() {
        let qs = serde_urlencoded::to_string(query).unwrap_or_default();
        target_url = format!("{}?{}", target_url, qs);
    }

    let mut req_builder = state
        .http_client
        .request(
            reqwest::Method::from_bytes(method.as_str().as_bytes()).unwrap(),
            &target_url,
        )
        .body(body);

    // Forward headers, skip host
    for (key, value) in &headers {
        if key.as_str() == "host" {
            continue;
        }
        if let Ok(val_str) = value.to_str() {
            req_builder = req_builder.header(key.as_str(), val_str);
        }
    }

    match req_builder.send().await {
        Ok(resp) => {
            let status = StatusCode::from_u16(resp.status().as_u16())
                .unwrap_or(StatusCode::INTERNAL_SERVER_ERROR);
            let resp_headers = resp.headers().clone();
            let body_bytes = resp.bytes().await.unwrap_or_default();

            let json_body: Value = serde_json::from_slice(&body_bytes)
                .unwrap_or_else(|_| Value::String(String::from_utf8_lossy(&body_bytes).to_string()));

            let mut response = axum::Json(json_body).into_response();
            *response.status_mut() = status;

            let h = response.headers_mut();
            for (key, value) in &resp_headers {
                if matches!(key.as_str(), "content-type" | "authorization" | "set-cookie" | "x-request-id") {
                    h.insert(key, value.clone());
                }
            }

            response
        }
        Err(e) => {
            eprintln!("Proxy error: {}", e);
            (
                StatusCode::BAD_GATEWAY,
                axum::Json(serde_json::json!({ "error": "Bad Gateway", "detail": e.to_string() })),
            )
                .into_response()
        }
    }
}

pub async fn auth_proxy(
    State(state): State<AppState>,
    method: Method,
    Path(path): Path<String>,
    Query(query): Query<HashMap<String, String>>,
    headers: HeaderMap,
    body: bytes::Bytes,
) -> Response {
    let full_path = format!("/api/auth/{}", path);
    let base = state.config.auth_service.clone();
    proxy_request(&state, method, &full_path, headers, &query, body, &base, "/api/auth", "/auth").await
}

pub async fn messages_proxy(
    State(state): State<AppState>,
    method: Method,
    Path(path): Path<String>,
    Query(query): Query<HashMap<String, String>>,
    headers: HeaderMap,
    body: bytes::Bytes,
) -> Response {
    let full_path = format!("/api/messages/{}", path);
    let base = state.config.message_service.clone();
    proxy_request(&state, method, &full_path, headers, &query, body, &base, "/api/messages", "/messages").await
}