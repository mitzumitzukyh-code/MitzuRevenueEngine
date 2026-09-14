from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./mitzu_revenue.db"
    max_daily_spend_usd: float = 5.0
    max_task_cost_usd: float = 1.0
    min_expected_profit_usd: float = 1.0
    min_roi: float = 3.0
    min_automation_score: int = 90
    autonomous_execution: bool = False
    wallet_enabled: bool = False
    binance_deposit_address: str = ""
    binance_deposit_network: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
