/* SPDX-FileCopyrightText: 2026 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

#pragma once

#include <string>
#include <utility>
#include <vector>

/**
 * Tunable values for physical iPad input.
 *
 * These were compile-time constants, which meant every attempt at tuning the
 * feel of touch input cost a full rebuild. They are now runtime values so a
 * build can be re-tuned from the override file described in
 * #GHOST_IOSInputTuning::reload_overrides() without recompiling.
 *
 * Defaults stay here, and stay in the header, so the compiled test harnesses
 * that include the pointer state can keep checking the math directly.
 */
namespace GHOST_IOSInputTuning {

struct Values {
  double pointer_acceleration_start_points_per_second = 120.0;
  double pointer_acceleration_full_points_per_second = 1100.0;
  double pointer_min_multiplier = 1.0;
  double pointer_max_multiplier = 4.0;
  bool pointer_always_wrap = true;

  double two_finger_right_click_hold_seconds = 0.30;
  double two_finger_right_click_slop_points = 14.0;
};

/** Process-wide values, starting at the defaults above. */
inline Values &values()
{
  static Values current;
  return current;
}

struct OverrideResult {
  int applied = 0;
  /** Human readable reasons for each entry that was not applied. */
  std::vector<std::string> rejected;
};

/**
 * Apply overrides to #values().
 *
 * Unknown names, out-of-range numbers and an inverted acceleration range are
 * rejected rather than clamped or ignored silently, so a typo in the override
 * file cannot quietly change how input behaves. Callers log `rejected`.
 */
inline OverrideResult apply_overrides(
    const std::vector<std::pair<std::string, double>> &numbers,
    const std::vector<std::pair<std::string, bool>> &flags)
{
  OverrideResult result;
  Values candidate = values();

  auto number = [&](const char *name, double *target, const double minimum, const double maximum) {
    for (const auto &entry : numbers) {
      if (entry.first != name) {
        continue;
      }
      /* Written as a negated range test so a NaN is rejected as well. */
      if (!(entry.second >= minimum && entry.second <= maximum)) {
        result.rejected.emplace_back(std::string(name) + ": out of range");
        return;
      }
      *target = entry.second;
      result.applied++;
      return;
    }
  };

  number("pointer_acceleration_start_points_per_second",
         &candidate.pointer_acceleration_start_points_per_second,
         1.0,
         10000.0);
  number("pointer_acceleration_full_points_per_second",
         &candidate.pointer_acceleration_full_points_per_second,
         1.0,
         10000.0);
  number("pointer_min_multiplier", &candidate.pointer_min_multiplier, 0.1, 20.0);
  number("pointer_max_multiplier", &candidate.pointer_max_multiplier, 0.1, 20.0);
  number("two_finger_right_click_hold_seconds",
         &candidate.two_finger_right_click_hold_seconds,
         0.05,
         3.0);
  number("two_finger_right_click_slop_points",
         &candidate.two_finger_right_click_slop_points,
         1.0,
         200.0);

  for (const auto &entry : flags) {
    if (entry.first == "pointer_always_wrap") {
      candidate.pointer_always_wrap = entry.second;
      result.applied++;
    }
    else {
      result.rejected.emplace_back(entry.first + ": unknown key");
    }
  }

  for (const auto &entry : numbers) {
    const std::string &name = entry.first;
    if (name != "pointer_acceleration_start_points_per_second" &&
        name != "pointer_acceleration_full_points_per_second" &&
        name != "pointer_min_multiplier" && name != "pointer_max_multiplier" &&
        name != "two_finger_right_click_hold_seconds" &&
        name != "two_finger_right_click_slop_points")
    {
      result.rejected.emplace_back(name + ": unknown key");
    }
  }

  /* The acceleration curve divides by this span, so an inverted or empty range
   * would turn cursor motion into NaN. Reject the whole edit instead. */
  if (candidate.pointer_acceleration_start_points_per_second >=
      candidate.pointer_acceleration_full_points_per_second)
  {
    result.rejected.emplace_back(
        "pointer_acceleration_start_points_per_second must be less than "
        "pointer_acceleration_full_points_per_second: no changes applied");
    result.applied = 0;
    return result;
  }
  if (candidate.pointer_min_multiplier > candidate.pointer_max_multiplier) {
    result.rejected.emplace_back("pointer_min_multiplier must not exceed pointer_max_multiplier: "
                                 "no changes applied");
    result.applied = 0;
    return result;
  }

  values() = candidate;
  return result;
}

/**
 * Read the override file from the app's Files-visible Documents directory and
 * apply it. Also writes a resolved echo next to it so the loaded values can be
 * confirmed without a debugger. Safe to call repeatedly; called on launch and
 * whenever the app returns to the foreground.
 *
 * Implemented in GHOST_IOSInputTuning.mm.
 */
void reload_overrides();

}  // namespace GHOST_IOSInputTuning
