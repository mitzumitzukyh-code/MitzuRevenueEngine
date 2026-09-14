from app.services.liquidations_prototype import LiquidationCluster


def test_liquidation_cluster_shape_is_data_only():
    cluster = LiquidationCluster(
        leverage=10,
        long_liq_estimate=90000.0,
        short_liq_estimate=110000.0,
    )
    assert cluster.leverage == 10
    assert cluster.long_liq_estimate < cluster.short_liq_estimate
