import textwrap
from pathlib import Path

import yaml

import craft_parts
from craft_parts import Step, Action


def test_stage_slices(new_dir):
    _parts_yaml = textwrap.dedent(
        """\
        parts:
          foo:
            plugin: nil
            stage-packages: [ca-certificates_data]
        """
    )

    parts = yaml.safe_load(_parts_yaml)

    lf = craft_parts.LifecycleManager(
        parts, application_name="test_slice", cache_dir=new_dir, work_dir=new_dir
    )

    actions = lf.plan(Step.PRIME)
    assert actions == [
        Action("foo", Step.PULL),
        Action("foo", Step.OVERLAY),
        Action("foo", Step.BUILD),
        Action("foo", Step.STAGE),
        Action("foo", Step.PRIME),
    ]

    with lf.action_executor() as ctx:
        ctx.execute(actions)

    root = Path(new_dir)
    assert (root / "prime/etc/ssl/certs/ca-certificates.crt").is_file()
    assert (root / "prime/usr/share/ca-certificates").is_dir()
