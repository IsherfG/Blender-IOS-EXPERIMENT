/* SPDX-FileCopyrightText: 2026 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

/** \file
 * \ingroup bli
 *
 * Apple-specific system queries shared by the macOS and iOS builds.
 */

#import <Foundation/Foundation.h>

#include "BLI_build_config.h"
#include "BLI_system.h"

#if defined(OS_IOS)
#  import <UIKit/UIKit.h>
#endif

namespace blender {

bool BLI_system_is_tablet()
{
#if defined(OS_IOS)
  return UIDevice.currentDevice.userInterfaceIdiom == UIUserInterfaceIdiomPad;
#else
  /* macOS has no tablet interface idiom. */
  return false;
#endif
}

}  // namespace blender
