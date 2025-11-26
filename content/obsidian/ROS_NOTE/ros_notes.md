---



title: ros_notes
date: 2025-11-26
lastmod: 2025-11-26
draft: false
tags:
- ROS_NOTE
- Security
- Ubuntu
- ROS
- RL
---
# ROS_notes

## 换源

```
sudo cp /etc/apt/sources.list /etc/apt/sources.list.back
sudo gedit /etc/apt/sources.list
```

将内容替换为
清华源

```

deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal universe
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates universe
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security universe
deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security multiverse

```

更新

```
sudo apt-get update
sudo apt-get upgrade
```

## ROS Installation

设置电脑以安装来自packages.ros.org的软件

```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```

设置密钥

```
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
```

开始安装

```
sudo apt update
sudo apt install ros-noetic-desktop-full
```

一般来说，每次打开新终端都要source一下

```
source /opt/ros/noetic/setup.bash
```

为了方便，设置自动source此脚本

```
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

**注意**如果安装了其他解释器，如zsh

上面*sh均更改为对应的解释器

bash改为zsh    bashrc改为zshrc

**zsh**

```
echo "source /opt/ros/noetic/setup.zsh" >> ~/.bashrc
source ~/.zshrc
```

## Create ROS Workspace

```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make
```

catkin_make之后,生成了build 和 devel
then, source这些文件中的任何一个都可以将当前工作空间设置在环境的最顶层。

```
source devel/setup.zsh
```

要保证工作区被安装脚本正确覆盖，需确定ROS_PACKAGE_PATH环境变量包含你当前的工作空间目录：

```
echo $ROS_PACKAGE_PATH

the result will be like:
/home/<username>/catkin_ws/src:/opt/ros/<distro>/share
```

## Filesystem Tools

Navigating with command-line tools such as ls and cd can be very tedious which is why ROS provides tools to help you.

### rospack

usage and example:

```
rospack find [pkg_name]

example:
rospack find roscpp
would return
YOUR_INSTALL_PATH/share/roscpp
```

### roscd

roscd是rosbash命令集的一部分，它允许你直接切换目录（cd）到某个软件包或者软件包集当中。

```
roscd [locationname[/subdir]]
```

example

### catkin工作空间

```
workspace_folder/        -- WORKSPACE
  src/                   -- SOURCE SPACE
    CMakeLists.txt       -- 'Toplevel' CMake file, provided by catkin
    package_1/
      CMakeLists.txt     -- CMakeLists.txt file for package_1
      package.xml        -- Package manifest for package_1
    ...
    package_n/
      CMakeLists.txt     -- CMakeLists.txt file for package_n
      package.xml        -- Package manifest for package_n
```

### Create pkg

```
cd ~/catkin_ws/src
```



现在使用catkin_create_pkg命令创建一个名为beginner_tutorials的新软件包，这个软件包依赖于std_msgs、roscpp和rospy：

```
$ catkin_create_pkg beginner_tutorials std_msgs rospy roscpp
```


这将会创建一个名为beginner_tutorials的文件夹，这个文件夹里面包含一个[package.xml](http://wiki.ros.org/catkin/package.xml)文件和一个[CMakeLists.txt](http://wiki.ros.org/catkin/CMakeLists.txt)文件，这两个文件都已经部分填写了你在执行catkin_create_pkg命令时提供的信息。

catkin_create_pkg命令会要求你输入package_name，如有需要还可以在后面添加一些需要依赖的其它软件包：

```
# This is an example, do not try to run this
# catkin_create_pkg <package_name> [depend1] [depend2] [depend3]
```



现在看下面最后去掉了注释和未使用标签后的[package.xml](http://wiki.ros.org/catkin/package.xml)文件就显得更加简洁了：

```
   1 <?xml version="1.0"?>
   2 <package format="2">
   3   <name>beginner_tutorials</name>
   4   <version>0.1.0</version>
   5   <description>The beginner_tutorials package</description>
   6 
   7   <maintainer email="you@yourdomain.tld">Your Name</maintainer>
   8   <license>BSD</license>
   9   <url type="website">http://wiki.ros.org/beginner_tutorials</url>
  10   <author email="you@yourdomain.tld">Jane Doe</author>
  11 
  12   <buildtool_depend>catkin</buildtool_depend>
  13 
  14   <build_depend>roscpp</build_depend>
  15   <build_depend>rospy</build_depend>
  16   <build_depend>std_msgs</build_depend>
  17 
  18   <exec_depend>roscpp</exec_depend>
  19   <exec_depend>rospy</exec_depend>
  20   <exec_depend>std_msgs</exec_depend>
  21 
  22 </package>
