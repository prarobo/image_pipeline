#!/usr/bin/env python

import cv2
from distutils.version import LooseVersion

class CvInterface(object):
    """
    Wrapper for opencv calibration functions for seamlessly switching between fisheye 
    and pinhole calibration models
    """
    def __init__(self, *args, **kwargs):
        if 'calibration_model' not in kwargs:
            self.calibration_model = 'pinhole'
        else:
            self.calibration_model = kwargs['calibration_model']

    def calibrateCamera(self, *args, **kwargs):
        """
        @brief Wrapper for camera calibration function
        """
        if self.calibration_model == 'fisheye':
            return cv2.fisheye.calibrate(*args, **kwargs)
        else:
            return cv2.calibrateCamera(*args, **kwargs)

    def setupCalibFlags(self, options):
        """
        @brief Wrapper to setup calibration flags structure
       
        @param options Commandline options that contain information about calibration flags
        """
        calib_flags = 0
        num_ks = options.k_coefficients
        if self.calibration_model == 'fisheye':
            if options.fix_principal_point:
                calib_flags |= cv2.fisheye.CALIB_FIX_PRINCIPAL_POINT
            # TODO Look at fisheye calibration model
            # if options.fix_aspect_ratio:
            #     calib_flags |= cv2.fisheye.CALIB_FIX_ASPECT_RATIO
            # if options.zero_tangent_dist:
            #     calib_flags |= cv2.fisheye.CALIB_ZERO_TANGENT_DIST
            # if (num_ks > 3):
            #     calib_flags |= cv2.fisheye.CALIB_RATIONAL_MODEL
            if (num_ks < 4):
                calib_flags |= cv2.fisheye.CALIB_FIX_K4
            if (num_ks < 3):
                calib_flags |= cv2.fisheye.CALIB_FIX_K3
            if (num_ks < 2):
                calib_flags |= cv2.fisheye.CALIB_FIX_K2
            if (num_ks < 1):
                calib_flags |= cv2.fisheye.CALIB_FIX_K1            
        else:
            if options.fix_principal_point:
                calib_flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
            if options.fix_aspect_ratio:
                calib_flags |= cv2.CALIB_FIX_ASPECT_RATIO
            if options.zero_tangent_dist:
                calib_flags |= cv2.CALIB_ZERO_TANGENT_DIST
            if (num_ks > 3):
                calib_flags |= cv2.CALIB_RATIONAL_MODEL
            if (num_ks < 6):
                calib_flags |= cv2.CALIB_FIX_K6
            if (num_ks < 5):
                calib_flags |= cv2.CALIB_FIX_K5
            if (num_ks < 4):
                calib_flags |= cv2.CALIB_FIX_K4
            if (num_ks < 3):
                calib_flags |= cv2.CALIB_FIX_K3
            if (num_ks < 2):
                calib_flags |= cv2.CALIB_FIX_K2
            if (num_ks < 1):
                calib_flags |= cv2.CALIB_FIX_K1
        return calib_flags    

    def initUndistortRectifyMap(self, *args, **kwargs):
        """
        @brief Wrapper for initUndistortRectifyMap
        """
        if self.calibration_model == 'fisheye':
            return cv2.fisheye.initUndistortRectifyMap(*args, **kwargs)
        else:
            return cv2.initUndistortRectifyMap(*args, **kwargs)

    def undistortPoints(self, *args, **kwargs):
        """
        @brief Wrapper for undistortPoints
        """
        if self.calibration_model == 'fisheye':
            return cv2.fisheye.undistortPoints(*args, **kwargs)
        else:
            return cv2.undistortPoints(*args, **kwargs)    

    def stereoCalibrate(self, opts, lipts, ripts, size,
                               l_intrinsics, l_distortion,
                               r_intrinsics, r_distortion,
                               R, T, *args, **kwargs):
        """
        @brief Wrapper for undistortPoints
        """
        if self.calibration_model == 'fisheye':
                return cv2.fisheye.stereoCalibrate(opts, lipts, ripts, 
                                           l_intrinsics, l_distortion,
                                           r_intrinsics, r_distortion,
                                           size, R, T, *args, **kwargs)
        else:
            if LooseVersion(cv2.__version__).version[0] == 2:
                return cv2.stereoCalibrate(opts, lipts, ripts, size,
                                           l_intrinsics, l_distortion,
                                           r_intrinsics, r_distortion,
                                           R, T, *args, **kwargs)
            else:
                return cv2.stereoCalibrate(opts, lipts, ripts, 
                                           l_intrinsics, l_distortion,
                                           r_intrinsics, r_distortion,
                                           size, R, T, *args, **kwargs)
