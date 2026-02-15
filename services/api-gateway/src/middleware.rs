use std::time::Instant;

use axum::{
    body::Body,
    extract::State,
    http::{HeaderValue, Method, StatusCode, header},
    middleware::Next,
    response::Response,
};
use chrono::Utc;

use crate::state::AppState;

/// Handles CORS preflight (OPTIONS) and attaches CORS headers to every response.
/// Supports credentials by echoing back the exact request Origin when it's allowed.
pub async fn cors_middleware(
    State(state): State<AppState>,
    req: axum::http::Request<Body>,
    next: Next,
) -> Response {
    let origin = req
        .headers()
        .get(header::ORIGIN)
        .and_then(|v| v.to_str().ok())
        .map(|s| s.to_string());

    let allowed = origin.as_deref().map_or(false, |o| {
        state.config.allowed_origins.iter().any(|a| a == o)
    });

    // For OPTIONS preflight, respond immediately
    if req.method() == Method::OPTIONS {
        let mut resp = Response::new(Body::empty());
        *resp.status_mut() = StatusCode::NO_CONTENT;
        if allowed {
            let o = origin.unwrap();
            let h = resp.headers_mut();
            h.insert(header::ACCESS_CONTROL_ALLOW_ORIGIN,      HeaderValue::from_str(&o).unwrap());
            h.insert(header::ACCESS_CONTROL_ALLOW_CREDENTIALS, HeaderValue::from_static("true"));
            h.insert(header::ACCESS_CONTROL_ALLOW_METHODS,     HeaderValue::from_static("GET,POST,PUT,PATCH,DELETE,OPTIONS"));
            h.insert(header::ACCESS_CONTROL_ALLOW_HEADERS,     HeaderValue::from_static("content-type,authorization,x-request-id,accept"));
            h.insert(header::ACCESS_CONTROL_MAX_AGE,            HeaderValue::from_static("3600"));
        }
        return resp;
    }

    let mut resp = next.run(req).await;

    if allowed {
        let o = origin.unwrap();
        let h = resp.headers_mut();
        h.insert(header::ACCESS_CONTROL_ALLOW_ORIGIN,      HeaderValue::from_str(&o).unwrap());
        h.insert(header::ACCESS_CONTROL_ALLOW_CREDENTIALS, HeaderValue::from_static("true"));
        h.insert(header::ACCESS_CONTROL_ALLOW_HEADERS,     HeaderValue::from_static("content-type,authorization,x-request-id,accept"));
        h.insert(header::ACCESS_CONTROL_EXPOSE_HEADERS,    HeaderValue::from_static("set-cookie,authorization"));
    }

    resp
}

pub async fn log_middleware(req: axum::http::Request<Body>, next: Next) -> Response {
    let method = req.method().clone();
    let path = req.uri().path().to_string();
    let start = Instant::now();

    let response = next.run(req).await;

    println!(
        "[{}] {} {} - {}ms",
        Utc::now().format("%Y-%m-%dT%H:%M:%S%.3fZ"),
        method,
        path,
        start.elapsed().as_millis()
    );

    response
}