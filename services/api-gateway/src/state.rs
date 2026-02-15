use reqwest::Client;
use crate::config::Config;

#[derive(Clone)]
pub struct AppState {
    pub config: Config,
    pub http_client: Client,
}

impl AppState {
    pub fn new(config: Config) -> Self {
        Self {
            config,
            http_client: Client::new(),
        }
    }
}