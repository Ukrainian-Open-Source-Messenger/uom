use std::env;
use dotenv::dotenv;

#[derive(Clone)]
pub struct Config {
    pub port: u16,
    pub auth_service: String,
    pub message_service: String,
    pub realtime_service: String,
    pub allowed_origins: Vec<String>,
}

impl Config {
    pub fn from_env() -> Self {
        dotenv().ok();
        let origins_raw = env::var("ALLOWED_ORIGINS")
            .unwrap_or_else(|_| "http://localhost:3000".into());
        let allowed_origins = origins_raw
            .split(',')
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty())
            .collect();

        Self {
            port: env::var("APP_PORT")
                .unwrap_or_else(|_| "8080".into())
                .parse()
                .unwrap_or(8080),
            auth_service: env::var("AUTH_SERVICE")
                .unwrap_or_else(|_| "http://localhost:3001".into()),
            message_service: env::var("MESSAGE_SERVICE")
                .unwrap_or_else(|_| "http://localhost:3002".into()),
            realtime_service: env::var("REALTIME_SERVICE")
                .unwrap_or_else(|_| "ws://localhost:3003".into()),
            allowed_origins,
        }
    }
}