```


build 目录是[构建空间](http://wiki.ros.org/catkin/workspaces#Build_Space)的默认位置，同时cmake和make也是在这里被调用来配置和构建你的软件包。而devel目录是[开发空间](http://wiki.ros.org/catkin/workspaces#Development_.28Devel.29_Space)的默认位置, 在安装软件包之前，这里可以存放可执行文件和库。




**roscore是你在运行所有ROS程序前首先要运行的命令。**



rosnode显示当前正在运行的ROS节点信息。rosnode list命令会列出这些活动的节点：

```
$ rosnode list
```


而rosnode info命令返回的是某个指定节点的信息。

```
$ rosnode info /rosout
```



ROS有一个强大的功能，就是你可以通过命令行重新分配名称。

关闭turtlesim窗口以停止节点（或回到rosrun turtlesim的终端并按Ctrl+C）。现在让我们重新运行它，但是这一次使用[重映射参数](http://wiki.ros.org/Remapping%20Arguments)来改变节点名称：

```
$ rosrun turtlesim turtlesim_node __name:=my_turtle
```


**注意：** 如果你仍看到/turtlesim在列表中，这可能因为你是在终端中使用Ctrl+C停止的节点而不是关闭窗口，或者你没有按[网络配置 - 单机器配置](http://wiki.ros.org/ROS/NetworkSetup#Single_machine_configuration)中的描述定义$ROS_HOSTNAME环境变量。可以尝试清除下rosnode列表:  $ rosnode cleanup



* roscore = ros+core：主节点（为ROS提供命名服务) + rosout (stdout/stderr) + 参数服务器（会在以后介绍）
* rosnode = ros+node：获取节点信息的ROS工具
* rosrun = ros+run：运行给定的软件包中的节点


### rqt_graph


打开一个**新**终端：

```
$ rosrun rqt_graph rqt_graph
```


### rostopic


rostopic echo可以显示在某个话题上发布的数据。

用法：

```
rostopic echo [topic]
```


rostopic list能够列出当前已被订阅和发布的所有话题。

让我们查看一下list子命令需要的参数。打开一个**新**终端：

```
$ rostopic list -h
```

* ```
  Usage: rostopic list [/topic]

  Options:
    -h, --help            show this help message and exit
    -b BAGFILE, --bag=BAGFILE
                          list topics in .bag file
    -v, --verbose         list full details about each topic
    -p                    list only publishers
    -s                    list only subscribers
  ```

在rostopic list中使用**verbose**选项：

```
$ rostopic list -v
```



rostopic type命令用来查看所发布话题的消息类型。

用法：

```
rostopic type [topic]
```



rostopic pub可以把数据发布到当前某个正在广播的话题上。

用法：

```
rostopic pub [topic] [msg_type] [args]
```


```
$ rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, 1.8]'
```


* 这条命令将消息发布到指定的话题：

  ```
  rostopic pub
  ```
* 这一选项会让rostopic只发布一条消息，然后退出：

  ```
   -1 
  ```
* 这是要发布到的话题的名称：

  ```
  /turtle1/cmd_vel
  ```
* 这是发布到话题时要使用的消息的类型：

  ```
  geometry_msgs/Twist
  ```
* 这一选项（两个破折号）用来告诉选项解析器，表明之后的参数都不是选项。如果参数前有破折号（-）比如负数，那么这是必需的。

  ```
  --
  ```
* 如前所述，一个turtlesim/Velocity消息有两个浮点型元素：linear和angular。在本例中，'[2.0, 0.0, 0.0]'表示linear的值为x=2.0, y=0.0, z=0.0，而'[0.0, 0.0, 1.8]'是说angular的值为x=0.0, y=0.0, z=1.8。这些参数实际上使用的是YAML语法，在[YAML命令行文档](http://wiki.ros.org/ROS/YAMLCommandLine)中有描述。

  ```
  '[2.0, 0.0, 0.0]' '[0.0, 0.0, 1.8]' 
  ```


rostopic hz报告数据发布的速率。

用法：

```
rostopic hz [topic]
```


rqt_plot命令可以在滚动时间图上显示发布到某个话题上的数据。这里我们将使用rqt_plot命令来绘制正被发布到/turtle1/pose话题上的数据。首先，在一个**新终端**中输入：

```
$ rosrun rqt_plot rqt_plot
```


### rosservice


osservice可以很容易地通过服务附加到ROS客户端/服务器框架上。rosservice有许多可用于服务的命令，如下所示：

用法：

```
rosservice list         输出活跃服务的信息
rosservice call         用给定的参数调用服务
rosservice type         输出服务的类型
rosservice find         按服务的类型查找服务
rosservice uri          输出服务的ROSRPC uri
```


```
rosservice list
```


rosservice type命令进一步查看clear（清除）服务


```
rosservice type /clear
```

* ```
  std_srvs/Empty
  ```

rosservice call


```
rosservice call [service] [args]
```

因为服务的类型为empty，所以进行无参数调用：

```
$ rosservice call /clear
```


```
$ rosservice call /clear
```

跟想象的一样，它清除了turtlesim_node背景上的轨迹。



再让我们看看服务具有参数的情况。查看spawn（产卵）服务的信息：

```
$ rosservice type /spawn | rossrv show
```

* ```
  float32 x
  float32 y
  float32 theta
  string name
  ---
  string name
  ```

### rosparam


rosparam能让我们在ROS[参数服务器（Parameter Server）](http://wiki.ros.org/Parameter%20Server)上存储和操作数据。参数服务器能够存储整型（integer）、浮点（float）、布尔（boolean）、字典（dictionaries）和列表（list）等数据类型。rosparam使用YAML标记语言的语法。一般而言，YAML的表述很自然：1是整型，1.0是浮点型，one是字符串，true是布尔型，[1, 2, 3]是整型组成的列表，{a: b, c: d}是字典。rosparam有很多命令可以用来操作参数，如下所示：

用法：

```
rosparam set            设置参数
rosparam get            获取参数
rosparam load           从文件中加载参数
rosparam dump           向文件中转储参数
rosparam delete         删除参数
rosparam list           列出参数名
```


现在我们修改背景颜色的红色通道值：

```
$ rosparam set /turtlesim/background_r 150
```


然后我们来查看参数服务器上其他参数的值。获取背景的绿色通道的值：

```
$ rosparam get /turtlesim/background_g 
```

* ```
  86
  ```

也可以用rosparam get /来显示参数服务器上的所有内容：

```
$ rosparam get /
```


rosparam dump  &  rosparam load


用法：

```
rosparam dump [file_name] [namespace]
rosparam load [file_name] [namespace]
```

在这里，我们将所有的参数写入params.yaml文件：

```
$ rosparam dump params.yaml
```

你甚至可以将yaml文件重载入新的命名空间，例如copy_turtle：

```
$ rosparam load params.yaml copy_turtle
$ rosparam get /copy_turtle/turtlesim/background_b
```

* ```
  255
  ```


### ros_console & ros_logger_level

rqt_console连接到了ROS的日志框架，以显示节点的输出信息。rqt_logger_level允许我们在节点运行时改变输出信息的详细级别，包括Debug、Info、Warn和Error`。

