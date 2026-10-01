/* SPDX-FileCopyrightText: 2026 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup ghost
 *
 * Runtime overrides for #GHOST_IOSInputTuning, read from a file the Files app
 * can see so the feel of iPad input can be tuned without rebuilding.
 */

#import <Foundation/Foundation.h>

#include <cstdio>
#include <string>
#include <utility>
#include <vector>

#include "GHOST_IOSInputTuning.hh"

using namespace GHOST_IOSInputTuning;

namespace {

/* Kept in Documents because release/ios/Blender.app/Info.plist already sets
 * UIFileSharingEnabled and LSSupportsOpeningDocumentsInPlace, so this directory
 * is reachable from the Files app on the device. */
NSString *const kOverrideFileName = @"input_tuning.json";
NSString *const kResolvedFileName = @"input_tuning.resolved.json";
NSString *const kFlagKey = @"pointer_always_wrap";

NSArray<NSString *> *numeric_keys()
{
  return @[
    @"pointer_acceleration_start_points_per_second",
    @"pointer_acceleration_full_points_per_second",
    @"pointer_min_multiplier",
    @"pointer_max_multiplier",
    @"two_finger_right_click_hold_seconds",
    @"two_finger_right_click_slop_points",
  ];
}

NSArray<NSString *> *tuning_keys()
{
  return [numeric_keys() arrayByAddingObject:kFlagKey];
}

NSString *documents_directory()
{
  NSArray<NSString *> *paths = NSSearchPathForDirectoriesInDomains(
      NSDocumentDirectory, NSUserDomainMask, YES);
  return paths.count > 0 ? paths.firstObject : nil;
}

/* NSNumber covers JSON booleans as well, and mistaking `true` for 1.0 would
 * silently overwrite a multiplier. */
BOOL is_json_boolean(id value)
{
  return value != nil && CFGetTypeID((__bridge CFTypeRef)value) == CFBooleanGetTypeID();
}

BOOL is_json_number(id value)
{
  return [value isKindOfClass:[NSNumber class]] && !is_json_boolean(value);
}

NSDictionary *template_contents()
{
  return @{
    @"_readme" : @[
      @"iPad input tuning. Change a value, then switch away from the app and back",
      @"(or relaunch) to apply it. Delete this file to return to the built-in defaults.",
      @"Entries that are not applied are listed in input_tuning.resolved.json.",
    ],
    @"pointer_acceleration_start_points_per_second" : @120,
    @"pointer_acceleration_full_points_per_second" : @1100,
    @"pointer_min_multiplier" : @1,
    @"pointer_max_multiplier" : @4,
    @"pointer_always_wrap" : @YES,
    @"two_finger_right_click_hold_seconds" : @0.30,
    @"two_finger_right_click_slop_points" : @14,
  };
}

BOOL write_json(id contents, NSString *path)
{
  NSError *error = nil;
  NSData *data = [NSJSONSerialization dataWithJSONObject:contents
                                                 options:NSJSONWritingPrettyPrinted
                                                   error:&error];
  if (data == nil) {
    fprintf(stderr,
            "[ios-input-tuning] could not encode %s: %s\n",
            path.UTF8String,
            error.localizedDescription.UTF8String ?: "unknown error");
    return NO;
  }
  if (![data writeToFile:path options:NSDataWritingAtomic error:&error]) {
    fprintf(stderr,
            "[ios-input-tuning] could not write %s: %s\n",
            path.UTF8String,
            error.localizedDescription.UTF8String ?: "unknown error");
    return NO;
  }
  return YES;
}

void write_resolved_echo(NSString *path, const Values &effective, const OverrideResult &result)
{
  NSMutableDictionary *echo = [@{
    @"_readme" : @"Written by the app when tuning is reloaded. Edit input_tuning.json, not this.",
    @"applied" : @(result.applied),
  } mutableCopy];

  echo[@"pointer_acceleration_start_points_per_second"] =
      @(effective.pointer_acceleration_start_points_per_second);
  echo[@"pointer_acceleration_full_points_per_second"] =
      @(effective.pointer_acceleration_full_points_per_second);
  echo[@"pointer_min_multiplier"] = @(effective.pointer_min_multiplier);
  echo[@"pointer_max_multiplier"] = @(effective.pointer_max_multiplier);
  echo[@"pointer_always_wrap"] = @(effective.pointer_always_wrap);
  echo[@"two_finger_right_click_hold_seconds"] = @(effective.two_finger_right_click_hold_seconds);
  echo[@"two_finger_right_click_slop_points"] = @(effective.two_finger_right_click_slop_points);

  NSMutableArray<NSString *> *rejected = [NSMutableArray array];
  for (const std::string &reason : result.rejected) {
    [rejected addObject:[NSString stringWithUTF8String:reason.c_str()]];
  }
  echo[@"rejected"] = rejected;

  write_json(echo, path);
}

void report(const Values &effective, const OverrideResult &result)
{
  for (const std::string &reason : result.rejected) {
    fprintf(stderr, "[ios-input-tuning] rejected %s\n", reason.c_str());
  }
  fprintf(stderr,
          "[ios-input-tuning] applied %d override(s); wrap=%d start=%.1f full=%.1f min=%.2f "
          "max=%.2f hold=%.2f slop=%.1f\n",
          result.applied,
          effective.pointer_always_wrap ? 1 : 0,
          effective.pointer_acceleration_start_points_per_second,
          effective.pointer_acceleration_full_points_per_second,
          effective.pointer_min_multiplier,
          effective.pointer_max_multiplier,
          effective.two_finger_right_click_hold_seconds,
          effective.two_finger_right_click_slop_points);
}

}  // namespace

