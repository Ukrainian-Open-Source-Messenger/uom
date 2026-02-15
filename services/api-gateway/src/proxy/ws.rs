use std::sync::Arc;

use axum::{
    extract::{State, WebSocketUpgrade},
    extract::ws::{Message, WebSocket},
    response::Response,
};
use futures_util::{SinkExt, StreamExt};
use tokio::sync::Mutex;
use tokio_tungstenite::connect_async;
use tokio_tungstenite::tungstenite::Message as WsMessage;

use crate::state::AppState;

pub async fn ws_proxy_handler(
    State(state): State<AppState>,
    ws: WebSocketUpgrade,
) -> Response {
    let url = state.config.realtime_service.clone();
    ws.on_upgrade(move |socket| handle_ws(socket, url))
}

async fn handle_ws(client_ws: WebSocket, realtime_service: String) {
    println!("WS connected");

    let (backend_stream, _) = match connect_async(&realtime_service).await {
        Ok(conn) => conn,
        Err(e) => {
            eprintln!("Failed to connect to backend WS: {}", e);
            return;
        }
    };

    let (mut backend_tx, mut backend_rx) = backend_stream.split();
    let (mut client_tx, mut client_rx) = client_ws.split();

    let client_tx  = Arc::new(Mutex::new(client_tx));
    let backend_tx = Arc::new(Mutex::new(backend_tx));

    let client_tx_c  = client_tx.clone();
    let backend_tx_c = backend_tx.clone();

    // Client → Backend
    let c2b = tokio::spawn(async move {
        while let Some(msg) = client_rx.next().await {
            match msg {
                Ok(Message::Text(text)) => {
                    if backend_tx_c.lock().await.send(WsMessage::Text(text.to_string())).await.is_err() {
                        break;
                    }
                }
                Ok(Message::Binary(data)) => {
                    if backend_tx_c.lock().await.send(WsMessage::Binary(data.into())).await.is_err() {
                        break;
                    }
                }
                Ok(Message::Close(_)) | Err(_) => break,
                _ => {}
            }
        }
    });

    // Backend → Client
    let b2c = tokio::spawn(async move {
        while let Some(msg) = backend_rx.next().await {
            match msg {
                Ok(WsMessage::Text(text)) => {
                    if client_tx_c.lock().await.send(Message::Text(text.into())).await.is_err() {
                        break;
                    }
                }
                Ok(WsMessage::Binary(data)) => {
                    if client_tx_c.lock().await.send(Message::Binary(data.into())).await.is_err() {
                        break;
                    }
                }
                Ok(WsMessage::Close(_)) | Err(_) => break,
                _ => {}
            }
        }
    });

    tokio::select! {
        _ = c2b => {},
        _ = b2c => {},
    }

    println!("WS disconnected");
}