from pydantic import SecretStr\nfrom pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./mitzu_revenue.db"\n    admin_key: SecretStr = SecretStr("")\n    public_base_url: str = ""
    cors_origins: str = ""
    default_rate_limit_per_minute: int = 120
    prepayment_rate_limit_per_minute: int = 20
    trust_proxy_headers: bool = False
    max_daily_spend_usd: float = 5.0
    max_task_cost_usd: float = 1.0
    min_expected_profit_usd: float = 1.0
    min_roi: float = 3.0
    min_automation_score: int = 90
    autonomous_execution: bool = False
    wallet_enabled: bool = False
    scout_enabled: bool = True
    scout_interval_seconds: int = 900
    circle_discovery_url: str = "https://api.circle.com/v2/x402/discovery/resources"
    open402_directory_url: str = "https://agentinternetruntime.com/api/directory?protocol=x402&limit=100"
    coinbase_bazaar_url: str = "https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources"
    coinbase_page_size: int = 100
    coinbase_max_pages: int = 200
    market_scan_interval_seconds: int = 3600
    binance_deposit_address: str = ""
    binance_deposit_network: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
