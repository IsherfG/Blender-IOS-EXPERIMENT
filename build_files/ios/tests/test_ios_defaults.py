#!/usr/bin/env python3

import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[3]
BLENDFILE_SOURCE = REPOSITORY / "source" / "blender" / "blenkernel" / "intern" / "blendfile.cc"
IOS_PLATFORM = REPOSITORY / "build_files" / "ios" / "cmake" / "platform_ios.cmake"
WM_INIT_EXIT = REPOSITORY / "source" / "blender" / "windowmanager" / "intern" / "wm_init_exit.cc"
WM_API = REPOSITORY / "source" / "blender" / "windowmanager" / "WM_api.hh"
IOS_SYSTEM = REPOSITORY / "intern" / "ghost" / "intern" / "GHOST_SystemIOS.mm"


def ui_scale(definitions: str, name: str) -> float:
    return float(definitions.split(f"-D{name}=")[1].split("f")[0])


class IOSDefaultsTests(unittest.TestCase):
    def test_factory_preferences_use_a_device_aware_ui_scale(self) -> None:
        source = BLENDFILE_SOURCE.read_text()
        defaults = source[
            source.index("UserDef *BKE_blendfile_userdef_from_defaults()") : source.index(
                "bool BKE_blendfile_userdef_write("
            )
        ]

        self.assertIn("#ifdef BLENDER_PLATFORM_DEFAULT_UI_SCALE", defaults)
        self.assertIn("BLI_system_is_tablet()", defaults)
        self.assertIn("BLENDER_PLATFORM_DEFAULT_UI_SCALE_TABLET", defaults)
        self.assertIn("userdef->ui_scale = BLENDER_PLATFORM_DEFAULT_UI_SCALE;", defaults)

        platform = IOS_PLATFORM.read_text()
        self.assertIn("-DBLENDER_PLATFORM_DEFAULT_UI_SCALE=1.65f", platform)
        self.assertIn("-DBLENDER_PLATFORM_DEFAULT_UI_SCALE_TABLET=1.2f", platform)

    def test_ipad_scale_is_smaller_than_the_iphone_scale(self) -> None:
        platform = IOS_PLATFORM.read_text()

        self.assertEqual(ui_scale(platform, "BLENDER_PLATFORM_DEFAULT_UI_SCALE"), 1.65)
        self.assertEqual(ui_scale(platform, "BLENDER_PLATFORM_DEFAULT_UI_SCALE_TABLET"), 1.2)
        self.assertLess(
            ui_scale(platform, "BLENDER_PLATFORM_DEFAULT_UI_SCALE_TABLET"),
            ui_scale(platform, "BLENDER_PLATFORM_DEFAULT_UI_SCALE"),
        )

    def test_suspended_apps_still_write_user_preferences(self) -> None:
        """iOS suspends and later kills apps, so the clean-exit save never runs."""
        system = IOS_SYSTEM.read_text()
        background = system.split("applicationDidEnterBackground:", 1)[1].split(
            "- (void)applicationWillTerminate:", 1
        )[0]
        self.assertIn("WM_userpref_save_on_suspend()", background)

        exit_source = WM_INIT_EXIT.read_text()
        save = exit_source[
            exit_source.index("void WM_userpref_save_on_suspend()") : exit_source.index(
                "void WM_exit_ex("
            )
        ]
        # The suspend path honours exactly the preferences the exit path honours.
        self.assertIn("USER_PREF_FLAG_SAVE", save)
        self.assertIn("G_FLAG_USERPREF_NO_SAVE_ON_EXIT", save)
        self.assertIn("U.runtime.is_dirty", save)
        self.assertIn("BKE_blendfile_userdef_write_all(nullptr)", save)

        self.assertIn("void WM_userpref_save_on_suspend();", WM_API.read_text())


if __name__ == "__main__":
    unittest.main()
