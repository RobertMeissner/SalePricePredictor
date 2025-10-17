from hydra import compose, initialize

from preprocessing.sklearn_pipeline_builder import pipeline_from_config


def test_pipeline_from_config_has_correct_step_order():
    with initialize(config_path="config", version_base=None):
        config = compose(config_name="default")
        pipeline = pipeline_from_config(config)
        assert len(pipeline.steps) == 4
        assert [name for name, _ in pipeline.steps] == [
            "drop_columns",
            "domain_mappings",
            "impute_and_scale",
            "drop_columns",
        ]