void GHOST_IOSInputTuning::reload_overrides()
{
  @autoreleasepool {
    NSString *directory = documents_directory();
    if (directory == nil) {
      fprintf(stderr, "[ios-input-tuning] no Documents directory; keeping defaults\n");
      return;
    }

    NSString *override_path = [directory stringByAppendingPathComponent:kOverrideFileName];
    NSString *resolved_path = [directory stringByAppendingPathComponent:kResolvedFileName];

    /* Write the template once so the file is discoverable, but never overwrite
     * values the user has already set. */
    if (![[NSFileManager defaultManager] fileExistsAtPath:override_path]) {
      if (write_json(template_contents(), override_path)) {
        fprintf(stderr, "[ios-input-tuning] wrote template %s\n", override_path.UTF8String);
      }
    }

    NSError *error = nil;
    NSData *data = [NSData dataWithContentsOfFile:override_path options:0 error:&error];
    if (data == nil) {
      fprintf(stderr,
              "[ios-input-tuning] could not read %s: %s\n",
              override_path.UTF8String,
              error.localizedDescription.UTF8String ?: "unknown error");
      write_resolved_echo(resolved_path, values(), OverrideResult{});
      return;
    }

    id parsed = [NSJSONSerialization JSONObjectWithData:data options:0 error:&error];
    if (![parsed isKindOfClass:[NSDictionary class]]) {
      fprintf(stderr,
              "[ios-input-tuning] %s is not a JSON object: %s\n",
              override_path.UTF8String,
              error.localizedDescription.UTF8String ?: "unexpected top level value");
      write_resolved_echo(resolved_path, values(), OverrideResult{});
      return;
    }

    NSDictionary *contents = parsed;
    NSArray<NSString *> *known = tuning_keys();
    std::vector<std::pair<std::string, double>> numbers;
    std::vector<std::pair<std::string, bool>> flags;
    OverrideResult result;

    for (NSString *key in contents) {
      if ([key hasPrefix:@"_"]) {
        continue; /* Documentation keys are not tuning entries. */
      }
      id value = contents[key];
      if ([key isEqualToString:kFlagKey]) {
        if (is_json_boolean(value)) {
          flags.emplace_back(key.UTF8String, [value boolValue] ? true : false);
        }
        else {
          result.rejected.emplace_back(key.UTF8String + std::string(": expected true or false"));
        }
        continue;
      }
      if ([known containsObject:key]) {
        if (is_json_number(value)) {
          numbers.emplace_back(key.UTF8String, [value doubleValue]);
        }
        else {
          result.rejected.emplace_back(key.UTF8String + std::string(": expected a number"));
        }
        continue;
      }
      /* Report typos instead of ignoring them. */
      result.rejected.emplace_back(key.UTF8String + std::string(": unknown key"));
    }

    const OverrideResult applied = apply_overrides(numbers, flags);
    result.applied = applied.applied;
    result.rejected.insert(result.rejected.end(), applied.rejected.begin(), applied.rejected.end());

    report(values(), result);
    write_resolved_echo(resolved_path, values(), result);
  }
}
