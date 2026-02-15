use axum::{
    Router,
    response::IntoResponse,
    routing::{any, get},
};

use crate::{
    middleware::{cors_middleware, log_middleware},
    proxy::{http::{auth_proxy, messages_proxy}, ws::ws_proxy_handler},
    state::AppState,
};

async fn root_handler() -> impl IntoResponse {
    "API Gateway is running"
}

pub fn build_router(state: AppState) -> Router {
    Router::new()
        .route("/", get(root_handler))
        .route("/api/auth/{path}", any(auth_proxy))
        .route("/api/auth/", any(auth_proxy))
        .route("/api/messages/{path}", any(messages_proxy))
        .route("/api/messages/", any(messages_proxy))
        .route("/ws", get(ws_proxy_handler))
        .layer(axum::middleware::from_fn_with_state(state.clone(), cors_middleware))
        .layer(axum::middleware::from_fn(log_middleware))
        .with_state(state)
}