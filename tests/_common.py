import os
import tempfile
from pathlib import Path

from jinja2 import Template

MINI_ESGF_CACHE_DIR = Path.home() / ".mini-esgf-data"
ROOCS_CFG = os.path.join(tempfile.gettempdir(), "roocs.ini")


def write_roocs_cfg():
    cfg_templ = """
    [project:c3s-cmip6-test]
    is_default_for_path = True
    base_dir = {{ base_dir }}/master/test_data/badc/cmip6/data/CMIP6
    facet_rule = mip_era activity_id institution_id source_id experiment_id member_id table_id variable_id grid_label version
    """
    cfg = Template(cfg_templ).render(base_dir=MINI_ESGF_CACHE_DIR)
    with open(ROOCS_CFG, "w") as fp:
        fp.write(cfg)
    # point to roocs cfg in environment
    os.environ["ROOCS_CONFIG"] = ROOCS_CFG
