"""Capture mode → device class map (ENV_MANIFEST_v0)."""

CAPTURE_MODE_TO_DEVICE_CLASS = {
    "robot_ros2": "robot_onboard",
    "android": "handheld_phone",
    "tablet_android": "handheld_tablet",
    "ios_later": "handheld_phone",  # v0: treat as phone path
}

DEFAULT_CATEGORY = "home_indoor"
SCHEMA_ID = "open-real2sim.env.manifest/0.1"
CAPTURE_SCHEMA_ID = "open-real2sim.capture.manifest/0.1"


def device_class_for(capture_mode: str) -> str:
    try:
        return CAPTURE_MODE_TO_DEVICE_CLASS[capture_mode]
    except KeyError as exc:
        known = ", ".join(sorted(CAPTURE_MODE_TO_DEVICE_CLASS))
        raise ValueError(f"unknown capture_mode {capture_mode!r}; expected one of: {known}") from exc
