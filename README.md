# csu_robotics_abb_project

2019 Central South University computer vision and machine learning inspection laboratory (CV-MLI)

Version 2.0

更新于2021/04/11

  最新的2.0代码放在code文件夹里，其中1-20.bmp和1-20.png图片是相机标定用的照片。camera1.jpg是测试用图片，morph.jpg展示了处理后的图片，world.jpg是预设的机械臂参考世界坐标点位置图，需要用这张照片计算积木与相机和机械臂的相对位置。
   主程序是program_abb.py，camera_tool.py是标定相机和矫正畸变的程序包，image_tool.py是图像处理程序，coordingnate_tool.py是获取积木坐标的程序包，TIS.py是调用相机的程序包，这几个程序包均会由主程序调用。

The latest 2.0 code is in the code folder, where the 1-20.bmp and 1-20.png images are for camera calibration. JPG is the test image, morph. JPG shows the processed image, and world. JPG is the preset reference world position map of the manipulator arm. This image is needed to calculate the position of the building blocks relative to the camera and the manipulator arm.

The main program is program_abb.py, camera_tool.py is the calibration camera and correction distortion of the program package, image_tool.py is the image processing program, coordingnate_tool.py is the acquisition of building block coordinates of the program package, TIS. These packages are all called by the main program.



Version 1.0

更新于2019/04/11

  所有的代码都放在codefile文件夹里。其中codefile中的Program2.py是同时调用两个相机和机械臂的代码。Program3.py是只调用一个相机和机械臂的代码。TIS.py和TIS.pyc是Program2.py和Program3.py所依赖的文件。其他都是测试用的代码文件。transcode文件夹是计算偏转角度的测试代码文件夹。textcode是其他的测试文件代码。当前版本的代码暂时未完成整合，我们将在下一个版本中对此进行更新。
  
  All code is in the codefile folder. In codefile program2.py is the code that calls both the camera and the robot arm. Program3.py is code that calls just one camera and a mechanical arm. TIS.py and TIS.pyc are files that program2.py and program3.py rely on. The rest are test code files. The transcode folder is the test code folder that calculates the deflection Angle. Textcode is the other test code file. The current version of the code is not currently consolidated and will be updated in the next version.