现在让我们来看一下turtlesim在rqt_console中输出的信息，同时在使用turtlesim时切换rqt_logger_level中的日志级别。在启动turtlesim之前先在两个**新**终端中运行rqt_console和rqt_logger_level：

```
$ rosrun rqt_console rqt_console
```

```
$ rosrun rqt_logger_level rqt_logger_level
```


### roslaunch


roslaunch可以用来启动定义在launch（启动）文件中的节点。

用法：

```
$ roslaunch [package] [filename.launch]
```

先切换到我们之前[创建](http://wiki.ros.org/cn/ROS/Tutorials/CreatingPackage)和[构建](http://wiki.ros.org/cn/ROS/Tutorials/BuildingPackages)的beginner_tutorials软件包目录下：

```
$ roscd beginner_tutorials
```

如果roscd提示类似于roscd: No such package/stack 'beginner_tutorials'的话，你需要按照[创建catkin工作空间](http://wiki.ros.org/cn/catkin/Tutorials/create_a_workspace)后面的步骤使环境变量生效：

```
$ cd ~/catkin_ws
$ source devel/setup.bash
$ roscd beginner_tutorials
```

然后创建一个launch目录：

```
$ mkdir launch
$ cd launch
```


现在一起创建一个名为turtlemimic.launch的launch文件并复制粘贴以下内容进去：


```
<launch>

  <group ns="turtlesim1">
    <node pkg="turtlesim" name="sim" type="turtlesim_node"/>
  </group>

  <group ns="turtlesim2">
    <node pkg="turtlesim" name="sim" type="turtlesim_node"/>
  </group>

  <node pkg="turtlesim" name="mimic" type="mimic">
    <remap from="input" to="turtlesim1/turtle1"/>
    <remap from="output" to="turtlesim2/turtle1"/>
  </node>

</launch>
```


下面我们开始拆解launch XML文件。


```
   1 <launch>
```

 首先用launch标签开头，以表明这是一个launch文件。


```
   3   <group ns="turtlesim1">
   4     <node pkg="turtlesim" name="sim" type="turtlesim_node"/>
   5   </group>
   6 
   7   <group ns="turtlesim2">
   8     <node pkg="turtlesim" name="sim" type="turtlesim_node"/>
   9   </group>
```

 此处我们创建了两个分组，并以命名空间（namespace）标签来区分，其中一个名为turtulesim1，另一个名为turtlesim2，两个分组中都有相同的名为sim的turtlesim节点。这样可以让我们同时启动两个turtlesim模拟器，而不会产生命名冲突。


```
  11   <node pkg="turtlesim" name="mimic" type="mimic">
  12     <remap from="input" to="turtlesim1/turtle1"/>
  13     <remap from="output" to="turtlesim2/turtle1"/>
  14   </node>
```

 在这里我们启动模仿节点，话题的输入和输出分别重命名为turtlesim1和turtlesim2，这样就可以让turtlesim2模仿turtlesim1了。


### rosed


rosed是[rosbash](http://wiki.ros.org/rosbash)套件的一部分。利用它可以直接通过软件包名编辑包中的文件，而无需键入完整路径。

用法：

```
$ rosed [package_name] [filename]
```

示例：

```
$ rosed roscpp Logger.msg
```

这个例子演示了如何编辑roscpp软件包中的Logger.msg文件。

如果该实例没有运行成功，可能是因为你没有安装vim编辑器。请参考[编辑器](http://wiki.ros.org/cn/ROS/Tutorials/UsingRosEd#A.2BfxaPkVZo-)部分进行设置。

如果你不知道怎么退出vim，请尝试按下键盘上的Esc，然后分别按下:q!。

如果文件名在包中不是唯一的，则菜单将提示你选择要编辑哪个文件。


### msg & srv


* [msg](http://wiki.ros.org/msg)（消息）：msg文件就是文本文件，用于描述ROS消息的字段。它们用于为不同编程语言编写的消息生成源代码。
* [srv](http://wiki.ros.org/srv)（服务）：一个srv文件描述一个服务。它由两部分组成：请求（request）和响应（response）。

msg文件存放在软件包的msg目录下，srv文件则存放在srv目录下。

msg文件就是简单的文本文件，每行都有一个字段类型和字段名称。可以使用的类型为：

* int8, int16, int32, int64 (以及 uint*)
* float32, float64
* string
* time, duration
* 其他msg文件
* variable-length array[] 和 fixed-length array[C]

ROS中还有一个特殊的数据类型：Header，它含有时间戳和ROS中广泛使用的坐标帧信息。在msg文件的第一行经常可以看到Header header。

下面是一个使用了Header、字符串原语和其他两个消息的示例： 下面是一个msg文件的样例，它使用了Header，string，和其他另外两个消息的类型：

```
  Header header
  string child_frame_id
  geometry_msgs/PoseWithCovariance pose
  geometry_msgs/TwistWithCovariance twist
```

srv文件和msg文件一样，只是它们包含两个部分：请求和响应。这两部分用一条---线隔开。下面是一个srv文件的示例：

```
int64 A
int64 B
---
int64 Sum
```

在上面的例子中，A和B是请求, Sum是响应。


创建和使用msg


下面，我们将在之前创建的软件包里定义一个新的消息。

```
$ roscd beginner_tutorials
$ mkdir msg
$ echo "int64 num" > msg/Num.msg
```

上面是最简单的示例，.msg文件只有一行。当然，你可以通过添加更多元素（每行一个）来创建一个更复杂的文件，如下所示：

```
string first_name
string last_name
uint8 age
uint32 score
```


不过还有关键的一步：我们要确保msg文件能被转换为C++、Python和其他语言的源代码。

打开package.xml, 确保它包含以下两行且没有被[注释](http://www.htmlhelp.com/reference/wilbur/misc/comment.html)。如果没有，添加进去：

```
  <build_depend>message_generation</build_depend>
  <exec_depend>message_runtime</exec_depend>
```

注意，在构建时，其实只需要message_generation，而在运行时，我们只需要message_runtime。

在你喜欢的文本编辑器中打开CMakeLists.txt文件（[rosed](http://wiki.ros.org/cn/ROS/Tutorials/UsingRosEd)是一个不错的选择）。

在CMakeLists.txt文件中，为已经存在里面的find_package调用添加message_generation依赖项，这样就能生成消息了。直接将message_generation添加到COMPONENTS列表中即可，如下所示：

```
# 不要直接复制这一大段，只需将message_generation加在括号闭合前即可
find_package(catkin REQUIRED COMPONENTS
   roscpp
   rospy
   std_msgs
   message_generation
)
```

你可能注意到了，有时即使没有使用全部依赖项调用find_package，项目也可以构建。这是因为catkin把你所有的项目整合在了一起，因此如果之前的项目调用了find_package，你的依赖关系也被配置成了一样的值。但是，忘记调用意味着你的项目在单独构建时很容易崩溃。

还要确保导出消息的运行时依赖关系：

```
catkin_package(
  ...
  CATKIN_DEPENDS message_runtime ...
  ...)
```

找到如下代码块：

```
# add_message_files(
#   FILES
#   Message1.msg
#   Message2.msg
# )
```

删除#符号来取消注释，然后将Message*.msg替换为你的.msg文件名，就像下边这样：

```
add_message_files(
  FILES
  Num.msg
)
```

手动添加.msg文件后，我们要确保CMake知道何时需要重新配置项目。

现在必须确保generate_messages()函数被调用：

 **在ROS Hydro及更新版本中，** 你需要取消下面几行的注释：

```
# generate_messages(
#   DEPENDENCIES
#   std_msgs
# )
```

* 像这样：
  ```
  generate_messages(
    DEPENDENCIES
    std_msgs
  )
  ```


以上就是创建消息的所有步骤。让我们通过rosmsg show命令看看ROS能否识别它。

用法：

```
$ rosmsg show [message type]
```

示例：

```
$ rosmsg show beginner_tutorials/Num
```

你会看到：

* ```
  int64 num
  ```

在上面的例子中，消息类型包含两部分：

* beginner_tutorials  -- 定义消息的软件包
* Num -- 消息的名称Num

如果不记得msg在哪个包中，也可以省略包名称。尝试：

```
$ rosmsg show Num
```

你会看到：

* ```
  [beginner_tutorials/Num]:
  int64 num
  ```


让我们使用之前创建的包再来创建服务：

```
$ roscd beginner_tutorials
$ mkdir srv
```

我们将从另一个包复制现有的srv定义，而不是手动创建新的srv。roscp是一个实用的命令行工具，用于将文件从一个包复制到另一个包。

用法：

```
$ roscp [package_name] [file_to_copy_path] [copy_path]
```

现在我们可以从[rospy_tutorials](http://wiki.ros.org/rospy_tutorials)包中复制一个服务：

```
$ roscp rospy_tutorials AddTwoInts.srv srv/AddTwoInts.srv
```

还有关键的一步：我们要确保msg文件能被转换为C++、Python和其他语言的源代码。

如果没做过上面的教程，请先打开package.xml，确保它包含以下两行且没有被[注释](http://www.htmlhelp.com/reference/wilbur/misc/comment.html)。如果没有，添加进去：

```
  <build_depend>message_generation</build_depend>
  <exec_depend>message_runtime</exec_depend>
```

如前所述，在构建时，其实只需要message_generation，而在运行时，我们只需要message_runtime。

如果没做过上面的教程，在CMakeLists.txt文件中，为已经存在里面的find_package调用添加message_generation依赖项，这样就能生成消息了。直接将message_generation添加到COMPONENTS列表中即可，如下所示：

```
# 不要直接复制这一大段，只需将message_generation加在括号闭合前即可
find_package(catkin REQUIRED COMPONENTS
   roscpp
   rospy
   std_msgs
   message_generation
)
```

（别被名字迷惑，message_generation对msg和srv都适用）

此外，你也需要像之前对消息那样在package.xml中修改服务字段，因此请看上面描述的所需附加依赖项。

```
# add_service_files(
#   FILES
#   Service1.srv
#   Service2.srv
# )
```

删除#符号来取消注释，然后将Service*.srv替换为你的.srv文件名，就像下边这样：

```
add_service_files(
  FILES
  AddTwoInts.srv
)
```

现在，你可以从srv文件定义中生成源代码文件了。


以上就是创建服务的所有步骤。让我们通过rossrv show命令看看ROS能否识别它。

用法：

```
$ rossrv show <service type>
```

示例：

```
$ rossrv show beginner_tutorials/AddTwoInts
```

你会看到：

* ```
  int64 a
  int64 b
  ---
  int64 sum
  ```
