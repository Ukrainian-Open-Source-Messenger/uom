mod config;
mod middleware;
mod proxy;
mod routes;
mod state;

use config::Config;
use routes::build_router;
use state::AppState;

#[tokio::main]
async fn main() {
    let config = Config::from_env();
    let port = config.port;

    println!("Allowed origins: {:?}", config.allowed_origins);

    let state = AppState::new(config);
    let app = build_router(state);

    let addr = format!("0.0.0.0:{}", port);
    println!("API Gateway running on http://{}", addr);

    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}