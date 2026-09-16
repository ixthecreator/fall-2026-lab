# 人脸：从节点到区域

当前 collage 的布局没有更改。研究页保存了原来的 VIE 数据，并增加两种照片描点及三种对称衍生图。所有图上的批注使用英文。

## 图的来源与可靠程度

参考 [Tony Oursler 的 2015 年伦敦展览档案](https://tonyoursler.com/templatevariantfriendstranger-london)。其中红色人像属于展览的人像装置；蓝色面具属于同场展览的平行金属板作品系列。“Red portrait”和“Blue mask”是描述性标签，未核实其作品名称。

| 布局     | 保存或描出的点 | 对称版本 | 视觉结构                     |
| -------- | -------------: | -------: | ---------------------------- |
| VIE      |             22 |       23 | 不规则三角网络               |
| 红色人像 |             15 |       17 | 水平延伸线与向下汇聚的放射线 |
| 蓝色面具 |             30 |       31 | 更密集的三角网格             |

VIE 的原始 22 点、39 条边逐字节保存在 `layouts/vie-preserved.json`。新提取采用人工观察照片的方法，不是识别算法输出。节点坐标近似；遮住的连线以灰色虚线表示推测。不能从照片确认的完整网络没有被宣称为已还原。

对称化先人工指定左右对应点，再平均它们的高度和距中轴的距离；中间的点移到中轴。缺少的对应点和边另外镜像补上，并用橙色标识。因此对称图是设计转化，不是艺术家原图。蓝色面具比红色人像更接近规则网格，但两者都存在遮挡和不对称。

“平面化”在这里指去掉背景图、保留二维节点关系；单张照片不足以准确恢复物体的正面几何或三维结构。没有资料能确认这些具体艺术作品分别采用了哪个商用识别算法，不能根据外观强行对应。

## 三类技术分别在做什么

**关键点检测：五官在哪里？** 输出眼角、鼻尖、嘴角等位置。连接关键点可以得到轮廓，多边形可以近似框选五官，但不会自动给每个像素分类。

**人脸语义分割：哪些像素属于眼睛、嘴唇或皮肤？** 输出区域 mask。这个结果更适合抠图，制作可拖动的五官。

**身份识别：这张脸与数据库中的哪张脸相符？** 输出用于比较身份的特征向量；不直接提供拼贴所需的五官图层。

### MediaPipe Face Landmarker

Google 的现有方案输出估计的 **478 个三维关键点**，另可输出 **52 个表情系数**。其连接定义包含眼睛、眉毛、嘴唇、虹膜、脸部外轮廓及三角网格。它适合浏览器里的照片或视频跟踪；关键点本身并不识别姓名或身份。可从密集网格中挑少量控制点，继续使用你的简洁视觉。

来源：[官方说明](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker)、[Web 实现指南](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker/web_js)、[官方连接定义](https://github.com/google-ai-edge/mediapipe/blob/master/mediapipe/tasks/web/vision/face_landmarker/face_landmarks_connections.ts)。

### dlib / 68 点

适合先理解“如何分组”。以下为从零开始的索引：

| 区域       | 索引         |   点数 |
| ---------- | ------------ | -----: |
| 下颌轮廓   | 0–16         |     17 |
| 两侧眉毛   | 17–21、22–26 |  5 + 5 |
| 鼻梁、鼻底 | 27–30、31–35 |  4 + 5 |
| 两只眼睛   | 36–41、42–47 |  6 + 6 |
| 外唇、内唇 | 48–59、60–67 | 12 + 8 |

这是稀疏轮廓，不包含完整额头和头发分区。接入不同工具时，要核对左右侧的定义以及图像是否镜像，不能只凭屏幕左右命名。

来源：[dlib 官方示例](https://github.com/davisking/dlib/blob/master/python_examples/face_landmark_detection.py)、[官方绘制代码与索引组](https://github.com/davisking/dlib/blob/master/dlib/image_processing/render_face_detections.h)。

### Face parsing / CelebAMask-HQ

CelebAMask-HQ 是分割数据集，不是单独一个识别系统。其 **19 类标签包含背景**，还包括皮肤、鼻子、眼镜、左右眼、左右眉、左右耳、口腔、上唇、下唇、头发、帽子、耳饰、项链、脖子、衣服。它们不是“19 块脸部皮肤”。

用这类标注训练的分割模型可以输出五官 mask；现有实现包括基于 BiSeNet 的人脸解析项目。额头、脸颊、下巴通常都落在皮肤类中，仍需要自己利用节点或形状进一步划分。

来源：[数据集官方页面](https://mmlab.ie.cuhk.edu.hk/projects/CelebA/CelebAMask_HQ.html)、[官方 19 类定义](https://github.com/switchablenorms/CelebAMask-HQ/blob/master/face_parsing/README.md)、[BiSeNet 人脸解析实现](https://github.com/zllrunning/face-parsing.PyTorch)。

### InsightFace / ArcFace

这是研究真正身份识别时可看的方案。典型流程是检测脸部、利用参考点对齐、提取身份向量，再比较向量相似程度。RetinaFace 的五个关键点帮助检测与对齐，并不足以形成精细的五官切片。ArcFace 关注身份表征学习，不能把它理解为眼睛、鼻子、嘴巴的分区器。

来源：[InsightFace](https://github.com/deepinsight/insightface)、[RetinaFace 论文](https://arxiv.org/abs/1905.00641)、[ArcFace 论文](https://arxiv.org/abs/1801.07698)。

## 在你的 collage 中怎么用

先采用十个**设计分组**：额头、左右眉、左右眼、鼻子、左右脸颊、嘴、下巴。研究页的区域图是原创示意，不是任何模型的预测图，也不声称有解剖学精度。

将眼睛图像与周围几个节点归为一组。拖眼睛时，这组点一起移动，连接其他区域的线随之伸缩；同样的方法可用于嘴和鼻子。画面上的节点负责连接，隐藏的裁切 mask 负责图像边界。这两套结构可以分开设计。

当前阶段用 HTML、CSS、SVG 加少量拖动 JavaScript 即可完成。若要脸随摄像头动，再引入 MediaPipe；若需要真实照片五官的细致抠图，先离线生成分割 mask。身份识别不属于当前拼贴的必要功能。本次仅完成布局研究与对照，没有加入摄像头或任何识别模型。

参考作品版权属于 Tony Oursler；研究页使用的原图来自艺术家档案与 Lisson Gallery。没有将原作图像宣称为本人的原创素材。本研究页未使用 AI 生成图片。
