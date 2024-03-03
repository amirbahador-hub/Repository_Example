import logging
import os
from time import sleep

from dotenv import load_dotenv
from memoization import cached
from omegaconf import OmegaConf

logger = logging.getLogger(__name__)


env_path = os.path.abspath(".env")
load_dotenv(dotenv_path=env_path)


CURRENT_CONFIG = None
CONFIG_IS_LOADING = False


def __load_config(config_dir: str = "./config"):
    global CURRENT_CONFIG, CONFIG_IS_LOADING
    while CONFIG_IS_LOADING:
        sleep(0.05)
    if CURRENT_CONFIG is not None:
        return CURRENT_CONFIG
    while CONFIG_IS_LOADING:
        sleep(0.05)
    CONFIG_IS_LOADING = True
    try:
        # Read default config
        try:
            default_config = OmegaConf.load(f"{config_dir}/default.yml")
        except FileNotFoundError:
            default_config = OmegaConf.create()

        # Read environment-dependent config
        delphai_environment = os.environ.get("PARLOA_ENVIRONMENT", "local")
        if not delphai_environment:
            raise Exception("PARLOA_ENVIRONMENT is not defined")
        try:
            delphai_env_config = OmegaConf.load(
                f"{config_dir}/{delphai_environment}.yml"
            )
        except FileNotFoundError:
            delphai_env_config = OmegaConf.create()

        CURRENT_CONFIG = OmegaConf.merge(default_config, delphai_env_config)
        OmegaConf.set_readonly(CURRENT_CONFIG, True)
        return CURRENT_CONFIG
    finally:
        CONFIG_IS_LOADING = False


@cached
def get_config(path: str = "", config_dir: str = "./config"):
    config = __load_config(config_dir=config_dir)
    if path is None:
        return config
    selected = OmegaConf.select(config, path)
    if OmegaConf.is_config(selected):
        return OmegaConf.to_container(selected, resolve=True)
    else:
        return selected